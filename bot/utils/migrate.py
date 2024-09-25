import logging
from datetime import datetime, timezone

from aiogram import Bot
from google.cloud.firestore_v1 import DELETE_FIELD

from bot.config import config
from bot.database.main import firebase
from bot.database.models.common import Model, ChatGPTVersion, Quota
from bot.database.models.feedback import Feedback, FeedbackStatus
from bot.database.models.subscription import SubscriptionType, SubscriptionLimit
from bot.database.models.user import UserSettings, User
from bot.database.operations.feedback.getters import get_feedbacks
from bot.database.operations.user.getters import get_users
from bot.helpers.senders.send_message_to_admins_and_developers import send_message_to_admins_and_developers


async def migrate(bot: Bot):
    logging.info('START_MIGRATION')

    try:
        current_date = datetime.now(timezone.utc)

        users = await get_users()
        for i in range(0, len(users), config.USER_BATCH_SIZE):
            batch = firebase.db.batch()
            user_batch = users[i:i + config.USER_BATCH_SIZE]

            for user in user_batch:
                user_ref = firebase.db.collection(User.COLLECTION_NAME).document(user.id)

                # Settings
                if user.settings[Model.CHAT_GPT][UserSettings.VERSION] == 'gpt-4-turbo':
                    user.settings[Model.CHAT_GPT][UserSettings.VERSION] = ChatGPTVersion.V4_Omni

                user.settings[Model.CHAT_GPT][UserSettings.SHOW_EXAMPLES] = False
                user.settings[Model.CLAUDE][UserSettings.SHOW_EXAMPLES] = False
                user.settings[Model.GEMINI] = User.DEFAULT_SETTINGS[Model.GEMINI]
                user.settings[Model.DALL_E][UserSettings.SHOW_EXAMPLES] = False
                user.settings[Model.MIDJOURNEY][UserSettings.SHOW_EXAMPLES] = False
                user.settings[Model.STABLE_DIFFUSION] = User.DEFAULT_SETTINGS[Model.STABLE_DIFFUSION]
                user.settings[Model.FACE_SWAP][UserSettings.SHOW_EXAMPLES] = False
                user.settings[Model.MUSIC_GEN][UserSettings.SHOW_EXAMPLES] = False
                user.settings[Model.SUNO][UserSettings.SHOW_EXAMPLES] = False

                # Daily Limits
                user.daily_limits = SubscriptionLimit.LIMITS.get(
                    user.subscription_type,
                    SubscriptionLimit.LIMITS[SubscriptionType.FREE]
                )

                # Quota
                if 'gpt4' in user.additional_usage_quota:
                    user.additional_usage_quota[Quota.CHAT_GPT4_OMNI] = (
                        user.additional_usage_quota.get('gpt4', 0) +
                        user.additional_usage_quota.get(Quota.CHAT_GPT4_OMNI, 0)
                    )
                    del user.additional_usage_quota['gpt4']
                user.additional_usage_quota[Quota.GEMINI_1_FLASH] = 0
                user.additional_usage_quota[Quota.GEMINI_1_PRO] = 0
                user.additional_usage_quota[Quota.STABLE_DIFFUSION] = 0

                batch.update(user_ref, {
                    'settings': user.settings,
                    'monthly_limits': DELETE_FIELD,
                    'daily_limits': user.daily_limits,
                    'additional_usage_quota': user.additional_usage_quota,
                    'edited_at': current_date,
                })

            await batch.commit()

        feedbacks = await get_feedbacks()
        for i in range(0, len(feedbacks), config.USER_BATCH_SIZE):
            batch = firebase.db.batch()
            feedback_batch = feedbacks[i:i + config.USER_BATCH_SIZE]

            for feedback in feedback_batch:
                feedback_ref = firebase.db.collection(Feedback.COLLECTION_NAME).document(feedback.id)

                batch.update(feedback_ref, {
                    'status': FeedbackStatus.WAITING,
                })

            await batch.commit()

        await send_message_to_admins_and_developers(bot, '<b>The database migration was successful!</b> 🎉')
    except Exception as e:
        logging.exception('Error in migration', e)
        await send_message_to_admins_and_developers(bot, '<b>The database migration was not successful!</b> 🚨')
    finally:
        logging.info('END_MIGRATION')
