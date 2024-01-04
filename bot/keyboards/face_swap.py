from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.database.models.face_swap_package import FaceSwapPackage
from bot.locales.main import get_localization


def build_face_swap_choose_keyboard(language_code: str, packages: List[FaceSwapPackage]) -> InlineKeyboardMarkup:
    buttons = []
    for package in packages:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=package.translated_names.get(language_code, package.name),
                    callback_data=f'face_swap_choose:{package.name}'
                )
            ],
        )

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_face_swap_package_keyboard(language_code: str, quantities: List[int]) -> InlineKeyboardMarkup:
    buttons = []
    for quantity in quantities:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=f'🔹 {quantity}',
                    callback_data=f'face_swap_package:{quantity}'
                )
            ]
        )

    buttons.extend([
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
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)
