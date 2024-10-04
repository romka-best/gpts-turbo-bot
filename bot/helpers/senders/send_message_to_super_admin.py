import logging

from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram import Bot

from bot.config import config


async def send_message_to_super_admin(bot: Bot, message: str, parse_mode='HTML'):
    try:
        await bot.send_message(
            chat_id=config.SUPER_ADMIN_ID,
            text=message,
            parse_mode=parse_mode,
        )
    except (TelegramBadRequest, TelegramForbiddenError) as error:
        logging.error(error)
