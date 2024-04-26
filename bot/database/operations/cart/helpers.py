from typing import List, Dict

from bot.database.main import firebase
from bot.database.models.cart import Cart


async def create_cart_object(user_id: str, items: List[Dict]) -> Cart:
    cart_ref = firebase.db.collection(Cart.COLLECTION_NAME).document()
    return Cart(
        id=cart_ref.id,
        user_id=user_id,
        items=items,
    )
