import logging
from datetime import datetime, timezone

from aiogram import Bot

from bot.config import config
from bot.database.main import firebase
from bot.database.models.common import Model, ChatGPTVersion, Quota
from bot.database.models.user import UserSettings, User
from bot.database.operations.user.getters import get_users
from bot.helpers.senders.send_message_to_admins_and_developers import send_message_to_admins_and_developers


async def migrate(bot: Bot):
    logging.info("START_MIGRATION")

    try:
        current_date = datetime.now(timezone.utc)

        users = await get_users()
        for i in range(0, len(users), config.USER_BATCH_SIZE):
            batch = firebase.db.batch()
            user_batch = users[i:i + config.USER_BATCH_SIZE]

            for user in user_batch:
                user_ref = firebase.db.collection(User.COLLECTION_NAME).document(user.id)

                if user.settings[Model.CHAT_GPT][UserSettings.VERSION] == 'gpt-3.5-turbo':
                    user.settings[Model.CHAT_GPT][UserSettings.VERSION] = ChatGPTVersion.V4_Omni_Mini

                if 'gpt3' in user.monthly_limits:
                    user.monthly_limits[Quota.CHAT_GPT4_OMNI_MINI] = user.monthly_limits.get('gpt3', 0)
                    del user.monthly_limits['gpt3']

                if 'gpt3' in user.additional_usage_quota:
                    user.additional_usage_quota[Quota.CHAT_GPT4_OMNI_MINI] = user.additional_usage_quota.get('gpt3', 0)
                    del user.additional_usage_quota['gpt3']

                batch.update(user_ref, {
                    "settings": user.settings,
                    "monthly_limits": user.monthly_limits,
                    "additional_usage_quota": user.additional_usage_quota,
                    "edited_at": current_date,
                })

            await batch.commit()

        await send_message_to_admins_and_developers(bot, "<b>The database migration was successful!</b> 🎉")
    except Exception as e:
        logging.exception("Error in migration", e)
        await send_message_to_admins_and_developers(bot, "<b>The database migration was not successful!</b> 🚨")
    finally:
        logging.info("END_MIGRATION")
