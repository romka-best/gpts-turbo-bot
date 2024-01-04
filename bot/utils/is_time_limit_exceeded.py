import asyncio

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from telegram import constants

from bot.config import config
from bot.database.models.common import Quota, Model
from bot.database.models.user import User
from bot.locales.main import get_localization


async def notify_user_after_timeout(bot: Bot, chat_id: int, delay: int, language_code: str, reply_to_message_id: int):
    await asyncio.sleep(delay)

    await bot.send_chat_action(chat_id=chat_id, action=constants.ChatAction.TYPING)
    await bot.send_message(
        chat_id=chat_id,
        text=get_localization(language_code).READY_FOR_NEW_REQUEST,
        reply_to_message_id=reply_to_message_id
    )


async def is_time_limit_exceeded(message: Message, state: FSMContext, user: User, current_time: float) -> bool:
    if user.additional_usage_quota[Quota.FAST_MESSAGES] or user.current_model == Model.FACE_SWAP:
        return False

    user_data = await state.get_data()
    last_request_time = user_data.get('last_request_time', None)

    if not last_request_time:
        return False

    time_elapsed = current_time - last_request_time
    if time_elapsed >= config.LIMIT_BETWEEN_REQUESTS_SECONDS:
        await state.clear()
        return False

    remaining_time = int(config.LIMIT_BETWEEN_REQUESTS_SECONDS - time_elapsed)
    if user_data.get('additional_request_made'):
        await message.reply(text=get_localization(user.language_code).ALREADY_MAKE_REQUEST)
    else:
        await state.update_data(additional_request_made=True)
        await message.reply(text=get_localization(user.language_code).wait_for_another_request(remaining_time))
        asyncio.create_task(notify_user_after_timeout(
            bot=message.bot,
            chat_id=message.chat.id,
            delay=remaining_time,
            language_code=user.language_code,
            reply_to_message_id=message.message_id
        ))
    return True
