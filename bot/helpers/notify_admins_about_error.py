import logging

from aiogram import Bot, Dispatcher
from aiogram.types import Update

from bot.database.main import firebase
from bot.database.operations.user.getters import get_user
from bot.helpers.initialize_user_for_the_first_time import initialize_user_for_the_first_time
from bot.helpers.senders.send_message_to_admins import send_message_to_admins
from bot.keyboards.common.common import build_recommendations_keyboard
from bot.locales.main import get_localization, set_user_language, get_user_language


async def notify_admins_about_error(bot: Bot, telegram_update: Update, dp: Dispatcher, e):
    try:
        user_id = None
        if telegram_update.callback_query and telegram_update.callback_query.from_user.id:
            user_id = str(telegram_update.callback_query.from_user.id)
        elif telegram_update.message and telegram_update.message.from_user.id:
            user_id = str(telegram_update.message.from_user.id)

        if user_id:
            user = await get_user(user_id)
            if not user:
                if telegram_update.callback_query:
                    language_code = telegram_update.callback_query.from_user.language_code
                    telegram_user = telegram_update.callback_query.from_user
                    chat_id = str(telegram_update.callback_query.message.chat.id)
                elif telegram_update.message:
                    language_code = telegram_update.message.from_user.language_code
                    telegram_user = telegram_update.message.from_user
                    chat_id = str(telegram_update.message.chat.id)
                else:
                    raise

                await set_user_language(user_id, language_code, dp.storage)

                chat_title = get_localization(language_code).DEFAULT_CHAT_TITLE
                transaction = firebase.db.transaction()
                await initialize_user_for_the_first_time(
                    transaction,
                    telegram_user,
                    chat_id,
                    chat_title,
                    None,
                    False,
                )

                user = await get_user(str(telegram_user.id))
                user_language_code = await get_user_language(user_id, dp.storage)

                greeting = get_localization(user_language_code).START
                reply_markup = await build_recommendations_keyboard(user.current_model, user_language_code, user.gender)
                await bot.send_message(
                    chat_id=chat_id,
                    text=greeting,
                    reply_markup=reply_markup,
                )
            else:
                await bot.send_message(
                    chat_id=user.telegram_chat_id,
                    text=get_localization(user.interface_language_code).ERROR,
                )
                await send_message_to_admins(
                    bot=bot,
                    message=f"#error\n\nALARM! Ошибка у пользователя: {user.id}\n"
                            f"Информация:\n{e}",
                    parse_mode=None,
                )
    except Exception as e:
        logging.exception(f"Error in notify_admins_about_error: {e}")

        await send_message_to_admins(
            bot=bot,
            message=f"#error\n\nALARM! ALARM! ALARM! Неизвестная ошибка\n"
                    f"Информация:\n{e}",
            parse_mode=None,
        )
