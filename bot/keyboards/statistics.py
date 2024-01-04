from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.locales.main import get_localization


def build_statistics_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text="За день 📅",
                callback_data=f'statistics:day'
            )
        ],
        [
            InlineKeyboardButton(
                text="За неделю 📆",
                callback_data=f'statistics:week'
            )
        ],
        [
            InlineKeyboardButton(
                text="За месяц 🗓️",
                callback_data=f'statistics:month'
            )
        ],
        [
            InlineKeyboardButton(
                text="За всё время ⏳",
                callback_data=f'statistics:all'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CLOSE,
                callback_data='statistics:close'
            )
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
