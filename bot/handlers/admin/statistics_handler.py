from datetime import datetime, timezone, timedelta

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.database.models.common import Model, MidjourneyAction
from bot.database.models.generation import GenerationReaction
from bot.database.models.subscription import SubscriptionType
from bot.database.models.transaction import TransactionType, ServiceType
from bot.database.operations.chat.getters import get_chats
from bot.database.operations.generation.getters import get_generations
from bot.database.operations.transaction.getters import get_transactions
from bot.database.operations.transaction.writers import write_transaction
from bot.database.operations.user.getters import get_users
from bot.keyboards.common.common import build_cancel_keyboard
from bot.states.statistics import Statistics
from bot.utils.is_admin import is_admin
from bot.keyboards.admin.statistics import (
    build_statistics_keyboard,
    build_statistics_write_transaction_keyboard,
    build_statistics_choose_service_keyboard,
    build_statistics_choose_currency_keyboard,
)
from bot.locales.main import get_localization, get_user_language

statistics_router = Router()


async def handle_statistics(chat_id: str, user_id: str, message: Message, state: FSMContext):
    if is_admin(chat_id):
        user_language_code = await get_user_language(str(user_id), state.storage)

        reply_markup = build_statistics_keyboard(user_language_code)
        await message.answer(
            text=get_localization(user_language_code).STATISTICS_INFO,
            reply_markup=reply_markup,
        )


@statistics_router.message(Command("statistics"))
async def statistics(message: Message, state: FSMContext):
    await state.clear()

    await handle_statistics(str(message.chat.id), str(message.from_user.id), message, state)


async def handle_write_transaction(callback_query: CallbackQuery, language_code: str):
    reply_markup = build_statistics_write_transaction_keyboard(language_code)
    await callback_query.message.edit_text(
        text=get_localization(language_code).STATISTICS_WRITE_TRANSACTION,
        reply_markup=reply_markup,
    )


async def handle_get_statistics(language_code: str, period: str):
    current_date = datetime.now(timezone.utc)
    start_date = None
    end_date = None
    if period == "day":
        start_date = (current_date - timedelta(days=1)).replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )
        end_date = (current_date - timedelta(days=1)).replace(
            hour=23,
            minute=59,
            second=59,
            microsecond=999999,
        )
        period = start_date.strftime("%d.%m.%Y")
    elif period == "week":
        start_date = (current_date - timedelta(days=current_date.weekday())).replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )
        end_date = (start_date + timedelta(days=6)).replace(
            hour=23,
            minute=59,
            second=59,
            microsecond=999999,
        )
        period = f"{start_date.strftime('%d.%m.%Y')}-{end_date.strftime('%d.%m.%Y')}"
    elif period == "month":
        start_date = current_date.replace(
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )
        end_date = start_date + timedelta(days=32)
        end_date = (end_date - timedelta(days=end_date.day)).replace(
            hour=23,
            minute=59,
            second=59,
            microsecond=999999,
        )
        period = f"{start_date.strftime('%d.%m.%Y')}-{end_date.strftime('%d.%m.%Y')}"
    else:
        period = "всё время"

    users = await get_users(start_date, end_date)
    transactions = await get_transactions(start_date, end_date)
    generations = await get_generations(start_date, end_date)
    chats = await get_chats(start_date, end_date)

    paid_users = set()
    activated_users = set()
    referral_users = set()
    english_users = set()
    russian_users = set()
    other_users = set()
    count_subscription_users = {
        SubscriptionType.FREE: 0,
        SubscriptionType.STANDARD: 0,
        SubscriptionType.VIP: 0,
        SubscriptionType.PLATINUM: 0,
    }
    count_blocked_users = 0
    for user in users:
        count_subscription_users[user.subscription_type] += 1
        if user.is_blocked:
            count_blocked_users += 1
        if user.referred_by:
            referral_users.add(user.id)

        if user.language_code == 'en':
            english_users.add(user.id)
        elif user.language_code == 'ru':
            russian_users.add(user.id)
        else:
            other_users.add(user.id)

    count_income_transactions = {
        ServiceType.CHAT_GPT3: 0,
        ServiceType.CHAT_GPT4: 0,
        ServiceType.DALL_E: 0,
        ServiceType.MIDJOURNEY: 0,
        ServiceType.FACE_SWAP: 0,
        ServiceType.MUSIC_GEN: 0,
        ServiceType.ADDITIONAL_CHATS: 0,
        ServiceType.ACCESS_TO_CATALOG: 0,
        ServiceType.VOICE_MESSAGES: 0,
        ServiceType.FAST_MESSAGES: 0,
        ServiceType.STANDARD: 0,
        ServiceType.VIP: 0,
        ServiceType.PLATINUM: 0,
    }
    count_expense_transactions = {
        ServiceType.CHAT_GPT3: 0,
        ServiceType.CHAT_GPT4: 0,
        ServiceType.DALL_E: 0,
        ServiceType.MIDJOURNEY: 0,
        ServiceType.FACE_SWAP: 0,
        ServiceType.MUSIC_GEN: [0, 0],
        ServiceType.VOICE_MESSAGES: 0,
        ServiceType.SERVER: 0,
        ServiceType.DATABASE: 0,
        ServiceType.OTHER: 0,
    }
    count_income_transactions_total = 0
    count_expense_transactions_total = 0
    count_transactions_total = 0
    count_income_money = {
        ServiceType.CHAT_GPT3: 0,
        ServiceType.CHAT_GPT4: 0,
        ServiceType.DALL_E: 0,
        ServiceType.MIDJOURNEY: 0,
        ServiceType.FACE_SWAP: 0,
        ServiceType.MUSIC_GEN: 0,
        ServiceType.ADDITIONAL_CHATS: 0,
        ServiceType.ACCESS_TO_CATALOG: 0,
        ServiceType.VOICE_MESSAGES: 0,
        ServiceType.FAST_MESSAGES: 0,
        ServiceType.STANDARD: 0,
        ServiceType.VIP: 0,
        ServiceType.PLATINUM: 0,
    }
    count_expense_money = {
        ServiceType.CHAT_GPT3: 0,
        ServiceType.CHAT_GPT4: 0,
        ServiceType.DALL_E: 0,
        ServiceType.MIDJOURNEY: 0,
        ServiceType.FACE_SWAP: 0,
        ServiceType.MUSIC_GEN: 0,
        ServiceType.VOICE_MESSAGES: 0,
        ServiceType.SERVER: 0,
        ServiceType.DATABASE: 0,
        ServiceType.OTHER: 0,
    }
    count_income_subscriptions_total_money = 0
    count_income_packages_total_money = 0
    count_expense_total_money = 0
    count_midjourney_usage = {
        MidjourneyAction.IMAGINE: 0,
        MidjourneyAction.UPSCALE: 0,
        MidjourneyAction.VARIATION: 0,
        MidjourneyAction.REROLL: 0,
        'ALL': 0,
    }
    count_face_swap_usage = {
        'CUSTOM': 0,
        'ALL': 0,
    }
    count_reactions = {
        ServiceType.MIDJOURNEY: {
            GenerationReaction.LIKED: 0,
            GenerationReaction.DISLIKED: 0,
            GenerationReaction.NONE: 0,
        },
        ServiceType.FACE_SWAP: {
            GenerationReaction.LIKED: 0,
            GenerationReaction.DISLIKED: 0,
            GenerationReaction.NONE: 0,
        },
        ServiceType.MUSIC_GEN: {
            GenerationReaction.LIKED: 0,
            GenerationReaction.DISLIKED: 0,
            GenerationReaction.NONE: 0,
        },
    }
    for transaction in transactions:
        if transaction.type == TransactionType.INCOME:
            count_income_transactions_total += 1
            count_income_transactions[transaction.service] += transaction.quantity
            count_income_money[transaction.service] += transaction.amount
            if (
                transaction.service == ServiceType.STANDARD or
                transaction.service == ServiceType.VIP or
                transaction.service == ServiceType.PLATINUM
            ):
                count_income_subscriptions_total_money += transaction.amount
            else:
                count_income_packages_total_money += transaction.amount
            paid_users.add(transaction.user_id)
        elif transaction.type == TransactionType.EXPENSE:
            count_expense_transactions_total += 1
            if transaction.service == ServiceType.MUSIC_GEN:
                count_expense_transactions[transaction.service][0] += transaction.quantity
                count_expense_transactions[transaction.service][1] += 1
            else:
                count_expense_transactions[transaction.service] += transaction.quantity
            count_expense_money[transaction.service] += transaction.amount
            count_expense_total_money += transaction.amount

            if transaction.service == ServiceType.MIDJOURNEY:
                midjourney_action = transaction.details.get('type')
                count_midjourney_usage[midjourney_action] = count_midjourney_usage.get(
                    midjourney_action,
                    0,
                ) + 1

            if transaction.service == ServiceType.FACE_SWAP and transaction.quantity != 0:
                face_swap_name = transaction.details.get('name', 'UNKNOWN')
                face_swap_images = transaction.details.get('images', ['UNKNOWN'])
                count_face_swap_usage[face_swap_name] = count_face_swap_usage.get(
                    face_swap_name,
                    0,
                ) + len(face_swap_images)

        activated_users.add(transaction.user_id)
        count_transactions_total += 1

    for generation in generations:
        if generation.model == Model.MIDJOURNEY and generation.details.get('action') == MidjourneyAction.UPSCALE:
            count_reactions[ServiceType.MIDJOURNEY][generation.reaction] += 1
        elif generation.model == Model.FACE_SWAP:
            count_reactions[ServiceType.FACE_SWAP][generation.reaction] += 1
        elif generation.model == Model.MUSIC_GEN:
            count_reactions[ServiceType.MUSIC_GEN][generation.reaction] += 1

    count_all_users = len(users)
    count_activated_users = len(activated_users)
    count_referral_users = len(referral_users)
    count_english_users = len(english_users)
    count_russian_users = len(russian_users)
    count_other_users = len(other_users)
    count_paid_users = len(paid_users)
    count_income_total_money = count_income_subscriptions_total_money + count_income_packages_total_money
    total_money = count_income_total_money - count_expense_total_money * 100

    count_chats_usage = {
        'ALL': len(chats),
    }
    count_midjourney_usage['ALL'] = sum(count_midjourney_usage.values())
    count_face_swap_usage['ALL'] = sum(count_face_swap_usage.values())
    for chat in chats:
        count_chats_usage[chat.role] = count_chats_usage.get(chat.role, 0) + 1

    return get_localization(language_code).statistics(
        period=period,
        count_all_users=count_all_users,
        count_activated_users=count_activated_users,
        count_referral_users=count_referral_users,
        count_english_users=count_english_users,
        count_russian_users=count_russian_users,
        count_other_users=count_other_users,
        count_paid_users=count_paid_users,
        count_blocked_users=count_blocked_users,
        count_subscription_users=count_subscription_users,
        count_income_transactions=count_income_transactions,
        count_expense_transactions=count_expense_transactions,
        count_income_transactions_total=count_income_transactions_total,
        count_expense_transactions_total=count_expense_transactions_total,
        count_transactions_total=count_transactions_total,
        count_expense_money=count_expense_money,
        count_income_money=count_income_money,
        count_income_subscriptions_total_money=count_income_subscriptions_total_money,
        count_income_packages_total_money=count_income_packages_total_money,
        count_income_total_money=count_income_total_money,
        count_expense_total_money=count_expense_total_money,
        count_total_money=total_money,
        count_chats_usage=count_chats_usage,
        count_midjourney_usage=count_midjourney_usage,
        count_face_swap_usage=count_face_swap_usage,
        count_reactions=count_reactions,
    )


@statistics_router.callback_query(lambda c: c.data.startswith('statistics:'))
async def handle_statistics_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_language_code = await get_user_language(str(callback_query.from_user.id), state.storage)

    period = callback_query.data.split(':')[1]

    if period == 'write_transaction':
        await handle_write_transaction(callback_query, user_language_code)
        return

    text = await handle_get_statistics(user_language_code, period)
    await callback_query.message.answer(
        text=text,
        protect_content=True,
    )


@statistics_router.callback_query(lambda c: c.data.startswith('statistics_write_transaction:'))
async def handle_statistics_write_transaction_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    transaction_type = callback_query.data.split(':')[1]
    if transaction_type == 'back':
        await handle_statistics(
            str(callback_query.message.chat.id),
            str(callback_query.from_user.id),
            callback_query.message,
            state,
        )

        await callback_query.message.delete()
    else:
        user_language_code = await get_user_language(str(callback_query.from_user.id), state.storage)

        reply_markup = build_statistics_choose_service_keyboard(user_language_code, transaction_type)
        await callback_query.message.edit_text(
            text=get_localization(user_language_code).STATISTICS_CHOOSE_SERVICE,
            reply_markup=reply_markup
        )

        await state.update_data(transaction_type=transaction_type)


@statistics_router.callback_query(lambda c: c.data.startswith('statistics_choose_service:'))
async def handle_statistics_choose_service_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    service_type = callback_query.data.split(':')[1]
    user_language_code = await get_user_language(str(callback_query.from_user.id), state.storage)

    reply_markup = build_statistics_choose_currency_keyboard(user_language_code)
    await callback_query.message.edit_text(
        text=get_localization(user_language_code).STATISTICS_CHOOSE_CURRENCY,
        reply_markup=reply_markup
    )

    await state.set_state(Statistics.waiting_for_statistics_service_quantity)
    await state.update_data(service_type=service_type)


@statistics_router.callback_query(lambda c: c.data.startswith('statistics_choose_currency:'))
async def handle_statistics_choose_currency_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    currency = callback_query.data.split(':')[1]
    user_language_code = await get_user_language(str(callback_query.from_user.id), state.storage)

    reply_markup = build_cancel_keyboard(user_language_code)
    await callback_query.message.edit_text(
        text=get_localization(user_language_code).STATISTICS_SERVICE_QUANTITY,
        reply_markup=reply_markup
    )

    await state.set_state(Statistics.waiting_for_statistics_service_quantity)
    await state.update_data(currency=currency)


@statistics_router.message(Statistics.waiting_for_statistics_service_quantity, ~F.text.startswith('/'))
async def statistics_service_quantity_sent(message: Message, state: FSMContext):
    user_language_code = await get_user_language(str(message.from_user.id), state.storage)

    try:
        quantity = int(message.text)
        if quantity < 1:
            reply_markup = build_cancel_keyboard(user_language_code)
            await message.answer(
                text=get_localization(user_language_code).MIN_ERROR,
                reply_markup=reply_markup,
            )
        else:
            reply_markup = build_cancel_keyboard(user_language_code)
            await message.answer(
                text=get_localization(user_language_code).STATISTICS_SERVICE_AMOUNT,
                reply_markup=reply_markup,
            )

            await state.update_data(service_quantity=quantity)
            await state.set_state(Statistics.waiting_for_statistics_service_amount)
    except (TypeError, ValueError):
        reply_markup = build_cancel_keyboard(user_language_code)
        await message.reply(
            text=get_localization(user_language_code).VALUE_ERROR,
            reply_markup=reply_markup,
        )


@statistics_router.message(Statistics.waiting_for_statistics_service_amount, ~F.text.startswith('/'))
async def statistics_service_amount_sent(message: Message, state: FSMContext):
    user_language_code = await get_user_language(str(message.from_user.id), state.storage)

    try:
        amount = float(message.text)
        if amount < 0:
            reply_markup = build_cancel_keyboard(user_language_code)
            await message.answer(
                text=get_localization(user_language_code).MIN_ERROR,
                reply_markup=reply_markup,
            )
        else:
            reply_markup = build_cancel_keyboard(user_language_code)
            await message.answer(
                text=get_localization(user_language_code).STATISTICS_SERVICE_DATE,
                reply_markup=reply_markup,
            )

            await state.update_data(service_amount=amount)
            await state.set_state(Statistics.waiting_for_statistics_service_date)
    except (TypeError, ValueError):
        reply_markup = build_cancel_keyboard(user_language_code)
        await message.reply(
            text=get_localization(user_language_code).VALUE_ERROR,
            reply_markup=reply_markup,
        )


@statistics_router.message(Statistics.waiting_for_statistics_service_date, ~F.text.startswith('/'))
async def statistics_service_date_sent(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    user_language_code = await get_user_language(user_id, state.storage)

    try:
        user_data = await state.get_data()
        service_date = datetime.strptime(message.text, "%d.%m.%Y")
        service_amount = user_data['service_amount']
        service_quantity = user_data['service_quantity']
        service_type = user_data['service_type']
        transaction_type = user_data['transaction_type']
        currency = user_data['currency']

        await write_transaction(
            user_id=user_id,
            type=transaction_type,
            service=service_type,
            amount=service_amount,
            currency=currency,
            quantity=service_quantity,
            created_at=service_date,
        )
        await message.answer(text=get_localization(user_language_code).STATISTICS_WRITE_TRANSACTION_SUCCESSFUL)

        await state.clear()
    except (TypeError, ValueError):
        reply_markup = build_cancel_keyboard(user_language_code)
        await message.reply(
            text=get_localization(user_language_code).STATISTICS_SERVICE_DATE_VALUE_ERROR,
            reply_markup=reply_markup,
        )
