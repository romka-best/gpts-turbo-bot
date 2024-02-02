from datetime import datetime, timezone
from typing import Optional, Dict, List

from telegram import User as TelegramUser

from bot.database.main import firebase
from bot.database.models.common import Model, Currency
from bot.database.models.subscription import SubscriptionType, SubscriptionLimit
from bot.database.models.user import User, UserGender


async def get_user(user_id: str) -> Optional[User]:
    user_ref = firebase.db.collection("users").document(user_id)
    user = await user_ref.get()

    if user.exists:
        user_dict = user.to_dict()

        return User(
            id=user_dict.get('id'),
            first_name=user_dict.get('first_name'),
            last_name=user_dict.get('last_name'),
            username=user_dict.get('username'),
            current_chat_id=user_dict.get('current_chat_id'),
            telegram_chat_id=user_dict.get('telegram_chat_id'),
            gender=user_dict.get('gender', UserGender.UNSPECIFIED),
            language_code=user_dict.get('language_code'),
            is_premium=user_dict.get('is_premium', False),
            is_blocked=user_dict.get('is_blocked', False),
            current_model=user_dict.get("current_model"),
            currency=user_dict.get("currency"),
            balance=user_dict.get("balance", 0),
            subscription_type=user_dict.get("subscription_type"),
            last_subscription_limit_update=user_dict.get("last_subscription_limit_update"),
            monthly_limits=user_dict.get("monthly_limits"),
            additional_usage_quota=user_dict.get("additional_usage_quota"),
            settings=user_dict.get("settings"),
            referred_by=user_dict.get("referred_by"),
            created_at=user_dict.get("created_at"),
            edited_at=user_dict.get("edited_at")
        )


async def get_users(start_date: Optional[datetime] = None,
                    end_date: Optional[datetime] = None) -> List[User]:
    users_query = firebase.db.collection("users")

    if start_date:
        users_query = users_query.where("created_at", ">=", start_date)
    if end_date:
        users_query = users_query.where("created_at", "<=", end_date)

    users = users_query.stream()
    return [
        User(
            id=user.to_dict().get('id'),
            first_name=user.to_dict().get('first_name'),
            last_name=user.to_dict().get('last_name'),
            username=user.to_dict().get('username'),
            current_chat_id=user.to_dict().get('current_chat_id'),
            telegram_chat_id=user.to_dict().get('telegram_chat_id'),
            gender=user.to_dict().get('gender', UserGender.UNSPECIFIED),
            language_code=user.to_dict().get('language_code'),
            is_premium=user.to_dict().get('is_premium', False),
            is_blocked=user.to_dict().get('is_blocked', False),
            current_model=user.to_dict().get("current_model"),
            currency=user.to_dict().get("currency"),
            balance=user.to_dict().get("balance", 0),
            subscription_type=user.to_dict().get("subscription_type"),
            last_subscription_limit_update=user.to_dict().get("last_subscription_limit_update"),
            monthly_limits=user.to_dict().get("monthly_limits"),
            additional_usage_quota=user.to_dict().get("additional_usage_quota"),
            settings=user.to_dict().get("settings"),
            referred_by=user.to_dict().get("referred_by"),
            created_at=user.to_dict().get("created_at"),
            edited_at=user.to_dict().get("edited_at")
        ) async for user in users
    ]


async def get_users_by_referral(referred_by: str) -> List[User]:
    users_stream = firebase.db.collection("users") \
        .where("referred_by", "==", referred_by) \
        .stream()
    return [
        User(
            id=user.to_dict().get('id'),
            first_name=user.to_dict().get('first_name'),
            last_name=user.to_dict().get('last_name'),
            username=user.to_dict().get('username'),
            current_chat_id=user.to_dict().get('current_chat_id'),
            telegram_chat_id=user.to_dict().get('telegram_chat_id'),
            gender=user.to_dict().get('gender', UserGender.UNSPECIFIED),
            language_code=user.to_dict().get('language_code'),
            is_premium=user.to_dict().get('is_premium', False),
            is_blocked=user.to_dict().get('is_blocked', False),
            current_model=user.to_dict().get("current_model"),
            currency=user.to_dict().get("currency"),
            balance=user.to_dict().get("balance", 0),
            subscription_type=user.to_dict().get("subscription_type"),
            last_subscription_limit_update=user.to_dict().get("last_subscription_limit_update"),
            monthly_limits=user.to_dict().get("monthly_limits"),
            additional_usage_quota=user.to_dict().get("additional_usage_quota"),
            settings=user.to_dict().get("settings"),
            referred_by=user.to_dict().get("referred_by"),
            created_at=user.to_dict().get("created_at"),
            edited_at=user.to_dict().get("edited_at")
        ) async for user in users_stream
    ]


def create_user_object(telegram_user: TelegramUser,
                       user_data: Dict,
                       chat_id: str,
                       telegram_chat_id: str,
                       referred_by: Optional[str]) -> User:
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
        current_model=user_data.get("current_model", Model.GPT3),
        currency=user_data.get("currency", Currency.RUB),
        balance=user_data.get("balance", 0),
        subscription_type=user_data.get("subscription_type", SubscriptionType.FREE),
        last_subscription_limit_update=user_data.get("last_subscription_limit_update", datetime.now(timezone.utc)),
        monthly_limits=user_data.get("monthly_limits", SubscriptionLimit.LIMITS[SubscriptionType.FREE]),
        additional_usage_quota=user_data.get("additional_usage_quota", User.DEFAULT_ADDITIONAL_USAGE_QUOTA),
        settings=user_data.get("settings", User.DEFAULT_SETTINGS),
        referred_by=user_data.get("referred_by", referred_by),
        created_at=user_data.get("created_at", None),
        edited_at=user_data.get("edited_at", None)
    )


async def write_user_in_transaction(transaction,
                                    telegram_user: TelegramUser,
                                    chat_id: str,
                                    telegram_chat_id: str,
                                    referred_by: Optional[str]) -> User:
    user_ref = firebase.db.collection('users').document(str(telegram_user.id))
    user_data = (await user_ref.get()).to_dict() or {}

    created_user = create_user_object(telegram_user, user_data, chat_id, telegram_chat_id, referred_by)

    transaction.set(user_ref, created_user.to_dict())

    return created_user


async def write_user(telegram_user: TelegramUser, chat_id: str, telegram_chat_id: str,
                     referred_by: Optional[str]) -> User:
    user_ref = firebase.db.collection('users').document(str(telegram_user.id))
    user_data = (await user_ref.get()).to_dict() or {}

    created_user = create_user_object(telegram_user, user_data, chat_id, telegram_chat_id, referred_by)

    await user_ref.set(created_user.to_dict())

    return created_user


async def update_user(user_id: str, data: Dict):
    user_ref = firebase.db.collection('users').document(user_id)
    data['edited_at'] = datetime.now(timezone.utc)

    await user_ref.update(data)


async def update_user_in_transaction(transaction, user_id: str, data: Dict):
    data['edited_at'] = datetime.now(timezone.utc)

    transaction.update(firebase.db.collection('users').document(user_id), data)
