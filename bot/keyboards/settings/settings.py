from typing import Dict, Optional

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.database.models.common import (
    Model,
    DALLEVersion,
    DALLEResolution,
    DALLEQuality,
    MidjourneyVersion,
    SunoSendType,
    SunoVersion, FluxSafetyTolerance,
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
                text=get_localization(language_code).FLUX,
                callback_data=f'settings_choose_image_model:{Model.FLUX}'
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
                text=get_localization(language_code).PHOTOSHOP_AI,
                callback_data=f'settings_choose_image_model:{Model.PHOTOSHOP_AI}'
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


def build_settings_keyboard(
    language_code: str,
    model: Model,
    model_type: str,
    settings: Dict,
    show_back_button=True,
    show_advanced_settings=False,
) -> InlineKeyboardMarkup:
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

        if show_advanced_settings:
            buttons.extend(
                [
                    [
                        InlineKeyboardButton(
                            text=get_localization(language_code).VOICE_MESSAGES,
                            callback_data=f'setting:voice_messages:{model}'
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text=get_localization(language_code).MANAGE_CHATS,
                            callback_data=f'setting:manage_chats:{model}'
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text=get_localization(language_code).MANAGE_CATALOG,
                            callback_data=f'setting:manage_catalog:{model}'
                        ),
                    ],
                ]
            )
    elif model == Model.DALL_E:
        buttons = [
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).SHOW_USAGE_QUOTA_IN_MESSAGES + (
                        ' ✅' if settings[model][UserSettings.SHOW_USAGE_QUOTA] else ' ❌'
                    ),
                    callback_data=f'setting:{UserSettings.SHOW_USAGE_QUOTA}:{model}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=DALLEResolution.LOW + (
                        ' ✅' if settings[model][UserSettings.RESOLUTION] == DALLEResolution.LOW else ''
                    ),
                    callback_data=f'setting:{DALLEResolution.LOW}:{model}'
                ),
                InlineKeyboardButton(
                    text=DALLEResolution.MEDIUM + (
                        ' ✅' if settings[model][UserSettings.RESOLUTION] == DALLEResolution.MEDIUM else ''
                    ),
                    callback_data=f'setting:{DALLEResolution.MEDIUM}:{model}'
                ),
                InlineKeyboardButton(
                    text=DALLEResolution.HIGH + (
                        ' ✅' if settings[model][UserSettings.RESOLUTION] == DALLEResolution.HIGH else ''
                    ),
                    callback_data=f'setting:{DALLEResolution.HIGH}:{model}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=DALLEQuality.STANDARD + (
                        ' ✅' if settings[model][UserSettings.QUALITY] == DALLEQuality.STANDARD else ''
                    ),
                    callback_data=f'setting:{DALLEQuality.STANDARD}:{model}'
                ),
                InlineKeyboardButton(
                    text=DALLEQuality.HD + (
                        ' ✅' if settings[model][UserSettings.QUALITY] == DALLEQuality.HD else ''
                    ),
                    callback_data=f'setting:{DALLEQuality.HD}:{model}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=DALLEVersion.V2 + (
                        ' ✅' if settings[model][UserSettings.VERSION] == DALLEVersion.V2 else ''),
                    callback_data=f'setting:{DALLEVersion.V2}:{model}'
                ),
                InlineKeyboardButton(
                    text=DALLEVersion.V3 + (
                        ' ✅' if settings[model][UserSettings.VERSION] == DALLEVersion.V3 else ''),
                    callback_data=f'setting:{DALLEVersion.V3}:{model}'
                ),
            ],
        ]
    elif model == Model.MIDJOURNEY:
        buttons = [
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).SHOW_USAGE_QUOTA_IN_MESSAGES + (
                        ' ✅' if settings[model][UserSettings.SHOW_USAGE_QUOTA] else ' ❌'
                    ),
                    callback_data=f'setting:{UserSettings.SHOW_USAGE_QUOTA}:{model}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=MidjourneyVersion.V5 + (
                        ' ✅' if settings[model][UserSettings.VERSION] == MidjourneyVersion.V5 else ''
                    ),
                    callback_data=f'setting:{MidjourneyVersion.V5}:{model}'
                ),
                InlineKeyboardButton(
                    text=MidjourneyVersion.V6 + (
                        ' ✅' if settings[model][UserSettings.VERSION] == MidjourneyVersion.V6 else ''
                    ),
                    callback_data=f'setting:{MidjourneyVersion.V6}:{model}'
                ),
            ],
        ]
    elif model == Model.FLUX:
        buttons = [
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).SHOW_USAGE_QUOTA_IN_MESSAGES + (
                        ' ✅' if settings[model][UserSettings.SHOW_USAGE_QUOTA] else ' ❌'
                    ),
                    callback_data=f'setting:{UserSettings.SHOW_USAGE_QUOTA}:{model}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).STRICT_SAFETY_TOLERANCE + (
                        ' ✅' if settings[model][UserSettings.SAFETY_TOLERANCE] == FluxSafetyTolerance.STRICT else ''
                    ),
                    callback_data=f'setting:{FluxSafetyTolerance.STRICT}:{model}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).MIDDLE_SAFETY_TOLERANCE + (
                        ' ✅' if settings[model][UserSettings.SAFETY_TOLERANCE] == FluxSafetyTolerance.MIDDLE else ''
                    ),
                    callback_data=f'setting:{FluxSafetyTolerance.MIDDLE}:{model}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).PERMISSIVE_SAFETY_TOLERANCE + (
                        ' ✅' if settings[model][UserSettings.SAFETY_TOLERANCE] == FluxSafetyTolerance.PERMISSIVE else ''
                    ),
                    callback_data=f'setting:{FluxSafetyTolerance.PERMISSIVE}:{model}'
                ),
            ],
        ]
    elif (
        model == Model.STABLE_DIFFUSION or
        model == Model.FACE_SWAP or
        model == Model.PHOTOSHOP_AI or
        model == Model.MUSIC_GEN
    ):
        buttons = [
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).SHOW_USAGE_QUOTA_IN_MESSAGES + (
                        ' ✅' if settings[model][UserSettings.SHOW_USAGE_QUOTA] else ' ❌'),
                    callback_data=f'setting:{UserSettings.SHOW_USAGE_QUOTA}:{model}'
                ),
            ],
        ]
    elif model == Model.SUNO:
        buttons = [
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).SHOW_USAGE_QUOTA_IN_MESSAGES + (
                        ' ✅' if settings[model][UserSettings.SHOW_USAGE_QUOTA] else ' ❌'),
                    callback_data=f'setting:{UserSettings.SHOW_USAGE_QUOTA}:{model}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).AUDIO + (
                        ' ✅' if settings[model][UserSettings.SEND_TYPE] == SunoSendType.AUDIO else ''),
                    callback_data=f'setting:{SunoSendType.AUDIO}:{model}'
                ),
                InlineKeyboardButton(
                    text=get_localization(language_code).VIDEO + (
                        ' ✅' if settings[model][UserSettings.SEND_TYPE] == SunoSendType.VIDEO else ''),
                    callback_data=f'setting:{SunoSendType.VIDEO}:{model}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=SunoVersion.V3 + (
                        ' ✅' if settings[model][UserSettings.VERSION] == SunoVersion.V3 else ''),
                    callback_data=f'setting:{SunoVersion.V3}:{model}'
                ),
                InlineKeyboardButton(
                    text=SunoVersion.V3_5 + (
                        ' ✅' if settings[model][UserSettings.VERSION] == SunoVersion.V3_5 else ''),
                    callback_data=f'setting:{SunoVersion.V3_5}:{model}'
                ),
            ],
        ]

    if show_back_button:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).BACK,
                    callback_data=f'setting:back:{model_type}'
                )
            ],
        )

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_voice_messages_settings_keyboard(
    language_code: str,
    settings: Dict,
    model: Optional[Model] = None,
) -> InlineKeyboardMarkup:
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
                callback_data=f'voice_messages_setting:back:{model}' if model else 'voice_messages_setting:back'
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
