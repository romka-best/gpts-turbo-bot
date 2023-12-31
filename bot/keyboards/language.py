from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.locales.main import get_localization


def build_language_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text="🇺🇸 English",
                callback_data='language:en',
            ),
            InlineKeyboardButton(
                text="🇷🇺 Русский",
                callback_data='language:ru',
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CLOSE,
                callback_data='close'
            ),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
