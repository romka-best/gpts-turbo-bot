from google.cloud import firestore

from bot.database.models.common import Quota
from bot.database.models.user import User
from bot.database.operations.message import write_message_in_transaction
from bot.database.operations.user import update_user_in_transaction


@firestore.async_transactional
async def create_new_message_and_update_user(transaction, role: str, content: str, user: User, user_quota: Quota):
    await write_message_in_transaction(transaction, user.current_chat_id, role, "", content)

    if user.monthly_limits[user_quota] > 0:
        user.monthly_limits[user_quota] -= 1
    elif user.additional_usage_quota[user_quota] > 0:
        user.additional_usage_quota[user_quota] -= 1
    else:
        raise PermissionError

    await update_user_in_transaction(transaction, user.id, {
        "monthly_limits": user.monthly_limits,
        "additional_usage_quota": user.additional_usage_quota,
    })
