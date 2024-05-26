from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.database.models.user import UserGender
from bot.locales.main import get_localization


def build_profile_keyboard(language_code: str, is_photo_uploaded: bool, is_gender_chosen: bool) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CHANGE_PHOTO if is_photo_uploaded else get_localization(
                    language_code).UPLOAD_PHOTO,
                callback_data=f'profile:change_photo'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CHANGE_GENDER if is_gender_chosen else get_localization(
                    language_code).CHOOSE_GENDER,
                callback_data=f'profile:change_gender'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).OPEN_BONUS_INFO,
                callback_data=f'profile:open_bonus_info'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).OPEN_BUY_SUBSCRIPTIONS_INFO,
                callback_data=f'profile:open_buy_subscriptions_info'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).OPEN_BUY_PACKAGES_INFO,
                callback_data=f'profile:open_buy_packages_info'
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
