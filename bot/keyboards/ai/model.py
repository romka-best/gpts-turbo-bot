from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.database.models.common import Model, ModelType, ChatGPTVersion, ClaudeGPTVersion, GeminiGPTVersion
from bot.locales.main import get_localization
from bot.locales.types import LanguageCode


def build_model_keyboard(
    language_code: LanguageCode,
    model: Model,
    model_version: ChatGPTVersion | ClaudeGPTVersion | GeminiGPTVersion,
    page=0,
    chosen_model=None,
) -> InlineKeyboardMarkup:
    buttons = []
    if page == 0:
        buttons.extend(
            [
                [
                    InlineKeyboardButton(
                        text=get_localization(language_code).TEXT_MODELS,
                        callback_data=f'model:{ModelType.TEXT}',
                    ),
                ],
            ]
        )
        if chosen_model == Model.CHAT_GPT:
            buttons.extend(
                [
                    [
                        InlineKeyboardButton(
                            text=get_localization(language_code).CHATGPT4_OMNI_MINI + (
                                ' ✅' if model == Model.CHAT_GPT and model_version == ChatGPTVersion.V4_Omni_Mini else ''
                            ),
                            callback_data=f'model:{Model.CHAT_GPT}:{ChatGPTVersion.V4_Omni_Mini}'
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text=get_localization(language_code).CHATGPT4_OMNI + (
                                ' ✅' if model == Model.CHAT_GPT and model_version == ChatGPTVersion.V4_Omni else ''
                            ),
                            callback_data=f'model:{Model.CHAT_GPT}:{ChatGPTVersion.V4_Omni}'
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text=get_localization(language_code).CHAT_GPT_O_1_MINI + (
                                ' ✅' if model == Model.CHAT_GPT and model_version == ChatGPTVersion.V1_O_Mini else ''
                            ),
                            callback_data=f'model:{Model.CHAT_GPT}:{ChatGPTVersion.V1_O_Mini}'
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text=get_localization(language_code).CHAT_GPT_O_1 + (
                                ' ✅' if model == Model.CHAT_GPT and model_version == ChatGPTVersion.V1_O else ''
                            ),
                            callback_data=f'model:{Model.CHAT_GPT}:{ChatGPTVersion.V1_O}'
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text=get_localization(language_code).BACK,
                            callback_data=f'model:{Model.CHAT_GPT}:back'
                        ),
                    ],
                ]
            )
        elif chosen_model == Model.CLAUDE:
            buttons.extend(
                [
                    [
                        InlineKeyboardButton(
                            text=get_localization(language_code).CLAUDE_3_HAIKU + (
                                ' ✅' if model == Model.CLAUDE and model_version == ClaudeGPTVersion.V3_Haiku else ''
                            ),
                            callback_data=f'model:{Model.CLAUDE}:{ClaudeGPTVersion.V3_Haiku}'
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text=get_localization(language_code).CLAUDE_3_SONNET + (
                                ' ✅' if model == Model.CLAUDE and model_version == ClaudeGPTVersion.V3_Sonnet else ''
                            ),
                            callback_data=f'model:{Model.CLAUDE}:{ClaudeGPTVersion.V3_Sonnet}'
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text=get_localization(language_code).CLAUDE_3_OPUS + (
                                ' ✅' if model == Model.CLAUDE and model_version == ClaudeGPTVersion.V3_Opus else ''
                            ),
                            callback_data=f'model:{Model.CLAUDE}:{ClaudeGPTVersion.V3_Opus}'
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text=get_localization(language_code).BACK,
                            callback_data=f'model:{Model.CLAUDE}:back'
                        ),
                    ],
                ]
            )
        elif chosen_model == Model.GEMINI:
            buttons.extend(
                [
                    [
                        InlineKeyboardButton(
                            text=get_localization(language_code).GEMINI_2_FLASH + (
                                ' ✅' if model == Model.GEMINI and model_version == GeminiGPTVersion.V2_Flash else ''
                            ),
                            callback_data=f'model:{Model.GEMINI}:{GeminiGPTVersion.V2_Flash}'
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text=get_localization(language_code).GEMINI_1_PRO + (
                                ' ✅' if model == Model.GEMINI and model_version == GeminiGPTVersion.V1_Pro else ''
                            ),
                            callback_data=f'model:{Model.GEMINI}:{GeminiGPTVersion.V1_Pro}'
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text=get_localization(language_code).GEMINI_1_ULTRA + (
                                ' ✅' if model == Model.GEMINI and model_version == GeminiGPTVersion.V1_Ultra else ''
                            ),
                            callback_data=f'model:{Model.GEMINI}:{GeminiGPTVersion.V1_Ultra}'
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text=get_localization(language_code).BACK,
                            callback_data=f'model:{Model.GEMINI}:back'
                        ),
                    ],
                ]
            )
        else:
            buttons.extend(
                [
                    [
                        InlineKeyboardButton(
                            text=get_localization(language_code).CHATGPT,
                            callback_data=f'model:{Model.CHAT_GPT}',
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text=get_localization(language_code).CLAUDE,
                            callback_data=f'model:{Model.CLAUDE}',
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text=get_localization(language_code).GEMINI,
                            callback_data=f'model:{Model.GEMINI}',
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text=get_localization(language_code).GROK + (
                                ' ✅' if model == Model.GROK else ''
                            ),
                            callback_data=f'model:{Model.GROK}'
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text=get_localization(language_code).PERPLEXITY + (
                                ' ✅' if model == Model.PERPLEXITY else ''
                            ),
                            callback_data=f'model:{Model.PERPLEXITY}'
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text='⬅️',
                            callback_data='model:back:4'
                        ),
                        InlineKeyboardButton(
                            text='1/5',
                            callback_data='model:page:0'
                        ),
                        InlineKeyboardButton(
                            text='➡️',
                            callback_data='model:next:1'
                        ),
                    ]
                ]
            )
    elif page == 1:
        buttons.extend([
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).SUMMARY_MODELS,
                    callback_data=f'model:{ModelType.SUMMARY}',
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).EIGHTIFY + (
                        ' ✅' if model == Model.EIGHTIFY else ''
                    ),
                    callback_data=f'model:{Model.EIGHTIFY}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).GEMINI_VIDEO + (
                        ' ✅' if model == Model.GEMINI_VIDEO else ''
                    ),
                    callback_data=f'model:{Model.GEMINI_VIDEO}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text='⬅️',
                    callback_data='model:back:0'
                ),
                InlineKeyboardButton(
                    text='2/5',
                    callback_data='model:page:1'
                ),
                InlineKeyboardButton(
                    text='➡️',
                    callback_data='model:next:2'
                ),
            ]
        ])
    elif page == 2:
        buttons.extend([
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).IMAGE_MODELS,
                    callback_data=f'model:{ModelType.IMAGE}',
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).DALL_E + (' ✅' if model == Model.DALL_E else ''),
                    callback_data=f'model:{Model.DALL_E}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).MIDJOURNEY + (' ✅' if model == Model.MIDJOURNEY else ''),
                    callback_data=f'model:{Model.MIDJOURNEY}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).STABLE_DIFFUSION + (
                        ' ✅' if model == Model.STABLE_DIFFUSION else ''
                    ),
                    callback_data=f'model:{Model.STABLE_DIFFUSION}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).FLUX + (
                        ' ✅' if model == Model.FLUX else ''
                    ),
                    callback_data=f'model:{Model.FLUX}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).LUMA_PHOTON + (
                        ' ✅' if model == Model.LUMA_PHOTON else ''
                    ),
                    callback_data=f'model:{Model.LUMA_PHOTON}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).FACE_SWAP + (
                        ' ✅' if model == Model.FACE_SWAP else ''
                    ),
                    callback_data=f'model:{Model.FACE_SWAP}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).PHOTOSHOP_AI + (
                        ' ✅' if model == Model.PHOTOSHOP_AI else ''
                    ),
                    callback_data=f'model:{Model.PHOTOSHOP_AI}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text='⬅️',
                    callback_data='model:back:1'
                ),
                InlineKeyboardButton(
                    text='3/5',
                    callback_data='model:page:2'
                ),
                InlineKeyboardButton(
                    text='➡️',
                    callback_data='model:next:3'
                ),
            ]
        ])
    elif page == 3:
        buttons.extend([
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).MUSIC_MODELS,
                    callback_data=f'model:{ModelType.MUSIC}',
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).MUSIC_GEN + (' ✅' if model == Model.MUSIC_GEN else ''),
                    callback_data=f'model:{Model.MUSIC_GEN}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).SUNO + (' ✅' if model == Model.SUNO else ''),
                    callback_data=f'model:{Model.SUNO}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text='⬅️',
                    callback_data='model:back:2'
                ),
                InlineKeyboardButton(
                    text='4/5',
                    callback_data='model:page:3'
                ),
                InlineKeyboardButton(
                    text='➡️',
                    callback_data='model:next:4'
                ),
            ]
        ])
    elif page == 4:
        buttons.extend([
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).VIDEO_MODELS,
                    callback_data=f'model:{ModelType.VIDEO}',
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).KLING + (
                        ' ✅' if model == Model.KLING else ''
                    ),
                    callback_data=f'model:{Model.KLING}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).RUNWAY + (
                        ' ✅' if model == Model.RUNWAY else ''
                    ),
                    callback_data=f'model:{Model.RUNWAY}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).LUMA_RAY + (
                        ' ✅' if model == Model.LUMA_RAY else ''
                    ),
                    callback_data=f'model:{Model.LUMA_RAY}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text='⬅️',
                    callback_data='model:back:3'
                ),
                InlineKeyboardButton(
                    text='5/5',
                    callback_data='model:page:4'
                ),
                InlineKeyboardButton(
                    text='➡️',
                    callback_data='model:next:0'
                ),
            ]
        ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_switched_to_ai_keyboard(language_code: LanguageCode, model: Model) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).SWITCHED_TO_AI_SETTINGS,
                callback_data=f'switched_to_ai:settings:{model}'
            ),
        ],
    ]

    if model not in [Model.EIGHTIFY, Model.GEMINI_VIDEO]:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).SWITCHED_TO_AI_INFO,
                    callback_data=f'switched_to_ai:info:{model}'
                ),
            ],
        )

    if model not in [
        Model.EIGHTIFY,
        Model.GEMINI_VIDEO,
        Model.FACE_SWAP,
        Model.PHOTOSHOP_AI,
        Model.RUNWAY,
        Model.LUMA_RAY,
    ]:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).SWITCHED_TO_AI_EXAMPLES,
                    callback_data=f'switched_to_ai:examples:{model}'
                )
            ],
        )

    return InlineKeyboardMarkup(inline_keyboard=buttons)
