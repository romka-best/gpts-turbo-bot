import asyncio
import logging

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError

from bot.database.operations.user.getters import get_users_by_language_code
from bot.database.operations.user.updaters import update_user


async def send_message_to_users(bot: Bot, language_code: str, message: str):
    users = await get_users_by_language_code(language_code)
    for user in users:
        try:
            if not user.is_blocked:
                asyncio.create_task(
                    bot.send_message(chat_id=user.telegram_chat_id, text=message, disable_notification=True)
                )
        except TelegramForbiddenError:
            asyncio.create_task(update_user(user.id, {'is_blocked': True}))
        except TelegramBadRequest as error:
            logging.error(error)
