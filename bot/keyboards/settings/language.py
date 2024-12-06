from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.locales.main import get_localization
from bot.locales.types import LanguageCode


def build_language_keyboard(language_code: LanguageCode) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text='🇺🇸 English',
                callback_data=f'language:{LanguageCode.EN}',
            ),
            InlineKeyboardButton(
                text='🇷🇺 Русский',
                callback_data=f'language:{LanguageCode.RU}',
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CLOSE,
                callback_data='language:close'
            ),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
