import asyncio
from typing import List

import openai
from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.chat_action import ChatActionSender
from telegram.constants import ParseMode

from bot.database.main import firebase
from bot.database.models.common import Quota, Currency, GPTVersion, Model
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
from bot.helpers.senders.send_message_to_admins import send_message_to_admins
from bot.integrations.openAI import get_response_message
from bot.keyboards.ai.chat_gpt import build_chat_gpt_continue_generating_keyboard, build_chat_gpt_keyboard
from bot.keyboards.common.common import build_recommendations_keyboard
from bot.locales.main import get_localization, get_user_language

chat_gpt_router = Router()

PRICE_GPT3_INPUT = 0.0000005
PRICE_GPT3_OUTPUT = 0.0000015
PRICE_GPT4_INPUT = 0.00001
PRICE_GPT4_OUTPUT = 0.00003


@chat_gpt_router.message(Command("chatgpt"))
async def chatgpt(message: Message, state: FSMContext):
    await state.clear()

    user_id = str(message.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    reply_markup = build_chat_gpt_keyboard(
        user_language_code,
        user.current_model,
        user.settings[Model.CHAT_GPT][UserSettings.VERSION],
    )
    await message.answer(
        text=get_localization(user_language_code).CHOOSE_CHATGPT_MODEL,
        reply_markup=reply_markup,
    )


@chat_gpt_router.callback_query(lambda c: c.data.startswith('chat_gpt:'))
async def handle_chat_gpt_choose_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    chosen_version = callback_query.data.split(':')[1]

    if user.current_model == Model.CHAT_GPT and chosen_version == user.settings[Model.CHAT_GPT][UserSettings.VERSION]:
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

        reply_markup = await build_recommendations_keyboard(Model.CHAT_GPT, user_language_code, user.gender)
        if keyboard_changed:
            user.current_model = Model.CHAT_GPT
            user.settings[Model.CHAT_GPT][UserSettings.VERSION] = chosen_version
            await update_user(user_id, {
                "current_model": user.current_model,
                "settings": user.settings,
            })

            text = get_localization(user_language_code).SWITCHED_TO_CHATGPT3 \
                if user.settings[user.current_model][UserSettings.VERSION] == GPTVersion.V3 \
                else get_localization(user_language_code).SWITCHED_TO_CHATGPT4
            await callback_query.message.answer(
                text=text,
                reply_markup=reply_markup,
            )
        else:
            text = get_localization(user_language_code).ALREADY_SWITCHED_TO_THIS_MODEL
            await callback_query.message.answer(
                text=text,
                reply_markup=reply_markup,
            )

    await state.clear()


async def handle_chatgpt(message: Message, state: FSMContext, user: User, user_quota: Quota, photo_filename=None):
    if user_quota != Quota.CHAT_GPT3 and user_quota != Quota.CHAT_GPT4:
        raise NotImplemented

    await state.update_data(is_processing=True)

    user_language_code = await get_user_language(user.id, state.storage)
    user_data = await state.get_data()

    text = user_data.get('recognized_text', None)
    if text is None:
        if message.caption:
            text = message.caption
        else:
            text = message.text

    if photo_filename and user_quota == Quota.CHAT_GPT4:
        await write_message(user.current_chat_id, "user", user.id, text, True, photo_filename)
    else:
        await write_message(user.current_chat_id, "user", user.id, text)

    chat = await get_chat(user.current_chat_id)
    messages = await get_messages_by_chat_id(user.current_chat_id)
    role = await get_role_by_name(chat.role)
    sorted_messages = sorted(messages, key=lambda m: m.created_at)
    if user_quota == Quota.CHAT_GPT3:
        history = [
                      {
                          'role': 'system',
                          'content': role.translated_instructions.get(user_language_code, 'en')
                      }
                  ] + [
                      {
                          'role': message.sender,
                          'content': message.content
                      } for message in sorted_messages
                  ]
    else:
        history = [
            {
                'role': 'system',
                'content': role.translated_instructions.get(user_language_code, 'en')
            }
        ]
        for sorted_message in sorted_messages:
            content = []
            if sorted_message.content:
                content.append({
                    'type': 'text',
                    'text': sorted_message.content,
                })

            if sorted_message.photo_filename:
                photo_path = f'users/chatgpt4_vision/{user.id}/{sorted_message.photo_filename}'
                photo = await firebase.bucket.get_blob(photo_path)
                photo_link = firebase.get_public_url(photo.name)
                content.append({
                    'type': 'image_url',
                    'image_url': {
                        'url': photo_link,
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
            response = await get_response_message(user.settings[user.current_model][UserSettings.VERSION], history)
            response_message = response['message']
            if user_quota == Quota.CHAT_GPT3:
                service = ServiceType.CHAT_GPT3
                input_price = response['input_tokens'] * PRICE_GPT3_INPUT
                output_price = response['output_tokens'] * PRICE_GPT3_OUTPUT
            else:
                service = ServiceType.CHAT_GPT4
                input_price = response['input_tokens'] * PRICE_GPT4_INPUT
                output_price = response['output_tokens'] * PRICE_GPT4_OUTPUT

            total_price = round(input_price + output_price, 6)
            message_role, message_content = response_message.role, response_message.content
            await write_transaction(
                user_id=user.id,
                type=TransactionType.EXPENSE,
                service=service,
                amount=total_price,
                currency=Currency.USD,
                quantity=1,
                details={
                    "input_tokens": response['input_tokens'],
                    "output_tokens": response['output_tokens'],
                    "request": text,
                    "answer": message_content,
                    "is_suggestion": False,
                },
            )

            transaction = firebase.db.transaction()
            await create_new_message_and_update_user(transaction, message_role, message_content, user, user_quota)

            if user.settings[user.current_model][UserSettings.TURN_ON_VOICE_MESSAGES]:
                reply_markup = build_chat_gpt_continue_generating_keyboard(user_language_code)
                await reply_with_voice(
                    message=message,
                    text=message_content,
                    user_id=user.id,
                    reply_markup=reply_markup if response['finish_reason'] == 'length' else None,
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
                reply_markup = build_chat_gpt_continue_generating_keyboard(user_language_code)
                try:
                    await message.reply(
                        f"{header_text}{message_content}{footer_text}",
                        reply_markup=reply_markup if response['finish_reason'] == 'length' else None,
                        parse_mode=ParseMode.MARKDOWN,
                    )
                except TelegramBadRequest as e:
                    if "can't parse entities" in str(e):
                        await message.reply(
                            f"{header_text}{message_content}{footer_text}",
                            reply_markup=reply_markup if response['finish_reason'] == 'length' else None,
                            parse_mode=None,
                        )
                    else:
                        raise
        except openai.BadRequestError as e:
            if e.code == 'content_policy_violation':
                await message.reply(
                    text=get_localization(user_language_code).REQUEST_FORBIDDEN_ERROR,
                )
            else:
                await message.answer(
                    text=get_localization(user_language_code).ERROR,
                    parse_mode=None,
                )

                await send_message_to_admins(
                    bot=message.bot,
                    message=f"#error\n\nALARM! Ошибка у пользователя при запросе в ChatGPT: {user.id}\n"
                            f"Информация:\n{e}",
                    parse_mode=None,
                )
        except Exception as e:
            await message.answer(
                text=get_localization(user_language_code).ERROR,
                parse_mode=None,
            )
            await send_message_to_admins(
                bot=message.bot,
                message=f"#error\n\nALARM! Ошибка у пользователя при запросе в ChatGPT: {user.id}\n"
                        f"Информация:\n{e}",
                parse_mode=None,
            )
        finally:
            await processing_message.delete()
            await state.update_data(is_processing=False)

    asyncio.create_task(
        handle_chatgpt4_example(
            user=user,
            user_language_code=user_language_code,
            prompt=text,
            history=history,
            message=message,
        )
    )


@chat_gpt_router.callback_query(lambda c: c.data.startswith('chat_gpt_continue_generation:'))
async def handle_chat_gpt_continue_generation_choose_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    action = callback_query.data.split(':')[1]

    if action == 'continue':
        await state.update_data(recognized_text=get_localization(user_language_code).CONTINUE_GENERATING)
        if user.settings[user.current_model][UserSettings.VERSION] == GPTVersion.V3:
            user_quota = Quota.CHAT_GPT3
        elif user.settings[user.current_model][UserSettings.VERSION] == GPTVersion.V4:
            user_quota = Quota.CHAT_GPT4
        else:
            raise NotImplemented

        await handle_chatgpt(callback_query.message, state, user, user_quota)
        await callback_query.message.edit_reply_markup(reply_markup=None)

    await state.clear()


async def handle_chatgpt4_example(user: User, user_language_code: str, prompt: str, history: List, message: Message):
    try:
        if (
            user.current_model == Model.CHAT_GPT and
            user.settings[user.current_model][UserSettings.VERSION] == GPTVersion.V3 and
            user.subscription_type == SubscriptionType.FREE and
            user.monthly_limits[Quota.CHAT_GPT3] + 1 in [1, 50, 90, 100]
        ):
            response = await get_response_message(GPTVersion.V4, history)
            response_message = response['message']

            service = ServiceType.CHAT_GPT4
            input_price = response['input_tokens'] * PRICE_GPT4_INPUT
            output_price = response['output_tokens'] * PRICE_GPT4_OUTPUT

            total_price = round(input_price + output_price, 6)
            message_role, message_content = response_message.role, response_message.content
            await write_transaction(
                user_id=user.id,
                type=TransactionType.EXPENSE,
                service=service,
                amount=total_price,
                currency=Currency.USD,
                quantity=1,
                details={
                    "input_tokens": response['input_tokens'],
                    "output_tokens": response['output_tokens'],
                    "request": prompt,
                    "answer": message_content,
                    "is_suggestion": True,
                },
            )

            header_text = f'{get_localization(user_language_code).CHATGPT4_EXAMPLE_FIRST_PART}\n\n'
            footer_text = f'\n\n{get_localization(user_language_code).CHATGPT4_EXAMPLE_LAST_PART}'
            try:
                await message.reply(
                    f"{header_text}{message_content}{footer_text}",
                    parse_mode=ParseMode.MARKDOWN,
                )
            except TelegramBadRequest as e:
                if "can't parse entities" in str(e):
                    await message.reply(
                        f"{header_text}{message_content}{footer_text}",
                        parse_mode=None,
                    )
                else:
                    raise
    except Exception as e:
        await send_message_to_admins(
            bot=message.bot,
            message=f"#error\n\nALARM! Ошибка у пользователя при попытке отправить пример ChatGPT-4.0 в запросе в ChatGPT-3.5: {user.id}\nИнформация:\n{e}",
            parse_mode=None,
        )
