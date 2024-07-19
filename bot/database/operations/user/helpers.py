from datetime import datetime, timezone
from typing import Dict, Optional

from telegram import User as TelegramUser

from bot.database.models.common import Model, Currency, Quota
from bot.database.models.subscription import SubscriptionType, SubscriptionLimit
from bot.database.models.user import User, UserGender


def create_user_object(
    telegram_user: TelegramUser,
    user_data: Dict,
    chat_id: str,
    telegram_chat_id: str,
    referred_by: Optional[str],
    is_referred_by_user=False,
    quota=Quota.CHAT_GPT4_OMNI_MINI,
    additional_quota=0,
) -> User:
    default_model = Model.CHAT_GPT
    default_additional_quota = User.DEFAULT_ADDITIONAL_USAGE_QUOTA
    default_additional_quota[quota] = additional_quota
    if quota in [Quota.CHAT_GPT4_OMNI_MINI, Quota.CHAT_GPT4_TURBO, Quota.CHAT_GPT4_OMNI]:
        default_model = Model.CHAT_GPT
    elif quota in [Quota.CLAUDE_3_SONNET, Quota.CLAUDE_3_OPUS]:
        default_model = Model.CLAUDE
    elif quota == Quota.DALL_E:
        default_model = Model.DALL_E
    elif quota == Quota.MIDJOURNEY:
        default_model = Model.MIDJOURNEY
    elif quota == Quota.FACE_SWAP:
        default_model = Model.FACE_SWAP
    elif quota == Quota.MUSIC_GEN:
        default_model = Model.MUSIC_GEN
    elif quota == Quota.SUNO:
        default_model = Model.SUNO

    return User(
        id=str(telegram_user.id),
        first_name=telegram_user.first_name,
        last_name=telegram_user.last_name or "",
        username=telegram_user.username,
        current_chat_id=chat_id,
        telegram_chat_id=telegram_chat_id,
        gender=user_data.get('gender', UserGender.UNSPECIFIED),
        language_code=telegram_user.language_code,
        interface_language_code=user_data.get(
            'interface_language_code',
            'ru' if telegram_user.language_code == 'ru' else 'en'
        ),
        is_premium=telegram_user.is_premium or False,
        is_blocked=False,
        is_banned=False,
        current_model=user_data.get("current_model", default_model),
        currency=user_data.get("currency", Currency.RUB if telegram_user.language_code == 'ru' else Currency.USD),
        balance=user_data.get("balance", 25.00 if is_referred_by_user else 0),
        subscription_type=user_data.get("subscription_type", SubscriptionType.FREE),
        last_subscription_limit_update=user_data.get("last_subscription_limit_update", datetime.now(timezone.utc)),
        monthly_limits=user_data.get("monthly_limits", SubscriptionLimit.LIMITS[SubscriptionType.FREE]),
        additional_usage_quota=user_data.get("additional_usage_quota", default_additional_quota),
        settings=user_data.get("settings", User.DEFAULT_SETTINGS),
        referred_by=user_data.get("referred_by", referred_by),
        created_at=user_data.get("created_at", None),
        edited_at=user_data.get("edited_at", None),
    )
