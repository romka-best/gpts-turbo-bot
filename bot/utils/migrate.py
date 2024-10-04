import asyncio
import logging
from datetime import datetime, timezone

from aiogram import Bot

from bot.config import config
from bot.database.main import firebase
from bot.database.models.common import Model, Quota, ClaudeGPTVersion
from bot.database.models.game import Game
from bot.database.models.subscription import SubscriptionType, SubscriptionLimit
from bot.database.models.user import UserSettings, User
from bot.database.operations.game.getters import get_games
from bot.database.operations.user.getters import get_users
from bot.helpers.senders.send_message_to_admins_and_developers import send_message_to_admins_and_developers
from bot.helpers.setters.set_commands import set_commands_for_user


async def migrate(bot: Bot):
    logging.info('START_MIGRATION')

    try:
        tasks = []
        current_date = datetime.now(timezone.utc)

        users = await get_users()
        for i in range(0, len(users), config.BATCH_SIZE):
            batch = firebase.db.batch()
            user_batch = users[i:i + config.BATCH_SIZE]

            for user in user_batch:
                user_ref = firebase.db.collection(User.COLLECTION_NAME).document(user.id)

                # Settings
                if (
                    user.subscription_type == SubscriptionType.FREE and
                    user.settings[Model.CLAUDE][UserSettings.VERSION] == ClaudeGPTVersion.V3_Sonnet
                ):
                    user.settings[Model.CLAUDE][UserSettings.VERSION] = ClaudeGPTVersion.V3_Haiku

                user.settings[Model.PHOTOSHOP_AI] = User.DEFAULT_SETTINGS[Model.PHOTOSHOP_AI]

                # Daily Limits
                user.daily_limits = SubscriptionLimit.LIMITS.get(
                    user.subscription_type,
                    SubscriptionLimit.LIMITS[SubscriptionType.FREE]
                )

                # Quota
                user.additional_usage_quota[Quota.CHAT_GPT_O_1_MINI] = 0
                user.additional_usage_quota[Quota.CHAT_GPT_O_1_PREVIEW] = 0
                user.additional_usage_quota[Quota.CLAUDE_3_HAIKU] = 0
                user.additional_usage_quota[Quota.GEMINI_1_ULTRA] = 0
                user.additional_usage_quota[Quota.PHOTOSHOP_AI] = 0

                # Blocked
                user.is_blocked = bool(user.is_blocked)

                batch.update(user_ref, {
                    'settings': user.settings,
                    'daily_limits': user.daily_limits,
                    'additional_usage_quota': user.additional_usage_quota,
                    'is_blocked': user.is_blocked,
                    'edited_at': current_date,
                })

                tasks.append(
                    set_commands_for_user(
                        bot,
                        user.telegram_chat_id,
                        user.interface_language_code,
                    )
                )

            await batch.commit()

        games = await get_games()
        for i in range(0, len(games), config.BATCH_SIZE):
            batch = firebase.db.batch()
            game_batch = games[i:i + config.BATCH_SIZE]

            for game in game_batch:
                game_ref = firebase.db.collection(Game.COLLECTION_NAME).document(game.id)

                batch.update(game_ref, {
                    'reward': 0,
                })

            await batch.commit()

        await asyncio.gather(*tasks)

        await send_message_to_admins_and_developers(bot, '<b>The database migration was successful!</b> 🎉')
    except Exception as e:
        logging.exception('Error in migration', e)
        await send_message_to_admins_and_developers(bot, '<b>The database migration was not successful!</b> 🚨')
    finally:
        logging.info('END_MIGRATION')
