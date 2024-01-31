import logging

from aiogram import Bot

from bot.config import config
from bot.database.main import firebase
from bot.database.models.common import Model
from bot.database.models.user import UserSettings
from bot.database.operations.user import update_user, get_users
from bot.helpers.send_message_to_admins import send_message_to_admins


async def migration_users_settings(bot: Bot):
    try:
        logging.info("START_MIGRATION_USER_SETTINGS")

        all_users = await get_users()
        need_notify = False
        for i in range(0, len(all_users), config.USER_BATCH_SIZE):
            batch = firebase.db.batch()
            user_batch = all_users[i:i + config.USER_BATCH_SIZE]

            for user in user_batch:
                if (
                    not user.settings.get(Model.GPT3) or
                    not user.settings.get(Model.GPT4) or
                    not user.settings.get(Model.DALLE3) or
                    not user.settings.get(Model.FACE_SWAP)
                ):
                    await update_user(user.id, {
                        "settings": {
                            Model.GPT3: {
                                UserSettings.SHOW_THE_NAME_OF_THE_CHATS: user.settings.get(
                                    'show_name_of_the_chat',
                                    True,
                                ),
                                UserSettings.SHOW_THE_NAME_OF_THE_ROLES: False,
                                UserSettings.SHOW_USAGE_QUOTA: user.settings.get(UserSettings.SHOW_USAGE_QUOTA, True),
                                UserSettings.TURN_ON_VOICE_MESSAGES: user.settings.get(
                                    UserSettings.TURN_ON_VOICE_MESSAGES,
                                    False),
                            },
                            Model.GPT4: {
                                UserSettings.SHOW_THE_NAME_OF_THE_CHATS: user.settings.get(
                                    'show_name_of_the_chat',
                                    True,
                                ),
                                UserSettings.SHOW_THE_NAME_OF_THE_ROLES: False,
                                UserSettings.SHOW_USAGE_QUOTA: user.settings.get(UserSettings.SHOW_USAGE_QUOTA, True),
                                UserSettings.TURN_ON_VOICE_MESSAGES: user.settings.get(
                                    UserSettings.TURN_ON_VOICE_MESSAGES,
                                    False,
                                ),
                            },
                            Model.DALLE3: {
                                UserSettings.SHOW_USAGE_QUOTA: user.settings.get(UserSettings.SHOW_USAGE_QUOTA, True),
                            },
                            Model.FACE_SWAP: {
                                UserSettings.SHOW_USAGE_QUOTA: user.settings.get(UserSettings.SHOW_USAGE_QUOTA, True),
                            },
                        }
                    })
                    need_notify = True

            await batch.commit()
        if need_notify:
            await send_message_to_admins(bot, "<b>The database migration was successful!</b> 🎉")
    except Exception:
        await send_message_to_admins(bot, "<b>The database migration was not successful!</b> 🚨")
    finally:
        logging.info("END_MIGRATION_USER_SETTINGS")
