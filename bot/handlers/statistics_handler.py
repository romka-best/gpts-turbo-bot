from datetime import datetime, timezone, timedelta

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from bot.config import config
from bot.database.models.common import RoleName
from bot.database.models.face_swap_package import FaceSwapPackageName
from bot.database.models.subscription import SubscriptionType
from bot.database.models.transaction import ServiceType, TransactionType
from bot.database.operations.chat import get_chats
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


@statistics_router.callback_query(lambda c: c.from_user.id in config.ADMIN_CHAT_IDS)
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
        RoleName.PERSONAL_ASSISTANT: 0,
        RoleName.TUTOR: 0,
        RoleName.LANGUAGE_TUTOR: 0,
        RoleName.TECHNICAL_ADVISOR: 0,
        RoleName.MARKETER: 0,
        RoleName.SMM_SPECIALIST: 0,
        RoleName.CONTENT_SPECIALIST: 0,
        RoleName.DESIGNER: 0,
        RoleName.SOCIAL_MEDIA_PRODUCER: 0,
        RoleName.LIFE_COACH: 0,
        RoleName.ENTREPRENEUR: 0,
        'ALL': len(chats),
    }
    for chat in chats:
        count_chats_usage[chat.role] += 1

    count_face_swap_usage = {
        FaceSwapPackageName.CELEBRITIES['name']: 0,
        FaceSwapPackageName.MOVIE_CHARACTERS['name']: 0,
        FaceSwapPackageName.PROFESSIONS['name']: 0,
        'ALL': len()
    }

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
    ))
