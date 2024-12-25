from datetime import datetime, timezone

from aiogram import Bot

from bot.config import config
from bot.database.main import firebase
from bot.database.models.common import Currency, Quota, Model, GeminiGPTVersion
from bot.database.models.product import ProductType, ProductCategory
from bot.database.models.user import User, UserSettings
from bot.database.operations.product.getters import get_active_products_by_product_type_and_category
from bot.database.operations.product.updaters import update_product
from bot.database.operations.product.writers import write_product
from bot.helpers.senders.send_message_to_admins_and_developers import send_message_to_admins_and_developers
from bot.locales.types import LanguageCode


async def migrate(bot: Bot):
    current_date = datetime.now(timezone.utc)

    await write_product(
        stripe_id='prod_RR5ksE4NqUbi4N',
        is_active=True,
        type=ProductType.PACKAGE,
        category=ProductCategory.TEXT,
        names={
            LanguageCode.RU: 'Grok 2.0 🐦',
            LanguageCode.EN: 'Grok 2.0 🐦',
        },
        descriptions={
            LanguageCode.RU: 'Откройте новый уровень понимания с Grok 2 — вашим интеллектуальным помощником от X 🐦',
            LanguageCode.EN: 'Discover a new level of understanding with Grok 2 — your intelligent assistant from X 🐦',
        },
        prices={
            Currency.RUB: 4,
            Currency.USD: 0.04,
            Currency.XTR: 4,
        },
        order=10,
        details={
            'quota': Quota.GROK_2,
            'support_documents': True,
            'support_photos': True,
        },
    )
    await write_product(
        stripe_id='prod_RR5koSFk7bd7sD',
        is_active=True,
        type=ProductType.PACKAGE,
        category=ProductCategory.TEXT,
        names={
            LanguageCode.RU: 'Perplexity 🌐',
            LanguageCode.EN: 'Perplexity 🌐',
        },
        descriptions={
            LanguageCode.RU: 'Откройте ответы на сложные вопросы с Perplexity для быстрого и точного поиска информации 🌐',
            LanguageCode.EN: 'Discover answers to complex questions with Perplexity for fast and accurate information retrieval 🌐',
        },
        prices={
            Currency.RUB: 4,
            Currency.USD: 0.04,
            Currency.XTR: 4,
        },
        order=11,
        details={
            'quota': Quota.PERPLEXITY,
            'support_documents': False,
            'support_photos': False,
        },
    )

    await write_product(
        stripe_id='prod_RR5rMaV3hFsnGq',
        is_active=True,
        type=ProductType.PACKAGE,
        category=ProductCategory.SUMMARY,
        names={
            LanguageCode.RU: 'Видео Резюме 📼',
            LanguageCode.EN: 'Video Summary 📼',
        },
        descriptions={
            LanguageCode.RU: 'Откройте суть видео с помощником в создании точных и лаконичных резюме видео 📼',
            LanguageCode.EN: 'Discover the essence of videos with an assistant for creating precise and concise video summaries 📼',
        },
        prices={
            Currency.RUB: 5,
            Currency.USD: 0.05,
            Currency.XTR: 5,
        },
        order=1,
        details={
            'quota': Quota.GEMINI_VIDEO,
        },
    )

    await write_product(
        stripe_id='prod_RR5rdKnia5i95f',
        is_active=True,
        type=ProductType.PACKAGE,
        category=ProductCategory.IMAGE,
        names={
            LanguageCode.RU: 'Luma Photon 🌌',
            LanguageCode.EN: 'Luma Photon 🌌',
        },
        descriptions={
            LanguageCode.RU: 'Создавайте потрясающий и уникальный визуальный контент с Luma Photon 🌌',
            LanguageCode.EN: 'Create stunning and unique visual content with Luma Photon 🌌',
        },
        prices={
            Currency.RUB: 8,
            Currency.USD: 0.08,
            Currency.XTR: 8,
        },
        order=4,
        details={
            'quota': Quota.LUMA_PHOTON,
            'support_photos': True,
        },
    )

    await write_product(
        stripe_id='prod_RSKKjOdzXuaye7',
        is_active=True,
        type=ProductType.PACKAGE,
        category=ProductCategory.VIDEO,
        names={
            LanguageCode.RU: 'Kling 🎬',
            LanguageCode.EN: 'Kling 🎬',
        },
        descriptions={
            LanguageCode.RU: 'Создавайте потрясающий и оригинальный видеоконтент с Kling 🎬',
            LanguageCode.EN: 'Create stunning and unique video content with Kling 🎬',
        },
        prices={
            Currency.RUB: 75,
            Currency.USD: 0.75,
            Currency.XTR: 75,
        },
        order=0,
        details={
            'quota': Quota.KLING,
            'support_photos': True,
        },
    )
    await write_product(
        stripe_id='prod_RR5snq0tqN7H0c',
        is_active=True,
        type=ProductType.PACKAGE,
        category=ProductCategory.VIDEO,
        names={
            LanguageCode.RU: 'Luma Ray 🔆',
            LanguageCode.EN: 'Luma Ray 🔆',
        },
        descriptions={
            LanguageCode.RU: 'Создавайте невероятный и уникальный видеоконтента с Luma Ray 🔆',
            LanguageCode.EN: 'Create incredible and unique video content with Luma Ray 🔆',
        },
        prices={
            Currency.RUB: 75,
            Currency.USD: 0.75,
            Currency.XTR: 75,
        },
        order=2,
        details={
            'quota': Quota.LUMA_RAY,
            'support_photos': True,
        },
    )

    product_subscriptions = await get_active_products_by_product_type_and_category(ProductType.SUBSCRIPTION)
    for product_subscription in product_subscriptions:
        product_subscription.details['limits'][Quota.GEMINI_2_FLASH] \
            = product_subscription.details['limits'][Quota.CHAT_GPT4_OMNI_MINI]
        product_subscription.details['limits'][Quota.GROK_2] \
            = product_subscription.details['limits'][Quota.CHAT_GPT4_OMNI]
        product_subscription.details['limits'][Quota.PERPLEXITY] \
            = product_subscription.details['limits'][Quota.CHAT_GPT4_OMNI]
        product_subscription.details['limits'][Quota.GEMINI_VIDEO] \
            = product_subscription.details['limits'][Quota.EIGHTIFY]
        product_subscription.details['limits'][Quota.LUMA_PHOTON] \
            = product_subscription.details['limits'][Quota.DALL_E]
        product_subscription.details['limits'][Quota.KLING] \
            = product_subscription.details['limits'][Quota.RUNWAY]
        product_subscription.details['limits'][Quota.LUMA_RAY] \
            = product_subscription.details['limits'][Quota.RUNWAY]

        try:
            del product_subscription.details['limits']['gemini_1_flash']
        except KeyError:
            pass

        await update_product(product_subscription.id, {
            'details': product_subscription.details,
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

            user.daily_limits[Quota.GEMINI_2_FLASH] = user.daily_limits.get(
                'gemini_1_flash',
                user.daily_limits[Quota.CHAT_GPT4_OMNI_MINI],
            )
            user.daily_limits[Quota.GROK_2] = user.daily_limits[Quota.CHAT_GPT4_OMNI]
            user.daily_limits[Quota.PERPLEXITY] = user.daily_limits[Quota.CHAT_GPT4_OMNI]
            user.daily_limits[Quota.GEMINI_VIDEO] = user.daily_limits[Quota.EIGHTIFY]
            user.daily_limits[Quota.LUMA_PHOTON] = user.daily_limits[Quota.DALL_E]
            user.daily_limits[Quota.KLING] = user.daily_limits[Quota.RUNWAY]
            user.daily_limits[Quota.LUMA_RAY] = user.daily_limits[Quota.RUNWAY]
            try:
                del user.daily_limits['gemini_1_flash']
            except KeyError:
                pass

            user.additional_usage_quota[Quota.GEMINI_2_FLASH] = user.additional_usage_quota.get('gemini_1_flash', 0)
            user.additional_usage_quota[Quota.GROK_2] = 0
            user.additional_usage_quota[Quota.PERPLEXITY] = 0
            user.additional_usage_quota[Quota.GEMINI_VIDEO] = 0
            user.additional_usage_quota[Quota.LUMA_PHOTON] = 0
            user.additional_usage_quota[Quota.KLING] = 0
            user.additional_usage_quota[Quota.LUMA_RAY] = 0
            try:
                del user.additional_usage_quota['gemini_1_flash']
            except KeyError:
                pass

            if user.settings[Model.GEMINI][UserSettings.VERSION] == 'gemini-1.5-flash':
                user.settings[Model.GEMINI][UserSettings.VERSION] = GeminiGPTVersion.V2_Flash
            user.settings[Model.GROK] = User.DEFAULT_SETTINGS[Model.GROK]
            user.settings[Model.PERPLEXITY] = User.DEFAULT_SETTINGS[Model.PERPLEXITY]
            user.settings[Model.GEMINI_VIDEO] = User.DEFAULT_SETTINGS[Model.GEMINI_VIDEO]
            user.settings[Model.LUMA_PHOTON] = User.DEFAULT_SETTINGS[Model.LUMA_PHOTON]
            user.settings[Model.KLING] = User.DEFAULT_SETTINGS[Model.KLING]
            user.settings[Model.LUMA_RAY] = User.DEFAULT_SETTINGS[Model.LUMA_RAY]

            batch.update(user_ref, {
                'daily_limits': user.daily_limits,
                'additional_usage_quota': user.additional_usage_quota,
                'settings': user.settings,
                'edited_at': current_date,
            })

        await batch.commit()

        if count < config.BATCH_SIZE:
            is_running = False
            break

        last_doc = doc
    await send_message_to_admins_and_developers(bot, '<b>Database Migration Was Successful!</b> 🎉')
