from aiogram.types import Update


def get_user_id_from_telegram_update(telegram_update: Update):
    user_id = None
    if telegram_update.callback_query and telegram_update.callback_query.from_user.id:
        user_id = str(telegram_update.callback_query.from_user.id)
    elif telegram_update.message and telegram_update.message.from_user.id:
        user_id = str(telegram_update.message.from_user.id)

    return user_id
