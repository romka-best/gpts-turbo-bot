from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.database.models.common import Model, ChatGPTVersion, ClaudeGPTVersion, GeminiGPTVersion, ModelType
from bot.locales.main import get_localization
from bot.locales.types import LanguageCode


def build_mode_keyboard(language_code: LanguageCode, model: Model, model_version: str, page=0) -> InlineKeyboardMarkup:
    buttons = []
    if page == 0:
        buttons.extend(
            [
                [
                    InlineKeyboardButton(
                        text=get_localization(language_code).TEXT_MODELS,
                        callback_data=f'mode:{ModelType.TEXT}',
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text=get_localization(language_code).CHATGPT4_OMNI_MINI + (
                            ' ✅' if model == Model.CHAT_GPT and model_version == ChatGPTVersion.V4_Omni_Mini else ''
                        ),
                        callback_data=f'mode:{Model.CHAT_GPT}:{ChatGPTVersion.V4_Omni_Mini}'
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text=get_localization(language_code).CHATGPT4_OMNI + (
                            ' ✅' if model == Model.CHAT_GPT and model_version == ChatGPTVersion.V4_Omni else ''
                        ),
                        callback_data=f'mode:{Model.CHAT_GPT}:{ChatGPTVersion.V4_Omni}'
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text=get_localization(language_code).CHAT_GPT_O_1_MINI + (
                            ' ✅' if model == Model.CHAT_GPT and model_version == ChatGPTVersion.V1_O_Mini else ''
                        ),
                        callback_data=f'mode:{Model.CHAT_GPT}:{ChatGPTVersion.V1_O_Mini}'
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text=get_localization(language_code).CHAT_GPT_O_1_PREVIEW + (
                            ' ✅' if model == Model.CHAT_GPT and model_version == ChatGPTVersion.V1_O_Preview else ''
                        ),
                        callback_data=f'mode:{Model.CHAT_GPT}:{ChatGPTVersion.V1_O_Preview}'
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text=get_localization(language_code).CLAUDE_3_HAIKU + (
                            ' ✅' if model == Model.CLAUDE and model_version == ClaudeGPTVersion.V3_Haiku else ''
                        ),
                        callback_data=f'mode:{Model.CLAUDE}:{ClaudeGPTVersion.V3_Haiku}'
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text=get_localization(language_code).CLAUDE_3_SONNET + (
                            ' ✅' if model == Model.CLAUDE and model_version == ClaudeGPTVersion.V3_Sonnet else ''
                        ),
                        callback_data=f'mode:{Model.CLAUDE}:{ClaudeGPTVersion.V3_Sonnet}'
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text=get_localization(language_code).CLAUDE_3_OPUS + (
                            ' ✅' if model == Model.CLAUDE and model_version == ClaudeGPTVersion.V3_Opus else ''
                        ),
                        callback_data=f'mode:{Model.CLAUDE}:{ClaudeGPTVersion.V3_Opus}'
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text=get_localization(language_code).GEMINI_1_FLASH + (
                            ' ✅' if model == Model.GEMINI and model_version == GeminiGPTVersion.V1_Flash else ''
                        ),
                        callback_data=f'mode:{Model.GEMINI}:{GeminiGPTVersion.V1_Flash}'
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text=get_localization(language_code).GEMINI_1_PRO + (
                            ' ✅' if model == Model.GEMINI and model_version == GeminiGPTVersion.V1_Pro else ''
                        ),
                        callback_data=f'mode:{Model.GEMINI}:{GeminiGPTVersion.V1_Pro}'
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text=get_localization(language_code).GEMINI_1_ULTRA + (
                            ' ✅' if model == Model.GEMINI and model_version == GeminiGPTVersion.V1_Ultra else ''
                        ),
                        callback_data=f'mode:{Model.GEMINI}:{GeminiGPTVersion.V1_Ultra}'
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text=get_localization(language_code).EIGHTIFY + (
                            ' ✅' if model == Model.EIGHTIFY else ''
                        ),
                        callback_data=f'mode:{Model.EIGHTIFY}'
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text='⬅️',
                        callback_data='mode:back:2'
                    ),
                    InlineKeyboardButton(
                        text='1/3',
                        callback_data='mode:page:0'
                    ),
                    InlineKeyboardButton(
                        text='➡️',
                        callback_data='mode:next:1'
                    ),
                ]
            ]
        )
    elif page == 1:
        buttons.extend([
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).IMAGE_MODELS,
                    callback_data=f'mode:{ModelType.IMAGE}',
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).DALL_E + (' ✅' if model == Model.DALL_E else ''),
                    callback_data=f'mode:{Model.DALL_E}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).MIDJOURNEY + (' ✅' if model == Model.MIDJOURNEY else ''),
                    callback_data=f'mode:{Model.MIDJOURNEY}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).STABLE_DIFFUSION + (
                        ' ✅' if model == Model.STABLE_DIFFUSION else ''
                    ),
                    callback_data=f'mode:{Model.STABLE_DIFFUSION}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).FLUX + (
                        ' ✅' if model == Model.FLUX else ''
                    ),
                    callback_data=f'mode:{Model.FLUX}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).FACE_SWAP + (' ✅' if model == Model.FACE_SWAP else ''),
                    callback_data=f'mode:{Model.FACE_SWAP}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).PHOTOSHOP_AI + (' ✅' if model == Model.PHOTOSHOP_AI else ''),
                    callback_data=f'mode:{Model.PHOTOSHOP_AI}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text='⬅️',
                    callback_data='mode:back:0'
                ),
                InlineKeyboardButton(
                    text='2/3',
                    callback_data='mode:page:1'
                ),
                InlineKeyboardButton(
                    text='➡️',
                    callback_data='mode:next:2'
                ),
            ]
        ])
    elif page == 2:
        buttons.extend([
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).MUSIC_MODELS,
                    callback_data=f'mode:{ModelType.MUSIC}',
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).MUSIC_GEN + (' ✅' if model == Model.MUSIC_GEN else ''),
                    callback_data=f'mode:{Model.MUSIC_GEN}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).SUNO + (' ✅' if model == Model.SUNO else ''),
                    callback_data=f'mode:{Model.SUNO}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text='⬅️',
                    callback_data='mode:back:1'
                ),
                InlineKeyboardButton(
                    text='3/3',
                    callback_data='mode:page:2'
                ),
                InlineKeyboardButton(
                    text='➡️',
                    callback_data='mode:next:0'
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

    if model not in [Model.EIGHTIFY]:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).SWITCHED_TO_AI_INFO,
                    callback_data=f'switched_to_ai:info:{model}'
                ),
            ],
        )

    if model not in [Model.EIGHTIFY, Model.FACE_SWAP, Model.PHOTOSHOP_AI]:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).SWITCHED_TO_AI_EXAMPLES,
                    callback_data=f'switched_to_ai:examples:{model}'
                )
            ],
        )

    return InlineKeyboardMarkup(inline_keyboard=buttons)
