from datetime import datetime, timezone, timedelta

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, URLInputFile
from google.cloud.firestore_v1 import Increment

from bot.config import config, MessageEffect
from bot.database.main import firebase
from bot.database.models.common import PaymentMethod
from bot.database.models.game import GameType, GameStatus
from bot.database.models.package import PackageType, Package, PackageStatus
from bot.database.models.transaction import TransactionType
from bot.database.operations.feedback.getters import get_count_of_approved_feedbacks_by_user_id
from bot.database.operations.game.getters import get_count_of_games_by_user_id
from bot.database.operations.game.writers import write_game
from bot.database.operations.package.writers import write_package
from bot.database.operations.transaction.writers import write_transaction
from bot.database.operations.user.getters import get_user, get_count_of_users_by_referral
from bot.database.operations.user.updaters import update_user
from bot.handlers.common.feedback_handler import handle_feedback
from bot.keyboards.payment.bonus import (
    build_bonus_keyboard,
    build_bonus_play_game_keyboard,
    build_bonus_cash_out_keyboard, build_bonus_play_game_chosen_keyboard,
)
from bot.keyboards.common.common import build_cancel_keyboard
from bot.locales.main import get_localization, get_user_language
from bot.states.bonus import Bonus

bonus_router = Router()


@bonus_router.message(Command('bonus'))
async def bonus(message: Message, state: FSMContext):
    await state.clear()

    await handle_bonus(message, str(message.from_user.id), state)


async def handle_bonus(message: Message, user_id: str, state: FSMContext):
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)
    count_of_referred_users = await get_count_of_users_by_referral(user_id)
    count_of_feedbacks = await get_count_of_approved_feedbacks_by_user_id(user_id)
    count_of_games = await get_count_of_games_by_user_id(user_id)

    photo_path = f'payments/packages_{user_language_code}.png'
    photo = await firebase.bucket.get_blob(photo_path)
    photo_link = firebase.get_public_url(photo.name)

    text = get_localization(user_language_code).bonus(
        user_id,
        user.balance,
        count_of_referred_users,
        count_of_feedbacks,
        count_of_games,
    )
    reply_markup = build_bonus_keyboard(user_language_code, user_id)
    await message.answer_photo(
        photo=URLInputFile(photo_link, filename=photo_path),
        caption=text,
        reply_markup=reply_markup,
    )


@bonus_router.callback_query(lambda c: c.data.startswith('bonus:'))
async def handle_bonus_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    action = callback_query.data.split(':')[1]
    if action == 'leave_feedback':
        await handle_feedback(callback_query.message, str(callback_query.from_user.id), state)
    elif action == 'play_game':
        user_language_code = await get_user_language(str(callback_query.from_user.id), state.storage)

        reply_markup = build_bonus_play_game_keyboard(user_language_code)
        await callback_query.message.edit_caption(
            caption=get_localization(user_language_code).PLAY_GAME_CHOOSE,
            reply_markup=reply_markup,
        )
    elif action == 'cash_out':
        user_language_code = await get_user_language(str(callback_query.from_user.id), state.storage)

        reply_markup = build_bonus_cash_out_keyboard(user_language_code)
        await callback_query.message.edit_caption(
            caption=get_localization(user_language_code).BONUS_CHOOSE_PACKAGE,
            reply_markup=reply_markup,
        )


@bonus_router.callback_query(lambda c: c.data.startswith('bonus_play_game:'))
async def handle_bonus_play_game_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)
    user_language_code = await get_user_language(user_id, state.storage)

    game_type = callback_query.data.split(':')[1]
    reply_markup = build_bonus_play_game_chosen_keyboard(user_language_code, game_type)
    if game_type == GameType.BOWLING:
        await callback_query.message.edit_caption(
            caption=get_localization(user_language_code).PLAY_BOWLING_GAME_DESCRIPTION,
            reply_markup=reply_markup,
        )
    elif game_type == GameType.SOCCER:
        await callback_query.message.edit_caption(
            caption=get_localization(user_language_code).PLAY_SOCCER_GAME_DESCRIPTION,
            reply_markup=reply_markup,
        )
    elif game_type == GameType.BASKETBALL:
        await callback_query.message.edit_caption(
            caption=get_localization(user_language_code).PLAY_BASKETBALL_GAME_DESCRIPTION,
            reply_markup=reply_markup,
        )
    elif game_type == GameType.DARTS:
        await callback_query.message.edit_caption(
            caption=get_localization(user_language_code).PLAY_DARTS_GAME_DESCRIPTION,
            reply_markup=reply_markup,
        )
    elif game_type == GameType.DICE:
        await callback_query.message.edit_caption(
            caption=get_localization(user_language_code).PLAY_DICE_GAME_CHOOSE,
            reply_markup=reply_markup,
        )
    elif game_type == GameType.CASINO:
        await callback_query.message.edit_caption(
            caption=get_localization(user_language_code).PLAY_CASINO_GAME_DESCRIPTION,
            reply_markup=reply_markup,
        )
    else:
        user = await get_user(user_id)

        count_of_referred_users = await get_count_of_users_by_referral(user_id)
        count_of_feedbacks = await get_count_of_approved_feedbacks_by_user_id(user_id)
        count_of_games = await get_count_of_games_by_user_id(user_id)

        text = get_localization(user_language_code).bonus(
            user_id,
            user.balance,
            count_of_referred_users,
            count_of_feedbacks,
            count_of_games,
        )
        reply_markup = build_bonus_keyboard(user_language_code, user_id)
        await callback_query.message.edit_caption(
            caption=text,
            reply_markup=reply_markup,
        )


@bonus_router.callback_query(lambda c: c.data.startswith('bonus_play_game_chosen:'))
async def handle_bonus_play_game_chosen_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)
    user_language_code = await get_user_language(user_id, state.storage)

    game_type = callback_query.data.split(':')[1]
    if game_type == 'back':
        reply_markup = build_bonus_play_game_keyboard(user_language_code)
        await callback_query.message.edit_caption(
            caption=get_localization(user_language_code).PLAY_GAME_CHOOSE,
            reply_markup=reply_markup,
        )
        return

    current_date = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    count_of_games = await get_count_of_games_by_user_id(user_id, current_date)
    if count_of_games > 0:
        await callback_query.message.answer(
            text=get_localization(user_language_code).PLAY_GAME_REACHED_LIMIT,
        )
        return

    final_credits = 0
    if game_type == GameType.BOWLING:
        final_credits = (await callback_query.message.answer_dice('🎳')).dice.value
    elif game_type == GameType.SOCCER:
        won_credits = (await callback_query.message.answer_dice('⚽️')).dice.value
        if won_credits > 2:
            final_credits = 5
    elif game_type == GameType.BASKETBALL:
        won_credits = (await callback_query.message.answer_dice('🏀')).dice.value
        if won_credits > 3:
            final_credits = 10
    elif game_type == GameType.DARTS:
        won_credits = (await callback_query.message.answer_dice('🎯')).dice.value
        if won_credits == 6:
            final_credits = 15
    elif game_type == GameType.DICE:
        won_credits = (await callback_query.message.answer_dice('🎲')).dice.value
        user_choice = int(callback_query.data.split(':')[2])
        if won_credits == user_choice:
            final_credits = 20
    elif game_type == GameType.CASINO:
        won_credits = (await callback_query.message.answer_dice('🎰')).dice.value
        if won_credits in [1, 22, 43]:
            final_credits = 50
        elif won_credits == 64:
            final_credits = 100

    game_status = GameStatus.WON if final_credits > 0 else GameStatus.LOST
    await write_game(user_id, game_type, game_status)

    if game_status == GameStatus.WON:
        await update_user(user_id, {
            'balance': Increment(final_credits),
        })

        await callback_query.message.answer(
            text=get_localization(user_language_code).PLAY_GAME_WON,
            message_effect_id=config.MESSAGE_EFFECTS.get(MessageEffect.CONGRATS),
        )
    else:
        await callback_query.message.answer(
            text=get_localization(user_language_code).PLAY_GAME_LOST,
        )


@bonus_router.callback_query(lambda c: c.data.startswith('bonus_cash_out:'))
async def handle_bonus_cash_out_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)
    user_language_code = await get_user_language(user_id, state.storage)

    package_type = callback_query.data.split(':')[1]
    if package_type == 'back':
        user = await get_user(user_id)
        count_of_referred_users = await get_count_of_users_by_referral(user_id)
        count_of_feedbacks = await get_count_of_approved_feedbacks_by_user_id(user_id)
        count_of_games = await get_count_of_games_by_user_id(user_id)

        text = get_localization(user_language_code).bonus(
            user_id,
            user.balance,
            count_of_referred_users,
            count_of_feedbacks,
            count_of_games,
        )
        reply_markup = build_bonus_keyboard(user_language_code, user_id)
        await callback_query.message.edit_caption(
            caption=text,
            reply_markup=reply_markup,
        )

        return

    message = get_localization(user_language_code).choose_min(package_type)

    reply_markup = build_cancel_keyboard(user_language_code)
    await callback_query.message.edit_caption(caption=message, reply_markup=reply_markup)

    await state.update_data(package_type=package_type)
    await state.set_state(Bonus.waiting_for_package_quantity)


@bonus_router.message(Bonus.waiting_for_package_quantity, ~F.text.startswith('/'))
async def quantity_of_bonus_package_sent(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    try:
        user_data = await state.get_data()
        package_type = user_data['package_type']
        package_quantity = int(message.text)
        price = Package.get_price(user.currency, package_type, package_quantity, 0)
        if price > user.balance:
            reply_markup = build_cancel_keyboard(user_language_code)
            await message.reply(
                text=get_localization(user_language_code).MAX_ERROR,
                reply_markup=reply_markup,
            )
        else:
            user.balance -= price
            until_at = None
            if (
                package_type == PackageType.VOICE_MESSAGES or
                package_type == PackageType.FAST_MESSAGES or
                package_type == PackageType.ACCESS_TO_CATALOG
            ):
                current_date = datetime.now(timezone.utc)
                until_at = current_date + timedelta(days=30 * package_quantity)
            package = await write_package(
                None,
                user_id,
                package_type,
                PackageStatus.SUCCESS,
                user.currency,
                0,
                0,
                package_quantity,
                PaymentMethod.GIFT,
                None,
                until_at,
            )

            (
                service_type,
                user.additional_usage_quota,
            ) = Package.get_service_type_and_update_quota(
                package_type,
                user.additional_usage_quota,
                package_quantity,
            )
            await write_transaction(
                user_id=user_id,
                type=TransactionType.INCOME,
                service=service_type,
                amount=0,
                clear_amount=0,
                currency=user.currency,
                quantity=package_quantity,
                details={
                    'payment_method': PaymentMethod.GIFT,
                    'package_id': package.id,
                    'provider_payment_charge_id': '',
                    'is_bonus': True,
                },
            )
            await update_user(user_id, {
                'balance': user.balance,
                'additional_usage_quota': user.additional_usage_quota,
            })

            await message.reply(text=get_localization(user_language_code).BONUS_ACTIVATED_SUCCESSFUL)

            await state.clear()
    except (TypeError, ValueError):
        reply_markup = build_cancel_keyboard(user_language_code)
        await message.reply(
            text=get_localization(user_language_code).VALUE_ERROR,
            reply_markup=reply_markup,
        )
