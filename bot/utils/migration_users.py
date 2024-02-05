import asyncio
import logging

from aiogram import Bot

from bot.database.models.common import Quota, Model
from bot.database.models.subscription import SubscriptionType
from bot.database.models.user import UserSettings
from bot.database.operations.user import get_users, update_user
from bot.helpers.send_message_to_admins import send_message_to_admins


async def migration_users(bot: Bot):
    try:
        logging.info("START_MIGRATION_USERS")

        users = await get_users()
        tasks = []
        for user in users:
            user.monthly_limits[Quota.MUSIC_GEN] = 60 if user.subscription_type == SubscriptionType.FREE else 300
            user.additional_usage_quota[Quota.MUSIC_GEN] = 0
            user.settings[Model.MUSIC_GEN] = {
                UserSettings.SHOW_USAGE_QUOTA: True,
            }

            tasks.append(
                update_user(
                    user.id,
                    {
                        "monthly_limits": user.monthly_limits,
                        "additional_usage_quota": user.additional_usage_quota,
                        "settings": user.settings,
                    }
                )
            )
        await asyncio.gather(*tasks)

        await send_message_to_admins(bot, "<b>The database migration with users was successful!</b> 🎉")
    except Exception as e:
        logging.exception("Error in migration_users", e)
        await send_message_to_admins(bot, "<b>The database migration with user was not successful!</b> 🚨")
    finally:
        logging.info("END_MIGRATION_USERS")
