import logging

from aiogram import Bot
from aiogram.types import Update

from bot.database.operations.user.getters import get_user
from bot.helpers.senders.send_message_to_admins import send_message_to_admins
from bot.locales.main import get_localization


async def notify_admins_about_error(bot: Bot, telegram_update: Update, e):
    try:
        user_id = None
        if telegram_update.callback_query and telegram_update.callback_query.from_user.id:
            user_id = str(telegram_update.callback_query.from_user.id)
        elif telegram_update.message and telegram_update.message.from_user.id:
            user_id = str(telegram_update.message.from_user.id)

        if user_id:
            user = await get_user(user_id)
            await bot.send_message(
                chat_id=user.telegram_chat_id,
                text=get_localization(user.language_code).ERROR,
            )
            await send_message_to_admins(
                bot=bot,
                message=f"#error\n\nALARM! Ошибка у пользователя: {user.id}\n"
                        f"Информация:\n{e}",
                parse_mode=None,
            )
    except Exception as e:
        logging.exception(f"Error in notify_admins_about_error: {e}")
