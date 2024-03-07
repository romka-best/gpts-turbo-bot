from typing import Optional

from google.cloud.firestore_v1 import FieldFilter

from bot.database.main import firebase
from bot.database.models.promo_code import PromoCode, UsedPromoCode


async def get_promo_code(promo_code_id: str) -> Optional[PromoCode]:
    promo_code_ref = firebase.firebase.db.collection(PromoCode.COLLECTION_NAME).document(promo_code_id)
    promo_code = await promo_code_ref.get()

    if promo_code.exists:
        return PromoCode(**promo_code.to_dict())


async def get_promo_code_by_name(promo_code_name: str) -> Optional[PromoCode]:
    promo_code_stream = firebase.db.collection(PromoCode.COLLECTION_NAME) \
        .where(filter=FieldFilter("name", "==", promo_code_name)) \
        .limit(1) \
        .stream()

    async for doc in promo_code_stream:
        return PromoCode(**doc.to_dict())


async def get_used_promo_code_by_user_id_and_promo_code_id(user_id: str, promo_code_id) -> Optional[UsedPromoCode]:
    used_promo_code_stream = firebase.db.collection(UsedPromoCode.COLLECTION_NAME) \
        .where(filter=FieldFilter("user_id", "==", user_id)) \
        .where(filter=FieldFilter("promo_code_id", "==", promo_code_id)) \
        .limit(1) \
        .stream()

    async for doc in used_promo_code_stream:
        return UsedPromoCode(**doc.to_dict())
