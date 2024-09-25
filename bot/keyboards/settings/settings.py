from typing import Dict

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.database.models.common import (
    Model,
    DALLEVersion,
    DALLEResolution,
    DALLEQuality,
    MidjourneyVersion,
    SunoSendType, SunoVersion,
)
from bot.database.models.user import UserSettings
from bot.locales.main import get_localization


def build_settings_choose_model_type_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).TEXT_MODELS,
                callback_data=f'settings_choose_model_type:text_models'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).IMAGE_MODELS,
                callback_data=f'settings_choose_model_type:image_models'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).MUSIC_MODELS,
                callback_data=f'settings_choose_model_type:music_models'
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


def build_settings_choose_text_model_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=f'{get_localization(language_code).CHATGPT}',
                callback_data=f'settings_choose_text_model:{Model.CHAT_GPT}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=f'{get_localization(language_code).CLAUDE}',
                callback_data=f'settings_choose_text_model:{Model.CLAUDE}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=f'{get_localization(language_code).GEMINI}',
                callback_data=f'settings_choose_text_model:{Model.GEMINI}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).VOICE_MESSAGES,
                callback_data=f'settings_choose_text_model:voice_messages'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).MANAGE_CHATS,
                callback_data=f'settings_choose_text_model:manage_chats'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).MANAGE_CATALOG,
                callback_data=f'settings_choose_text_model:manage_catalog'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).BACK,
                callback_data='settings_choose_text_model:back'
            ),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_settings_choose_image_model_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).DALL_E,
                callback_data=f'settings_choose_image_model:{Model.DALL_E}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).MIDJOURNEY,
                callback_data=f'settings_choose_image_model:{Model.MIDJOURNEY}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).STABLE_DIFFUSION,
                callback_data=f'settings_choose_image_model:{Model.STABLE_DIFFUSION}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).FACE_SWAP,
                callback_data=f'settings_choose_image_model:{Model.FACE_SWAP}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).BACK,
                callback_data='settings_choose_image_model:back'
            ),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_settings_choose_music_model_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).MUSIC_GEN,
                callback_data=f'settings_choose_music_model:{Model.MUSIC_GEN}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).SUNO,
                callback_data=f'settings_choose_music_model:{Model.SUNO}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).BACK,
                callback_data='settings_choose_music_model:back'
            ),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_settings_keyboard(language_code: str, model: Model, model_type: str, settings: Dict) -> InlineKeyboardMarkup:
    buttons = []
    if model == Model.CHAT_GPT or model == Model.CLAUDE or model == Model.GEMINI:
        buttons = [
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).SHOW_THE_NAME_OF_THE_CHATS + (
                        ' ✅' if settings[model][UserSettings.SHOW_THE_NAME_OF_THE_CHATS] else ' ❌'
                    ),
                    callback_data=f'setting:{UserSettings.SHOW_THE_NAME_OF_THE_CHATS}:{model}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).SHOW_THE_NAME_OF_THE_ROLES + (
                        ' ✅' if settings[model][UserSettings.SHOW_THE_NAME_OF_THE_ROLES] else ' ❌'
                    ),
                    callback_data=f'setting:{UserSettings.SHOW_THE_NAME_OF_THE_ROLES}:{model}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).SHOW_USAGE_QUOTA_IN_MESSAGES + (
                        ' ✅' if settings[model][UserSettings.SHOW_USAGE_QUOTA] else ' ❌'
                    ),
                    callback_data=f'setting:{UserSettings.SHOW_USAGE_QUOTA}:{model}'
                ),
            ],
        ]
    elif model == Model.DALL_E:
        buttons = [
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).SHOW_USAGE_QUOTA_IN_MESSAGES + (
                        ' ✅' if settings[model][UserSettings.SHOW_USAGE_QUOTA] else ' ❌'),
                    callback_data=f'setting:{UserSettings.SHOW_USAGE_QUOTA}:{Model.DALL_E}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=DALLEResolution.LOW + (
                        ' ✅' if settings[model][UserSettings.RESOLUTION] == DALLEResolution.LOW else ''),
                    callback_data=f'setting:{DALLEResolution.LOW}:{Model.DALL_E}'
                ),
                InlineKeyboardButton(
                    text=DALLEResolution.MEDIUM + (
                        ' ✅' if settings[model][UserSettings.RESOLUTION] == DALLEResolution.MEDIUM else ''),
                    callback_data=f'setting:{DALLEResolution.MEDIUM}:{Model.DALL_E}'
                ),
                InlineKeyboardButton(
                    text=DALLEResolution.HIGH + (
                        ' ✅' if settings[model][UserSettings.RESOLUTION] == DALLEResolution.HIGH else ''),
                    callback_data=f'setting:{DALLEResolution.HIGH}:{Model.DALL_E}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=DALLEQuality.STANDARD + (
                        ' ✅' if settings[model][UserSettings.QUALITY] == DALLEQuality.STANDARD else ''),
                    callback_data=f'setting:{DALLEQuality.STANDARD}:{Model.DALL_E}'
                ),
                InlineKeyboardButton(
                    text=DALLEQuality.HD + (
                        ' ✅' if settings[model][UserSettings.QUALITY] == DALLEQuality.HD else ''),
                    callback_data=f'setting:{DALLEQuality.HD}:{Model.DALL_E}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=DALLEVersion.V2 + (
                        ' ✅' if settings[model][UserSettings.VERSION] == DALLEVersion.V2 else ''),
                    callback_data=f'setting:{DALLEVersion.V2}:{Model.DALL_E}'
                ),
                InlineKeyboardButton(
                    text=DALLEVersion.V3 + (
                        ' ✅' if settings[model][UserSettings.VERSION] == DALLEVersion.V3 else ''),
                    callback_data=f'setting:{DALLEVersion.V3}:{Model.DALL_E}'
                ),
            ],
        ]
    elif model == Model.MIDJOURNEY:
        buttons = [
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).SHOW_USAGE_QUOTA_IN_MESSAGES + (
                        ' ✅' if settings[model][UserSettings.SHOW_USAGE_QUOTA] else ' ❌'),
                    callback_data=f'setting:{UserSettings.SHOW_USAGE_QUOTA}:{Model.MIDJOURNEY}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=MidjourneyVersion.V5 + (
                        ' ✅' if settings[model][UserSettings.VERSION] == MidjourneyVersion.V5 else ''),
                    callback_data=f'setting:{MidjourneyVersion.V5}:{Model.MIDJOURNEY}'
                ),
                InlineKeyboardButton(
                    text=MidjourneyVersion.V6 + (
                        ' ✅' if settings[model][UserSettings.VERSION] == MidjourneyVersion.V6 else ''),
                    callback_data=f'setting:{MidjourneyVersion.V6}:{Model.MIDJOURNEY}'
                ),
            ],
        ]
    elif model == Model.STABLE_DIFFUSION:
        buttons = [
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).SHOW_USAGE_QUOTA_IN_MESSAGES + (
                        ' ✅' if settings[model][UserSettings.SHOW_USAGE_QUOTA] else ' ❌'),
                    callback_data=f'setting:{UserSettings.SHOW_USAGE_QUOTA}:{Model.STABLE_DIFFUSION}'
                ),
            ],
        ]
    elif model == Model.FACE_SWAP:
        buttons = [
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).SHOW_USAGE_QUOTA_IN_MESSAGES + (
                        ' ✅' if settings[model][UserSettings.SHOW_USAGE_QUOTA] else ' ❌'),
                    callback_data=f'setting:{UserSettings.SHOW_USAGE_QUOTA}:{Model.FACE_SWAP}'
                ),
            ],
        ]
    elif model == Model.MUSIC_GEN:
        buttons = [
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).SHOW_USAGE_QUOTA_IN_MESSAGES + (
                        ' ✅' if settings[model][UserSettings.SHOW_USAGE_QUOTA] else ' ❌'),
                    callback_data=f'setting:{UserSettings.SHOW_USAGE_QUOTA}:{Model.MUSIC_GEN}'
                ),
            ],
        ]
    elif model == Model.SUNO:
        buttons = [
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).SHOW_USAGE_QUOTA_IN_MESSAGES + (
                        ' ✅' if settings[model][UserSettings.SHOW_USAGE_QUOTA] else ' ❌'),
                    callback_data=f'setting:{UserSettings.SHOW_USAGE_QUOTA}:{Model.SUNO}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).AUDIO + (
                        ' ✅' if settings[model][UserSettings.SEND_TYPE] == SunoSendType.AUDIO else ''),
                    callback_data=f'setting:{SunoSendType.AUDIO}:{Model.SUNO}'
                ),
                InlineKeyboardButton(
                    text=get_localization(language_code).VIDEO + (
                        ' ✅' if settings[model][UserSettings.SEND_TYPE] == SunoSendType.VIDEO else ''),
                    callback_data=f'setting:{SunoSendType.VIDEO}:{Model.SUNO}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=SunoVersion.V3 + (
                        ' ✅' if settings[model][UserSettings.VERSION] == SunoVersion.V3 else ''),
                    callback_data=f'setting:{SunoVersion.V3}:{Model.SUNO}'
                ),
                InlineKeyboardButton(
                    text=SunoVersion.V3_5 + (
                        ' ✅' if settings[model][UserSettings.VERSION] == SunoVersion.V3_5 else ''),
                    callback_data=f'setting:{SunoVersion.V3_5}:{Model.SUNO}'
                ),
            ],
        ]

    buttons.append([
        InlineKeyboardButton(
            text=get_localization(language_code).BACK,
            callback_data=f'setting:back:{model_type}'
        )
    ], )

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_voice_messages_settings_keyboard(language_code: str, settings: Dict) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).TURN_ON_VOICE_MESSAGES_FROM_RESPONDS + (
                    ' ✅' if settings[Model.CHAT_GPT][UserSettings.TURN_ON_VOICE_MESSAGES] else ' ❌'),
                callback_data=f'voice_messages_setting:{UserSettings.TURN_ON_VOICE_MESSAGES}'
            ),
        ],
        [
            InlineKeyboardButton(
                text='👕 alloy' + (' ✅' if settings[Model.CHAT_GPT][UserSettings.VOICE] == 'alloy' else ''),
                callback_data=f'voice_messages_setting:alloy'
            ),
            InlineKeyboardButton(
                text='👕 echo' + (' ✅' if settings[Model.CHAT_GPT][UserSettings.VOICE] == 'echo' else ''),
                callback_data=f'voice_messages_setting:echo'
            ),
        ],
        [
            InlineKeyboardButton(
                text='👚 nova' + (' ✅' if settings[Model.CHAT_GPT][UserSettings.VOICE] == 'nova' else ''),
                callback_data=f'voice_messages_setting:nova'
            ),
            InlineKeyboardButton(
                text='👚 shimmer' + (' ✅' if settings[Model.CHAT_GPT][UserSettings.VOICE] == 'shimmer' else ''),
                callback_data=f'voice_messages_setting:shimmer'
            ),
        ],
        [
            InlineKeyboardButton(
                text='👕 fable' + (' ✅' if settings[Model.CHAT_GPT][UserSettings.VOICE] == 'fable' else ''),
                callback_data=f'voice_messages_setting:fable'
            ),
            InlineKeyboardButton(
                text='👕 onyx' + (' ✅' if settings[Model.CHAT_GPT][UserSettings.VOICE] == 'onyx' else ''),
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
