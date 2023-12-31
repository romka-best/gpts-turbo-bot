import logging

from aiogram.exceptions import TelegramBadRequest
from aiogram import Bot

from bot.config import config


async def send_message_to_admins(bot: Bot, message: str):
    for chat_id in config.ADMIN_CHAT_IDS:
        try:
            await bot.send_message(chat_id=chat_id, text=message)
        except TelegramBadRequest as error:
            logging.error(error)
