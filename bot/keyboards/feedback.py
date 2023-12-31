from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.locales.main import get_localization


def build_feedback_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CANCEL,
                callback_data='cancel'
            ),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
