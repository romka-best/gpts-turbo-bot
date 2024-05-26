from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.database.models.package import Package, PackageType
from bot.locales.main import get_localization


def build_bonus_keyboard(language_code: str, user_id: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).INVITE_FRIEND,
                url=get_localization(language_code).referral_link(user_id, True),
                callback_data=f'bonus:invite_friend'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).LEAVE_FEEDBACK,
                callback_data=f'bonus:leave_feedback'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CASH_OUT,
                callback_data=f'bonus:cash_out'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CLOSE,
                callback_data=f'bonus:close'
            ),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_bonus_cash_out_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = []
    for package_type in PackageType.get_class_attributes_in_order():
        buttons.append(
            [
                InlineKeyboardButton(
                    text=Package.get_translate_name_and_description(
                        get_localization(language_code),
                        package_type,
                    ).get('name'),
                    callback_data=f'bonus_cash_out:{package_type}'
                ),
            ],
        )
    buttons.append(
        [
            InlineKeyboardButton(
                text=get_localization(language_code).BACK,
                callback_data='bonus_cash_out:back'
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=buttons)
