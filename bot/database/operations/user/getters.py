from datetime import datetime
from typing import Optional, List

from google.cloud.firestore_v1 import FieldFilter

from bot.database.main import firebase
from bot.database.models.subscription import SubscriptionType
from bot.database.models.user import User


async def get_user(user_id: str) -> Optional[User]:
    user_ref = firebase.db.collection(User.COLLECTION_NAME).document(user_id)
    user = await user_ref.get()

    if user.exists:
        return User(**user.to_dict())


async def get_users(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    is_blocked: Optional[bool] = None,
) -> List[User]:
    users_query = firebase.db.collection(User.COLLECTION_NAME)

    if start_date:
        users_query = users_query.where(filter=FieldFilter('created_at', '>=', start_date))
    if end_date:
        users_query = users_query.where(filter=FieldFilter('created_at', '<=', end_date))
    if is_blocked is not None:
        users_query = users_query.where(filter=FieldFilter('is_blocked', '==', is_blocked))

    users = users_query.stream()
    return [
        User(**user.to_dict()) async for user in users
    ]


async def get_count_of_users(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    subscription_type: Optional[SubscriptionType] = None,
    is_blocked: Optional[bool] = None,
    language_code: Optional[str] = None,
) -> int:
    users_query = firebase.db.collection(User.COLLECTION_NAME)

    if start_date:
        users_query = users_query.where(filter=FieldFilter('created_at', '>=', start_date))
    if end_date:
        users_query = users_query.where(filter=FieldFilter('created_at', '<=', end_date))
    if subscription_type:
        users_query = users_query.where(filter=FieldFilter('subscription_type', '==', subscription_type))
    if is_blocked is not None:
        users_query = users_query.where(filter=FieldFilter('is_blocked', '==', is_blocked))
    if language_code:
        users_query = users_query.where(filter=FieldFilter('language_code', '==', language_code))

    users_query = await users_query.count().get()

    return int(users_query[0][0].value)


async def get_count_of_users_referred_by(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> int:
    users_query = firebase.db.collection(User.COLLECTION_NAME)

    if start_date:
        users_query = users_query.where(filter=FieldFilter('created_at', '>=', start_date))
    if end_date:
        users_query = users_query.where(filter=FieldFilter('created_at', '<=', end_date))

    users_query = await users_query.where(filter=FieldFilter('referred_by', '>=', '')) \
        .order_by('referred_by') \
        .count() \
        .get()

    return int(users_query[0][0].value)


async def get_count_of_users_by_referral(referred_by: str) -> int:
    users_query = await firebase.db.collection(User.COLLECTION_NAME) \
        .where(filter=FieldFilter('referred_by', '==', referred_by)) \
        .count() \
        .get()

    return int(users_query[0][0].value)


async def get_users_by_language_code(language_code: str) -> List[User]:
    users_stream = firebase.db.collection(User.COLLECTION_NAME) \
        .where(filter=FieldFilter('interface_language_code', '==', language_code)) \
        .stream()

    return [
        User(**user.to_dict()) async for user in users_stream
    ]
