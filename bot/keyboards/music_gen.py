from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.locales.main import get_localization


def build_music_gen_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).SECONDS_30,
                callback_data=f'music_gen:30'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).SECONDS_60,
                callback_data=f'music_gen:60'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).SECONDS_180,
                callback_data=f'music_gen:180'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CANCEL,
                callback_data=f'music_gen:cancel'
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
