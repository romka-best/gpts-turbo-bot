import asyncio
import base64
from typing import List

import anthropic
import httpx
from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.chat_action import ChatActionSender

from bot.database.main import firebase
from bot.database.models.common import Model, ClaudeGPTVersion, Quota, Currency
from bot.database.models.subscription import SubscriptionType
from bot.database.models.transaction import ServiceType, TransactionType
from bot.database.models.user import UserSettings, User
from bot.database.operations.chat.getters import get_chat
from bot.database.operations.message.getters import get_messages_by_chat_id
from bot.database.operations.message.writers import write_message
from bot.database.operations.role.getters import get_role_by_name
from bot.database.operations.transaction.writers import write_transaction
from bot.database.operations.user.getters import get_user
from bot.database.operations.user.updaters import update_user
from bot.helpers.creaters.create_new_message_and_update_user import create_new_message_and_update_user
from bot.helpers.reply_with_voice import reply_with_voice
from bot.helpers.senders.send_error_info import send_error_info
from bot.helpers.split_message import split_message
from bot.integrations.anthropic import get_response_message
from bot.keyboards.ai.claude import build_claude_keyboard, build_claude_continue_generating_keyboard
from bot.keyboards.common.common import build_recommendations_keyboard, build_error_keyboard
from bot.locales.main import get_user_language, get_localization

claude_router = Router()

PRICE_CLAUDE_3_SONNET_INPUT = 0.000003
PRICE_CLAUDE_3_SONNET_OUTPUT = 0.000015
PRICE_CLAUDE_3_OPUS_INPUT = 0.000015
PRICE_CLAUDE_3_OPUS_OUTPUT = 0.000075


@claude_router.message(Command("claude"))
async def claude(message: Message, state: FSMContext):
    await state.clear()

    user_id = str(message.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    reply_markup = build_claude_keyboard(
        user_language_code,
        user.current_model,
        user.settings[Model.CLAUDE][UserSettings.VERSION],
    )
    await message.answer(
        text=get_localization(user_language_code).CHOOSE_CLAUDE_MODEL,
        reply_markup=reply_markup,
    )


@claude_router.callback_query(lambda c: c.data.startswith('claude:'))
async def handle_claude_choose_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    chosen_version = callback_query.data.split(':')[1]

    if user.current_model == Model.CLAUDE and chosen_version == user.settings[Model.CLAUDE][UserSettings.VERSION]:
        reply_markup = await build_recommendations_keyboard(user.current_model, user_language_code, user.gender)
        await callback_query.message.answer(
            text=get_localization(user_language_code).ALREADY_SWITCHED_TO_THIS_MODEL,
            reply_markup=reply_markup,
        )
    else:
        keyboard = callback_query.message.reply_markup.inline_keyboard
        keyboard_changed = False

        new_keyboard = []
        for row in keyboard:
            new_row = []
            for button in row:
                text = button.text
                callback_data = button.callback_data.split(":", 1)[1]

                if callback_data == chosen_version:
                    if "✅" not in text:
                        text += " ✅"
                        keyboard_changed = True
                else:
                    text = text.replace(" ✅", "")
                new_row.append(InlineKeyboardButton(text=text, callback_data=button.callback_data))
            new_keyboard.append(new_row)
        await callback_query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=new_keyboard))

        reply_markup = await build_recommendations_keyboard(Model.CLAUDE, user_language_code, user.gender)
        if keyboard_changed:
            user.current_model = Model.CLAUDE
            user.settings[Model.CLAUDE][UserSettings.VERSION] = chosen_version
            await update_user(user_id, {
                "current_model": user.current_model,
                "settings": user.settings,
            })

            text = get_localization(user_language_code).SWITCHED_TO_CLAUDE_3_SONNET \
                if user.settings[user.current_model][UserSettings.VERSION] == ClaudeGPTVersion.V3_Sonnet \
                else get_localization(user_language_code).SWITCHED_TO_CLAUDE_3_OPUS
            await callback_query.message.answer(
                text=text,
                reply_markup=reply_markup,
                message_effect_id="5104841245755180586",
            )
        else:
            text = get_localization(user_language_code).ALREADY_SWITCHED_TO_THIS_MODEL
            await callback_query.message.answer(
                text=text,
                reply_markup=reply_markup,
            )

    await state.clear()


async def handle_claude(message: Message, state: FSMContext, user: User, user_quota: Quota, filenames=None):
    if user_quota != Quota.CLAUDE_3_SONNET and user_quota != Quota.CLAUDE_3_OPUS:
        raise NotImplemented

    await state.update_data(is_processing=True)

    user_language_code = await get_user_language(user.id, state.storage)
    user_data = await state.get_data()

    text = user_data.get('recognized_text', None)
    if text is None:
        if message.caption:
            text = message.caption
        elif message.text:
            text = message.text
        else:
            text = ""

    if filenames and len(filenames):
        await write_message(user.current_chat_id, "user", user.id, text, True, filenames)
    else:
        await write_message(user.current_chat_id, "user", user.id, text)

    chat = await get_chat(user.current_chat_id)
    messages = await get_messages_by_chat_id(user.current_chat_id)
    role = await get_role_by_name(chat.role)
    sorted_messages = sorted(messages, key=lambda m: m.created_at)
    system_prompt = role.translated_instructions.get(user_language_code, 'en')
    history = []
    for sorted_message in sorted_messages:
        content = []
        if sorted_message.content:
            content.append({
                'type': 'text',
                'text': sorted_message.content,
            })

        if sorted_message.photo_filenames:
            for photo_filename in sorted_message.photo_filenames:
                photo_path = f'users/vision/{user.id}/{photo_filename}'
                photo = await firebase.bucket.get_blob(photo_path)
                photo_link = firebase.get_public_url(photo.name)

                image_media_type = "image/jpeg"
                image_data = base64.b64encode(httpx.get(photo_link).content).decode("utf-8")
                content.append({
                    'type': 'image',
                    'source': {
                        "type": "base64",
                        "media_type": image_media_type,
                        "data": image_data,
                    },
                })

        history.append({
            'role': sorted_message.sender,
            'content': content,
        })

    processing_message = await message.reply(text=get_localization(user_language_code).processing_request_text())

    if user.settings[user.current_model][UserSettings.TURN_ON_VOICE_MESSAGES]:
        chat_action_sender = ChatActionSender.record_voice
    else:
        chat_action_sender = ChatActionSender.typing

    async with chat_action_sender(bot=message.bot, chat_id=message.chat.id):
        try:
            history = get_history_without_duplicates(history)

            response = await get_response_message(
                user.settings[user.current_model][UserSettings.VERSION],
                system_prompt,
                history,
            )
            response_message = response['message']
            if user_quota == Quota.CLAUDE_3_SONNET:
                service = ServiceType.CLAUDE_3_SONNET
                input_price = response['input_tokens'] * PRICE_CLAUDE_3_SONNET_INPUT
                output_price = response['output_tokens'] * PRICE_CLAUDE_3_SONNET_OUTPUT
            else:
                service = ServiceType.CLAUDE_3_OPUS
                input_price = response['input_tokens'] * PRICE_CLAUDE_3_OPUS_INPUT
                output_price = response['output_tokens'] * PRICE_CLAUDE_3_OPUS_OUTPUT

            total_price = round(input_price + output_price, 6)
            message_role, message_content = "assistant", response_message
            await write_transaction(
                user_id=user.id,
                type=TransactionType.EXPENSE,
                service=service,
                amount=total_price,
                clear_amount=total_price,
                currency=Currency.USD,
                quantity=1,
                details={
                    "input_tokens": response['input_tokens'],
                    "output_tokens": response['output_tokens'],
                    "request": text,
                    "answer": message_content,
                    "is_suggestion": False,
                    "has_error": False,
                },
            )

            transaction = firebase.db.transaction()
            await create_new_message_and_update_user(transaction, message_role, message_content, user, user_quota)

            if user.settings[user.current_model][UserSettings.TURN_ON_VOICE_MESSAGES]:
                reply_markup = build_claude_continue_generating_keyboard(user_language_code)
                await reply_with_voice(
                    message=message,
                    text=message_content,
                    user_id=user.id,
                    reply_markup=reply_markup if response['finish_reason'] == 'max_tokens' else None,
                    voice=user.settings[user.current_model][UserSettings.VOICE],
                )
            else:
                chat_info = f'💬 {chat.title}\n' if (
                    user.settings[user.current_model][UserSettings.SHOW_THE_NAME_OF_THE_CHATS]
                ) else ''
                role_info = f'{role.translated_names.get(user_language_code, "en")}\n' if (
                    user.settings[user.current_model][UserSettings.SHOW_THE_NAME_OF_THE_ROLES]
                ) else ''
                header_text = f'{chat_info}{role_info}\n' if chat_info or role_info else ''
                footer_text = f'\n\n✉️ {user.monthly_limits[user_quota] + user.additional_usage_quota[user_quota] + 1}' \
                    if user.settings[user.current_model][UserSettings.SHOW_USAGE_QUOTA] else ''
                reply_markup = build_claude_continue_generating_keyboard(user_language_code)
                try:
                    full_text = f"{header_text}{message_content}{footer_text}"
                    if len(full_text) <= 4096:
                        await message.reply(
                            full_text,
                            reply_markup=reply_markup if response['finish_reason'] == 'max_tokens' else None,
                            parse_mode=ParseMode.MARKDOWN,
                        )
                    elif len(message_content) <= 4096:
                        await message.reply(
                            message_content,
                            reply_markup=reply_markup if response['finish_reason'] == 'max_tokens' else None,
                            parse_mode=ParseMode.MARKDOWN,
                        )
                    else:
                        chunks = split_message(full_text)
                        for i in range(len(chunks)):
                            if i == 0:
                                await message.reply(
                                    chunks[i],
                                    parse_mode=None,
                                )
                            elif i == len(chunks) - 1:
                                await message.reply(
                                    chunks[i],
                                    reply_markup=reply_markup if response['finish_reason'] == 'max_tokens' else None,
                                    parse_mode=None,
                                )
                            else:
                                await message.answer(
                                    chunks[i],
                                    parse_mode=None,
                                )
                except TelegramBadRequest as e:
                    if "can't parse entities" in str(e):
                        await message.reply(
                            f"{header_text}{message_content}{footer_text}",
                            reply_markup=reply_markup if response['finish_reason'] == 'max_tokens' else None,
                            parse_mode=None,
                        )
                    else:
                        raise
        except anthropic.BadRequestError as e:
            if 'content_policy_violation' in str(e):
                await message.reply(
                    text=get_localization(user_language_code).REQUEST_FORBIDDEN_ERROR,
                )
            elif 'Overloaded' in str(e):
                await message.reply(
                    text=get_localization(user_language_code).SERVER_OVERLOADED_ERROR,
                )
            else:
                reply_markup = build_error_keyboard(user_language_code)
                await message.answer(
                    text=get_localization(user_language_code).ERROR,
                    reply_markup=reply_markup,
                    parse_mode=None,
                )

                await send_error_info(
                    bot=message.bot,
                    user_id=user.id,
                    info=str(e),
                    hashtags=["claude"],
                )
        except Exception as e:
            reply_markup = build_error_keyboard(user_language_code)
            await message.answer(
                text=get_localization(user_language_code).ERROR,
                reply_markup=reply_markup,
                parse_mode=None,
            )

            await send_error_info(
                bot=message.bot,
                user_id=user.id,
                info=str(e),
                hashtags=["claude"],
            )
        finally:
            await processing_message.delete()
            await state.update_data(is_processing=False)

    asyncio.create_task(
        handle_claude_3_opus_example(
            user=user,
            user_language_code=user_language_code,
            prompt=text,
            system_prompt=system_prompt,
            history=history,
            message=message,
        )
    )


@claude_router.callback_query(lambda c: c.data.startswith('claude_continue_generation:'))
async def handle_claude_continue_generation_choose_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    action = callback_query.data.split(':')[1]

    if action == 'continue':
        await state.update_data(recognized_text=get_localization(user_language_code).CONTINUE_GENERATING)
        if user.settings[user.current_model][UserSettings.VERSION] == ClaudeGPTVersion.V3_Sonnet:
            user_quota = Quota.CLAUDE_3_SONNET
        elif user.settings[user.current_model][UserSettings.VERSION] == ClaudeGPTVersion.V3_Opus:
            user_quota = Quota.CLAUDE_3_OPUS
        else:
            raise NotImplemented

        await handle_claude(callback_query.message, state, user, user_quota)
        await callback_query.message.edit_reply_markup(reply_markup=None)

    await state.clear()


async def handle_claude_3_opus_example(
    user: User,
    user_language_code: str,
    prompt: str,
    system_prompt: str,
    history: List,
    message: Message,
):
    try:
        if (
            user.current_model == Model.CLAUDE and
            user.settings[user.current_model][UserSettings.VERSION] == ClaudeGPTVersion.V3_Sonnet and
            user.subscription_type == SubscriptionType.FREE and
            user.monthly_limits[Quota.CLAUDE_3_SONNET] + 1 in [1, 10, 20]
        ):
            history = get_history_without_duplicates(history)

            response = await get_response_message(ClaudeGPTVersion.V3_Opus, system_prompt, history)
            response_message = response['message']

            service = ServiceType.CLAUDE_3_OPUS
            input_price = response['input_tokens'] * PRICE_CLAUDE_3_OPUS_INPUT
            output_price = response['output_tokens'] * PRICE_CLAUDE_3_OPUS_OUTPUT

            total_price = round(input_price + output_price, 6)
            message_role, message_content = "assistant", response_message
            await write_transaction(
                user_id=user.id,
                type=TransactionType.EXPENSE,
                service=service,
                amount=total_price,
                clear_amount=total_price,
                currency=Currency.USD,
                quantity=1,
                details={
                    "input_tokens": response['input_tokens'],
                    "output_tokens": response['output_tokens'],
                    "request": prompt,
                    "answer": message_content,
                    "is_suggestion": True,
                    "has_error": False,
                },
            )

            header_text = f'{get_localization(user_language_code).CLAUDE_3_OPUS_EXAMPLE}\n\n'
            try:
                full_text = f"{header_text}{message_content}"
                if len(full_text) <= 4096:
                    await message.reply(
                        full_text,
                        parse_mode=ParseMode.MARKDOWN,
                    )
                elif len(header_text) + len(message_content) <= 4096:
                    await message.reply(
                        f"{header_text}{message_content}",
                        parse_mode=ParseMode.MARKDOWN,
                    )
                else:
                    chunks = split_message(full_text)
                    for i in range(len(chunks)):
                        if i == 0:
                            await message.reply(
                                chunks[i],
                                parse_mode=None,
                            )
                        else:
                            await message.answer(
                                chunks[i],
                                parse_mode=None,
                            )
            except TelegramBadRequest as e:
                if "can't parse entities" in str(e):
                    await message.reply(
                        f"{header_text}{message_content}",
                        parse_mode=None,
                    )
                else:
                    raise
    except Exception as e:
        await send_error_info(
            bot=message.bot,
            user_id=user.id,
            info=str(e),
            hashtags=["claude", "example"],
        )


def get_history_without_duplicates(history: List) -> List:
    result = []
    first_user_found = False

    for item in history:
        if not first_user_found and item['role'] == 'user':
            first_user_found = True

        if first_user_found:
            if result and item['role'] == result[-1]['role']:
                result[-1] = item
            else:
                result.append(item)

    return result
