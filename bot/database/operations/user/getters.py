from datetime import datetime
from typing import Optional, List

from google.cloud.firestore_v1 import FieldFilter

from bot.database.main import firebase
from bot.database.models.user import User, UserGender


async def get_user(user_id: str) -> Optional[User]:
    user_ref = firebase.db.collection(User.COLLECTION_NAME).document(user_id)
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


async def get_users(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> List[User]:
    users_query = firebase.db.collection(User.COLLECTION_NAME)

    if start_date:
        users_query = users_query.where(filter=FieldFilter("created_at", ">=", start_date))
    if end_date:
        users_query = users_query.where(filter=FieldFilter("created_at", "<=", end_date))

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
    users_stream = firebase.db.collection(User.COLLECTION_NAME) \
        .where(filter=FieldFilter("referred_by", "==", referred_by)) \
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


async def get_users_by_language_code(language_code: str) -> List[User]:
    users_stream = firebase.db.collection(User.COLLECTION_NAME) \
        .where(filter=FieldFilter("language_code", "==", language_code)) \
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
