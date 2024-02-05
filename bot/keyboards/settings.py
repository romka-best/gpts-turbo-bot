from typing import Dict

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.database.models.common import Model
from bot.database.models.user import UserSettings
from bot.locales.main import get_localization


def build_settings_keyboard(language_code: str, model: Model, settings: Dict) -> InlineKeyboardMarkup:
    buttons = []
    if model == Model.GPT3 or model == Model.GPT4:
        buttons = [
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).SHOW_THE_NAME_OF_THE_CHATS + (
                        " ✅" if settings[model][UserSettings.SHOW_THE_NAME_OF_THE_CHATS] else " ❌"),
                    callback_data=f'setting:{UserSettings.SHOW_THE_NAME_OF_THE_CHATS}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).SHOW_THE_NAME_OF_THE_ROLES + (
                        " ✅" if settings[model][UserSettings.SHOW_THE_NAME_OF_THE_ROLES] else " ❌"),
                    callback_data=f'setting:{UserSettings.SHOW_THE_NAME_OF_THE_ROLES}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).SHOW_USAGE_QUOTA_IN_MESSAGES + (
                        " ✅" if settings[model][UserSettings.SHOW_USAGE_QUOTA] else " ❌"),
                    callback_data=f'setting:{UserSettings.SHOW_USAGE_QUOTA}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).TURN_ON_VOICE_MESSAGES_FROM_RESPONDS + (
                        " ✅" if settings[model][UserSettings.TURN_ON_VOICE_MESSAGES] else " ❌"
                    ),
                    callback_data=f'setting:{UserSettings.TURN_ON_VOICE_MESSAGES}'
                ),
            ],
        ]
    elif model == Model.DALLE3:
        buttons = [
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).SHOW_USAGE_QUOTA_IN_MESSAGES + (
                        " ✅" if settings[model][UserSettings.SHOW_USAGE_QUOTA] else " ❌"),
                    callback_data=f'setting:{UserSettings.SHOW_USAGE_QUOTA}'
                ),
            ],
        ]
    elif model == Model.FACE_SWAP:
        buttons = [
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).SHOW_USAGE_QUOTA_IN_MESSAGES + (
                        " ✅" if settings[model][UserSettings.SHOW_USAGE_QUOTA] else " ❌"),
                    callback_data=f'setting:{UserSettings.SHOW_USAGE_QUOTA}'
                ),
            ],
        ]
    elif model == Model.MUSIC_GEN:
        buttons = [
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).SHOW_USAGE_QUOTA_IN_MESSAGES + (
                        " ✅" if settings[model][UserSettings.SHOW_USAGE_QUOTA] else " ❌"),
                    callback_data=f'setting:{UserSettings.SHOW_USAGE_QUOTA}'
                ),
            ],
        ]

    buttons.append([
        InlineKeyboardButton(
            text=get_localization(language_code).CLOSE,
            callback_data='setting:close'
        )
    ], )

    return InlineKeyboardMarkup(inline_keyboard=buttons)
