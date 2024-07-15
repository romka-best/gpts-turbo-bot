import calendar
from datetime import datetime, timezone, timedelta

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.chat_action import ChatActionSender

from bot.database.models.common import Model, MidjourneyAction, SunoMode, Currency
from bot.database.models.generation import GenerationReaction
from bot.database.models.subscription import SubscriptionType
from bot.database.models.transaction import TransactionType, ServiceType
from bot.database.operations.chat.getters import get_chats
from bot.database.operations.feedback.getters import get_feedbacks
from bot.database.operations.generation.getters import get_generations
from bot.database.operations.promo_code.getters import get_used_promo_codes
from bot.database.operations.transaction.getters import get_transactions
from bot.database.operations.transaction.writers import write_transaction
from bot.database.operations.user.getters import get_users, get_user
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


async def handle_get_statistics(language_code: str, period: str):
    current_date = datetime.now(timezone.utc)
    start_date = None
    end_date = None
    start_date_before = None
    end_date_before = None
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

        start_date_before = start_date - timedelta(days=1)
        end_date_before = end_date - timedelta(days=1)
    elif period == "week":
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
        period = f"{start_date.strftime('%d.%m.%Y')}-{end_date.strftime('%d.%m.%Y')}"

        start_date_before = start_date - timedelta(days=7)
        end_date_before = end_date - timedelta(days=7)
    elif period == "month":
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
        period = f"{start_date.strftime('%d.%m.%Y')}-{end_date.strftime('%d.%m.%Y')}"

        start_date_before = start_date - timedelta(days=calendar.monthrange(start_date.year, start_date.month)[1] - 1)
        end_date_before = start_date - timedelta(days=1)
        end_date_before = end_date_before.replace(
            hour=23,
            minute=59,
            second=59,
            microsecond=999999,
        )
    else:
        period = "всё время"

    users = await get_users(start_date, end_date)
    users_before = await get_users(start_date_before, end_date_before) \
        if start_date_before and end_date_before \
        else []

    transactions = await get_transactions(start_date, end_date)
    transactions_before = await get_transactions(start_date_before, end_date_before) \
        if start_date_before and end_date_before \
        else []

    generations = await get_generations(start_date, end_date)
    generations_before = await get_generations(start_date_before, end_date_before) \
        if start_date_before and end_date_before \
        else []

    chats = await get_chats(start_date, end_date)
    chats_before = await get_chats(start_date_before, end_date_before) \
        if start_date_before and end_date_before \
        else []

    feedbacks = await get_feedbacks(start_date, end_date)
    feedbacks_before = await get_feedbacks(start_date_before, end_date_before) \
        if start_date_before and end_date_before \
        else []

    used_promo_codes = await get_used_promo_codes(start_date, end_date)
    used_promo_codes_before = await get_used_promo_codes(start_date_before, end_date_before) \
        if start_date_before and end_date_before \
        else []

    free_users = set()
    free_users_before = set()
    standard_users = set()
    standard_users_before = set()
    vip_users = set()
    vip_users_before = set()
    premium_users = set()
    premium_users_before = set()
    paid_users = set()
    paid_users_before = set()
    activated_users = set()
    activated_users_before = set()
    referral_users = set()
    referral_users_before = set()
    english_users = set()
    english_users_before = set()
    russian_users = set()
    russian_users_before = set()
    other_users = set()
    other_users_before = set()
    count_subscription_users = {
        SubscriptionType.FREE: 0,
        SubscriptionType.STANDARD: 0,
        SubscriptionType.VIP: 0,
        SubscriptionType.PREMIUM: 0,
    }
    count_subscription_users_before = {
        SubscriptionType.FREE: 0,
        SubscriptionType.STANDARD: 0,
        SubscriptionType.VIP: 0,
        SubscriptionType.PREMIUM: 0,
    }
    count_blocked_users = 0
    count_blocked_users_before = 0
    count_banned_users = 0
    count_banned_users_before = 0
    for user in users:
        count_subscription_users[user.subscription_type] += 1

        if user.is_blocked:
            count_blocked_users += 1
        if user.is_banned:
            count_banned_users += 1
        if user.referred_by:
            referral_users.add(user.id)

        if user.language_code == 'en':
            english_users.add(user.id)
        elif user.language_code == 'ru':
            russian_users.add(user.id)
        else:
            other_users.add(user.id)
    for user_before in users_before:
        count_subscription_users_before[user_before.subscription_type] += 1

        if user_before.is_blocked:
            count_blocked_users_before += 1
        if user_before.is_banned:
            count_banned_users_before += 1
        if user_before.referred_by:
            referral_users_before.add(user_before.id)

        if user_before.language_code == 'en':
            english_users_before.add(user_before.id)
        elif user_before.language_code == 'ru':
            russian_users_before.add(user_before.id)
        else:
            other_users_before.add(user_before.id)

    count_all_transactions = {
        ServiceType.CHAT_GPT3_TURBO: {
            'SUCCESS': 0,
            'FAIL': 0,
            'EXAMPLE': 0,
            'ALL': 0,
            'BONUS': 0,
        },
        ServiceType.CHAT_GPT4_TURBO: {
            'SUCCESS': 0,
            'FAIL': 0,
            'EXAMPLE': 0,
            'ALL': 0,
            'BONUS': 0,
        },
        ServiceType.CHAT_GPT4_OMNI: {
            'SUCCESS': 0,
            'FAIL': 0,
            'EXAMPLE': 0,
            'ALL': 0,
            'BONUS': 0,
        },
        ServiceType.CLAUDE_3_SONNET: {
            'SUCCESS': 0,
            'FAIL': 0,
            'EXAMPLE': 0,
            'ALL': 0,
            'BONUS': 0,
        },
        ServiceType.CLAUDE_3_OPUS: {
            'SUCCESS': 0,
            'FAIL': 0,
            'EXAMPLE': 0,
            'ALL': 0,
            'BONUS': 0,
        },
        ServiceType.DALL_E: {
            'SUCCESS': 0,
            'FAIL': 0,
            'EXAMPLE': 0,
            'ALL': 0,
            'BONUS': 0,
        },
        ServiceType.MIDJOURNEY: {
            'SUCCESS': 0,
            'FAIL': 0,
            'EXAMPLE': 0,
            'ALL': 0,
            'BONUS': 0,
        },
        ServiceType.FACE_SWAP: {
            'SUCCESS': 0,
            'FAIL': 0,
            'EXAMPLE': 0,
            'ALL': 0,
            'BONUS': 0,
        },
        ServiceType.MUSIC_GEN: {
            'SUCCESS': 0,
            'FAIL': 0,
            'EXAMPLE': 0,
            'ALL': 0,
            'BONUS': 0,
        },
        ServiceType.SUNO: {
            'SUCCESS': 0,
            'FAIL': 0,
            'EXAMPLE': 0,
            'ALL': 0,
            'BONUS': 0,
        },
        ServiceType.ADDITIONAL_CHATS: {
            'SUCCESS': 0,
            'FAIL': 0,
            'EXAMPLE': 0,
            'ALL': 0,
            'BONUS': 0,
        },
        ServiceType.ACCESS_TO_CATALOG: {
            'SUCCESS': 0,
            'FAIL': 0,
            'EXAMPLE': 0,
            'ALL': 0,
            'BONUS': 0,
        },
        ServiceType.VOICE_MESSAGES: {
            'SUCCESS': 0,
            'FAIL': 0,
            'EXAMPLE': 0,
            'ALL': 0,
            'BONUS': 0,
        },
        ServiceType.FAST_MESSAGES: {
            'SUCCESS': 0,
            'FAIL': 0,
            'EXAMPLE': 0,
            'ALL': 0,
            'BONUS': 0,
        },
        ServiceType.SERVER: {
            'SUCCESS': 0,
            'FAIL': 0,
            'EXAMPLE': 0,
            'ALL': 0,
            'BONUS': 0,
        },
        ServiceType.DATABASE: {
            'SUCCESS': 0,
            'FAIL': 0,
            'EXAMPLE': 0,
            'ALL': 0,
            'BONUS': 0,
        },
        ServiceType.STANDARD: {
            'SUCCESS': 0,
            'FAIL': 0,
            'EXAMPLE': 0,
            'ALL': 0,
            'BONUS': 0,
        },
        ServiceType.VIP: {
            'SUCCESS': 0,
            'FAIL': 0,
            'EXAMPLE': 0,
            'ALL': 0,
            'BONUS': 0,
        },
        ServiceType.PREMIUM: {
            'SUCCESS': 0,
            'FAIL': 0,
            'EXAMPLE': 0,
            'ALL': 0,
            'BONUS': 0,
        },
        ServiceType.OTHER: {
            'SUCCESS': 0,
            'FAIL': 0,
            'EXAMPLE': 0,
            'ALL': 0,
            'BONUS': 0,
        },
    }
    count_all_transactions_before = {
        ServiceType.CHAT_GPT3_TURBO: {
            'SUCCESS': 0,
            'FAIL': 0,
            'EXAMPLE': 0,
            'ALL': 0,
            'BONUS': 0,
        },
        ServiceType.CHAT_GPT4_TURBO: {
            'SUCCESS': 0,
            'FAIL': 0,
            'EXAMPLE': 0,
            'ALL': 0,
            'BONUS': 0,
        },
        ServiceType.CHAT_GPT4_OMNI: {
            'SUCCESS': 0,
            'FAIL': 0,
            'EXAMPLE': 0,
            'ALL': 0,
            'BONUS': 0,
        },
        ServiceType.CLAUDE_3_SONNET: {
            'SUCCESS': 0,
            'FAIL': 0,
            'EXAMPLE': 0,
            'ALL': 0,
            'BONUS': 0,
        },
        ServiceType.CLAUDE_3_OPUS: {
            'SUCCESS': 0,
            'FAIL': 0,
            'EXAMPLE': 0,
            'ALL': 0,
            'BONUS': 0,
        },
        ServiceType.DALL_E: {
            'SUCCESS': 0,
            'FAIL': 0,
            'EXAMPLE': 0,
            'ALL': 0,
            'BONUS': 0,
        },
        ServiceType.MIDJOURNEY: {
            'SUCCESS': 0,
            'FAIL': 0,
            'EXAMPLE': 0,
            'ALL': 0,
            'BONUS': 0,
        },
        ServiceType.FACE_SWAP: {
            'SUCCESS': 0,
            'FAIL': 0,
            'EXAMPLE': 0,
            'ALL': 0,
            'BONUS': 0,
        },
        ServiceType.MUSIC_GEN: {
            'SUCCESS': 0,
            'FAIL': 0,
            'EXAMPLE': 0,
            'ALL': 0,
            'BONUS': 0,
        },
        ServiceType.SUNO: {
            'SUCCESS': 0,
            'FAIL': 0,
            'EXAMPLE': 0,
            'ALL': 0,
            'BONUS': 0,
        },
        ServiceType.ADDITIONAL_CHATS: {
            'SUCCESS': 0,
            'FAIL': 0,
            'EXAMPLE': 0,
            'ALL': 0,
            'BONUS': 0,
        },
        ServiceType.ACCESS_TO_CATALOG: {
            'SUCCESS': 0,
            'FAIL': 0,
            'EXAMPLE': 0,
            'ALL': 0,
            'BONUS': 0,
        },
        ServiceType.VOICE_MESSAGES: {
            'SUCCESS': 0,
            'FAIL': 0,
            'EXAMPLE': 0,
            'ALL': 0,
            'BONUS': 0,
        },
        ServiceType.FAST_MESSAGES: {
            'SUCCESS': 0,
            'FAIL': 0,
            'EXAMPLE': 0,
            'ALL': 0,
            'BONUS': 0,
        },
        ServiceType.SERVER: {
            'SUCCESS': 0,
            'FAIL': 0,
            'EXAMPLE': 0,
            'ALL': 0,
            'BONUS': 0,
        },
        ServiceType.DATABASE: {
            'SUCCESS': 0,
            'FAIL': 0,
            'EXAMPLE': 0,
            'ALL': 0,
            'BONUS': 0,
        },
        ServiceType.STANDARD: {
            'SUCCESS': 0,
            'FAIL': 0,
            'EXAMPLE': 0,
            'ALL': 0,
            'BONUS': 0,
        },
        ServiceType.VIP: {
            'SUCCESS': 0,
            'FAIL': 0,
            'EXAMPLE': 0,
            'ALL': 0,
            'BONUS': 0,
        },
        ServiceType.PREMIUM: {
            'SUCCESS': 0,
            'FAIL': 0,
            'EXAMPLE': 0,
            'ALL': 0,
            'BONUS': 0,
        },
        ServiceType.OTHER: {
            'SUCCESS': 0,
            'FAIL': 0,
            'EXAMPLE': 0,
            'ALL': 0,
            'BONUS': 0,
        },
    }

    count_income_money = {
        ServiceType.CHAT_GPT3_TURBO: 0,
        ServiceType.CHAT_GPT4_TURBO: 0,
        ServiceType.CHAT_GPT4_OMNI: 0,
        ServiceType.CLAUDE_3_SONNET: 0,
        ServiceType.CLAUDE_3_OPUS: 0,
        ServiceType.DALL_E: 0,
        ServiceType.MIDJOURNEY: 0,
        ServiceType.FACE_SWAP: 0,
        ServiceType.MUSIC_GEN: 0,
        ServiceType.SUNO: 0,
        ServiceType.ADDITIONAL_CHATS: 0,
        ServiceType.ACCESS_TO_CATALOG: 0,
        ServiceType.VOICE_MESSAGES: 0,
        ServiceType.FAST_MESSAGES: 0,
        ServiceType.STANDARD: 0,
        ServiceType.VIP: 0,
        ServiceType.PREMIUM: 0,
        'SUBSCRIPTION_ALL': 0,
        'PACKAGES_ALL': 0,
        'AVERAGE_PRICE': 0,
        'ALL': 0,
        'VAL': 0,
    }
    count_income_money_before = {
        ServiceType.CHAT_GPT3_TURBO: 0,
        ServiceType.CHAT_GPT4_TURBO: 0,
        ServiceType.CHAT_GPT4_OMNI: 0,
        ServiceType.CLAUDE_3_SONNET: 0,
        ServiceType.CLAUDE_3_OPUS: 0,
        ServiceType.DALL_E: 0,
        ServiceType.MIDJOURNEY: 0,
        ServiceType.FACE_SWAP: 0,
        ServiceType.MUSIC_GEN: 0,
        ServiceType.SUNO: 0,
        ServiceType.ADDITIONAL_CHATS: 0,
        ServiceType.ACCESS_TO_CATALOG: 0,
        ServiceType.VOICE_MESSAGES: 0,
        ServiceType.FAST_MESSAGES: 0,
        ServiceType.STANDARD: 0,
        ServiceType.VIP: 0,
        ServiceType.PREMIUM: 0,
        'SUBSCRIPTION_ALL': 0,
        'PACKAGES_ALL': 0,
        'AVERAGE_PRICE': 0,
        'ALL': 0,
        'VAL': 0,
    }
    count_income_money_total = 0
    count_income_money_before_total = 0
    count_expense_money = {
        ServiceType.CHAT_GPT3_TURBO: {
            'AVERAGE_EXAMPLE_PRICE': 0,
            'EXAMPLE_ALL': 0,
            'AVERAGE_PRICE': 0,
            'ALL': 0,
        },
        ServiceType.CHAT_GPT4_TURBO: {
            'AVERAGE_EXAMPLE_PRICE': 0,
            'EXAMPLE_ALL': 0,
            'AVERAGE_PRICE': 0,
            'ALL': 0,
        },
        ServiceType.CHAT_GPT4_OMNI: {
            'AVERAGE_EXAMPLE_PRICE': 0,
            'EXAMPLE_ALL': 0,
            'AVERAGE_PRICE': 0,
            'ALL': 0,
        },
        ServiceType.CLAUDE_3_SONNET: {
            'AVERAGE_EXAMPLE_PRICE': 0,
            'EXAMPLE_ALL': 0,
            'AVERAGE_PRICE': 0,
            'ALL': 0,
        },
        ServiceType.CLAUDE_3_OPUS: {
            'AVERAGE_EXAMPLE_PRICE': 0,
            'EXAMPLE_ALL': 0,
            'AVERAGE_PRICE': 0,
            'ALL': 0,
        },
        ServiceType.DALL_E: {
            'AVERAGE_EXAMPLE_PRICE': 0,
            'EXAMPLE_ALL': 0,
            'AVERAGE_PRICE': 0,
            'ALL': 0,
        },
        ServiceType.MIDJOURNEY: {
            'AVERAGE_EXAMPLE_PRICE': 0,
            'EXAMPLE_ALL': 0,
            'AVERAGE_PRICE': 0,
            'ALL': 0,
        },
        ServiceType.FACE_SWAP: {
            'AVERAGE_EXAMPLE_PRICE': 0,
            'EXAMPLE_ALL': 0,
            'AVERAGE_PRICE': 0,
            'ALL': 0,
        },
        ServiceType.MUSIC_GEN: {
            'AVERAGE_EXAMPLE_PRICE': 0,
            'EXAMPLE_ALL': 0,
            'AVERAGE_PRICE': 0,
            'ALL': 0,
        },
        ServiceType.SUNO: {
            'AVERAGE_EXAMPLE_PRICE': 0,
            'EXAMPLE_ALL': 0,
            'AVERAGE_PRICE': 0,
            'ALL': 0,
        },
        ServiceType.VOICE_MESSAGES: {
            'AVERAGE_EXAMPLE_PRICE': 0,
            'EXAMPLE_ALL': 0,
            'AVERAGE_PRICE': 0,
            'ALL': 0,
        },
        ServiceType.SERVER: {
            'AVERAGE_EXAMPLE_PRICE': 0,
            'EXAMPLE_ALL': 0,
            'AVERAGE_PRICE': 0,
            'ALL': 0,
        },
        ServiceType.DATABASE: {
            'AVERAGE_EXAMPLE_PRICE': 0,
            'EXAMPLE_ALL': 0,
            'AVERAGE_PRICE': 0,
            'ALL': 0,
        },
        ServiceType.OTHER: {
            'AVERAGE_EXAMPLE_PRICE': 0,
            'EXAMPLE_ALL': 0,
            'AVERAGE_PRICE': 0,
            'ALL': 0,
        },
        SubscriptionType.FREE: {
            'AVERAGE_EXAMPLE_PRICE': 0,
            'EXAMPLE_ALL': 0,
            'AVERAGE_PRICE': 0,
            'ALL': 0,
        },
        SubscriptionType.STANDARD: {
            'AVERAGE_EXAMPLE_PRICE': 0,
            'EXAMPLE_ALL': 0,
            'AVERAGE_PRICE': 0,
            'ALL': 0,
        },
        SubscriptionType.VIP: {
            'AVERAGE_EXAMPLE_PRICE': 0,
            'EXAMPLE_ALL': 0,
            'AVERAGE_PRICE': 0,
            'ALL': 0,
        },
        SubscriptionType.PREMIUM: {
            'AVERAGE_EXAMPLE_PRICE': 0,
            'EXAMPLE_ALL': 0,
            'AVERAGE_PRICE': 0,
            'ALL': 0,
        },
        'ALL': 0,
    }
    count_expense_money_before = {
        ServiceType.CHAT_GPT3_TURBO: {
            'AVERAGE_EXAMPLE_PRICE': 0,
            'EXAMPLE_ALL': 0,
            'AVERAGE_PRICE': 0,
            'ALL': 0,
        },
        ServiceType.CHAT_GPT4_TURBO: {
            'AVERAGE_EXAMPLE_PRICE': 0,
            'EXAMPLE_ALL': 0,
            'AVERAGE_PRICE': 0,
            'ALL': 0,
        },
        ServiceType.CHAT_GPT4_OMNI: {
            'AVERAGE_EXAMPLE_PRICE': 0,
            'EXAMPLE_ALL': 0,
            'AVERAGE_PRICE': 0,
            'ALL': 0,
        },
        ServiceType.CLAUDE_3_SONNET: {
            'AVERAGE_EXAMPLE_PRICE': 0,
            'EXAMPLE_ALL': 0,
            'AVERAGE_PRICE': 0,
            'ALL': 0,
        },
        ServiceType.CLAUDE_3_OPUS: {
            'AVERAGE_EXAMPLE_PRICE': 0,
            'EXAMPLE_ALL': 0,
            'AVERAGE_PRICE': 0,
            'ALL': 0,
        },
        ServiceType.DALL_E: {
            'AVERAGE_EXAMPLE_PRICE': 0,
            'EXAMPLE_ALL': 0,
            'AVERAGE_PRICE': 0,
            'ALL': 0,
        },
        ServiceType.MIDJOURNEY: {
            'AVERAGE_EXAMPLE_PRICE': 0,
            'EXAMPLE_ALL': 0,
            'AVERAGE_PRICE': 0,
            'ALL': 0,
        },
        ServiceType.FACE_SWAP: {
            'AVERAGE_EXAMPLE_PRICE': 0,
            'EXAMPLE_ALL': 0,
            'AVERAGE_PRICE': 0,
            'ALL': 0,
        },
        ServiceType.MUSIC_GEN: {
            'AVERAGE_EXAMPLE_PRICE': 0,
            'EXAMPLE_ALL': 0,
            'AVERAGE_PRICE': 0,
            'ALL': 0,
        },
        ServiceType.SUNO: {
            'AVERAGE_EXAMPLE_PRICE': 0,
            'EXAMPLE_ALL': 0,
            'AVERAGE_PRICE': 0,
            'ALL': 0,
        },
        ServiceType.VOICE_MESSAGES: {
            'AVERAGE_EXAMPLE_PRICE': 0,
            'EXAMPLE_ALL': 0,
            'AVERAGE_PRICE': 0,
            'ALL': 0,
        },
        ServiceType.SERVER: {
            'AVERAGE_EXAMPLE_PRICE': 0,
            'EXAMPLE_ALL': 0,
            'AVERAGE_PRICE': 0,
            'ALL': 0,
        },
        ServiceType.DATABASE: {
            'AVERAGE_EXAMPLE_PRICE': 0,
            'EXAMPLE_ALL': 0,
            'AVERAGE_PRICE': 0,
            'ALL': 0,
        },
        ServiceType.OTHER: {
            'AVERAGE_EXAMPLE_PRICE': 0,
            'EXAMPLE_ALL': 0,
            'AVERAGE_PRICE': 0,
            'ALL': 0,
        },
        SubscriptionType.FREE: {
            'AVERAGE_EXAMPLE_PRICE': 0,
            'EXAMPLE_ALL': 0,
            'AVERAGE_PRICE': 0,
            'ALL': 0,
        },
        SubscriptionType.STANDARD: {
            'AVERAGE_EXAMPLE_PRICE': 0,
            'EXAMPLE_ALL': 0,
            'AVERAGE_PRICE': 0,
            'ALL': 0,
        },
        SubscriptionType.VIP: {
            'AVERAGE_EXAMPLE_PRICE': 0,
            'EXAMPLE_ALL': 0,
            'AVERAGE_PRICE': 0,
            'ALL': 0,
        },
        SubscriptionType.PREMIUM: {
            'AVERAGE_EXAMPLE_PRICE': 0,
            'EXAMPLE_ALL': 0,
            'AVERAGE_PRICE': 0,
            'ALL': 0,
        },
        'ALL': 0,
    }
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
    count_suno_usage = {
        SunoMode.SIMPLE: 0,
        SunoMode.CUSTOM: 0,
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
        ServiceType.SUNO: {
            GenerationReaction.LIKED: 0,
            GenerationReaction.DISLIKED: 0,
            GenerationReaction.NONE: 0,
        },
    }
    count_reactions_before = {
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
        ServiceType.SUNO: {
            GenerationReaction.LIKED: 0,
            GenerationReaction.DISLIKED: 0,
            GenerationReaction.NONE: 0,
        },
    }
    count_credits = {
        'INVITE_FRIENDS': 0,
        'LEAVE_FEEDBACKS': 0,
        'ALL': 0,
    }
    count_credits_before = {
        'INVITE_FRIENDS': 0,
        'LEAVE_FEEDBACKS': 0,
        'ALL': 0,
    }

    for transaction in transactions:
        if transaction.type == TransactionType.INCOME:
            count_income_money_total += 1
            if transaction.currency == Currency.USD:
                count_income_money[transaction.service] += transaction.clear_amount * 100
                if transaction.service in [ServiceType.STANDARD, ServiceType.VIP, ServiceType.PREMIUM]:
                    count_income_money['SUBSCRIPTION_ALL'] += transaction.clear_amount * 100
                elif transaction.service in [
                    ServiceType.CHAT_GPT3_TURBO, ServiceType.CHAT_GPT4_TURBO, ServiceType.CHAT_GPT4_OMNI,
                    ServiceType.CLAUDE_3_SONNET, ServiceType.CLAUDE_3_OPUS,
                    ServiceType.DALL_E, ServiceType.MIDJOURNEY, ServiceType.MIDJOURNEY,
                    ServiceType.MUSIC_GEN, ServiceType.SUNO,
                    ServiceType.ADDITIONAL_CHATS,
                    ServiceType.ACCESS_TO_CATALOG,
                    ServiceType.VOICE_MESSAGES,
                    ServiceType.FAST_MESSAGES,
                ]:
                    count_income_money['PACKAGES_ALL'] += transaction.clear_amount * 100
                count_income_money['ALL'] += transaction.clear_amount * 100
            elif transaction.currency == Currency.RUB:
                count_income_money[transaction.service] += transaction.clear_amount
                if transaction.service in [ServiceType.STANDARD, ServiceType.VIP, ServiceType.PREMIUM]:
                    count_income_money['SUBSCRIPTION_ALL'] += transaction.clear_amount
                elif transaction.service in [
                    ServiceType.CHAT_GPT3_TURBO, ServiceType.CHAT_GPT4_TURBO, ServiceType.CHAT_GPT4_OMNI,
                    ServiceType.CLAUDE_3_SONNET, ServiceType.CLAUDE_3_OPUS,
                    ServiceType.DALL_E, ServiceType.MIDJOURNEY, ServiceType.MIDJOURNEY,
                    ServiceType.MUSIC_GEN, ServiceType.SUNO,
                    ServiceType.ADDITIONAL_CHATS,
                    ServiceType.ACCESS_TO_CATALOG,
                    ServiceType.VOICE_MESSAGES,
                    ServiceType.FAST_MESSAGES,
                ]:
                    count_income_money['PACKAGES_ALL'] += transaction.clear_amount
                count_income_money['ALL'] += transaction.clear_amount
            else:
                count_income_money[transaction.service] += transaction.clear_amount * 2
                if transaction.service in [ServiceType.STANDARD, ServiceType.VIP, ServiceType.PREMIUM]:
                    count_income_money['SUBSCRIPTION_ALL'] += transaction.clear_amount * 2
                elif transaction.service in [
                    ServiceType.CHAT_GPT3_TURBO, ServiceType.CHAT_GPT4_TURBO, ServiceType.CHAT_GPT4_OMNI,
                    ServiceType.CLAUDE_3_SONNET, ServiceType.CLAUDE_3_OPUS,
                    ServiceType.DALL_E, ServiceType.MIDJOURNEY, ServiceType.MIDJOURNEY,
                    ServiceType.MUSIC_GEN, ServiceType.SUNO,
                    ServiceType.ADDITIONAL_CHATS,
                    ServiceType.ACCESS_TO_CATALOG,
                    ServiceType.VOICE_MESSAGES,
                    ServiceType.FAST_MESSAGES,
                ]:
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

            if transaction.user_id in free_users:
                count_expense_money[SubscriptionType.FREE]['ALL'] += transaction.amount
            elif transaction.user_id in standard_users:
                count_expense_money[SubscriptionType.STANDARD]['ALL'] += transaction.amount
            elif transaction.user_id in vip_users:
                count_expense_money[SubscriptionType.VIP]['ALL'] += transaction.amount
            elif transaction.user_id in premium_users:
                count_expense_money[SubscriptionType.PREMIUM]['ALL'] += transaction.amount

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

            if transaction.service == ServiceType.SUNO:
                suno_mode = transaction.details.get('mode', 'Payment')
                count_suno_usage[suno_mode] = count_suno_usage.get(
                    suno_mode,
                    0,
                ) + transaction.quantity

        transaction_user = await get_user(transaction.user_id)
        if transaction_user.subscription_type == SubscriptionType.FREE:
            free_users.add(transaction_user.id)
        elif transaction_user.subscription_type == SubscriptionType.STANDARD:
            standard_users.add(transaction_user.id)
        elif transaction_user.subscription_type == SubscriptionType.VIP:
            vip_users.add(transaction_user.id)
        elif transaction_user.subscription_type == SubscriptionType.PREMIUM:
            premium_users.add(transaction_user.id)
        activated_users.add(transaction.user_id)
    for service in [
        ServiceType.CHAT_GPT3_TURBO, ServiceType.CHAT_GPT4_TURBO, ServiceType.CHAT_GPT4_OMNI,
        ServiceType.CLAUDE_3_SONNET, ServiceType.CLAUDE_3_OPUS,
        ServiceType.DALL_E, ServiceType.MIDJOURNEY, ServiceType.FACE_SWAP,
        ServiceType.MUSIC_GEN, ServiceType.SUNO,
    ]:
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
    count_expense_money[SubscriptionType.STANDARD]['AVERAGE_PRICE'] = (
        count_expense_money[SubscriptionType.STANDARD]['ALL'] / len(standard_users)
    ) if len(standard_users) else 0
    count_expense_money[SubscriptionType.VIP]['AVERAGE_PRICE'] = (
        count_expense_money[SubscriptionType.VIP]['ALL'] / len(vip_users)
    ) if len(vip_users) else 0
    count_expense_money[SubscriptionType.PREMIUM]['AVERAGE_PRICE'] = (
        count_expense_money[SubscriptionType.PREMIUM]['ALL'] / len(premium_users)
    ) if len(premium_users) else 0
    for transaction_before in transactions_before:
        if transaction_before.type == TransactionType.INCOME:
            count_income_money_before_total += 1
            if transaction_before.currency == Currency.USD:
                count_income_money_before[transaction_before.service] += transaction_before.clear_amount * 100
                if transaction_before.service in [ServiceType.STANDARD, ServiceType.VIP, ServiceType.PREMIUM]:
                    count_income_money_before['SUBSCRIPTION_ALL'] += transaction_before.clear_amount * 100
                elif transaction_before.service in [
                    ServiceType.CHAT_GPT3_TURBO, ServiceType.CHAT_GPT4_TURBO, ServiceType.CHAT_GPT4_OMNI,
                    ServiceType.CLAUDE_3_SONNET, ServiceType.CLAUDE_3_OPUS,
                    ServiceType.DALL_E, ServiceType.MIDJOURNEY, ServiceType.MIDJOURNEY,
                    ServiceType.MUSIC_GEN, ServiceType.SUNO,
                    ServiceType.ADDITIONAL_CHATS,
                    ServiceType.ACCESS_TO_CATALOG,
                    ServiceType.VOICE_MESSAGES,
                    ServiceType.FAST_MESSAGES,
                ]:
                    count_income_money_before['PACKAGES_ALL'] += transaction_before.clear_amount * 100
                count_income_money_before['ALL'] += transaction_before.clear_amount * 100
            elif transaction_before.currency == Currency.RUB:
                count_income_money_before[transaction_before.service] += transaction_before.clear_amount
                if transaction_before.service in [ServiceType.STANDARD, ServiceType.VIP, ServiceType.PREMIUM]:
                    count_income_money_before['SUBSCRIPTION_ALL'] += transaction_before.clear_amount
                elif transaction_before.service in [
                    ServiceType.CHAT_GPT3_TURBO, ServiceType.CHAT_GPT4_TURBO, ServiceType.CHAT_GPT4_OMNI,
                    ServiceType.CLAUDE_3_SONNET, ServiceType.CLAUDE_3_OPUS,
                    ServiceType.DALL_E, ServiceType.MIDJOURNEY, ServiceType.MIDJOURNEY,
                    ServiceType.MUSIC_GEN, ServiceType.SUNO,
                    ServiceType.ADDITIONAL_CHATS,
                    ServiceType.ACCESS_TO_CATALOG,
                    ServiceType.VOICE_MESSAGES,
                    ServiceType.FAST_MESSAGES,
                ]:
                    count_income_money_before['PACKAGES_ALL'] += transaction_before.clear_amount
                count_income_money_before['ALL'] += transaction_before.clear_amount
            else:
                count_income_money_before[transaction_before.service] += transaction_before.clear_amount * 2
                if transaction_before.service in [ServiceType.STANDARD, ServiceType.VIP, ServiceType.PREMIUM]:
                    count_income_money_before['SUBSCRIPTION_ALL'] += transaction_before.clear_amount * 2
                elif transaction_before.service in [
                    ServiceType.CHAT_GPT3_TURBO, ServiceType.CHAT_GPT4_TURBO, ServiceType.CHAT_GPT4_OMNI,
                    ServiceType.CLAUDE_3_SONNET, ServiceType.CLAUDE_3_OPUS,
                    ServiceType.DALL_E, ServiceType.MIDJOURNEY, ServiceType.MIDJOURNEY,
                    ServiceType.MUSIC_GEN, ServiceType.SUNO,
                    ServiceType.ADDITIONAL_CHATS,
                    ServiceType.ACCESS_TO_CATALOG,
                    ServiceType.VOICE_MESSAGES,
                    ServiceType.FAST_MESSAGES,
                ]:
                    count_income_money_before['PACKAGES_ALL'] += transaction_before.clear_amount * 2
                count_income_money_before['ALL'] += transaction_before.clear_amount * 2

            count_all_transactions_before[transaction_before.service]['BONUS'] += 1 \
                if transaction_before.details.get('is_bonus', False) \
                else 0

            if transaction_before.clear_amount > 0:
                paid_users_before.add(transaction_before.user_id)
        elif transaction_before.type == TransactionType.EXPENSE:
            count_all_transactions_before[transaction_before.service]['SUCCESS'] += transaction_before.quantity \
                if not transaction_before.details.get('has_error', False) \
                else 0
            count_all_transactions_before[transaction_before.service]['FAIL'] += transaction_before.quantity \
                if transaction_before.details.get('has_error', False) \
                else 0
            count_all_transactions_before[transaction_before.service]['EXAMPLE'] += transaction_before.quantity \
                if transaction_before.details.get('is_suggestion', False) \
                else 0
            count_all_transactions_before[transaction_before.service]['ALL'] += transaction_before.quantity

            count_expense_money_before[transaction_before.service]['AVERAGE_EXAMPLE_PRICE'] += transaction_before.amount \
                if transaction_before.details.get('is_suggestion', False) \
                else 0
            count_expense_money_before[transaction_before.service]['EXAMPLE_ALL'] += transaction_before.amount \
                if transaction_before.details.get('is_suggestion', False) \
                else 0
            count_expense_money_before[transaction_before.service]['AVERAGE_PRICE'] += transaction_before.amount \
                if not transaction_before.details.get('is_suggestion', False) \
                else 0
            count_expense_money_before[transaction_before.service]['ALL'] += transaction_before.amount
            count_expense_money_before['ALL'] += transaction_before.amount

            if transaction_before.user_id in free_users:
                count_expense_money_before[SubscriptionType.FREE]['ALL'] += transaction_before.amount
            elif transaction_before.user_id in standard_users:
                count_expense_money_before[SubscriptionType.STANDARD]['ALL'] += transaction_before.amount
            elif transaction_before.user_id in vip_users:
                count_expense_money_before[SubscriptionType.VIP]['ALL'] += transaction_before.amount
            elif transaction_before.user_id in premium_users:
                count_expense_money_before[SubscriptionType.PREMIUM]['ALL'] += transaction_before.amount

        transaction_before_user = await get_user(transaction_before.user_id)
        if transaction_before_user.subscription_type == SubscriptionType.FREE:
            free_users_before.add(transaction_before_user.id)
        elif transaction_before_user.subscription_type == SubscriptionType.STANDARD:
            standard_users_before.add(transaction_before_user.id)
        elif transaction_before_user.subscription_type == SubscriptionType.VIP:
            vip_users_before.add(transaction_before_user.id)
        elif transaction_before_user.subscription_type == SubscriptionType.PREMIUM:
            premium_users_before.add(transaction_before_user.id)
        activated_users_before.add(transaction_before.user_id)
    for service_before in [
        ServiceType.CHAT_GPT3_TURBO, ServiceType.CHAT_GPT4_TURBO, ServiceType.CHAT_GPT4_OMNI,
        ServiceType.CLAUDE_3_SONNET, ServiceType.CLAUDE_3_OPUS,
        ServiceType.DALL_E, ServiceType.MIDJOURNEY, ServiceType.FACE_SWAP,
        ServiceType.MUSIC_GEN, ServiceType.SUNO,
    ]:
        successes = count_all_transactions_before[service_before]['SUCCESS']
        fails = count_all_transactions_before[service_before]['FAIL']
        examples = count_all_transactions_before[service_before]['EXAMPLE']
        total = successes + fails

        average_price = count_expense_money_before[service_before]['AVERAGE_PRICE']
        average_example_price = count_expense_money_before[service_before]['AVERAGE_EXAMPLE_PRICE']

        count_expense_money_before[service_before]['AVERAGE_PRICE'] = average_price / total \
            if total > 0 else 0
        count_expense_money_before[service_before]['AVERAGE_EXAMPLE_PRICE'] = average_example_price / examples \
            if examples > 0 else 0
    count_expense_money_before[SubscriptionType.FREE]['AVERAGE_PRICE'] = (
        count_expense_money_before[SubscriptionType.FREE]['ALL'] / len(free_users_before)
    ) if len(free_users_before) else 0
    count_expense_money_before[SubscriptionType.STANDARD]['AVERAGE_PRICE'] = (
        count_expense_money_before[SubscriptionType.STANDARD]['ALL'] / len(standard_users_before)
    ) if len(standard_users_before) else 0
    count_expense_money_before[SubscriptionType.VIP]['AVERAGE_PRICE'] = (
        count_expense_money_before[SubscriptionType.VIP]['ALL'] / len(vip_users_before)
    ) if len(vip_users_before) else 0
    count_expense_money_before[SubscriptionType.PREMIUM]['AVERAGE_PRICE'] = (
        count_expense_money_before[SubscriptionType.PREMIUM]['ALL'] / len(premium_users_before)
    ) if len(premium_users_before) else 0

    for generation in generations:
        if (
            generation.model == Model.MIDJOURNEY and
            generation.details.get('action') == MidjourneyAction.UPSCALE
        ):
            count_reactions[ServiceType.MIDJOURNEY][generation.reaction] += 1
        elif generation.model == Model.FACE_SWAP:
            count_reactions[ServiceType.FACE_SWAP][generation.reaction] += 1
        elif generation.model == Model.MUSIC_GEN:
            count_reactions[ServiceType.MUSIC_GEN][generation.reaction] += 1
        elif generation.model == Model.SUNO:
            count_reactions[ServiceType.SUNO][generation.reaction] += 1
    for generation_before in generations_before:
        if (
            generation_before.model == Model.MIDJOURNEY and
            generation_before.details.get('action') == MidjourneyAction.UPSCALE
        ):
            count_reactions_before[ServiceType.MIDJOURNEY][generation_before.reaction] += 1
        elif generation_before.model == Model.FACE_SWAP:
            count_reactions_before[ServiceType.FACE_SWAP][generation_before.reaction] += 1
        elif generation_before.model == Model.MUSIC_GEN:
            count_reactions_before[ServiceType.MUSIC_GEN][generation_before.reaction] += 1
        elif generation_before.model == Model.SUNO:
            count_reactions_before[ServiceType.SUNO][generation_before.reaction] += 1

    count_all_users = len(users)
    count_all_users_before = len(users_before)
    count_activated_users = len(activated_users)
    count_activated_users_before = len(activated_users_before)
    count_referral_users = len(referral_users)
    count_referral_users_before = len(referral_users_before)
    count_english_users = len(english_users)
    count_english_users_before = len(english_users_before)
    count_russian_users = len(russian_users)
    count_russian_users_before = len(russian_users_before)
    count_other_users = len(other_users)
    count_other_users_before = len(other_users_before)
    count_paid_users = len(paid_users)
    count_paid_users_before = len(paid_users_before)
    count_feedbacks = len(feedbacks)
    count_feedbacks_before = len(feedbacks_before)
    count_credits['INVITE_FRIENDS'] = 50 * count_referral_users
    count_credits_before['INVITE_FRIENDS'] = 50 * count_referral_users_before
    count_credits['LEAVE_FEEDBACKS'] = 25 * count_feedbacks
    count_credits_before['LEAVE_FEEDBACKS'] = 25 * count_feedbacks_before
    count_credits['ALL'] = count_credits['INVITE_FRIENDS'] + count_credits['LEAVE_FEEDBACKS']
    count_credits_before['ALL'] = count_credits_before['INVITE_FRIENDS'] + count_credits_before['LEAVE_FEEDBACKS']
    count_activated_promo_codes = len(used_promo_codes)
    count_activated_promo_codes_before = len(used_promo_codes_before)
    count_income_money['AVERAGE_PRICE'] = (
        count_income_money['ALL'] / count_income_money_total
    ) if count_income_money_total else 0
    count_income_money_before['AVERAGE_PRICE'] = (
        count_income_money_before['ALL'] / count_income_money_before_total
    ) if count_income_money_before_total else 0
    count_income_money['VAL'] = count_income_money['ALL'] - count_expense_money['ALL'] * 100
    count_income_money_before['VAL'] = count_income_money_before['ALL'] - count_expense_money_before['ALL'] * 100

    count_chats_usage = {
        'ALL': len(chats),
    }
    count_chats_usage_before = {
        'ALL': len(chats_before),
    }
    count_midjourney_usage['ALL'] = sum(count_midjourney_usage.values())
    count_face_swap_usage['ALL'] = sum(count_face_swap_usage.values())
    count_suno_usage['ALL'] = sum(count_suno_usage.values())
    for chat in chats:
        count_chats_usage[chat.role] = count_chats_usage.get(chat.role, 0) + 1
    for chat_before in chats_before:
        count_chats_usage_before[chat_before.role] = count_chats_usage_before.get(chat_before.role, 0) + 1

    texts = [
        get_localization(language_code).statistics_users(
            period=period,
            count_all_users=count_all_users,
            count_all_users_before=count_all_users_before,
            count_activated_users=count_activated_users,
            count_activated_users_before=count_activated_users_before,
            count_referral_users=count_referral_users,
            count_referral_users_before=count_referral_users_before,
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
            count_banned_users=count_banned_users,
            count_banned_users_before=count_banned_users_before,
            count_subscription_users=count_subscription_users,
            count_subscription_users_before=count_subscription_users_before,
        ),
        get_localization(language_code).statistics_text_models(
            period=period,
            count_all_transactions=count_all_transactions,
            count_all_transactions_before=count_all_transactions_before,
            count_chats_usage=count_chats_usage,
            count_chats_usage_before=count_chats_usage_before,
        ),
        get_localization(language_code).statistics_image_models(
            period=period,
            count_all_transactions=count_all_transactions,
            count_all_transactions_before=count_all_transactions_before,
            count_midjourney_usage=count_midjourney_usage,
            count_face_swap_usage=count_face_swap_usage,
        ),
        get_localization(language_code).statistics_music_models(
            period=period,
            count_all_transactions=count_all_transactions,
            count_all_transactions_before=count_all_transactions_before,
            count_suno_usage=count_suno_usage,
        ),
        get_localization(language_code).statistics_reactions(
            period=period,
            count_reactions=count_reactions,
            count_reactions_before=count_reactions_before,
            count_feedbacks=count_feedbacks,
            count_feedbacks_before=count_feedbacks_before,
        ),
        get_localization(language_code).statistics_bonuses(
            period=period,
            count_credits=count_credits,
            count_credits_before=count_credits_before,
            count_all_transactions=count_all_transactions,
            count_all_transactions_before=count_all_transactions_before,
            count_activated_promo_codes=count_activated_promo_codes,
            count_activated_promo_codes_before=count_activated_promo_codes_before,
        ),
        get_localization(language_code).statistics_expenses(
            period=period,
            count_expense_money=count_expense_money,
            count_expense_money_before=count_expense_money_before,
        ),
        get_localization(language_code).statistics_incomes(
            period=period,
            count_income_money=count_income_money,
            count_income_money_before=count_income_money_before,
        )
    ]

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
        text=get_localization(user_language_code).processing_statistics()
    )

    async with ChatActionSender.typing(bot=callback_query.bot, chat_id=callback_query.message.chat.id):
        texts = await handle_get_statistics(user_language_code, period)
        for text in texts:
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
        )
