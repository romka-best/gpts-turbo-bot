from datetime import datetime
from typing import Optional

from google.cloud.firestore_v1 import FieldFilter

from bot.database.main import firebase
from bot.database.models.package import PackageType
from bot.database.models.promo_code import PromoCode, UsedPromoCode
from bot.database.models.subscription import SubscriptionType


async def get_promo_code(promo_code_id: str) -> Optional[PromoCode]:
    promo_code_ref = firebase.firebase.db.collection(PromoCode.COLLECTION_NAME).document(promo_code_id)
    promo_code = await promo_code_ref.get()

    if promo_code.exists:
        return PromoCode(**promo_code.to_dict())


async def get_promo_code_by_name(promo_code_name: str) -> Optional[PromoCode]:
    promo_code_stream = firebase.db.collection(PromoCode.COLLECTION_NAME) \
        .where(filter=FieldFilter('name', '==', promo_code_name)) \
        .limit(1) \
        .stream()

    async for doc in promo_code_stream:
        return PromoCode(**doc.to_dict())


async def get_used_promo_code_by_user_id_and_promo_code_id(user_id: str, promo_code_id: str) -> Optional[UsedPromoCode]:
    used_promo_code_stream = firebase.db.collection(UsedPromoCode.COLLECTION_NAME) \
        .where(filter=FieldFilter('user_id', '==', user_id)) \
        .where(filter=FieldFilter('promo_code_id', '==', promo_code_id)) \
        .limit(1) \
        .stream()

    async for doc in used_promo_code_stream:
        return UsedPromoCode(**doc.to_dict())


# TODO DELETE AFTER MIGRATION
async def get_promo_codes() -> list[PromoCode]:
    promo_codes = firebase.db.collection(PromoCode.COLLECTION_NAME).stream()

    return [PromoCode(**promo_code.to_dict()) async for promo_code in promo_codes]


# TODO DELETE AFTER MIGRATION
async def get_promo_codes_by_subscription_type(subscription_type: SubscriptionType) -> list[PromoCode]:
    promo_codes = firebase.db.collection(PromoCode.COLLECTION_NAME) \
        .where(filter=FieldFilter('details.subscription_type', '==', subscription_type)) \
        .stream()

    return [PromoCode(**promo_code.to_dict()) async for promo_code in promo_codes]


# TODO DELETE AFTER MIGRATION
async def get_promo_codes_by_package_type(package_type: PackageType) -> list[PromoCode]:
    promo_codes = firebase.db.collection(PromoCode.COLLECTION_NAME) \
        .where(filter=FieldFilter('details.package_type', '==', package_type)) \
        .stream()

    return [PromoCode(**promo_code.to_dict()) async for promo_code in promo_codes]


async def get_count_of_used_promo_codes(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> int:
    used_promo_code_query = firebase.db.collection(UsedPromoCode.COLLECTION_NAME)

    if start_date:
        used_promo_code_query = used_promo_code_query.where(filter=FieldFilter('created_at', '>=', start_date))
    if end_date:
        used_promo_code_query = used_promo_code_query.where(filter=FieldFilter('created_at', '<=', end_date))

    used_promo_codes_query = await used_promo_code_query.count().get()

    return int(used_promo_codes_query[0][0].value)
