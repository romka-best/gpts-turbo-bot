import logging

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest

from bot.database.operations.user import get_users_by_language_code


async def send_message_to_users(bot: Bot, language_code: str, message: str):
    users = await get_users_by_language_code(language_code)
    for user in users:
        try:
            await bot.send_message(
                chat_id=user.telegram_chat_id,
                text=message,
            )
        except TelegramBadRequest as error:
            logging.error(error)
