import logging

from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram import Bot

from bot.config import config


async def send_message_to_developers(bot: Bot, message: str, parse_mode='HTML'):
    for chat_id in config.DEVELOPER_IDS:
        try:
            await bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode=parse_mode,
            )
        except (TelegramBadRequest, TelegramForbiddenError) as error:
            logging.error(error)
