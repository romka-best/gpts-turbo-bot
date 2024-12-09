import logging

from aiogram import Bot
from aiogram.fsm.storage.base import BaseStorage

from bot.config import config, MessageSticker
from bot.database.models.subscription import SUBSCRIPTION_FREE_LIMITS
from bot.database.models.user import User
from bot.database.operations.product.getters import get_product
from bot.database.operations.subscription.getters import get_subscription
from bot.helpers.checkers.check_user_last_activity import check_user_last_activity
from bot.helpers.senders.send_message_to_users import send_message_to_user
from bot.helpers.senders.send_sticker import send_sticker
from bot.locales.main import get_user_language, get_localization


async def notify_user_about_quota(bot: Bot, user: User, storage: BaseStorage):
    try:
        should_notify = await check_user_last_activity(user.id, storage)
        if not should_notify:
            return

        user_language_code = await get_user_language(user.id, storage)

        if user.subscription_id:
            user_subscription = await get_subscription(user.subscription_id)
            product_subscription = await get_product(user_subscription.product_id)
            subscription_limits = product_subscription.details.get('limits')
        else:
            subscription_limits = SUBSCRIPTION_FREE_LIMITS

        await send_sticker(
            bot,
            user.id,
            config.MESSAGE_STICKERS.get(MessageSticker.HELLO),
        )
        await send_message_to_user(
            bot,
            user,
            get_localization(user_language_code).notify_about_quota(subscription_limits),
        )
    except Exception as e:
        logging.exception(f'error in notify_user_about_quota: {e}')
