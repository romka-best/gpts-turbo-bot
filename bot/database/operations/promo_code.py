from typing import Optional

from bot.database.main import firebase
from bot.database.models.promo_code import PromoCode, UsedPromoCode, PromoCodeType


async def get_promo_code(promo_code_id: str) -> Optional[PromoCode]:
    promo_code_ref = firebase.firebase.db.collection("promo_codes").document(promo_code_id)
    promo_code = await promo_code_ref.get()

    if promo_code.exists:
        return PromoCode(**promo_code.to_dict())


async def get_promo_code_by_name(promo_code_name: str) -> Optional[PromoCode]:
    promo_code_stream = firebase.db.collection("promo_codes") \
        .where("name", "==", promo_code_name) \
        .limit(1) \
        .stream()

    async for doc in promo_code_stream:
        return PromoCode(**doc.to_dict())


async def get_used_promo_code_by_user_id_and_promo_code_id(user_id: str, promo_code_id) -> Optional[UsedPromoCode]:
    used_promo_code_stream = firebase.db.collection("used_promo_codes") \
        .where("user_id", "==", user_id) \
        .where("promo_code_id", "==", promo_code_id) \
        .limit(1) \
        .stream()

    async for doc in used_promo_code_stream:
        return UsedPromoCode(**doc.to_dict())


async def create_promo_code_object(created_by_user_id: str,
                                   name: str,
                                   type: PromoCodeType,
                                   details: dict,
                                   until=None) -> PromoCode:
    promo_code_ref = firebase.db.collection('promo_codes').document()

    return PromoCode(
        id=promo_code_ref.id,
        created_by_user_id=created_by_user_id,
        name=name,
        type=type,
        details=details,
        until=until
    )


async def create_used_promo_code_object(user_id: str,
                                        promo_code_id: str) -> UsedPromoCode:
    used_promo_code_ref = firebase.db.collection('used_promo_codes').document()

    return UsedPromoCode(
        id=used_promo_code_ref.id,
        user_id=user_id,
        promo_code_id=promo_code_id
    )


async def write_promo_code(created_by_user_id: str,
                           name: str,
                           type: PromoCodeType,
                           details: dict,
                           until=None) -> PromoCode:
    promo_code = await create_promo_code_object(created_by_user_id, name, type, details, until)
    await firebase.db.collection('promo_codes').document(promo_code.id).set(promo_code.to_dict())

    return promo_code


async def write_used_promo_code(user_id: str, promo_code_id: str) -> UsedPromoCode:
    used_promo_code = await create_used_promo_code_object(user_id, promo_code_id)
    await firebase.db.collection('used_promo_codes').document(used_promo_code.id).set(used_promo_code.to_dict())

    return used_promo_code
