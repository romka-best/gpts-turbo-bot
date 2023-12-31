from typing import Dict

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.database.models.user import UserSettings
from bot.locales.main import get_localization


def build_settings_keyboard(language_code: str, settings: Dict) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).SHOW_NAME_OF_THE_CHAT + (
                    " ✅" if settings[UserSettings.SHOW_NAME_OF_THE_CHAT] else " ❌"),
                callback_data=f'setting:{UserSettings.SHOW_NAME_OF_THE_CHAT}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).SHOW_USAGE_QUOTA_IN_MESSAGES + (
                    " ✅" if settings[UserSettings.SHOW_USAGE_QUOTA] else " ❌"),
                callback_data=f'setting:{UserSettings.SHOW_USAGE_QUOTA}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).TURN_ON_VOICE_MESSAGES_FROM_RESPONDS + (
                    " ✅" if settings[UserSettings.TURN_ON_VOICE_MESSAGES] else " ❌"
                ),
                callback_data=f'setting:{UserSettings.TURN_ON_VOICE_MESSAGES}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CLOSE,
                callback_data='close'
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
