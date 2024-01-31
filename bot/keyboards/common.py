import random

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from bot.database.models.common import Model
from bot.database.models.face_swap_package import FaceSwapPackageStatus
from bot.database.models.user import User
from bot.database.operations.face_swap_package import get_face_swap_packages_by_gender
from bot.locales.main import get_localization


async def build_recommendations_keyboard(user: User) -> ReplyKeyboardMarkup:
    buttons = []
    if user.current_model == Model.GPT3 or user.current_model == Model.GPT4:
        recommendations = get_localization(user.language_code).chatgpt_recommendations()
        random.shuffle(recommendations)
        for recommendation in recommendations[:4]:
            buttons.append([
                KeyboardButton(
                    text=recommendation,
                )
            ])
    elif user.current_model == Model.DALLE3:
        recommendations = get_localization(user.language_code).dalle_recommendations()
        random.shuffle(recommendations)
        for recommendation in recommendations[:4]:
            buttons.append([
                KeyboardButton(
                    text=recommendation,
                )
            ])
    elif user.current_model == Model.FACE_SWAP:
        face_swap_packages = await get_face_swap_packages_by_gender(user.gender,
                                                                    status=FaceSwapPackageStatus.PUBLIC)
        for face_swap_package in face_swap_packages:
            buttons.append(
                [
                    KeyboardButton(
                        text=face_swap_package.translated_names.get(user.language_code, face_swap_package.name),
                    )
                ],
            )

    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def build_cancel_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CANCEL,
                callback_data='common:cancel'
            )
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
