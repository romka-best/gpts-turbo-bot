from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.database.models.face_swap_package import FaceSwapPackageName
from bot.locales.main import get_localization


def build_face_swap_choose_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CELEBRITIES,
                callback_data=f'face_swap_choose:{FaceSwapPackageName.CELEBRITIES["name"]}'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).MOVIE_CHARACTERS,
                callback_data=f'face_swap_choose:{FaceSwapPackageName.MOVIE_CHARACTERS["name"]}'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).PROFESSIONS,
                callback_data=f'face_swap_choose:{FaceSwapPackageName.PROFESSIONS["name"]}'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).SEVEN_WONDERS_OF_THE_ANCIENT_WORLD,
                callback_data=f'face_swap_choose:{FaceSwapPackageName.SEVEN_WONDERS_OF_THE_ANCIENT_WORLD["name"]}'
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_face_swap_package_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).BACK,
                callback_data='face_swap_package:back'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CANCEL,
                callback_data='face_swap_package:cancel'
            )
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
