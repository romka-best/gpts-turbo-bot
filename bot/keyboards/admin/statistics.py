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
                text=get_localization(language_code).BACK,
                callback_data='statistics:back'
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


def build_statistics_choose_service_keyboard(
    language_code: str,
    transaction_type: TransactionType,
) -> InlineKeyboardMarkup:
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
                    text="PREMIUM 💎",
                    callback_data=f'statistics_choose_service:{ServiceType.PREMIUM}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="ChatGPT 3.5 Turbo ✉️",
                    callback_data=f'statistics_choose_service:{ServiceType.CHAT_GPT3_TURBO}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="ChatGPT 4.0 Turbo 🧠",
                    callback_data=f'statistics_choose_service:{ServiceType.CHAT_GPT4_TURBO}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="ChatGPT 4.0 Omni 💥",
                    callback_data=f'statistics_choose_service:{ServiceType.CHAT_GPT4_OMNI}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="Claude 3.5 Sonnet 💫",
                    callback_data=f'statistics_choose_service:{ServiceType.CLAUDE_3_SONNET}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="Claude 3 Opus 🚀",
                    callback_data=f'statistics_choose_service:{ServiceType.CLAUDE_3_OPUS}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="DALL-E 🖼",
                    callback_data=f'statistics_choose_service:{ServiceType.DALL_E}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="Midjourney 🎨",
                    callback_data=f'statistics_choose_service:{ServiceType.MIDJOURNEY}'
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
                    text="MusicGen 🎵",
                    callback_data=f'statistics_choose_service:{ServiceType.MUSIC_GEN}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="Suno 🎸",
                    callback_data=f'statistics_choose_service:{ServiceType.SUNO}'
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
                    text="ChatGPT 3.5 Turbo ✉️",
                    callback_data=f'statistics_choose_service:{ServiceType.CHAT_GPT3_TURBO}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="ChatGPT 4.0 Turbo 🧠",
                    callback_data=f'statistics_choose_service:{ServiceType.CHAT_GPT4_TURBO}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="ChatGPT 4.0 Omni 💥",
                    callback_data=f'statistics_choose_service:{ServiceType.CHAT_GPT4_OMNI}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="Claude 3.5 Sonnet 💫",
                    callback_data=f'statistics_choose_service:{ServiceType.CLAUDE_3_SONNET}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="Claude 3 Opus 🚀",
                    callback_data=f'statistics_choose_service:{ServiceType.CLAUDE_3_OPUS}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="DALL-E 🖼",
                    callback_data=f'statistics_choose_service:{ServiceType.DALL_E}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="Midjourney 🎨",
                    callback_data=f'statistics_choose_service:{ServiceType.MIDJOURNEY}'
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
                    text="MusicGen 🎵",
                    callback_data=f'statistics_choose_service:{ServiceType.MUSIC_GEN}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="Suno 🎸",
                    callback_data=f'statistics_choose_service:{ServiceType.SUNO}'
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
                text="Telegram Stars ⭐",
                callback_data=f'statistics_choose_currency:{Currency.XTR}'
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
