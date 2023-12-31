import time

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from telegram import constants

from bot.database.main import db
from bot.database.models.common import Model, Quota, Currency
from bot.database.models.transaction import ServiceType, TransactionType
from bot.database.models.user import UserSettings
from bot.database.operations.chat import get_chat
from bot.database.operations.message import write_message, get_messages_by_chat_id
from bot.database.operations.transaction import write_transaction
from bot.database.operations.user import get_user
from bot.helpers.create_new_message_and_update_user import create_new_message_and_update_user
from bot.helpers.reply_with_voice import reply_with_voice
from bot.helpers.send_message_to_admins import send_message_to_admins
from bot.integrations.openAI import get_response_message
from bot.keyboards.chat_gpt import build_chat_gpt_continue_generating_keyboard
from bot.locales.main import get_localization
from bot.utils.is_messages_limit_exceeded import is_messages_limit_exceeded
from bot.utils.is_time_limit_exceeded import is_time_limit_exceeded

chat_gpt_router = Router()

PRICE_GPT3_INPUT = 0.000001
PRICE_GPT3_OUTPUT = 0.000002
PRICE_GPT4_INPUT = 0.00001
PRICE_GPT4_OUTPUT = 0.00003


@chat_gpt_router.message()
async def handle_chatgpt(message: Message, state: FSMContext):
    user = await get_user(str(message.from_user.id))
    user_data = await state.get_data()

    current_time = time.time()

    if user.current_model == Model.GPT3:
        user_quota = Quota.GPT3
    elif user.current_model == Model.GPT4:
        user_quota = Quota.GPT4
    else:
        return
    need_exit = (await is_time_limit_exceeded(message, state, user, current_time) or
                 await is_messages_limit_exceeded(message, user, user_quota))
    if need_exit:
        return
    await state.update_data(last_request_time=current_time)

    text = user_data.get('recognized_text', None)
    if text is None:
        text = message.text

    await write_message(user.current_chat_id, "user", user.id, text)

    chat = await get_chat(user.current_chat_id)
    messages = await get_messages_by_chat_id(user.current_chat_id)
    sorted_messages = sorted(messages, key=lambda m: m.created_at)
    history = [
                  {
                      'role': 'system',
                      'content': getattr(get_localization(user.language_code), chat.role)["instruction"]
                  }
              ] + [
                  {
                      'role': message.sender,
                      'content': message.content
                  } for message in sorted_messages
              ]

    processing_message = await message.reply(text=get_localization(user.language_code).processing_request())

    if user.settings[UserSettings.TURN_ON_VOICE_MESSAGES]:
        await message.bot.send_chat_action(chat_id=message.chat.id, action=constants.ChatAction.RECORD_VOICE)
    else:
        await message.bot.send_chat_action(chat_id=message.chat.id, action=constants.ChatAction.TYPING)

    try:
        response = await get_response_message(user.current_model, history)
        response_message = response['message']
        if user_quota == Quota.GPT3:
            service = ServiceType.GPT3
            input_price = response['input_tokens'] * PRICE_GPT3_INPUT
            output_price = response['output_tokens'] * PRICE_GPT3_OUTPUT
        elif user_quota == Quota.GPT4:
            service = ServiceType.GPT4
            input_price = response['input_tokens'] * PRICE_GPT4_INPUT
            output_price = response['output_tokens'] * PRICE_GPT4_OUTPUT
        else:
            raise NotImplemented

        total_price = round(input_price + output_price, 6)
        await write_transaction(user_id=user.id,
                                type=TransactionType.EXPENSE,
                                service=service,
                                amount=total_price,
                                currency=Currency.USD,
                                quantity=1)

        role, content = response_message.role, response_message.content
        transaction = db.transaction()
        await create_new_message_and_update_user(transaction, role, content, user, user_quota)

        if user.settings[UserSettings.TURN_ON_VOICE_MESSAGES]:
            reply_markup = build_chat_gpt_continue_generating_keyboard(user.language_code)
            await reply_with_voice(message=message,
                                   text=content,
                                   user_id=user.id,
                                   reply_markup=reply_markup if response['finish_reason'] == 'length' else None)
        else:
            header_text = f'💬 {chat.title}\n\n' if user.settings[UserSettings.SHOW_NAME_OF_THE_CHAT] else ''
            footer_text = f'\n\n✉️ {user.monthly_limits[user_quota] + user.additional_usage_quota[user_quota] + 1}' \
                if user.settings[UserSettings.SHOW_USAGE_QUOTA] else ''
            reply_markup = build_chat_gpt_continue_generating_keyboard(user.language_code)
            await message.reply(
                f"{header_text}{content}{footer_text}",
                reply_markup=reply_markup if response['finish_reason'] == 'length' else None,
            )
    except Exception as e:
        await message.answer(f"{get_localization(user.language_code).ERROR}: {e}\n\nPlease contact @roman_danilov")
        await send_message_to_admins(bot=message.bot,
                                     message=f"#error\n\nALARM! Ошибка у пользователя: {user.id}\nИнформация:\n{e}")
    finally:
        await processing_message.delete()
