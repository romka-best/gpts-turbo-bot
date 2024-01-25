from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.database.models.common import Currency
from bot.database.models.transaction import TransactionType, ServiceType
from bot.locales.main import get_localization


def build_statistics_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text="За день 📅",
                callback_data=f'statistics:day'
            )
        ],
        [
            InlineKeyboardButton(
                text="За неделю 📆",
                callback_data=f'statistics:week'
            )
        ],
        [
            InlineKeyboardButton(
                text="За месяц 🗓️",
                callback_data=f'statistics:month'
            )
        ],
        [
            InlineKeyboardButton(
                text="За всё время ⏳",
                callback_data=f'statistics:all'
            )
        ],
        [
            InlineKeyboardButton(
                text="Записать транзакцию ➕➖",
                callback_data=f'statistics:write_transaction'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CLOSE,
                callback_data='statistics:close'
            )
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_statistics_write_transaction_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text="Записать доход 📈",
                callback_data=f'statistics_write_transaction:{TransactionType.INCOME}'
            )
        ],
        [
            InlineKeyboardButton(
                text="Записать расход 📉",
                callback_data=f'statistics_write_transaction:{TransactionType.EXPENSE}'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).BACK,
                callback_data='statistics_write_transaction:back'
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_statistics_choose_service_keyboard(language_code: str,
                                             transaction_type: TransactionType) -> InlineKeyboardMarkup:
    buttons = []
    if transaction_type == TransactionType.INCOME:
        buttons = [
            [
                InlineKeyboardButton(
                    text="STANDARD ⭐️",
                    callback_data=f'statistics_choose_service:{ServiceType.STANDARD}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="VIP 🔥",
                    callback_data=f'statistics_choose_service:{ServiceType.VIP}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="PLATINUM 💎",
                    callback_data=f'statistics_choose_service:{ServiceType.PLATINUM}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="ChatGPT 3.5 ✉️",
                    callback_data=f'statistics_choose_service:{ServiceType.GPT3}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="ChatGPT 4.0 🧠",
                    callback_data=f'statistics_choose_service:{ServiceType.GPT4}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="DALLE-3 🖼",
                    callback_data=f'statistics_choose_service:{ServiceType.DALLE3}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="FaceSwap 📷",
                    callback_data=f'statistics_choose_service:{ServiceType.FACE_SWAP}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="Additional chats 💬",
                    callback_data=f'statistics_choose_service:{ServiceType.ADDITIONAL_CHATS}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="Fast messages ⚡",
                    callback_data=f'statistics_choose_service:{ServiceType.FAST_MESSAGES}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="Voice messages 🎙",
                    callback_data=f'statistics_choose_service:{ServiceType.VOICE_MESSAGES}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="Access to catalog 🎭",
                    callback_data=f'statistics_choose_service:{ServiceType.ACCESS_TO_CATALOG}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="Other 🤷",
                    callback_data=f'statistics_choose_service:{ServiceType.OTHER}'
                )
            ],
        ]
    elif transaction_type == TransactionType.EXPENSE:
        buttons = [
            [
                InlineKeyboardButton(
                    text="ChatGPT 3.5 ✉️",
                    callback_data=f'statistics_choose_service:{ServiceType.GPT3}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="ChatGPT 4.0 🧠",
                    callback_data=f'statistics_choose_service:{ServiceType.GPT4}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="DALLE-3 🖼",
                    callback_data=f'statistics_choose_service:{ServiceType.DALLE3}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="FaceSwap 📷",
                    callback_data=f'statistics_choose_service:{ServiceType.FACE_SWAP}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="Additional chats 💬",
                    callback_data=f'statistics_choose_service:{ServiceType.ADDITIONAL_CHATS}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="Fast messages ⚡",
                    callback_data=f'statistics_choose_service:{ServiceType.FAST_MESSAGES}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="Voice messages 🎙",
                    callback_data=f'statistics_choose_service:{ServiceType.VOICE_MESSAGES}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="Access to catalog 🎭",
                    callback_data=f'statistics_choose_service:{ServiceType.ACCESS_TO_CATALOG}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="Server 💻",
                    callback_data=f'statistics_choose_service:{ServiceType.SERVER}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="Database 🗄",
                    callback_data=f'statistics_choose_service:{ServiceType.DATABASE}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="Other 🤷",
                    callback_data=f'statistics_choose_service:{ServiceType.OTHER}'
                )
            ],
        ]
    buttons.append([
        InlineKeyboardButton(
            text=get_localization(language_code).CANCEL,
            callback_data='statistics_choose_service:cancel'
        )
    ], )

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_statistics_choose_currency_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text="Рубли ₽",
                callback_data=f'statistics_choose_currency:{Currency.RUB}'
            )
        ],
        [
            InlineKeyboardButton(
                text="Доллары $",
                callback_data=f'statistics_choose_currency:{Currency.USD}'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CANCEL,
                callback_data='statistics_choose_currency:cancel'
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
