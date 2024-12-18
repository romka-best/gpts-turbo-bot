from datetime import datetime, timezone

from aiogram import Bot
from google.cloud.firestore_v1 import DELETE_FIELD

from bot.config import config
from bot.database.main import firebase
from bot.database.models.common import Currency, Quota, Model
from bot.database.models.product import ProductType, ProductCategory
from bot.database.models.user import User
from bot.database.operations.product.getters import get_active_products_by_product_type_and_category
from bot.database.operations.product.updaters import update_product
from bot.database.operations.product.writers import write_product
from bot.helpers.senders.send_message_to_admins_and_developers import send_message_to_admins_and_developers
from bot.locales.types import LanguageCode


async def migrate(bot: Bot):
    current_date = datetime.now(timezone.utc)

    await write_product(
        stripe_id='prod_RQ1aTtPbLzct18',
        is_active=True,
        type=ProductType.PACKAGE,
        category=ProductCategory.VIDEO,
        names={
            LanguageCode.RU: 'Runway Gen-3 Alpha Turbo 🎥',
            LanguageCode.EN: 'Runway Gen-3 Alpha Turbo 🎥',
        },
        descriptions={
            LanguageCode.RU: 'Откройте мир видеотворчества с Runway — вашим помощником в генерации уникальных видео 🎥',
            LanguageCode.EN: 'Discover the world of video creativity with Runway — your assistant in generating unique videos 🎥',
        },
        prices={
            Currency.RUB: 50,
            Currency.USD: 0.5,
            Currency.XTR: 50,
        },
        order=0,
        details={
            'quota': Quota.RUNWAY,
            'support_photos': True,
        },
    )

    product_subscriptions = await get_active_products_by_product_type_and_category(ProductType.SUBSCRIPTION)
    for product_subscription in product_subscriptions:
        product_subscription.details['limits'][Quota.RUNWAY] = 0
        product_subscription.details['limits'][Quota.CHAT_GPT_O_1] = \
            product_subscription.details['limits']['o1-preview']
        await update_product(product_subscription.id, {
            'details': product_subscription.details,
            'details.limits.o1-preview': DELETE_FIELD,
            'edited_at': current_date,
        })

    users_query = firebase.db.collection(User.COLLECTION_NAME).limit(config.BATCH_SIZE)
    is_running = True
    last_doc = None

    while is_running:
        if last_doc:
            users_query = users_query.start_after(last_doc)

        docs = users_query.stream()

        batch = firebase.db.batch()

        count = 0
        async for doc in docs:
            count += 1

            user = User(**doc.to_dict())

            user_ref = firebase.db.collection(User.COLLECTION_NAME).document(user.id)

            user.daily_limits[Quota.CHAT_GPT_O_1] = user.daily_limits['o1-preview']
            user.daily_limits[Model.RUNWAY] = 0
            user.additional_usage_quota[Quota.CHAT_GPT_O_1] = user.additional_usage_quota['o1-preview']
            user.additional_usage_quota[Model.RUNWAY] = 0
            user.settings[Model.RUNWAY] = User.DEFAULT_SETTINGS[Model.RUNWAY]

            batch.update(user_ref, {
                'daily_limits': user.daily_limits,
                'daily_limits.o1-preview': DELETE_FIELD,
                'additional_usage_quota': user.additional_usage_quota,
                'additional_usage_quota.o1-preview': DELETE_FIELD,
                'settings': user.settings,
                'edited_at': current_date,
            })

        await batch.commit()

        if count < config.BATCH_SIZE:
            is_running = False
            break

        last_doc = doc

    await send_message_to_admins_and_developers(bot, '<b>Database Migration Was Successful!</b> 🎉')
