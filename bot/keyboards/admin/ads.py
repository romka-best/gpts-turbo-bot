from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.locales.main import get_localization


def build_ads_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).ADS_CREATE,
                callback_data='ads:create',
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).ADS_GET,
                callback_data='ads:get',
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).BACK,
                callback_data='ads:back',
            ),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_ads_create_choose_source_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text='Telegram ✈️',
                callback_data='ads_create_choose_source:telegram',
            ),
        ],
        [
            InlineKeyboardButton(
                text='Instagram 📷',
                callback_data='ads_create_choose_source:instagram',
            ),
        ],
        [
            InlineKeyboardButton(
                text='Google 🔍',
                callback_data='ads_create_choose_source:google',
            ),
        ],
        [
            InlineKeyboardButton(
                text='Yandex 🔎',
                callback_data='ads_create_choose_source:google',
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).BACK,
                callback_data='ads_create_choose_source:back',
            ),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_ads_create_choose_medium_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text='Контекстная Реклама 🪧',
                callback_data='ads_create_choose_medium:cpc',
            ),
        ],
        [
            InlineKeyboardButton(
                text='E-Mail 📧',
                callback_data='ads_create_choose_medium:email',
            ),
        ],
        [
            InlineKeyboardButton(
                text='Социальные Сети 🌐',
                callback_data='ads_create_choose_medium:social',
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).BACK,
                callback_data='ads_create_choose_medium:back',
            ),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_ads_create_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).BACK,
                callback_data='ads_create:back',
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CANCEL,
                callback_data='ads_create:cancel',
            ),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_ads_get_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).BACK,
                callback_data='ads_get:back',
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CANCEL,
                callback_data='ads_get:cancel',
            ),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
