from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.database.models.package import Package, PackageType
from bot.locales.main import get_localization


def build_bonus_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = []
    for package_type in PackageType.get_class_attributes_in_order():
        buttons.append(
            [
                InlineKeyboardButton(
                    text=Package.get_translate_name_and_description(
                        get_localization(language_code),
                        package_type,
                    ).get('name'),
                    callback_data=f'bonus:{package_type}'
                ),
            ],
        )
    buttons.append(
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CLOSE,
                callback_data='bonus:close'
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=buttons)
