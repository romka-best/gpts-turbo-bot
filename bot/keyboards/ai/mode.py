from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.database.models.common import Model, ChatGPTVersion, ClaudeGPTVersion
from bot.locales.main import get_localization


def build_mode_keyboard(language_code: str, model: Model, model_version: str, page=0) -> InlineKeyboardMarkup:
    buttons = []
    if page == 0:
        buttons.extend(
            [
                [
                    InlineKeyboardButton(
                        text=get_localization(language_code).TEXT_MODELS,
                        callback_data='mode:text',
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text=get_localization(language_code).CHATGPT3_TURBO + (
                            " ✅" if model == Model.CHAT_GPT and model_version == ChatGPTVersion.V3_Turbo else ""
                        ),
                        callback_data=f'mode:{Model.CHAT_GPT}:{ChatGPTVersion.V3_Turbo}'
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text=get_localization(language_code).CHATGPT4_TURBO + (
                            " ✅" if model == Model.CHAT_GPT and model_version == ChatGPTVersion.V4_Turbo else ""
                        ),
                        callback_data=f'mode:{Model.CHAT_GPT}:{ChatGPTVersion.V4_Turbo}'
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text=get_localization(language_code).CHATGPT4_OMNI + (
                            " ✅" if model == Model.CHAT_GPT and model_version == ChatGPTVersion.V4_Omni else ""
                        ),
                        callback_data=f'mode:{Model.CHAT_GPT}:{ChatGPTVersion.V4_Omni}'
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text=get_localization(language_code).CLAUDE_3_SONNET + (
                            " ✅" if model == Model.CLAUDE and model_version == ClaudeGPTVersion.V3_Sonnet else ""
                        ),
                        callback_data=f'mode:{Model.CLAUDE}:{ClaudeGPTVersion.V3_Sonnet}'
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text=get_localization(language_code).CLAUDE_3_OPUS + (
                            " ✅" if model == Model.CLAUDE and model_version == ClaudeGPTVersion.V3_Opus else ""),
                        callback_data=f'mode:{Model.CLAUDE}:{ClaudeGPTVersion.V3_Opus}'
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="⬅️",
                        callback_data="mode:back:2"
                    ),
                    InlineKeyboardButton(
                        text="1/3",
                        callback_data="mode:page:0"
                    ),
                    InlineKeyboardButton(
                        text="➡️",
                        callback_data="mode:next:1"
                    ),
                ]
            ]
        )
    elif page == 1:
        buttons.extend([
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).IMAGE_MODELS,
                    callback_data='mode:text',
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).DALL_E + (" ✅" if model == Model.DALL_E else ""),
                    callback_data=f'mode:{Model.DALL_E}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).MIDJOURNEY + (" ✅" if model == Model.MIDJOURNEY else ""),
                    callback_data=f'mode:{Model.MIDJOURNEY}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).FACE_SWAP + (" ✅" if model == Model.FACE_SWAP else ""),
                    callback_data=f'mode:{Model.FACE_SWAP}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text="⬅️",
                    callback_data="mode:back:0"
                ),
                InlineKeyboardButton(
                    text="2/3",
                    callback_data="mode:page:1"
                ),
                InlineKeyboardButton(
                    text="➡️",
                    callback_data="mode:next:2"
                ),
            ]
        ])
    elif page == 2:
        buttons.extend([
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).MUSIC_MODELS,
                    callback_data='mode:text',
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).MUSIC_GEN + (" ✅" if model == Model.MUSIC_GEN else ""),
                    callback_data=f'mode:{Model.MUSIC_GEN}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).SUNO + (" ✅" if model == Model.SUNO else ""),
                    callback_data=f'mode:{Model.SUNO}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text="⬅️",
                    callback_data="mode:back:1"
                ),
                InlineKeyboardButton(
                    text="3/3",
                    callback_data="mode:page:2"
                ),
                InlineKeyboardButton(
                    text="➡️",
                    callback_data="mode:next:0"
                ),
            ]
        ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)
