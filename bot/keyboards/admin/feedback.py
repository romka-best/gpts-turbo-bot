from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.locales.main import get_localization


def build_manage_feedback_keyboard(language_code: str, user_id: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).FEEDBACK_ADMIN_APPROVE,
                callback_data=f'manage_feedback:approve:{user_id}'
            ),
            InlineKeyboardButton(
                text=get_localization(language_code).FEEDBACK_ADMIN_DENY,
                callback_data=f'manage_feedback:deny:{user_id}'
            ),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)

