from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.database.models.common import RoleName
from bot.locales.main import get_localization


def build_catalog_keyboard(language_code: str, current_role: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).PERSONAL_ASSISTANT['name'] + (
                    " ✅" if current_role == RoleName.PERSONAL_ASSISTANT else " ❌"
                ),
                callback_data=f'catalog:{RoleName.PERSONAL_ASSISTANT}'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).TUTOR['name'] + (
                    " ✅" if current_role == RoleName.TUTOR else " ❌"
                ),
                callback_data=f'catalog:{RoleName.TUTOR}'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).LANGUAGE_TUTOR['name'] + (
                    " ✅" if current_role == RoleName.LANGUAGE_TUTOR else " ❌"
                ),
                callback_data=f'catalog:{RoleName.LANGUAGE_TUTOR}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CREATIVE_WRITER['name'] + (
                    " ✅" if current_role == RoleName.CREATIVE_WRITER else " ❌"
                ),
                callback_data=f'catalog:{RoleName.CREATIVE_WRITER}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).TECHNICAL_ADVISOR['name'] + (
                    " ✅" if current_role == RoleName.TECHNICAL_ADVISOR else " ❌"
                ),
                callback_data=f'catalog:{RoleName.TECHNICAL_ADVISOR}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).MARKETER['name'] + (
                    " ✅" if current_role == RoleName.MARKETER else " ❌"
                ),
                callback_data=f'catalog:{RoleName.MARKETER}'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).SMM_SPECIALIST['name'] + (
                    " ✅" if current_role == RoleName.SMM_SPECIALIST else " ❌"
                ),
                callback_data=f'catalog:{RoleName.SMM_SPECIALIST}'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CONTENT_SPECIALIST['name'] + (
                    " ✅" if current_role == RoleName.CONTENT_SPECIALIST else " ❌"
                ),
                callback_data=f'catalog:{RoleName.CONTENT_SPECIALIST}'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).DESIGNER['name'] + (
                    " ✅" if current_role == RoleName.DESIGNER else " ❌"
                ),
                callback_data=f'catalog:{RoleName.DESIGNER}'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).SOCIAL_MEDIA_PRODUCER['name'] + (
                    " ✅" if current_role == RoleName.SOCIAL_MEDIA_PRODUCER else " ❌"
                ),
                callback_data=f'catalog:{RoleName.SOCIAL_MEDIA_PRODUCER}'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).LIFE_COACH['name'] + (
                    " ✅" if current_role == RoleName.LIFE_COACH else " ❌"
                ),
                callback_data=f'catalog:{RoleName.LIFE_COACH}'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).ENTREPRENEUR['name'] + (
                    " ✅" if current_role == {RoleName.ENTREPRENEUR} else " ❌"
                ),
                callback_data=f'catalog:{RoleName.ENTREPRENEUR}'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CLOSE,
                callback_data='catalog:close'
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
