from datetime import datetime, timezone, timedelta

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.database.models.subscription import SubscriptionType
from bot.database.models.transaction import ServiceType, TransactionType
from bot.database.operations.chat import get_chats
from bot.database.operations.face_swap_package import get_used_face_swap_packages, get_face_swap_packages
from bot.database.operations.transaction import get_transactions, write_transaction
from bot.database.operations.user import get_user, get_users
from bot.keyboards.common import build_cancel_keyboard
from bot.states.statistics import Statistics
from bot.utils.is_admin import is_admin
from bot.keyboards.statistics import build_statistics_keyboard, build_statistics_write_transaction_keyboard, \
    build_statistics_choose_service_keyboard, build_statistics_choose_currency_keyboard
from bot.locales.main import get_localization

statistics_router = Router()


async def handle_statistics(chat_id: str, user_id: str, message: Message):
    if is_admin(chat_id):
        user = await get_user(user_id)

        reply_markup = build_statistics_keyboard(user.language_code)
        await message.answer(text=get_localization(user.language_code).STATISTICS_INFO,
                             reply_markup=reply_markup)


@statistics_router.message(Command("statistics"))
async def statistics(message: Message):
    await handle_statistics(str(message.chat.id), str(message.from_user.id), message)


async def handle_write_transaction(callback_query: CallbackQuery, language_code: str):
    reply_markup = build_statistics_write_transaction_keyboard(language_code)
    await callback_query.message.edit_text(text=get_localization(language_code).STATISTICS_WRITE_TRANSACTION,
                                           reply_markup=reply_markup)


@statistics_router.callback_query(lambda c: c.data.startswith('statistics:'))
async def handle_statistics_selection(callback_query: CallbackQuery):
    await callback_query.answer()

    user = await get_user(str(callback_query.from_user.id))

    period = callback_query.data.split(':')[1]

    if period == 'write_transaction':
        await handle_write_transaction(callback_query, user.language_code)
        return

    current_date = datetime.now(timezone.utc)
    start_date = None
    end_date = None
    if period == "day":
        start_date = current_date - timedelta(days=1)
        end_date = current_date - timedelta(days=1)
        period = current_date.strftime("%d.%m.%Y")
    elif period == "week":
        start_date = current_date - timedelta(days=current_date.weekday())
        end_date = start_date + timedelta(days=6)
        period = f"{start_date.strftime('%d.%m.%Y')}-{end_date.strftime('%d.%m.%Y')}"
    elif period == "month":
        start_date = current_date.replace(day=1)
        end_date = current_date.replace(day=1) + timedelta(days=32)
        end_date = end_date - timedelta(days=end_date.day)
        period = f"{start_date.strftime('%d.%m.%Y')}-{end_date.strftime('%d.%m.%Y')}"
    else:
        period = "всё время"

    users = await get_users(start_date, end_date)
    transactions = await get_transactions(start_date, end_date)
    chats = await get_chats(start_date, end_date)
    face_swap_packages = await get_face_swap_packages()
    used_face_swap_packages = await get_used_face_swap_packages(start_date, end_date)

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

    paid_users = set()
    count_income_transactions = {
        ServiceType.GPT3: 0,
        ServiceType.GPT4: 0,
        ServiceType.DALLE3: 0,
        ServiceType.FACE_SWAP: 0,
        ServiceType.ADDITIONAL_CHATS: 0,
        ServiceType.ACCESS_TO_CATALOG: 0,
        ServiceType.VOICE_MESSAGES: 0,
        ServiceType.FAST_MESSAGES: 0,
        ServiceType.STANDARD: 0,
        ServiceType.VIP: 0,
        ServiceType.PLATINUM: 0,
    }
    count_expense_transactions = {
        ServiceType.GPT3: 0,
        ServiceType.GPT4: 0,
        ServiceType.DALLE3: 0,
        ServiceType.FACE_SWAP: 0,
        ServiceType.VOICE_MESSAGES: 0,
        ServiceType.SERVER: 0,
        ServiceType.DATABASE: 0,
    }
    count_income_transactions_total = 0
    count_expense_transactions_total = 0
    count_transactions_total = 0
    count_income_money = {
        ServiceType.GPT3: 0,
        ServiceType.GPT4: 0,
        ServiceType.DALLE3: 0,
        ServiceType.FACE_SWAP: 0,
        ServiceType.ADDITIONAL_CHATS: 0,
        ServiceType.ACCESS_TO_CATALOG: 0,
        ServiceType.VOICE_MESSAGES: 0,
        ServiceType.FAST_MESSAGES: 0,
        ServiceType.STANDARD: 0,
        ServiceType.VIP: 0,
        ServiceType.PLATINUM: 0,
    }
    count_expense_money = {
        ServiceType.GPT3: 0,
        ServiceType.GPT4: 0,
        ServiceType.DALLE3: 0,
        ServiceType.FACE_SWAP: 0,
        ServiceType.VOICE_MESSAGES: 0,
        ServiceType.SERVER: 0,
        ServiceType.DATABASE: 0,
    }
    count_income_subscriptions_total_money = 0
    count_income_packages_total_money = 0
    count_expense_total_money = 0
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
            count_expense_transactions[transaction.service] += transaction.quantity
            count_expense_money[transaction.service] += transaction.amount
            count_expense_total_money += transaction.amount

        count_transactions_total += 1

    count_all_users = len(users)
    count_activated_users = len(paid_users)
    count_income_total_money = count_income_subscriptions_total_money + count_income_packages_total_money
    total_money = count_income_total_money - count_expense_total_money * 100

    count_chats_usage = {
        'ALL': len(chats),
    }
    for chat in chats:
        count_chats_usage[chat.role] = count_chats_usage.get(chat.role, 0) + 1

    count_face_swap_usage = {
        'ALL': 0,
    }
    for face_swap_package in face_swap_packages:
        used_face_swap_package = list(
            filter(
                lambda used: face_swap_package.id == used.package_id, used_face_swap_packages
            )
        )
        used_images = len(used_face_swap_package[0].used_images) if len(used_face_swap_package) else 0
        count_face_swap_usage[face_swap_package.name] = count_face_swap_usage.get(
            face_swap_package.name,
            used_images
        )
    for count in count_face_swap_usage.values():
        count_face_swap_usage['ALL'] += count

    await callback_query.message.answer(
        text=get_localization(user.language_code).statistics(
            period=period,
            count_all_users=count_all_users,
            count_activated_users=count_activated_users,
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
            count_face_swap_usage=count_face_swap_usage,
        ),
        protect_content=True,
    )


@statistics_router.callback_query(lambda c: c.data.startswith('statistics_write_transaction:'))
async def handle_statistics_write_transaction_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    transaction_type = callback_query.data.split(':')[1]
    if transaction_type == 'back':
        await handle_statistics(str(callback_query.message.chat.id),
                                str(callback_query.from_user.id),
                                callback_query.message)

        await callback_query.message.delete()
    else:
        user = await get_user(str(callback_query.from_user.id))

        reply_markup = build_statistics_choose_service_keyboard(user.language_code, transaction_type)
        await callback_query.message.edit_text(
            text=get_localization(user.language_code).STATISTICS_CHOOSE_SERVICE,
            reply_markup=reply_markup
        )

        await state.update_data(transaction_type=transaction_type)


@statistics_router.callback_query(lambda c: c.data.startswith('statistics_choose_service:'))
async def handle_statistics_choose_service_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    service_type = callback_query.data.split(':')[1]
    if service_type == 'cancel':
        await callback_query.message.delete()
        await state.clear()
    else:
        user = await get_user(str(callback_query.from_user.id))

        reply_markup = build_statistics_choose_currency_keyboard(user.language_code)
        await callback_query.message.edit_text(
            text=get_localization(user.language_code).STATISTICS_CHOOSE_CURRENCY,
            reply_markup=reply_markup
        )

        await state.set_state(Statistics.waiting_for_statistics_service_quantity)
        await state.update_data(service_type=service_type)


@statistics_router.callback_query(lambda c: c.data.startswith('statistics_choose_currency:'))
async def handle_statistics_choose_currency_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    currency = callback_query.data.split(':')[1]
    if currency == 'cancel':
        await callback_query.message.delete()
        await state.clear()
    else:
        user = await get_user(str(callback_query.from_user.id))

        reply_markup = build_cancel_keyboard(user.language_code)
        await callback_query.message.edit_text(
            text=get_localization(user.language_code).STATISTICS_SERVICE_QUANTITY,
            reply_markup=reply_markup
        )

        await state.set_state(Statistics.waiting_for_statistics_service_quantity)
        await state.update_data(currency=currency)


@statistics_router.message(Statistics.waiting_for_statistics_service_quantity)
async def statistics_service_quantity_sent(message: Message, state: FSMContext):
    user = await get_user(str(message.from_user.id))

    try:
        quantity = int(message.text)
        if quantity < 1:
            reply_markup = build_cancel_keyboard(user.language_code)
            await message.answer(text=get_localization(user.language_code).MIN_ERROR,
                                 reply_markup=reply_markup)
        else:
            reply_markup = build_cancel_keyboard(user.language_code)
            await message.answer(text=get_localization(user.language_code).STATISTICS_SERVICE_AMOUNT,
                                 reply_markup=reply_markup)

            await state.update_data(service_quantity=quantity)
            await state.set_state(Statistics.waiting_for_statistics_service_amount)
    except ValueError:
        reply_markup = build_cancel_keyboard(user.language_code)
        await message.reply(text=get_localization(user.language_code).VALUE_ERROR,
                            reply_markup=reply_markup)


@statistics_router.message(Statistics.waiting_for_statistics_service_amount)
async def statistics_service_amount_sent(message: Message, state: FSMContext):
    user = await get_user(str(message.from_user.id))

    try:
        amount = float(message.text)
        if amount < 0:
            reply_markup = build_cancel_keyboard(user.language_code)
            await message.answer(text=get_localization(user.language_code).MIN_ERROR,
                                 reply_markup=reply_markup)
        else:
            reply_markup = build_cancel_keyboard(user.language_code)
            await message.answer(text=get_localization(user.language_code).STATISTICS_SERVICE_DATE,
                                 reply_markup=reply_markup)

            await state.update_data(service_amount=amount)
            await state.set_state(Statistics.waiting_for_statistics_service_date)
    except ValueError:
        reply_markup = build_cancel_keyboard(user.language_code)
        await message.reply(text=get_localization(user.language_code).VALUE_ERROR,
                            reply_markup=reply_markup)


@statistics_router.message(Statistics.waiting_for_statistics_service_date)
async def statistics_service_date_sent(message: Message, state: FSMContext):
    user = await get_user(str(message.from_user.id))

    try:
        user_data = await state.get_data()
        service_date = datetime.strptime(message.text, "%d.%m.%Y")
        service_amount = user_data['service_amount']
        service_quantity = user_data['service_quantity']
        service_type = user_data['service_type']
        transaction_type = user_data['transaction_type']
        currency = user_data['currency']

        await write_transaction(
            user_id=user.id,
            type=transaction_type,
            service=service_type,
            amount=service_amount,
            currency=currency,
            quantity=service_quantity,
            created_at=service_date,
        )
        await message.answer(text=get_localization(user.language_code).STATISTICS_WRITE_TRANSACTION_SUCCESSFUL)

        await state.clear()
    except ValueError:
        reply_markup = build_cancel_keyboard(user.language_code)
        await message.reply(
            text=get_localization(user.language_code).STATISTICS_SERVICE_DATE_VALUE_ERROR,
            reply_markup=reply_markup,
        )
