import asyncio
import calendar
from datetime import datetime, timezone, timedelta
from typing import Optional

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.chat_action import ChatActionSender
from google.cloud.firestore_v1 import FieldFilter

from bot.config import config
from bot.database.main import firebase
from bot.database.models.common import Model, MidjourneyAction, SunoMode, Currency, PhotoshopAIAction
from bot.database.models.feedback import FeedbackStatus
from bot.database.models.game import GameType
from bot.database.models.generation import GenerationReaction
from bot.database.models.subscription import SubscriptionType, SubscriptionStatus
from bot.database.models.transaction import TransactionType, ServiceType, Transaction
from bot.database.operations.feedback.getters import get_count_of_feedbacks
from bot.database.operations.game.getters import get_count_of_games, get_sum_of_games_reward
from bot.database.operations.generation.getters import get_count_of_generations
from bot.database.operations.promo_code.getters import get_count_of_used_promo_codes
from bot.database.operations.subscription.getters import get_count_of_subscriptions
from bot.database.operations.transaction.writers import write_transaction
from bot.database.operations.user.getters import get_user, get_count_of_users, get_count_of_users_referred_by
from bot.keyboards.admin.admin import build_admin_keyboard
from bot.keyboards.common.common import build_cancel_keyboard
from bot.states.statistics import Statistics
from bot.keyboards.admin.statistics import (
    build_statistics_keyboard,
    build_statistics_write_transaction_keyboard,
    build_statistics_choose_service_keyboard,
    build_statistics_choose_currency_keyboard,
)
from bot.locales.main import get_localization, get_user_language
from bot.utils.is_admin import is_admin

statistics_router = Router()


async def handle_statistics(message: Message, user_id: str, state: FSMContext):
    user_language_code = await get_user_language(str(user_id), state.storage)

    reply_markup = build_statistics_keyboard(user_language_code, is_admin(str(user_id)))
    await message.edit_text(
        text=get_localization(user_language_code).STATISTICS_INFO,
        reply_markup=reply_markup,
    )


async def handle_write_transaction(callback_query: CallbackQuery, language_code: str):
    reply_markup = build_statistics_write_transaction_keyboard(language_code)
    await callback_query.message.edit_text(
        text=get_localization(language_code).STATISTICS_WRITE_TRANSACTION,
        reply_markup=reply_markup,
    )


async def get_zero():
    return 0


async def get_statistics_by_transactions_query(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
):
    free_users = set()
    mini_users = set()
    standard_users = set()
    vip_users = set()
    premium_users = set()
    unlimited_users = set()
    paid_users = set()
    activated_users = set()

    user_cache = {}

    default_transaction_nested_dict = {
        'SUCCESS': 0,
        'FAIL': 0,
        'EXAMPLE': 0,
        'ALL': 0,
        'BONUS': 0,
    }
    count_all_transactions = {
        value: default_transaction_nested_dict.copy() for key, value in vars(ServiceType).items()
        if not key.startswith('__')
    }

    count_income_money_total = 0
    count_income_money = {
        value: 0 for key, value in vars(ServiceType).items()
        if not key.startswith('__') and value not in {
            ServiceType.SERVER,
            ServiceType.DATABASE,
        }
    }
    count_income_money.update({
        'SUBSCRIPTION_ALL': 0,
        'PACKAGES_ALL': 0,
        'AVERAGE_PRICE': 0,
        'ALL': 0,
        'VAL': 0,
    })

    default_expense_money_nested_dict = {
        'AVERAGE_EXAMPLE_PRICE': 0,
        'EXAMPLE_ALL': 0,
        'AVERAGE_PRICE': 0,
        'ALL': 0,
    }
    count_expense_money = {
        value: default_expense_money_nested_dict.copy() for key, value in vars(ServiceType).items()
        if not key.startswith('__') and value not in {
            ServiceType.ADDITIONAL_CHATS,
            ServiceType.FAST_MESSAGES,
            ServiceType.ACCESS_TO_CATALOG,
        }
    }
    count_expense_money[SubscriptionType.FREE] = default_expense_money_nested_dict.copy()
    count_expense_money['ALL'] = 0

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
    count_photoshop_ai_usage = {
        PhotoshopAIAction.RESTORATION: 0,
        PhotoshopAIAction.COLORIZATION: 0,
        PhotoshopAIAction.REMOVAL_BACKGROUND: 0,
        'ALL': 0,
    }
    count_suno_usage = {
        SunoMode.SIMPLE: 0,
        SunoMode.CUSTOM: 0,
        'ALL': 0,
    }

    service_subscriptions = [
        ServiceType.MINI,
        ServiceType.STANDARD,
        ServiceType.VIP,
        ServiceType.PREMIUM,
        ServiceType.UNLIMITED,
    ]
    service_ai_models = [
        ServiceType.CHAT_GPT3_TURBO, ServiceType.CHAT_GPT4_TURBO,
        ServiceType.CHAT_GPT4_OMNI, ServiceType.CHAT_GPT4_OMNI_MINI,
        ServiceType.CHAT_GPT_O_1_MINI, ServiceType.CHAT_GPT_O_1_PREVIEW,
        ServiceType.CLAUDE_3_HAIKU, ServiceType.CLAUDE_3_SONNET, ServiceType.CLAUDE_3_OPUS,
        ServiceType.GEMINI_1_FLASH, ServiceType.GEMINI_1_PRO, ServiceType.GEMINI_1_ULTRA,
        ServiceType.DALL_E, ServiceType.MIDJOURNEY, ServiceType.STABLE_DIFFUSION,
        ServiceType.FACE_SWAP, ServiceType.PHOTOSHOP_AI,
        ServiceType.MUSIC_GEN, ServiceType.SUNO,
    ]
    service_packages = service_ai_models + [
        ServiceType.ADDITIONAL_CHATS,
        ServiceType.ACCESS_TO_CATALOG,
        ServiceType.VOICE_MESSAGES,
        ServiceType.FAST_MESSAGES,
    ]

    transactions_query = firebase.db.collection(Transaction.COLLECTION_NAME).order_by('created_at')

    if start_date:
        transactions_query = transactions_query.where(filter=FieldFilter('created_at', '>=', start_date))
    if end_date:
        transactions_query = transactions_query.where(filter=FieldFilter('created_at', '<=', end_date))

    transactions_query = transactions_query.limit(config.BATCH_SIZE)

    is_running = True
    last_doc = None

    while is_running:
        if last_doc:
            transactions_query = transactions_query.start_after(last_doc)

        docs = transactions_query.stream()

        count = 0
        async for doc in docs:
            count += 1

            transaction = Transaction(**doc.to_dict())

            if transaction.user_id not in user_cache:
                transaction_user = await get_user(transaction.user_id)
                user_cache[transaction.user_id] = transaction_user
            else:
                transaction_user = user_cache[transaction.user_id]

            if transaction_user.subscription_type == SubscriptionType.FREE:
                free_users.add(transaction_user.id)
            elif transaction_user.subscription_type == SubscriptionType.MINI:
                mini_users.add(transaction_user.id)
            elif transaction_user.subscription_type == SubscriptionType.STANDARD:
                standard_users.add(transaction_user.id)
            elif transaction_user.subscription_type == SubscriptionType.VIP:
                vip_users.add(transaction_user.id)
            elif transaction_user.subscription_type == SubscriptionType.PREMIUM:
                premium_users.add(transaction_user.id)
            elif transaction_user.subscription_type == SubscriptionType.UNLIMITED:
                unlimited_users.add(transaction_user.id)
            activated_users.add(transaction.user_id)

            if transaction.type == TransactionType.INCOME:
                count_income_money_total += 1
                if transaction.currency == Currency.USD:
                    count_income_money[transaction.service] += transaction.clear_amount * 100
                    if transaction.service in service_subscriptions:
                        count_income_money['SUBSCRIPTION_ALL'] += transaction.clear_amount * 100
                    elif transaction.service in service_packages:
                        count_income_money['PACKAGES_ALL'] += transaction.clear_amount * 100
                    count_income_money['ALL'] += transaction.clear_amount * 100
                elif transaction.currency == Currency.RUB:
                    count_income_money[transaction.service] += transaction.clear_amount
                    if transaction.service in service_subscriptions:
                        count_income_money['SUBSCRIPTION_ALL'] += transaction.clear_amount
                    elif transaction.service in service_packages:
                        count_income_money['PACKAGES_ALL'] += transaction.clear_amount
                    count_income_money['ALL'] += transaction.clear_amount
                else:
                    count_income_money[transaction.service] += transaction.clear_amount * 2
                    if transaction.service in service_subscriptions:
                        count_income_money['SUBSCRIPTION_ALL'] += transaction.clear_amount * 2
                    elif transaction.service in service_packages:
                        count_income_money['PACKAGES_ALL'] += transaction.clear_amount * 2
                    count_income_money['ALL'] += transaction.clear_amount * 2

                count_all_transactions[transaction.service]['BONUS'] += 1 \
                    if transaction.details.get('is_bonus', False) \
                    else 0

                if transaction.clear_amount > 0:
                    paid_users.add(transaction.user_id)
            elif transaction.type == TransactionType.EXPENSE:
                count_all_transactions[transaction.service]['SUCCESS'] += transaction.quantity \
                    if not transaction.details.get('has_error', False) \
                    else 0
                count_all_transactions[transaction.service]['FAIL'] += transaction.quantity \
                    if transaction.details.get('has_error', False) \
                    else 0
                count_all_transactions[transaction.service]['EXAMPLE'] += transaction.quantity \
                    if transaction.details.get('is_suggestion', False) \
                    else 0
                count_all_transactions[transaction.service]['ALL'] += transaction.quantity

                count_expense_money[transaction.service]['AVERAGE_EXAMPLE_PRICE'] += transaction.amount \
                    if transaction.details.get('is_suggestion', False) \
                    else 0
                count_expense_money[transaction.service]['EXAMPLE_ALL'] += transaction.amount \
                    if transaction.details.get('is_suggestion', False) \
                    else 0
                count_expense_money[transaction.service]['AVERAGE_PRICE'] += transaction.amount \
                    if not transaction.details.get('is_suggestion', False) \
                    else 0
                count_expense_money[transaction.service]['ALL'] += transaction.amount
                count_expense_money['ALL'] += transaction.amount

                is_super_admin = transaction.user_id == config.SUPER_ADMIN_ID
                if transaction.user_id in free_users and not is_super_admin:
                    count_expense_money[SubscriptionType.FREE]['ALL'] += transaction.amount
                elif transaction.user_id in mini_users and not is_super_admin:
                    count_expense_money[SubscriptionType.MINI]['ALL'] += transaction.amount
                elif transaction.user_id in standard_users and not is_super_admin:
                    count_expense_money[SubscriptionType.STANDARD]['ALL'] += transaction.amount
                elif transaction.user_id in vip_users and not is_super_admin:
                    count_expense_money[SubscriptionType.VIP]['ALL'] += transaction.amount
                elif transaction.user_id in premium_users and not is_super_admin:
                    count_expense_money[SubscriptionType.PREMIUM]['ALL'] += transaction.amount
                elif transaction.user_id in unlimited_users and not is_super_admin:
                    count_expense_money[SubscriptionType.UNLIMITED]['ALL'] += transaction.amount

                if transaction.service == ServiceType.MIDJOURNEY:
                    midjourney_action = transaction.details.get('type', MidjourneyAction.PAYMENT)
                    count_midjourney_usage[midjourney_action] = count_midjourney_usage.get(
                        midjourney_action,
                        0,
                    ) + transaction.quantity

                if transaction.service == ServiceType.FACE_SWAP and transaction.quantity != 0:
                    face_swap_name = transaction.details.get('name', 'UNKNOWN')
                    face_swap_images = transaction.details.get('images', ['UNKNOWN'])
                    count_face_swap_usage[face_swap_name] = count_face_swap_usage.get(
                        face_swap_name,
                        0,
                    ) + len(face_swap_images)

                if transaction.service == ServiceType.PHOTOSHOP_AI:
                    photoshop_ai_action = transaction.details.get('type', 'UNKNOWN')
                    count_photoshop_ai_usage[photoshop_ai_action] = count_photoshop_ai_usage.get(
                        photoshop_ai_action,
                        0,
                    ) + transaction.quantity

                if transaction.service == ServiceType.SUNO:
                    suno_mode = transaction.details.get('mode', 'Payment')
                    count_suno_usage[suno_mode] = count_suno_usage.get(
                        suno_mode,
                        0,
                    ) + transaction.quantity

        if count < config.BATCH_SIZE:
            is_running = False
            break

        last_doc = doc

    for service in service_ai_models:
        successes = count_all_transactions[service]['SUCCESS']
        fails = count_all_transactions[service]['FAIL']
        examples = count_all_transactions[service]['EXAMPLE']
        total = successes + fails

        average_price = count_expense_money[service]['AVERAGE_PRICE']
        average_example_price = count_expense_money[service]['AVERAGE_EXAMPLE_PRICE']

        count_expense_money[service]['AVERAGE_PRICE'] = average_price / total \
            if total > 0 else 0
        count_expense_money[service]['AVERAGE_EXAMPLE_PRICE'] = average_example_price / examples \
            if examples > 0 else 0
    count_expense_money[SubscriptionType.FREE]['AVERAGE_PRICE'] = (
        count_expense_money[SubscriptionType.FREE]['ALL'] / len(free_users)
    ) if len(free_users) else 0
    count_expense_money[SubscriptionType.MINI]['AVERAGE_PRICE'] = (
        count_expense_money[SubscriptionType.MINI]['ALL'] / len(mini_users)
    ) if len(mini_users) else 0
    count_expense_money[SubscriptionType.STANDARD]['AVERAGE_PRICE'] = (
        count_expense_money[SubscriptionType.STANDARD]['ALL'] / len(standard_users)
    ) if len(standard_users) else 0
    count_expense_money[SubscriptionType.VIP]['AVERAGE_PRICE'] = (
        count_expense_money[SubscriptionType.VIP]['ALL'] / len(vip_users)
    ) if len(vip_users) else 0
    count_expense_money[SubscriptionType.PREMIUM]['AVERAGE_PRICE'] = (
        count_expense_money[SubscriptionType.PREMIUM]['ALL'] / len(premium_users)
    ) if len(premium_users) else 0
    count_expense_money[SubscriptionType.UNLIMITED]['AVERAGE_PRICE'] = (
        count_expense_money[SubscriptionType.UNLIMITED]['ALL'] / len(unlimited_users)
    ) if len(unlimited_users) else 0

    return (
        free_users,
        mini_users,
        standard_users,
        vip_users,
        premium_users,
        unlimited_users,
        paid_users,
        activated_users,
        count_all_transactions,
        count_income_money_total,
        count_income_money,
        count_expense_money,
        count_midjourney_usage,
        count_face_swap_usage,
        count_photoshop_ai_usage,
        count_suno_usage,
    )


async def handle_get_statistics(language_code: str, period: str):
    current_date = datetime.now(timezone.utc)
    start_date = None
    end_date = None
    start_date_before = None
    end_date_before = None
    if period == 'day':
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
        period = start_date.strftime('%d.%m.%Y')

        start_date_before = start_date - timedelta(days=1)
        end_date_before = end_date - timedelta(days=1)
    elif period == 'week':
        start_date = (current_date - timedelta(days=current_date.weekday() + 7)).replace(
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
        period = f'{start_date.strftime("%d.%m.%Y")}-{end_date.strftime("%d.%m.%Y")}'

        start_date_before = start_date - timedelta(days=7)
        end_date_before = end_date - timedelta(days=7)
    elif period == 'month':
        first_day_of_last_month = current_date.replace(day=1) - timedelta(days=1)
        start_date = first_day_of_last_month.replace(
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )

        last_day_of_last_month = start_date + timedelta(
            days=calendar.monthrange(start_date.year, start_date.month)[1] - 1,
        )
        end_date = last_day_of_last_month.replace(
            hour=23,
            minute=59,
            second=59,
            microsecond=999999,
        )
        period = f'{start_date.strftime("%d.%m.%Y")}-{end_date.strftime("%d.%m.%Y")}'

        start_date_before = start_date - timedelta(days=calendar.monthrange(start_date.year, start_date.month)[1] - 1)
        end_date_before = start_date - timedelta(days=1)
        end_date_before = end_date_before.replace(
            hour=23,
            minute=59,
            second=59,
            microsecond=999999,
        )
    else:
        period = 'всё время'

    # users
    (
        count_all_users,
        count_all_users_before,
        count_blocked_users,
        count_blocked_users_before,
        count_referred_users,
        count_referred_users_before,
        count_english_users,
        count_english_users_before,
        count_russian_users,
        count_russian_users_before,
    ) = await asyncio.gather(
        # count_all_users
        get_count_of_users(
            start_date=start_date,
            end_date=end_date,
        ),
        # count_all_users_before
        get_count_of_users(
            start_date=start_date_before,
            end_date=end_date_before,
        ) if start_date_before and end_date_before else get_zero(),
        # count_blocked_users
        get_count_of_users(
            start_date=start_date,
            end_date=end_date,
            is_blocked=True,
        ),
        # count_blocked_users_before
        get_count_of_users(
            start_date=start_date_before,
            end_date=end_date_before,
            is_blocked=True,
        ) if start_date_before and end_date_before else get_zero(),
        # count_referred_users
        get_count_of_users_referred_by(
            start_date=start_date,
            end_date=end_date,
        ),
        # count_referred_users_before
        get_count_of_users_referred_by(
            start_date=start_date_before,
            end_date=end_date_before,
        ) if start_date_before and end_date_before else get_zero(),
        # count_english_users
        get_count_of_users(
            start_date=start_date,
            end_date=end_date,
            language_code='en',
        ),
        # count_english_users_before
        get_count_of_users(
            start_date=start_date_before,
            end_date=end_date_before,
            language_code='en',
        ) if start_date_before and end_date_before else get_zero(),
        # count_russian_users
        get_count_of_users(
            start_date=start_date,
            end_date=end_date,
            language_code='ru',
        ),
        # count_russian_users_before
        get_count_of_users(
            start_date=start_date_before,
            end_date=end_date_before,
            language_code='ru',
        ) if start_date_before and end_date_before else get_zero(),
    )
    (
        count_other_users,
        count_other_users_before,
    ) = (
        count_all_users - (count_english_users + count_russian_users),
        count_all_users_before - (count_english_users_before + count_russian_users_before),
    )

    subscriptions = [value for key, value in vars(SubscriptionType).items() if not key.startswith('__')]
    count_subscription_users = {}
    count_subscription_users_before = {}
    subscription_tasks = [
        get_count_of_subscriptions(
            start_date=start_date,
            end_date=end_date,
            type=subscription,
            statuses=[SubscriptionStatus.ACTIVE, SubscriptionStatus.CANCELED],
        ) if start_date and end_date else get_count_of_users(
            subscription_type=subscription,
        ) for subscription in subscriptions
    ]
    subscription_before_tasks = [
        get_count_of_subscriptions(
            start_date=start_date_before,
            end_date=end_date_before,
            type=subscription,
            statuses=[SubscriptionStatus.ACTIVE, SubscriptionStatus.CANCELED],
        ) if start_date_before and end_date_before else get_zero() for subscription in subscriptions
    ]

    subscription_results, subscription_before_results = await asyncio.gather(
        asyncio.gather(*subscription_tasks),
        asyncio.gather(*subscription_before_tasks)
    )

    for subscription, count, count_before in zip(subscriptions, subscription_results, subscription_before_results):
        count_subscription_users[subscription] = count
        count_subscription_users_before[subscription] = count_before

    count_users = await get_count_of_users()
    count_subscription_users[SubscriptionType.FREE] = abs(
        count_users - sum(count_subscription_users.values())
    ) if count_subscription_users[SubscriptionType.FREE] == 0 \
        else count_subscription_users[SubscriptionType.FREE]
    count_subscription_users_before[SubscriptionType.FREE] = abs(
        count_users - sum(count_subscription_users_before.values())
    ) if count_subscription_users_before[SubscriptionType.FREE] == 0 \
        else count_subscription_users_before[SubscriptionType.FREE]

    # reactions
    default_reactions_nested_dict = {
        GenerationReaction.LIKED: 0,
        GenerationReaction.DISLIKED: 0,
        GenerationReaction.NONE: 0,
    }
    count_reactions = {
        value: default_reactions_nested_dict.copy() for key, value in vars(ServiceType).items()
        if not key.startswith('__') and value in {
            ServiceType.MIDJOURNEY,
            ServiceType.STABLE_DIFFUSION,
            ServiceType.FACE_SWAP,
            ServiceType.PHOTOSHOP_AI,
            ServiceType.MUSIC_GEN,
            ServiceType.SUNO,
        }
    }
    count_reactions_before = {
        value: default_reactions_nested_dict.copy() for key, value in vars(ServiceType).items()
        if not key.startswith('__') and value in {
            ServiceType.MIDJOURNEY,
            ServiceType.STABLE_DIFFUSION,
            ServiceType.FACE_SWAP,
            ServiceType.PHOTOSHOP_AI,
            ServiceType.MUSIC_GEN,
            ServiceType.SUNO,
        }
    }

    for generation_reaction in [GenerationReaction.LIKED, GenerationReaction.DISLIKED, GenerationReaction.NONE]:
        (
            count_reactions[ServiceType.MIDJOURNEY][generation_reaction],
            count_reactions_before[ServiceType.MIDJOURNEY][generation_reaction],
            count_reactions[ServiceType.STABLE_DIFFUSION][generation_reaction],
            count_reactions_before[ServiceType.STABLE_DIFFUSION][generation_reaction],
            count_reactions[ServiceType.FACE_SWAP][generation_reaction],
            count_reactions_before[ServiceType.FACE_SWAP][generation_reaction],
            count_reactions[ServiceType.PHOTOSHOP_AI][generation_reaction],
            count_reactions_before[ServiceType.PHOTOSHOP_AI][generation_reaction],
            count_reactions[ServiceType.MUSIC_GEN][generation_reaction],
            count_reactions_before[ServiceType.MUSIC_GEN][generation_reaction],
            count_reactions[ServiceType.SUNO][generation_reaction],
            count_reactions_before[ServiceType.SUNO][generation_reaction],
        ) = await asyncio.gather(
            get_count_of_generations(
                start_date=start_date,
                end_date=end_date,
                reaction=generation_reaction,
                model=Model.MIDJOURNEY,
                action=MidjourneyAction.UPSCALE,
            ),
            get_count_of_generations(
                start_date=start_date_before,
                end_date=end_date_before,
                reaction=generation_reaction,
                model=Model.MIDJOURNEY,
                action=MidjourneyAction.UPSCALE,
            ) if start_date_before and end_date_before else get_zero(),
            get_count_of_generations(
                start_date=start_date,
                end_date=end_date,
                reaction=generation_reaction,
                model=Model.STABLE_DIFFUSION,
            ),
            get_count_of_generations(
                start_date=start_date_before,
                end_date=end_date_before,
                reaction=generation_reaction,
                model=Model.STABLE_DIFFUSION,
            ) if start_date_before and end_date_before else get_zero(),
            get_count_of_generations(
                start_date=start_date,
                end_date=end_date,
                reaction=generation_reaction,
                model=Model.FACE_SWAP,
            ),
            get_count_of_generations(
                start_date=start_date_before,
                end_date=end_date_before,
                reaction=generation_reaction,
                model=Model.FACE_SWAP,
            ) if start_date_before and end_date_before else get_zero(),
            get_count_of_generations(
                start_date=start_date,
                end_date=end_date,
                reaction=generation_reaction,
                model=Model.PHOTOSHOP_AI,
            ),
            get_count_of_generations(
                start_date=start_date_before,
                end_date=end_date_before,
                reaction=generation_reaction,
                model=Model.PHOTOSHOP_AI,
            ) if start_date_before and end_date_before else get_zero(),
            get_count_of_generations(
                start_date=start_date,
                end_date=end_date,
                reaction=generation_reaction,
                model=Model.MUSIC_GEN,
            ),
            get_count_of_generations(
                start_date=start_date_before,
                end_date=end_date_before,
                reaction=generation_reaction,
                model=Model.MUSIC_GEN,
            ) if start_date_before and end_date_before else get_zero(),
            get_count_of_generations(
                start_date=start_date,
                end_date=end_date,
                reaction=generation_reaction,
                model=Model.SUNO,
            ),
            get_count_of_generations(
                start_date=start_date_before,
                end_date=end_date_before,
                reaction=generation_reaction,
                model=Model.SUNO,
            ) if start_date_before and end_date_before else get_zero(),
        )

    # transactions
    (
        free_users,
        mini_users,
        standard_users,
        vip_users,
        premium_users,
        unlimited_users,
        paid_users,
        activated_users,
        count_all_transactions,
        count_income_money_total,
        count_income_money,
        count_expense_money,
        count_midjourney_usage,
        count_face_swap_usage,
        count_photoshop_ai_usage,
        count_suno_usage,
    ) = await get_statistics_by_transactions_query(
        start_date=start_date,
        end_date=end_date,
    )
    (
        free_users_before,
        mini_users_before,
        standard_users_before,
        vip_users_before,
        premium_users_before,
        unlimited_users_before,
        paid_users_before,
        activated_users_before,
        count_all_transactions_before,
        count_income_money_total_before,
        count_income_money_before,
        count_expense_money_before,
        count_midjourney_usage_before,
        count_face_swap_usage_before,
        count_photoshop_ai_usage_before,
        count_suno_usage_before,
    ) = await get_statistics_by_transactions_query(
        start_date=start_date_before,
        end_date=end_date_before,
    )

    count_activated_users = len(activated_users)
    count_activated_users_before = len(activated_users_before)
    count_paid_users = len(paid_users)
    count_paid_users_before = len(paid_users_before)

    count_games = {
        value: 0 for key, value in vars(GameType).items()
        if not key.startswith('__')
    }
    count_games_before = {
        value: 0 for key, value in vars(GameType).items()
        if not key.startswith('__')
    }

    (
        count_games_reward,
        count_games_reward_before,
        count_games[GameType.BOWLING],
        count_games_before[GameType.BOWLING],
        count_games[GameType.SOCCER],
        count_games_before[GameType.SOCCER],
        count_games[GameType.BASKETBALL],
        count_games_before[GameType.BASKETBALL],
        count_games[GameType.DARTS],
        count_games_before[GameType.DARTS],
        count_games[GameType.DICE],
        count_games_before[GameType.DICE],
        count_games[GameType.CASINO],
        count_games_before[GameType.CASINO],
    ) = await asyncio.gather(
        get_sum_of_games_reward(
            start_date=start_date,
            end_date=end_date,
        ),
        get_sum_of_games_reward(
            start_date=start_date_before,
            end_date=end_date_before,
        ) if start_date_before and end_date_before else get_zero(),
        get_count_of_games(
            start_date=start_date,
            end_date=end_date,
            type=GameType.BOWLING,
        ),
        get_count_of_games(
            start_date=start_date_before,
            end_date=end_date_before,
            type=GameType.BOWLING,
        ) if start_date_before and end_date_before else get_zero(),
        get_count_of_games(
            start_date=start_date,
            end_date=end_date,
            type=GameType.SOCCER,
        ),
        get_count_of_games(
            start_date=start_date_before,
            end_date=end_date_before,
            type=GameType.SOCCER,
        ) if start_date_before and end_date_before else get_zero(),
        get_count_of_games(
            start_date=start_date,
            end_date=end_date,
            type=GameType.BASKETBALL,
        ),
        get_count_of_games(
            start_date=start_date_before,
            end_date=end_date_before,
            type=GameType.BASKETBALL,
        ) if start_date_before and end_date_before else get_zero(),
        get_count_of_games(
            start_date=start_date,
            end_date=end_date,
            type=GameType.DARTS,
        ),
        get_count_of_games(
            start_date=start_date_before,
            end_date=end_date_before,
            type=GameType.DARTS,
        ) if start_date_before and end_date_before else get_zero(),
        get_count_of_games(
            start_date=start_date,
            end_date=end_date,
            type=GameType.DICE,
        ),
        get_count_of_games(
            start_date=start_date_before,
            end_date=end_date_before,
            type=GameType.DICE,
        ) if start_date_before and end_date_before else get_zero(),
        get_count_of_games(
            start_date=start_date,
            end_date=end_date,
            type=GameType.CASINO,
        ),
        get_count_of_games(
            start_date=start_date_before,
            end_date=end_date_before,
            type=GameType.CASINO,
        ) if start_date_before and end_date_before else get_zero(),
    )

    count_activated_promo_codes = await get_count_of_used_promo_codes(start_date, end_date)
    count_activated_promo_codes_before = await get_count_of_used_promo_codes(start_date_before, end_date_before) \
        if start_date_before and end_date_before \
        else []

    # feedbacks
    all_feedbacks = await get_count_of_feedbacks(start_date, end_date)
    all_feedbacks_before = await get_count_of_feedbacks(start_date_before, end_date_before) \
        if start_date_before and end_date_before \
        else 0
    approved_feedbacks = await get_count_of_feedbacks(start_date, end_date, FeedbackStatus.APPROVED)
    approved_feedbacks_before = await get_count_of_feedbacks(
        start_date_before,
        end_date_before,
        FeedbackStatus.APPROVED
    ) if start_date_before and end_date_before else 0
    denied_feedbacks = await get_count_of_feedbacks(start_date, end_date, FeedbackStatus.DENIED)
    denied_feedbacks_before = await get_count_of_feedbacks(
        start_date_before,
        end_date_before,
        FeedbackStatus.DENIED
    ) if start_date_before and end_date_before else 0
    count_feedbacks = {
        FeedbackStatus.APPROVED: approved_feedbacks,
        FeedbackStatus.DENIED: denied_feedbacks,
        FeedbackStatus.WAITING: all_feedbacks - (approved_feedbacks + denied_feedbacks)
    }
    count_feedbacks_before = {
        FeedbackStatus.APPROVED: approved_feedbacks_before,
        FeedbackStatus.DENIED: denied_feedbacks_before,
        FeedbackStatus.WAITING: all_feedbacks_before - (approved_feedbacks_before + denied_feedbacks_before)
    }

    # credits
    count_credits = {
        'INVITE_FRIENDS': 0,
        'LEAVE_FEEDBACKS': 0,
        'PLAY_GAMES': 0,
        'ALL': 0,
    }
    count_credits_before = {
        'INVITE_FRIENDS': 0,
        'LEAVE_FEEDBACKS': 0,
        'PLAY_GAMES': 0,
        'ALL': 0,
    }
    count_credits['INVITE_FRIENDS'] = 50 * count_referred_users
    count_credits_before['INVITE_FRIENDS'] = 50 * count_referred_users_before
    count_credits['LEAVE_FEEDBACKS'] = 25 * approved_feedbacks
    count_credits_before['LEAVE_FEEDBACKS'] = 25 * approved_feedbacks_before
    count_credits['PLAY_GAMES'] = count_games_reward
    count_credits_before['PLAY_GAMES'] = count_games_reward_before
    count_credits['ALL'] = (
        count_credits['INVITE_FRIENDS'] +
        count_credits['LEAVE_FEEDBACKS'] +
        count_credits['PLAY_GAMES']
    )
    count_credits_before['ALL'] = (
        count_credits_before['INVITE_FRIENDS'] +
        count_credits_before['LEAVE_FEEDBACKS'] +
        count_credits_before['PLAY_GAMES']
    )

    count_income_money['AVERAGE_PRICE'] = (
        count_income_money['ALL'] / count_income_money_total
    ) if count_income_money_total else 0
    count_income_money_before['AVERAGE_PRICE'] = (
        count_income_money_before['ALL'] / count_income_money_total_before
    ) if count_income_money_total_before else 0
    count_income_money['VAL'] = count_income_money['ALL'] - count_expense_money['ALL'] * 100
    count_income_money_before['VAL'] = count_income_money_before['ALL'] - count_expense_money_before['ALL'] * 100

    count_midjourney_usage['ALL'] = sum(count_midjourney_usage.values())
    count_face_swap_usage['ALL'] = sum(count_face_swap_usage.values())
    count_photoshop_ai_usage['ALL'] = sum(count_photoshop_ai_usage.values())
    count_suno_usage['ALL'] = sum(count_suno_usage.values())

    texts = {
        'users': get_localization(language_code).statistics_users(
            period=period,
            count_all_users=count_all_users,
            count_all_users_before=count_all_users_before,
            count_activated_users=count_activated_users,
            count_activated_users_before=count_activated_users_before,
            count_referral_users=count_referred_users,
            count_referral_users_before=count_activated_users_before,
            count_english_users=count_english_users,
            count_english_users_before=count_english_users_before,
            count_russian_users=count_russian_users,
            count_russian_users_before=count_russian_users_before,
            count_other_users=count_other_users,
            count_other_users_before=count_other_users_before,
            count_paid_users=count_paid_users,
            count_paid_users_before=count_paid_users_before,
            count_blocked_users=count_blocked_users,
            count_blocked_users_before=count_blocked_users_before,
            count_subscription_users=count_subscription_users,
            count_subscription_users_before=count_subscription_users_before,
        ),
        'text_models': get_localization(language_code).statistics_text_models(
            period=period,
            count_all_transactions=count_all_transactions,
            count_all_transactions_before=count_all_transactions_before,
        ),
        'image_models': get_localization(language_code).statistics_image_models(
            period=period,
            count_all_transactions=count_all_transactions,
            count_all_transactions_before=count_all_transactions_before,
            count_midjourney_usage=count_midjourney_usage,
            count_face_swap_usage=count_face_swap_usage,
            count_photoshop_ai_usage=count_photoshop_ai_usage,
        ),
        'music_models': get_localization(language_code).statistics_music_models(
            period=period,
            count_all_transactions=count_all_transactions,
            count_all_transactions_before=count_all_transactions_before,
            count_suno_usage=count_suno_usage,
        ),
        'reactions': get_localization(language_code).statistics_reactions(
            period=period,
            count_reactions=count_reactions,
            count_reactions_before=count_reactions_before,
            count_feedbacks=count_feedbacks,
            count_feedbacks_before=count_feedbacks_before,
            count_games=count_games,
            count_games_before=count_games_before,
        ),
        'bonuses': get_localization(language_code).statistics_bonuses(
            period=period,
            count_credits=count_credits,
            count_credits_before=count_credits_before,
            count_all_transactions=count_all_transactions,
            count_all_transactions_before=count_all_transactions_before,
            count_activated_promo_codes=count_activated_promo_codes,
            count_activated_promo_codes_before=count_activated_promo_codes_before,
        ),
        'expenses': get_localization(language_code).statistics_expenses(
            period=period,
            count_expense_money=count_expense_money,
            count_expense_money_before=count_expense_money_before,
        ),
        'incomes': get_localization(language_code).statistics_incomes(
            period=period,
            count_income_money=count_income_money,
            count_income_money_before=count_income_money_before,
        ),
    }

    return texts


@statistics_router.callback_query(lambda c: c.data.startswith('statistics:'))
async def handle_statistics_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_language_code = await get_user_language(str(callback_query.from_user.id), state.storage)

    period = callback_query.data.split(':')[1]
    if period == 'back':
        reply_markup = build_admin_keyboard(user_language_code)
        await callback_query.message.edit_text(
            text=get_localization(user_language_code).ADMIN_INFO,
            reply_markup=reply_markup,
        )

        return
    elif period == 'write_transaction':
        await handle_write_transaction(callback_query, user_language_code)
        return

    processing_message = await callback_query.message.reply(
        text=get_localization(user_language_code).processing_statistics(),
        allow_sending_without_reply=True,
    )

    async with ChatActionSender.typing(bot=callback_query.bot, chat_id=callback_query.message.chat.id):
        texts = await handle_get_statistics(user_language_code, period)
        for text in texts.values():
            await callback_query.message.answer(
                text=text,
                protect_content=True,
            )

    await processing_message.delete()


@statistics_router.callback_query(lambda c: c.data.startswith('statistics_write_transaction:'))
async def handle_statistics_write_transaction_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    transaction_type = callback_query.data.split(':')[1]
    if transaction_type == 'back':
        await handle_statistics(
            callback_query.message,
            str(callback_query.from_user.id),
            state,
        )
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
            allow_sending_without_reply=True,
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
            allow_sending_without_reply=True,
        )


@statistics_router.message(Statistics.waiting_for_statistics_service_date, ~F.text.startswith('/'))
async def statistics_service_date_sent(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    user_language_code = await get_user_language(user_id, state.storage)

    try:
        user_data = await state.get_data()
        service_date = datetime.strptime(message.text, '%d.%m.%Y')
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
            clear_amount=service_amount,
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
            allow_sending_without_reply=True,
        )
