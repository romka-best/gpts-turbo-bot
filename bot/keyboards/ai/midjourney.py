from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def build_midjourney_keyboard(hash_id: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text="U1",
                callback_data=f'midjourney:u1:{hash_id}'
            ),
            InlineKeyboardButton(
                text="U2",
                callback_data=f'midjourney:u2:{hash_id}'
            ),
            InlineKeyboardButton(
                text="U3",
                callback_data=f'midjourney:u3:{hash_id}'
            ),
            InlineKeyboardButton(
                text="U4",
                callback_data=f'midjourney:u4:{hash_id}'
            ),
        ],
        [
            InlineKeyboardButton(
                text="V1",
                callback_data=f'midjourney:v1:{hash_id}'
            ),
            InlineKeyboardButton(
                text="V2",
                callback_data=f'midjourney:v2:{hash_id}'
            ),
            InlineKeyboardButton(
                text="V3",
                callback_data=f'midjourney:v3:{hash_id}'
            ),
            InlineKeyboardButton(
                text="V4",
                callback_data=f'midjourney:v4:{hash_id}'
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔄",
                callback_data=f'midjourney:again:{hash_id}'
            ),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)

