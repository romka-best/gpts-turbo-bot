import asyncio
import logging

from aiogram import Bot

from bot.database.models.common import Model, DALLEResolution, DALLEQuality
from bot.database.models.user import UserSettings
from bot.database.operations.user import get_users, update_user
from bot.helpers.send_message_to_admins import send_message_to_admins
from bot.helpers.set_commands import set_commands_for_user


async def migrate_users(bot: Bot):
    logging.info("START_MIGRATION_USERS")

    try:
        users = await get_users()
        tasks = []
        for user in users:
            old_gpt3 = 'gpt-3.5-turbo-1106'
            old_gpt4 = 'gpt-4-1106-preview'
            if user.settings.get(old_gpt3):
                old_gpt3_settings = user.settings.get(old_gpt3, user.settings[Model.GPT3])
                user.settings[Model.GPT3] = old_gpt3_settings
                if user.current_model == old_gpt3:
                    user.current_model = Model.GPT3
                del user.settings[old_gpt3]
            if user.settings.get(old_gpt4):
                old_gpt3_settings = user.settings.get(old_gpt3, user.settings[Model.GPT3])
                user.settings[Model.GPT4] = old_gpt3_settings
                if user.current_model == old_gpt4:
                    user.current_model = Model.GPT4
                del user.settings[old_gpt4]

            user.settings[Model.GPT3][UserSettings.VOICE] = 'alloy'
            user.settings[Model.GPT4][UserSettings.VOICE] = 'alloy'
            user.settings[Model.DALLE3] = {
                UserSettings.SHOW_USAGE_QUOTA: user.settings[Model.DALLE3][UserSettings.SHOW_USAGE_QUOTA],
                UserSettings.RESOLUTION: DALLEResolution.LOW,
                UserSettings.QUALITY: DALLEQuality.STANDARD,
            }

            tasks.append(
                update_user(
                    user.id,
                    {
                        "current_model": user.current_model,
                        "settings": user.settings,
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

        await send_message_to_admins(bot, "<b>The database migration with users was successful!</b> 🎉")
    except Exception as e:
        logging.exception("Error in migration_users", e)
        await send_message_to_admins(bot, "<b>The database migration with user was not successful!</b> 🚨")
    finally:
        logging.info("END_MIGRATION_USERS")
