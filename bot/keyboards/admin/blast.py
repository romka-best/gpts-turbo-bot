from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.locales.main import get_localization
from bot.locales.types import LanguageCode


def build_blast_keyboard(language_code: LanguageCode) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text='🆓 Только бесплатные подписчики',
                callback_data='blast:free',
            ),
        ],
        [
            InlineKeyboardButton(
                text='💰 Только платные подписчики',
                callback_data='blast:paid',
            ),
        ],
        [
            InlineKeyboardButton(
                text='🌍 Все',
                callback_data='blast:all',
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).BACK,
                callback_data='blast:back'
            ),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_blast_language_keyboard(language_code: LanguageCode) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text='🇺🇸 English',
                callback_data='blast_language:en',
            ),
            InlineKeyboardButton(
                text='🇷🇺 Русский',
                callback_data='blast_language:ru',
            ),
        ],
        [
            InlineKeyboardButton(
                text='🌍 Для всех',
                callback_data='blast_language:all',
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).BACK,
                callback_data='blast_language:back'
            ),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_blast_confirmation_keyboard(language_code: LanguageCode) -> InlineKeyboardMarkup:
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
