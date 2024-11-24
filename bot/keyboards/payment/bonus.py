from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.database.models.game import GameType
from bot.database.models.product import Product
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
                text=get_localization(language_code).PLAY_GAME,
                callback_data=f'bonus:play_game'
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


def build_bonus_play_game_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).PLAY_BOWLING_GAME,
                callback_data=f'bonus_play_game:{GameType.BOWLING}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).PLAY_SOCCER_GAME,
                callback_data=f'bonus_play_game:{GameType.SOCCER}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).PLAY_BASKETBALL_GAME,
                callback_data=f'bonus_play_game:{GameType.BASKETBALL}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).PLAY_DARTS_GAME,
                callback_data=f'bonus_play_game:{GameType.DARTS}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).PLAY_DICE_GAME,
                callback_data=f'bonus_play_game:{GameType.DICE}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).PLAY_CASINO_GAME,
                callback_data=f'bonus_play_game:{GameType.CASINO}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).BACK,
                callback_data=f'bonus_play_game:back'
            ),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_bonus_play_game_chosen_keyboard(language_code: str, game_type: GameType) -> InlineKeyboardMarkup:
    buttons = []
    if (
        game_type == GameType.BOWLING or
        game_type == GameType.SOCCER or
        game_type == GameType.BASKETBALL or
        game_type == GameType.DARTS or
        game_type == GameType.CASINO
    ):
        buttons.append([
            InlineKeyboardButton(
                text=get_localization(language_code).PLAY,
                callback_data=f'bonus_play_game_chosen:{game_type}'
            ),
        ])
    elif game_type == GameType.DICE:
        buttons.extend([
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).PLAY_DICE_GAME_CHOOSE_1,
                    callback_data=f'bonus_play_game_chosen:{game_type}:1'
                ),
                InlineKeyboardButton(
                    text=get_localization(language_code).PLAY_DICE_GAME_CHOOSE_2,
                    callback_data=f'bonus_play_game_chosen:{game_type}:2'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).PLAY_DICE_GAME_CHOOSE_3,
                    callback_data=f'bonus_play_game_chosen:{game_type}:3'
                ),
                InlineKeyboardButton(
                    text=get_localization(language_code).PLAY_DICE_GAME_CHOOSE_4,
                    callback_data=f'bonus_play_game_chosen:{game_type}:4'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).PLAY_DICE_GAME_CHOOSE_5,
                    callback_data=f'bonus_play_game_chosen:{game_type}:5'
                ),
                InlineKeyboardButton(
                    text=get_localization(language_code).PLAY_DICE_GAME_CHOOSE_6,
                    callback_data=f'bonus_play_game_chosen:{game_type}:6'
                ),
            ],
        ])
    buttons.append([
        InlineKeyboardButton(
            text=get_localization(language_code).BACK,
            callback_data=f'bonus_play_game_chosen:back'
        ),
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_bonus_cash_out_keyboard(language_code: str, products: list[Product]) -> InlineKeyboardMarkup:
    buttons = []
    for product in products:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=product.names.get(language_code),
                    callback_data=f'bonus_cash_out:{product.id}'
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
