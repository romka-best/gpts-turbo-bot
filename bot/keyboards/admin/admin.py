from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.locales.main import get_localization


def build_admin_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text="😇 Создать промокод",
                callback_data='admin:create_promo_code',
            ),
        ],
        [
            InlineKeyboardButton(
                text="📸 Управление контентом в FaceSwap",
                callback_data='admin:manage_face_swap',
            ),
        ],
        [
            InlineKeyboardButton(
                text="🎩 Управление ролями в чатах",
                callback_data='admin:manage_catalog',
            ),
        ],
        [
            InlineKeyboardButton(
                text="📊 Статистика",
                callback_data='admin:statistics',
            ),
        ],
        [
            InlineKeyboardButton(
                text="📣 Сделать рассылку",
                callback_data='admin:blast',
            ),
        ],
        [
            InlineKeyboardButton(
                text="⛔️ Бан/Разбан пользователя",
                callback_data='admin:ban',
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CLOSE,
                callback_data='admin:close'
            ),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
