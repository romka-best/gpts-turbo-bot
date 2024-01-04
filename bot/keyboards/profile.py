from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.database.models.user import UserGender
from bot.locales.main import get_localization


def build_profile_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CHANGE_PHOTO,
                callback_data=f'profile:change_photo'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CHANGE_GENDER,
                callback_data=f'profile:change_gender'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CLOSE,
                callback_data=f'profile:close'
            ),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_profile_gender_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).MALE,
                callback_data=f'profile_gender:{UserGender.MALE}'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).FEMALE,
                callback_data=f'profile_gender:{UserGender.FEMALE}'
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
