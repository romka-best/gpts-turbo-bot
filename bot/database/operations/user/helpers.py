from datetime import datetime, timezone
from typing import Dict, Optional

from telegram import User as TelegramUser

from bot.database.models.common import Model, Currency
from bot.database.models.subscription import SubscriptionType, SubscriptionLimit
from bot.database.models.user import User, UserGender


def create_user_object(
    telegram_user: TelegramUser,
    user_data: Dict,
    chat_id: str,
    telegram_chat_id: str,
    referred_by: Optional[str],
) -> User:
    return User(
        id=str(telegram_user.id),
        first_name=telegram_user.first_name,
        last_name=telegram_user.last_name or "",
        username=telegram_user.username,
        current_chat_id=chat_id,
        telegram_chat_id=telegram_chat_id,
        gender=user_data.get('gender', UserGender.UNSPECIFIED),
        language_code=telegram_user.language_code,
        is_premium=telegram_user.is_premium or False,
        is_blocked=False,
        current_model=user_data.get("current_model", Model.CHAT_GPT),
        currency=user_data.get("currency", Currency.RUB),
        balance=user_data.get("balance", 0),
        subscription_type=user_data.get("subscription_type", SubscriptionType.FREE),
        last_subscription_limit_update=user_data.get("last_subscription_limit_update", datetime.now(timezone.utc)),
        monthly_limits=user_data.get("monthly_limits", SubscriptionLimit.LIMITS[SubscriptionType.FREE]),
        additional_usage_quota=user_data.get("additional_usage_quota", User.DEFAULT_ADDITIONAL_USAGE_QUOTA),
        settings=user_data.get("settings", User.DEFAULT_SETTINGS),
        referred_by=user_data.get("referred_by", referred_by),
        created_at=user_data.get("created_at", None),
        edited_at=user_data.get("edited_at", None),
    )
