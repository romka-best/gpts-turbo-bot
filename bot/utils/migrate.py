import asyncio
import logging

from aiogram import Bot

from bot.database.models.common import Model, Quota, SunoSendType
from bot.database.models.subscription import SubscriptionType
from bot.database.models.user import UserSettings
from bot.database.operations.feedback.getters import get_feedbacks_by_user_id
from bot.database.operations.user.getters import get_users
from bot.database.operations.user.updaters import update_user
from bot.helpers.senders.send_message_to_admins import send_message_to_admins
from bot.helpers.setters.set_commands import set_commands_for_user


async def migrate(bot: Bot):
    logging.info("START_MIGRATION")

    try:
        tasks = []

        users = await get_users()
        for user in users:
            user.settings[Model.SUNO] = {
                UserSettings.SHOW_USAGE_QUOTA: True,
                UserSettings.SEND_TYPE: SunoSendType.VIDEO,
            }
            user.additional_usage_quota[Quota.SUNO] = 0
            if user.subscription_type == SubscriptionType.FREE:
                user.additional_usage_quota[Quota.MIDJOURNEY] += 5
                user.additional_usage_quota[Quota.SUNO] = 10
                user.monthly_limits[Quota.SUNO] = 0
            elif user.subscription_type == SubscriptionType.STANDARD:
                user.monthly_limits[Quota.SUNO] = 50
            elif user.subscription_type == SubscriptionType.VIP:
                user.monthly_limits[Quota.SUNO] = 100
            elif user.subscription_type == SubscriptionType.PLATINUM:
                user.monthly_limits[Quota.SUNO] = 200

            users_feedbacks = await get_feedbacks_by_user_id(user.id)
            if len(users_feedbacks):
                user.balance += 50.00

            tasks.append(
                update_user(
                    user.id,
                    {
                        "additional_usage_quota": user.additional_usage_quota,
                        "monthly_limits": user.monthly_limits,
                        "settings": user.settings,
                        "balance": user.balance,
                    }
                )
            )
            tasks.append(
                set_commands_for_user(
                    bot,
                    user.telegram_chat_id,
                    user.language_code,
                )
            )

        await asyncio.gather(*tasks)

        await send_message_to_admins(bot, "<b>The database migration was successful!</b> 🎉")
    except Exception as e:
        logging.exception("Error in migration", e)
        await send_message_to_admins(bot, "<b>The database migration was not successful!</b> 🚨")
    finally:
        logging.info("END_MIGRATION")
