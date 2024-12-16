from datetime import datetime, timezone

from aiogram import Bot

from bot.config import config
from bot.database.main import firebase
from bot.database.models.common import Model
from bot.database.models.user import User, UserSettings
from bot.helpers.senders.send_message_to_admins_and_developers import send_message_to_admins_and_developers


async def migrate(bot: Bot):
    current_date = datetime.now(timezone.utc)

    users_query = firebase.db.collection(User.COLLECTION_NAME).limit(config.BATCH_SIZE)
    is_running = True
    last_doc = None

    while is_running:
        if last_doc:
            users_query = users_query.start_after(last_doc)

        docs = users_query.stream()

        batch = firebase.db.batch()

        count = 0
        async for doc in docs:
            count += 1

            user = User(**doc.to_dict())

            user_ref = firebase.db.collection(User.COLLECTION_NAME).document(user.id)

            user.settings[Model.FACE_SWAP][UserSettings.GENDER] = user.gender

            batch.update(user_ref, {
                'settings': user.settings,
                'edited_at': current_date,
            })

        await batch.commit()

        if count < config.BATCH_SIZE:
            is_running = False
            break

        last_doc = doc

    await send_message_to_admins_and_developers(bot, '<b>Database Migration Was Successful!</b> 🎉')
