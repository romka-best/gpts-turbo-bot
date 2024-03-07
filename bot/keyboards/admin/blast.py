from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.locales.main import get_localization


def build_blast_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text="🇺🇸 English",
                callback_data='blast:en',
            ),
            InlineKeyboardButton(
                text="🇷🇺 Русский",
                callback_data='blast:ru',
            ),
        ],
        [
            InlineKeyboardButton(
                text="🌍 Для всех",
                callback_data='blast:all',
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CLOSE,
                callback_data='blast:close'
            ),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_blast_confirmation_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).APPROVE,
                callback_data='blast_confirmation:approve'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CANCEL,
                callback_data='blast_confirmation:cancel'
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
