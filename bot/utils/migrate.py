from datetime import datetime, timezone

from aiogram import Bot

from bot.config import config
from bot.database.main import firebase
from bot.database.models.common import Currency, Quota, Model
from bot.database.models.product import ProductType, ProductCategory
from bot.database.models.user import User
from bot.database.operations.product.getters import get_active_products_by_product_type_and_category
from bot.database.operations.product.updaters import update_product
from bot.database.operations.product.writers import write_product
from bot.database.operations.user.getters import get_users
from bot.helpers.senders.send_message_to_admins_and_developers import send_message_to_admins_and_developers
from bot.locales.types import LanguageCode


async def migrate(bot: Bot):
    current_date = datetime.now(timezone.utc)

    await write_product(
        stripe_id='prod_RO63PXxubduAPX',
        is_active=True,
        type=ProductType.PACKAGE,
        category=ProductCategory.SUMMARY,
        names={
            LanguageCode.RU: 'Eightify 👀',
            LanguageCode.EN: 'Eightify 👀',
        },
        descriptions={
            LanguageCode.RU: 'Откройте мир ясности с Eightify AI — вашим помощником в суммаризации YouTube-видео 👀',
            LanguageCode.EN: 'Discover the world of clarity with Eightify AI — your assistant in summarizing YouTube videos 👀',
        },
        prices={
            Currency.RUB: 1,
            Currency.USD: 0.01,
            Currency.XTR: 1,
        },
        order=10,
        details={
            'quota': Quota.EIGHTIFY,
        },
    )

    product_subscriptions = await get_active_products_by_product_type_and_category(ProductType.SUBSCRIPTION)
    for product_subscription in product_subscriptions:
        product_subscription.details['limits'][Quota.EIGHTIFY] \
            = product_subscription.details['limits'][Quota.CHAT_GPT4_OMNI_MINI]
        await update_product(product_subscription.id, {
            'details': product_subscription.details,
            'edited_at': current_date,
        })

    users = await get_users()
    for i in range(0, len(users), config.BATCH_SIZE):
        batch = firebase.db.batch()
        user_batch = users[i:i + config.BATCH_SIZE]

        for user in user_batch:
            user_ref = firebase.db.collection(User.COLLECTION_NAME).document(user.id)

            user.settings[Model.EIGHTIFY] = User.DEFAULT_SETTINGS[Model.EIGHTIFY]
            user.daily_limits[Quota.EIGHTIFY] = float('inf')
            user.additional_usage_quota[Quota.EIGHTIFY] = 0

            batch.update(user_ref, {
                'settings': user.settings,
                'daily_limits': user.daily_limits,
                'additional_usage_quota': user.additional_usage_quota,
                'edited_at': current_date,
            })
        await batch.commit()
    await send_message_to_admins_and_developers(bot, '<b>Database Migration Was Successful!</b> 🎉')
