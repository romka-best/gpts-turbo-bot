from typing import Dict

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.database.models.common import Model, DALLEResolution, DALLEQuality
from bot.database.models.user import UserSettings
from bot.locales.main import get_localization


def build_settings_choose_model_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=f"{get_localization(language_code).CHATGPT3} / {get_localization(language_code).CHATGPT4}",
                callback_data=f'settings_choose_model:{Model.GPT3}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).DALLE3,
                callback_data=f'settings_choose_model:{Model.DALLE3}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).FACE_SWAP,
                callback_data=f'settings_choose_model:{Model.FACE_SWAP}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).MUSIC_GEN,
                callback_data=f'settings_choose_model:{Model.MUSIC_GEN}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CLOSE,
                callback_data='settings_choose_model:close'
            ),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_settings_keyboard(language_code: str, model: Model, settings: Dict) -> InlineKeyboardMarkup:
    buttons = []
    if model == Model.GPT3 or model == Model.GPT4:
        buttons = [
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).SHOW_THE_NAME_OF_THE_CHATS + (
                        " ✅" if settings[model][UserSettings.SHOW_THE_NAME_OF_THE_CHATS] else " ❌"),
                    callback_data=f'setting:{UserSettings.SHOW_THE_NAME_OF_THE_CHATS}:{Model.GPT3}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).SHOW_THE_NAME_OF_THE_ROLES + (
                        " ✅" if settings[model][UserSettings.SHOW_THE_NAME_OF_THE_ROLES] else " ❌"),
                    callback_data=f'setting:{UserSettings.SHOW_THE_NAME_OF_THE_ROLES}:{Model.GPT3}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).SHOW_USAGE_QUOTA_IN_MESSAGES + (
                        " ✅" if settings[model][UserSettings.SHOW_USAGE_QUOTA] else " ❌"),
                    callback_data=f'setting:{UserSettings.SHOW_USAGE_QUOTA}:{Model.GPT3}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).VOICE_MESSAGES,
                    callback_data=f'setting:voice_messages:{Model.GPT3}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).MANAGE_CHATS,
                    callback_data=f'setting:manage_chats:{Model.GPT3}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).MANAGE_CATALOG,
                    callback_data=f'setting:manage_catalog:{Model.GPT3}'
                ),
            ],
        ]
    elif model == Model.DALLE3:
        buttons = [
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).SHOW_USAGE_QUOTA_IN_MESSAGES + (
                        " ✅" if settings[model][UserSettings.SHOW_USAGE_QUOTA] else " ❌"),
                    callback_data=f'setting:{UserSettings.SHOW_USAGE_QUOTA}:{Model.DALLE3}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=DALLEResolution.LOW + (
                        " ✅" if settings[model][UserSettings.RESOLUTION] == DALLEResolution.LOW else ""),
                    callback_data=f'setting:{DALLEResolution.LOW}:{Model.DALLE3}'
                ),
                InlineKeyboardButton(
                    text=DALLEResolution.MEDIUM + (
                        " ✅" if settings[model][UserSettings.RESOLUTION] == DALLEResolution.MEDIUM else ""),
                    callback_data=f'setting:{DALLEResolution.MEDIUM}:{Model.DALLE3}'
                ),
                InlineKeyboardButton(
                    text=DALLEResolution.HIGH + (
                        " ✅" if settings[model][UserSettings.RESOLUTION] == DALLEResolution.HIGH else ""),
                    callback_data=f'setting:{DALLEResolution.HIGH}:{Model.DALLE3}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=DALLEQuality.STANDARD + (
                        " ✅" if settings[model][UserSettings.QUALITY] == DALLEQuality.STANDARD else ""),
                    callback_data=f'setting:{DALLEQuality.STANDARD}:{Model.DALLE3}'
                ),
                InlineKeyboardButton(
                    text=DALLEQuality.HD + (
                        " ✅" if settings[model][UserSettings.QUALITY] == DALLEQuality.HD else ""),
                    callback_data=f'setting:{DALLEQuality.HD}:{Model.DALLE3}'
                ),
            ],
        ]
    elif model == Model.FACE_SWAP:
        buttons = [
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).SHOW_USAGE_QUOTA_IN_MESSAGES + (
                        " ✅" if settings[model][UserSettings.SHOW_USAGE_QUOTA] else " ❌"),
                    callback_data=f'setting:{UserSettings.SHOW_USAGE_QUOTA}:{Model.FACE_SWAP}'
                ),
            ],
        ]
    elif model == Model.MUSIC_GEN:
        buttons = [
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).SHOW_USAGE_QUOTA_IN_MESSAGES + (
                        " ✅" if settings[model][UserSettings.SHOW_USAGE_QUOTA] else " ❌"),
                    callback_data=f'setting:{UserSettings.SHOW_USAGE_QUOTA}:{Model.MUSIC_GEN}'
                ),
            ],
        ]

    buttons.append([
        InlineKeyboardButton(
            text=get_localization(language_code).BACK,
            callback_data='setting:back'
        )
    ], )

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_voice_messages_settings_keyboard(language_code: str, settings: Dict) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).TURN_ON_VOICE_MESSAGES_FROM_RESPONDS + (
                    " ✅" if settings[Model.GPT3][UserSettings.TURN_ON_VOICE_MESSAGES] else " ❌"),
                callback_data=f'voice_messages_setting:{UserSettings.TURN_ON_VOICE_MESSAGES}'
            ),
        ],
        [
            InlineKeyboardButton(
                text="👕 alloy" + (" ✅" if settings[Model.GPT3][UserSettings.VOICE] == "alloy" else ""),
                callback_data=f'voice_messages_setting:alloy'
            ),
            InlineKeyboardButton(
                text="👕 echo" + (" ✅" if settings[Model.GPT3][UserSettings.VOICE] == "echo" else ""),
                callback_data=f'voice_messages_setting:echo'
            ),
        ],
        [
            InlineKeyboardButton(
                text="👚 nova" + (" ✅" if settings[Model.GPT3][UserSettings.VOICE] == "nova" else ""),
                callback_data=f'voice_messages_setting:nova'
            ),
            InlineKeyboardButton(
                text="👚 shimmer" + (" ✅" if settings[Model.GPT3][UserSettings.VOICE] == "shimmer" else ""),
                callback_data=f'voice_messages_setting:shimmer'
            ),
        ],
        [
            InlineKeyboardButton(
                text="👕 fable" + (" ✅" if settings[Model.GPT3][UserSettings.VOICE] == "fable" else ""),
                callback_data=f'voice_messages_setting:fable'
            ),
            InlineKeyboardButton(
                text="👕 onyx" + (" ✅" if settings[Model.GPT3][UserSettings.VOICE] == "onyx" else ""),
                callback_data=f'voice_messages_setting:onyx'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).LISTEN_VOICES,
                callback_data=f'voice_messages_setting:listen'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).BACK,
                callback_data='voice_messages_setting:back'
            )
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
