from google.cloud import firestore

from bot.database.models.common import Quota
from bot.database.models.user import User
from bot.database.operations.chat import write_chat_in_transaction
from bot.database.operations.user import update_user_in_transaction


@firestore.async_transactional
async def create_new_chat(transaction, user: User, telegram_chat_id: str, title: str):
    await write_chat_in_transaction(transaction, user.id, telegram_chat_id, title)

    user.additional_usage_quota[Quota.ADDITIONAL_CHATS] -= 1
    await update_user_in_transaction(transaction, user.id, {
        "additional_usage_quota": user.additional_usage_quota,
    })
