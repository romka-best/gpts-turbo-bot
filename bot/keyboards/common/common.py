import random

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from bot.database.models.common import Model
from bot.database.models.face_swap_package import FaceSwapPackageStatus
from bot.database.models.generation import GenerationReaction
from bot.database.models.user import UserGender
from bot.database.operations.face_swap_package.getters import get_face_swap_packages_by_gender
from bot.locales.main import get_localization


async def build_recommendations_keyboard(
    current_model: Model,
    language_code: str,
    gender: UserGender,
) -> ReplyKeyboardMarkup:
    buttons = []
    if current_model == Model.CHAT_GPT:
        recommendations = get_localization(language_code).chatgpt_recommendations()
        random.shuffle(recommendations)
        for recommendation in recommendations[:4]:
            buttons.append([
                KeyboardButton(
                    text=recommendation,
                )
            ])
    elif current_model == Model.DALL_E or current_model == Model.MIDJOURNEY:
        recommendations = get_localization(language_code).image_recommendations()
        random.shuffle(recommendations)
        for recommendation in recommendations[:4]:
            buttons.append([
                KeyboardButton(
                    text=recommendation,
                )
            ])
    elif current_model == Model.FACE_SWAP:
        face_swap_packages = await get_face_swap_packages_by_gender(
            gender,
            status=FaceSwapPackageStatus.PUBLIC,
        )
        for face_swap_package in face_swap_packages:
            buttons.append(
                [
                    KeyboardButton(
                        text=face_swap_package.translated_names.get(language_code, face_swap_package.name),
                    )
                ],
            )
    elif current_model == Model.MUSIC_GEN or current_model == Model.SUNO:
        recommendations = get_localization(language_code).music_recommendations()
        random.shuffle(recommendations)
        for recommendation in recommendations[:4]:
            buttons.append([
                KeyboardButton(
                    text=recommendation,
                )
            ])

    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def build_reaction_keyboard(generation_id: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text="👍",
                callback_data=f'reaction:{GenerationReaction.LIKED}:{generation_id}'
            ),
            InlineKeyboardButton(
                text="👎",
                callback_data=f'reaction:{GenerationReaction.DISLIKED}:{generation_id}'
            ),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


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
