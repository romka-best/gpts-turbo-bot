from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.database.models.common import Model, ChatGPTVersion, ClaudeGPTVersion
from bot.locales.main import get_localization


def build_info_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).TEXT_MODELS,
                callback_data=f'info:text'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).IMAGE_MODELS,
                callback_data=f'info:image'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).MUSIC_MODELS,
                callback_data=f'info:music'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CLOSE,
                callback_data='info:close'
            ),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_info_text_models_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CHATGPT,
                callback_data=f'info_text_models:{Model.CHAT_GPT}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CLAUDE,
                callback_data=f'info_text_models:{Model.CLAUDE}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).BACK,
                callback_data='info_text_models:back'
            ),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_info_image_models_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).DALL_E,
                callback_data=f'info_image_models:{Model.DALL_E}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).MIDJOURNEY,
                callback_data=f'info_image_models:{Model.MIDJOURNEY}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).FACE_SWAP,
                callback_data=f'info_image_models:{Model.FACE_SWAP}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).BACK,
                callback_data='info_text_models:back'
            ),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_info_music_models_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).MUSIC_GEN,
                callback_data=f'info_music_models:{Model.MUSIC_GEN}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).SUNO,
                callback_data=f'info_music_models:{Model.SUNO}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).BACK,
                callback_data='info_text_models:back'
            ),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_info_chosen_model_keyboard(language_code: str, model_type: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).BACK,
                callback_data=f'info_chosen_model:back:{model_type}'
            ),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
