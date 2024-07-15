from typing import Optional

from aiogram.types import User
from google.cloud import firestore

from bot.database.models.common import Quota
from bot.database.operations.cart.writers import write_cart_in_transaction
from bot.database.operations.chat.writers import write_chat_in_transaction
from bot.database.operations.user.writers import write_user_in_transaction


@firestore.async_transactional
async def initialize_user_for_the_first_time(
    transaction,
    telegram_user: User,
    telegram_chat_id: str,
    title: str,
    referred_by: Optional[str],
    is_referred_by_user=False,
    quota=Quota.CHAT_GPT3_TURBO,
    additional_quota=0,
):
    await write_cart_in_transaction(transaction, str(telegram_user.id), [])
    chat = await write_chat_in_transaction(transaction, str(telegram_user.id), telegram_chat_id, title)
    await write_user_in_transaction(
        transaction,
        telegram_user,
        chat.id,
        telegram_chat_id,
        referred_by,
        is_referred_by_user,
        quota,
        additional_quota,
    )
