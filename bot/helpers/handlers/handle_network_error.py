from aiogram import Bot

from bot.config import config, MessageSticker
from bot.database.operations.user.getters import get_user
from bot.locales.main import get_localization


async def handle_network_error(bot: Bot, user_id: str):
    if user_id:
        user = await get_user(user_id)
        if user:
            await bot.send_sticker(
                chat_id=user.telegram_chat_id,
                sticker=config.MESSAGE_STICKERS.get(MessageSticker.CONNECTION_ERROR),
            )
            await bot.send_message(
                chat_id=user.telegram_chat_id,
                text=get_localization(user.interface_language_code).NETWORK_ERROR,
            )
