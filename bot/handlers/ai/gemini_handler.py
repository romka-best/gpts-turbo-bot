import asyncio
from datetime import datetime, timezone
from io import BytesIO
from typing import List

import PIL.Image
import httpx
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.chat_action import ChatActionSender

from bot.config import config, MessageEffect
from bot.database.main import firebase
from bot.database.models.common import Model, GeminiGPTVersion, Quota, Currency
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
from bot.helpers.senders.send_ai_message import send_ai_message
from bot.helpers.senders.send_error_info import send_error_info
from bot.integrations.googleAI import get_response_message
from bot.keyboards.ai.gemini import build_gemini_keyboard, build_gemini_continue_generating_keyboard
from bot.keyboards.common.common import build_recommendations_keyboard, build_error_keyboard
from bot.locales.main import get_user_language, get_localization

gemini_router = Router()

PRICE_GEMINI_1_FLASH_INPUT = 0.000000075
PRICE_GEMINI_1_FLASH_OUTPUT = 0.00000030
PRICE_GEMINI_1_PRO_INPUT = 0.00000350
PRICE_GEMINI_1_PRO_OUTPUT = 0.00001050


@gemini_router.message(Command('gemini'))
async def gemini(message: Message, state: FSMContext):
    await state.clear()

    user_id = str(message.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    reply_markup = build_gemini_keyboard(
        user_language_code,
        user.current_model,
        user.settings[Model.GEMINI][UserSettings.VERSION],
    )
    await message.answer(
        text=get_localization(user_language_code).CHOOSE_GEMINI_MODEL,
        reply_markup=reply_markup,
    )


@gemini_router.callback_query(lambda c: c.data.startswith('gemini:'))
async def handle_gemini_choose_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    chosen_version = callback_query.data.split(':')[1]

    if user.current_model == Model.GEMINI and chosen_version == user.settings[Model.GEMINI][UserSettings.VERSION]:
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
                callback_data = button.callback_data.split(':', 1)[1]

                if callback_data == chosen_version:
                    if '✅' not in text:
                        text += ' ✅'
                        keyboard_changed = True
                else:
                    text = text.replace(' ✅', '')
                new_row.append(InlineKeyboardButton(text=text, callback_data=button.callback_data))
            new_keyboard.append(new_row)
        await callback_query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=new_keyboard))

        reply_markup = await build_recommendations_keyboard(Model.GEMINI, user_language_code, user.gender)
        if keyboard_changed:
            user.current_model = Model.GEMINI
            user.settings[Model.GEMINI][UserSettings.VERSION] = chosen_version
            await update_user(user_id, {
                'current_model': user.current_model,
                'settings': user.settings,
            })

            if user.settings[user.current_model][UserSettings.VERSION] == GeminiGPTVersion.V1_Flash:
                text = get_localization(user_language_code).SWITCHED_TO_GEMINI_1_FLASH
            else:
                text = get_localization(user_language_code).SWITCHED_TO_GEMINI_1_PRO

            await callback_query.message.answer(
                text=text,
                reply_markup=reply_markup,
                message_effect_id=config.MESSAGE_EFFECTS.get(MessageEffect.FIRE),
            )
        else:
            text = get_localization(user_language_code).ALREADY_SWITCHED_TO_THIS_MODEL
            await callback_query.message.answer(
                text=text,
                reply_markup=reply_markup,
            )

    await state.clear()


async def handle_gemini(message: Message, state: FSMContext, user: User, user_quota: Quota, filenames=None):
    if user_quota != Quota.GEMINI_1_FLASH and user_quota != Quota.GEMINI_1_PRO:
        raise NotImplemented(f'User quota is not implemented: {user_quota}')

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
            text = ''

    if filenames and len(filenames):
        await write_message(user.current_chat_id, 'user', user.id, text, True, filenames)
    else:
        await write_message(user.current_chat_id, 'user', user.id, text)

    chat = await get_chat(user.current_chat_id)
    messages = await get_messages_by_chat_id(user.current_chat_id)
    role = await get_role_by_name(chat.role)
    sorted_messages = sorted(messages, key=lambda m: m.created_at)
    system_prompt = role.translated_instructions.get(user_language_code, 'en')
    history = []
    for sorted_message in sorted_messages:
        parts = []
        if sorted_message.content:
            parts.append(sorted_message.content)

        if sorted_message.photo_filenames:
            for photo_filename in sorted_message.photo_filenames:
                photo_path = f'users/vision/{user.id}/{photo_filename}'
                photo = await firebase.bucket.get_blob(photo_path)
                photo_link = firebase.get_public_url(photo.name)
                photo_file = PIL.Image.open(BytesIO(httpx.get(photo_link).content))

                parts.append(photo_file)

        history.append({
            'role': sorted_message.sender if sorted_message.sender == 'user' else 'model',
            'parts': parts,
        })

    processing_message = await message.reply(text=get_localization(user_language_code).processing_request_text())

    if user.settings[user.current_model][UserSettings.TURN_ON_VOICE_MESSAGES]:
        chat_action_sender = ChatActionSender.record_voice
    else:
        chat_action_sender = ChatActionSender.typing

    async with chat_action_sender(bot=message.bot, chat_id=message.chat.id):
        try:
            response = await get_response_message(
                model_version=user.settings[user.current_model][UserSettings.VERSION],
                system_prompt=system_prompt,
                new_prompt=history[-1],
                history=history[:-1],
            )
            response_message = response['message']
            if user_quota == Quota.GEMINI_1_FLASH:
                service = ServiceType.GEMINI_1_FLASH
                input_price = response['input_tokens'] * PRICE_GEMINI_1_FLASH_INPUT
                output_price = response['output_tokens'] * PRICE_GEMINI_1_FLASH_OUTPUT
            else:
                service = ServiceType.GEMINI_1_PRO
                input_price = response['input_tokens'] * PRICE_GEMINI_1_PRO_INPUT
                output_price = response['output_tokens'] * PRICE_GEMINI_1_PRO_OUTPUT

            total_price = round(input_price + output_price, 6)
            message_role, message_content = 'assistant', response_message
            await write_transaction(
                user_id=user.id,
                type=TransactionType.EXPENSE,
                service=service,
                amount=total_price,
                clear_amount=total_price,
                currency=Currency.USD,
                quantity=1,
                details={
                    'input_tokens': response['input_tokens'],
                    'output_tokens': response['output_tokens'],
                    'request': text,
                    'answer': message_content,
                    'is_suggestion': False,
                    'has_error': False,
                },
            )

            transaction = firebase.db.transaction()
            await create_new_message_and_update_user(transaction, message_role, message_content, user, user_quota)

            if user.settings[user.current_model][UserSettings.TURN_ON_VOICE_MESSAGES]:
                reply_markup = build_gemini_continue_generating_keyboard(user_language_code)
                await reply_with_voice(
                    message=message,
                    text=message_content,
                    user_id=user.id,
                    reply_markup=reply_markup if response['finish_reason'] == 'MAX_TOKENS' else None,
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
                footer_text = f'\n\n✉️ {user.daily_limits[user_quota] + user.additional_usage_quota[user_quota] + 1}' \
                    if user.settings[user.current_model][UserSettings.SHOW_USAGE_QUOTA] and \
                       user.daily_limits[user_quota] != float('inf') else ''
                reply_markup = build_gemini_continue_generating_keyboard(user_language_code)
                full_text = f'{header_text}{message_content}{footer_text}'
                await send_ai_message(
                    message=message,
                    text=full_text,
                    reply_markup=reply_markup if response['finish_reason'] == 'MAX_TOKENS' else None,
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
                hashtags=['gemini'],
            )
        finally:
            await processing_message.delete()
            await state.update_data(is_processing=False)

    asyncio.create_task(
        handle_gemini_1_pro_example(
            user=user,
            user_language_code=user_language_code,
            prompt=text,
            system_prompt=system_prompt,
            history=history,
            message=message,
        )
    )


async def handle_gemini_1_pro_example(
    user: User,
    user_language_code: str,
    prompt: str,
    system_prompt: str,
    history: List,
    message: Message,
):
    try:
        current_date = datetime.now(timezone.utc)
        if (
            user.subscription_type == SubscriptionType.FREE and
            user.current_model == Model.GEMINI and
            user.settings[user.current_model][UserSettings.SHOW_EXAMPLES] and
            user.daily_limits[Quota.GEMINI_1_FLASH] + 1 in [1, 10] and
            (current_date - user.last_subscription_limit_update).days <= 3
        ):
            response = await get_response_message(
                model_version=GeminiGPTVersion.V1_Pro,
                system_prompt=system_prompt,
                new_prompt=history[-1].get('parts'),
                history=history[:-1],
            )
            response_message = response['message']

            service = ServiceType.GEMINI_1_PRO
            input_price = response['input_tokens'] * PRICE_GEMINI_1_PRO_INPUT
            output_price = response['output_tokens'] * PRICE_GEMINI_1_PRO_OUTPUT

            total_price = round(input_price + output_price, 6)
            message_role, message_content = 'assistant', response_message
            await write_transaction(
                user_id=user.id,
                type=TransactionType.EXPENSE,
                service=service,
                amount=total_price,
                clear_amount=total_price,
                currency=Currency.USD,
                quantity=1,
                details={
                    'input_tokens': response['input_tokens'],
                    'output_tokens': response['output_tokens'],
                    'request': prompt,
                    'answer': message_content,
                    'is_suggestion': True,
                    'has_error': False,
                },
            )

            header_text = f'{get_localization(user_language_code).GEMINI_1_PRO_EXAMPLE}\n\n'
            full_text = f'{header_text}{message_content}'
            await send_ai_message(
                message=message,
                text=full_text,
            )
    except Exception as e:
        await send_error_info(
            bot=message.bot,
            user_id=user.id,
            info=str(e),
            hashtags=['gemini', 'example'],
        )