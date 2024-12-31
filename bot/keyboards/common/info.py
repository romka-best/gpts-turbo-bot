from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.database.models.common import Model, ModelType
from bot.locales.main import get_localization
from bot.locales.types import LanguageCode


def build_info_keyboard(language_code: LanguageCode) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).MODELS_TEXT,
                callback_data=f'info:{ModelType.TEXT}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).MODELS_IMAGE,
                callback_data=f'info:{ModelType.IMAGE}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).MODELS_MUSIC,
                callback_data=f'info:{ModelType.MUSIC}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).MODELS_VIDEO,
                callback_data=f'info:{ModelType.VIDEO}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).ACTION_CLOSE,
                callback_data='info:close'
            ),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_info_text_models_keyboard(language_code: LanguageCode) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CHAT_GPT,
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
                text=get_localization(language_code).GEMINI,
                callback_data=f'info_text_models:{Model.GEMINI}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).GROK,
                callback_data=f'info_text_models:{Model.GROK}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).PERPLEXITY,
                callback_data=f'info_text_models:{Model.PERPLEXITY}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).ACTION_BACK,
                callback_data='info_text_models:back'
            ),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_info_image_models_keyboard(language_code: LanguageCode) -> InlineKeyboardMarkup:
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
                text=get_localization(language_code).STABLE_DIFFUSION,
                callback_data=f'info_image_models:{Model.STABLE_DIFFUSION}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).FLUX,
                callback_data=f'info_image_models:{Model.FLUX}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).LUMA_PHOTON,
                callback_data=f'info_image_models:{Model.LUMA_PHOTON}'
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
                text=get_localization(language_code).PHOTOSHOP_AI,
                callback_data=f'info_image_models:{Model.PHOTOSHOP_AI}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).ACTION_BACK,
                callback_data='info_image_models:back'
            ),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_info_music_models_keyboard(language_code: LanguageCode) -> InlineKeyboardMarkup:
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
                text=get_localization(language_code).ACTION_BACK,
                callback_data='info_music_models:back'
            ),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_info_video_models_keyboard(language_code: LanguageCode) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).KLING,
                callback_data=f'info_video_models:{Model.KLING}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).RUNWAY,
                callback_data=f'info_video_models:{Model.RUNWAY}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).LUMA_RAY,
                callback_data=f'info_video_models:{Model.LUMA_RAY}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).ACTION_BACK,
                callback_data='info_video_models:back'
            ),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_info_chosen_model_type_keyboard(language_code: LanguageCode, model_type: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).ACTION_BACK,
                callback_data=f'info_chosen_model_type:back:{model_type}'
            ),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
