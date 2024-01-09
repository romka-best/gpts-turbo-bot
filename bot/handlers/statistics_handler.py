from datetime import datetime, timezone, timedelta

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from bot.database.models.subscription import SubscriptionType
from bot.database.models.transaction import ServiceType, TransactionType
from bot.database.operations.chat import get_chats
from bot.database.operations.face_swap_package import get_used_face_swap_packages, get_face_swap_packages
from bot.database.operations.transaction import get_transactions
from bot.database.operations.user import get_user, get_users
from bot.utils.is_admin import is_admin
from bot.keyboards.statistics import build_statistics_keyboard
from bot.locales.main import get_localization

statistics_router = Router()


@statistics_router.message(Command("statistics"))
async def statistics(message: Message):
    if is_admin(str(message.chat.id)):
        user = await get_user(str(message.from_user.id))

        reply_markup = build_statistics_keyboard(user.language_code)
        await message.answer(text=get_localization(user.language_code).STATISTICS_INFO,
                             reply_markup=reply_markup)


@statistics_router.callback_query(lambda c: c.data.startswith('statistics:'))
async def handle_statistics_selection(callback_query: CallbackQuery):
    await callback_query.answer()

    user = await get_user(str(callback_query.from_user.id))

    period = callback_query.data.split(':')[1]

    current_date = datetime.now(timezone.utc)
    start_date = None
    end_date = None
    if period == "day":
        start_date = current_date
        end_date = current_date
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
    for user in users:
        count_subscription_users[user.subscription_type] += 1

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
        elif transaction.type == TransactionType.EXPENSE:
            count_expense_transactions_total += 1
            count_expense_transactions[transaction.service] += transaction.quantity
            count_expense_money[transaction.service] += transaction.amount
            count_expense_total_money += transaction.amount
            paid_users.add(transaction.user_id)

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
        'ALL': len(used_face_swap_packages)
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

    await callback_query.message.answer(text=get_localization(user.language_code).statistics(
        period=period,
        count_all_users=count_all_users,
        count_activated_users=count_activated_users,
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
    ))
