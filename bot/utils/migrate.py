import asyncio
import logging

from aiogram import Bot

from bot.config import config
from bot.database.main import firebase
from bot.database.models.common import Model, Quota, ClaudeGPTVersion
from bot.database.models.subscription import SubscriptionType
from bot.database.models.user import UserSettings
from bot.database.operations.user.getters import get_users
from bot.helpers.senders.send_message_to_admins import send_message_to_admins
from bot.helpers.setters.set_commands import set_commands_for_user


async def migrate(bot: Bot):
    logging.info("START_MIGRATION")

    try:
        tasks = []

        users = await get_users()
        for i in range(0, len(users), config.USER_BATCH_SIZE):
            batch = firebase.db.batch()
            user_batch = users[i:i + config.USER_BATCH_SIZE]

            for user in user_batch:
                user_ref = firebase.db.collection("users").document(user.id)

                if user.subscription_type == "PLATINUM":
                    user.subscription_type = SubscriptionType.PREMIUM

                user.settings[Model.CLAUDE] = {
                    UserSettings.SHOW_THE_NAME_OF_THE_CHATS: False,
                    UserSettings.SHOW_THE_NAME_OF_THE_ROLES: False,
                    UserSettings.SHOW_USAGE_QUOTA: False,
                    UserSettings.TURN_ON_VOICE_MESSAGES: False,
                    UserSettings.VOICE: 'alloy',
                    UserSettings.VERSION: ClaudeGPTVersion.V3_Sonnet,
                }
                user.additional_usage_quota[Quota.CHAT_GPT4_OMNI] = 0
                user.additional_usage_quota[Quota.CLAUDE_3_SONNET] = 0
                user.additional_usage_quota[Quota.CLAUDE_3_OPUS] = 0
                if user.subscription_type == SubscriptionType.FREE:
                    user.monthly_limits[Quota.CHAT_GPT4_OMNI] = 0
                    user.monthly_limits[Quota.CLAUDE_3_SONNET] = 20
                    user.monthly_limits[Quota.CLAUDE_3_OPUS] = 0
                elif user.subscription_type == SubscriptionType.STANDARD:
                    user.monthly_limits[Quota.CHAT_GPT4_OMNI] = 25
                    user.monthly_limits[Quota.CLAUDE_3_SONNET] = 250
                    user.monthly_limits[Quota.CLAUDE_3_OPUS] = 25
                elif user.subscription_type == SubscriptionType.VIP:
                    user.monthly_limits[Quota.CHAT_GPT4_OMNI] = 50
                    user.monthly_limits[Quota.CLAUDE_3_SONNET] = 500
                    user.monthly_limits[Quota.CLAUDE_3_OPUS] = 50
                elif user.subscription_type == SubscriptionType.PREMIUM:
                    user.monthly_limits[Quota.CHAT_GPT4_OMNI] = 100
                    user.monthly_limits[Quota.CLAUDE_3_SONNET] = 1000
                    user.monthly_limits[Quota.CLAUDE_3_OPUS] = 100

                batch.update(user_ref, {
                    "is_banned": False,
                    "subscription_type": user.subscription_type,
                    "additional_usage_quota": user.additional_usage_quota,
                    "current_model": user.current_model,
                    "monthly_limits": user.monthly_limits,
                    "settings": user.settings,
                })

                tasks.append(
                    set_commands_for_user(
                        bot,
                        user.telegram_chat_id,
                        user.language_code,
                    )
                )

            await batch.commit()

            await asyncio.gather(*tasks)

        await send_message_to_admins(bot, "<b>The database migration was successful!</b> 🎉")
    except Exception as e:
        logging.exception("Error in migration", e)
        await send_message_to_admins(bot, "<b>The database migration was not successful!</b> 🚨")
    finally:
        logging.info("END_MIGRATION")
