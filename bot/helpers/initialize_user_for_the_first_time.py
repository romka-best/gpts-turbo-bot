from aiogram.types import User
from google.cloud import firestore

from bot.database.operations.chat import write_chat_in_transaction
from bot.database.operations.user import write_user_in_transaction


@firestore.async_transactional
async def initialize_user_for_the_first_time(transaction, telegram_user: User, telegram_chat_id: str, title: str):
    chat = await write_chat_in_transaction(transaction, str(telegram_user.id), telegram_chat_id, title)
    await write_user_in_transaction(transaction, telegram_user, chat.id, telegram_chat_id)
