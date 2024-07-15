import logging

from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram import Bot

from bot.config import config


async def send_message_to_admins_and_developers(bot: Bot, message: str, parse_mode='HTML'):
    for chat_id in list(set(id for ids in [config.ADMIN_IDS, config.DEVELOPER_IDS] for id in ids)):
        try:
            await bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode=parse_mode,
            )
        except (TelegramBadRequest, TelegramForbiddenError) as error:
            logging.error(error)
