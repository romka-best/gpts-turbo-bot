from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.database.models.common import Currency
from bot.database.models.subscription import Subscription, SubscriptionType
from bot.database.models.transaction import TransactionType, ServiceType
from bot.locales.main import get_localization


def build_statistics_keyboard(language_code: str, is_admin: bool) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text='За день 📅',
                callback_data=f'statistics:day'
            )
        ],
        [
            InlineKeyboardButton(
                text='За неделю 📆',
                callback_data=f'statistics:week'
            )
        ],
        [
            InlineKeyboardButton(
                text='За месяц 🗓️',
                callback_data=f'statistics:month'
            )
        ],
        [
            InlineKeyboardButton(
                text='За всё время ⏳',
                callback_data=f'statistics:all'
            )
        ],
    ]

    if is_admin:
        buttons.append([
            InlineKeyboardButton(
                text='Записать транзакцию ➕➖',
                callback_data=f'statistics:write_transaction'
            )
        ])

    buttons.append([
        InlineKeyboardButton(
            text=get_localization(language_code).BACK,
            callback_data='statistics:back'
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_statistics_write_transaction_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text='Записать доход 📈',
                callback_data=f'statistics_write_transaction:{TransactionType.INCOME}'
            )
        ],
        [
            InlineKeyboardButton(
                text='Записать расход 📉',
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
        emojis = Subscription.get_emojis()
        buttons = [
            [
                InlineKeyboardButton(
                    text=f'{SubscriptionType.MINI} {emojis[SubscriptionType.MINI]}',
                    callback_data=f'statistics_choose_service:{ServiceType.MINI}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=f'{SubscriptionType.STANDARD} {emojis[SubscriptionType.STANDARD]}',
                    callback_data=f'statistics_choose_service:{ServiceType.STANDARD}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=f'{SubscriptionType.VIP} {emojis[SubscriptionType.VIP]}',
                    callback_data=f'statistics_choose_service:{ServiceType.VIP}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=f'{SubscriptionType.PREMIUM} {emojis[SubscriptionType.PREMIUM]}',
                    callback_data=f'statistics_choose_service:{ServiceType.PREMIUM}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=f'{SubscriptionType.UNLIMITED} {emojis[SubscriptionType.UNLIMITED]}',
                    callback_data=f'statistics_choose_service:{ServiceType.UNLIMITED}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).CHATGPT3_TURBO,
                    callback_data=f'statistics_choose_service:{ServiceType.CHAT_GPT3_TURBO}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).CHATGPT4_TURBO,
                    callback_data=f'statistics_choose_service:{ServiceType.CHAT_GPT4_TURBO}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).CHATGPT4_OMNI_MINI,
                    callback_data=f'statistics_choose_service:{ServiceType.CHAT_GPT4_OMNI_MINI}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).CHATGPT4_OMNI,
                    callback_data=f'statistics_choose_service:{ServiceType.CHAT_GPT4_OMNI}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).CHAT_GPT_O_1_MINI,
                    callback_data=f'statistics_choose_service:{ServiceType.CHAT_GPT_O_1_MINI}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).CHAT_GPT_O_1_PREVIEW,
                    callback_data=f'statistics_choose_service:{ServiceType.CHAT_GPT_O_1_PREVIEW}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).CLAUDE_3_HAIKU,
                    callback_data=f'statistics_choose_service:{ServiceType.CLAUDE_3_HAIKU}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).CLAUDE_3_SONNET,
                    callback_data=f'statistics_choose_service:{ServiceType.CLAUDE_3_SONNET}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).CLAUDE_3_OPUS,
                    callback_data=f'statistics_choose_service:{ServiceType.CLAUDE_3_OPUS}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).GEMINI_1_FLASH,
                    callback_data=f'statistics_choose_service:{ServiceType.GEMINI_1_FLASH}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).GEMINI_1_PRO,
                    callback_data=f'statistics_choose_service:{ServiceType.GEMINI_1_PRO}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).GEMINI_1_ULTRA,
                    callback_data=f'statistics_choose_service:{ServiceType.GEMINI_1_ULTRA}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).DALL_E,
                    callback_data=f'statistics_choose_service:{ServiceType.DALL_E}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).MIDJOURNEY,
                    callback_data=f'statistics_choose_service:{ServiceType.MIDJOURNEY}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).STABLE_DIFFUSION,
                    callback_data=f'statistics_choose_service:{ServiceType.STABLE_DIFFUSION}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).FLUX,
                    callback_data=f'statistics_choose_service:{ServiceType.FLUX}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).FACE_SWAP,
                    callback_data=f'statistics_choose_service:{ServiceType.FACE_SWAP}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).PHOTOSHOP_AI,
                    callback_data=f'statistics_choose_service:{ServiceType.PHOTOSHOP_AI}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).MUSIC_GEN,
                    callback_data=f'statistics_choose_service:{ServiceType.MUSIC_GEN}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).SUNO,
                    callback_data=f'statistics_choose_service:{ServiceType.SUNO}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).THEMATIC_CHATS,
                    callback_data=f'statistics_choose_service:{ServiceType.ADDITIONAL_CHATS}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).FAST_ANSWERS,
                    callback_data=f'statistics_choose_service:{ServiceType.FAST_MESSAGES}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).VOICE_MESSAGES,
                    callback_data=f'statistics_choose_service:{ServiceType.VOICE_MESSAGES}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).ACCESS_TO_CATALOG,
                    callback_data=f'statistics_choose_service:{ServiceType.ACCESS_TO_CATALOG}'
                )
            ],
            [
                InlineKeyboardButton(
                    text='Other 🤷',
                    callback_data=f'statistics_choose_service:{ServiceType.OTHER}'
                )
            ],
        ]
    elif transaction_type == TransactionType.EXPENSE:
        buttons = [
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).CHATGPT3_TURBO,
                    callback_data=f'statistics_choose_service:{ServiceType.CHAT_GPT3_TURBO}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).CHATGPT4_TURBO,
                    callback_data=f'statistics_choose_service:{ServiceType.CHAT_GPT4_TURBO}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).CHATGPT4_OMNI_MINI,
                    callback_data=f'statistics_choose_service:{ServiceType.CHAT_GPT4_OMNI_MINI}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).CHATGPT4_OMNI,
                    callback_data=f'statistics_choose_service:{ServiceType.CHAT_GPT4_OMNI}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).CHAT_GPT_O_1_MINI,
                    callback_data=f'statistics_choose_service:{ServiceType.CHAT_GPT_O_1_MINI}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).CHAT_GPT_O_1_PREVIEW,
                    callback_data=f'statistics_choose_service:{ServiceType.CHAT_GPT_O_1_PREVIEW}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).CLAUDE_3_HAIKU,
                    callback_data=f'statistics_choose_service:{ServiceType.CLAUDE_3_HAIKU}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).CLAUDE_3_SONNET,
                    callback_data=f'statistics_choose_service:{ServiceType.CLAUDE_3_SONNET}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).CLAUDE_3_OPUS,
                    callback_data=f'statistics_choose_service:{ServiceType.CLAUDE_3_OPUS}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).GEMINI_1_FLASH,
                    callback_data=f'statistics_choose_service:{ServiceType.GEMINI_1_FLASH}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).GEMINI_1_PRO,
                    callback_data=f'statistics_choose_service:{ServiceType.GEMINI_1_PRO}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).GEMINI_1_ULTRA,
                    callback_data=f'statistics_choose_service:{ServiceType.GEMINI_1_ULTRA}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).DALL_E,
                    callback_data=f'statistics_choose_service:{ServiceType.DALL_E}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).MIDJOURNEY,
                    callback_data=f'statistics_choose_service:{ServiceType.MIDJOURNEY}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).STABLE_DIFFUSION,
                    callback_data=f'statistics_choose_service:{ServiceType.STABLE_DIFFUSION}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).FLUX,
                    callback_data=f'statistics_choose_service:{ServiceType.FLUX}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).FACE_SWAP,
                    callback_data=f'statistics_choose_service:{ServiceType.FACE_SWAP}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).PHOTOSHOP_AI,
                    callback_data=f'statistics_choose_service:{ServiceType.PHOTOSHOP_AI}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).MUSIC_GEN,
                    callback_data=f'statistics_choose_service:{ServiceType.MUSIC_GEN}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).SUNO,
                    callback_data=f'statistics_choose_service:{ServiceType.SUNO}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).THEMATIC_CHATS,
                    callback_data=f'statistics_choose_service:{ServiceType.ADDITIONAL_CHATS}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).FAST_ANSWERS,
                    callback_data=f'statistics_choose_service:{ServiceType.FAST_MESSAGES}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).VOICE_MESSAGES,
                    callback_data=f'statistics_choose_service:{ServiceType.VOICE_MESSAGES}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).ACCESS_TO_CATALOG,
                    callback_data=f'statistics_choose_service:{ServiceType.ACCESS_TO_CATALOG}'
                )
            ],
            [
                InlineKeyboardButton(
                    text='Server 💻',
                    callback_data=f'statistics_choose_service:{ServiceType.SERVER}'
                )
            ],
            [
                InlineKeyboardButton(
                    text='Database 🗄',
                    callback_data=f'statistics_choose_service:{ServiceType.DATABASE}'
                )
            ],
            [
                InlineKeyboardButton(
                    text='Other 🤷',
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
                text='RUB ₽',
                callback_data=f'statistics_choose_currency:{Currency.RUB}'
            )
        ],
        [
            InlineKeyboardButton(
                text='USD $',
                callback_data=f'statistics_choose_currency:{Currency.USD}'
            )
        ],
        [
            InlineKeyboardButton(
                text='Telegram Stars ⭐',
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
