import logging
from datetime import datetime, timezone

import aiohttp
import stripe
from aiogram import Bot
from google.cloud.firestore_v1 import DELETE_FIELD

from bot.config import config
from bot.database.main import firebase
from bot.database.models.cart import Cart
from bot.database.models.common import Currency, Quota, Model, SunoVersion
from bot.database.models.generation import Generation
from bot.database.models.package import PackageType
from bot.database.models.product import ProductType, ProductCategory
from bot.database.models.subscription import SubscriptionType, SubscriptionPeriod
from bot.database.models.transaction import ServiceType, Transaction
from bot.database.models.user import User, UserSettings
from bot.database.operations.cart.getters import get_carts
from bot.database.operations.generation.getters import get_generations_by_model, get_generations
from bot.database.operations.generation.updaters import update_generation
from bot.database.operations.package.getters import get_packages_by_type, get_packages
from bot.database.operations.package.updaters import update_package
from bot.database.operations.product.writers import write_product
from bot.database.operations.promo_code.getters import (
    get_promo_codes_by_subscription_type,
    get_promo_codes_by_package_type,
    get_promo_codes,
)
from bot.database.operations.promo_code.updaters import update_promo_code
from bot.database.operations.request.getters import get_requests_by_model, get_requests
from bot.database.operations.request.updaters import update_request
from bot.database.operations.subscription.getters import (
    get_subscriptions_by_type,
    get_last_subscription_by_user_id,
    get_subscriptions,
)
from bot.database.operations.subscription.updaters import update_subscription
from bot.database.operations.transaction.getters import get_transactions
from bot.database.operations.transaction.updaters import update_transaction
from bot.database.operations.user.getters import get_users, get_users_by_subscription_type
from bot.database.operations.user.updaters import update_user
from bot.helpers.senders.send_message_to_admins_and_developers import send_message_to_admins_and_developers


async def migrate(bot: Bot):
    logging.info('START_MIGRATION')

    try:
        await send_message_to_admins_and_developers(bot, '<b>Check before migration started!</b>')

        await get_subscriptions_by_type('TEST')
        await get_transactions(service='TEST')
        await get_promo_codes_by_subscription_type('TEST')
        await get_users_by_subscription_type('TEST')
        await get_requests_by_model('TEST')
        await get_generations_by_model('TEST')

        await send_message_to_admins_and_developers(bot, '<b>The check before migration was successful!</b> 🎉')
    except Exception as e:
        logging.exception('Error in migration', e)
        await send_message_to_admins_and_developers(
            bot,
            f'The check before migration was not successful! 🚨\n\n{e}',
            parse_mode=None,
        )

    try:
        await send_message_to_admins_and_developers(bot, '<b>first migration started!</b>')
        # create products
        # MINI
        mini_monthly_product = await write_product(
            stripe_id='prod_RHNcjbft7nET1G',
            is_active=True,
            type=ProductType.SUBSCRIPTION,
            category=ProductCategory.MONTHLY,
            names={
                'ru': 'Mini 🍬',
                'en': 'Mini 🍬',
            },
            descriptions={
                'ru': '',
                'en': '',
            },
            prices={
                Currency.RUB: 199,
                Currency.USD: 2.50,
                Currency.XTR: 150,
            },
            photos={
                'ru': 'payments/subscription_mini_ru.png',
                'en': 'payments/subscription_mini_en.png',
            },
            order=0,
            details={
                'limits': {
                    Quota.CHAT_GPT4_OMNI_MINI: 20,
                    Quota.CHAT_GPT4_OMNI: 10,
                    Quota.CLAUDE_3_HAIKU: 20,
                    Quota.CLAUDE_3_SONNET: 10,
                    Quota.CLAUDE_3_OPUS: 0,
                    Quota.GEMINI_1_FLASH: 20,
                    Quota.GEMINI_1_PRO: 10,
                    Quota.GEMINI_1_ULTRA: 0,
                    Quota.CHAT_GPT_O_1_MINI: 10,
                    Quota.CHAT_GPT_O_1_PREVIEW: 0,
                    Quota.DALL_E: 5,
                    Quota.MIDJOURNEY: 5,
                    Quota.STABLE_DIFFUSION: 5,
                    Quota.FLUX: 5,
                    Quota.FACE_SWAP: 5,
                    Quota.PHOTOSHOP_AI: 5,
                    Quota.MUSIC_GEN: 5,
                    Quota.SUNO: 5,
                    Quota.ADDITIONAL_CHATS: 2,
                    Quota.ACCESS_TO_CATALOG: True,
                    Quota.FAST_MESSAGES: True,
                    Quota.VOICE_MESSAGES: True,
                },
                'discount': 10,
            },
        )
        mini_yearly_product = await write_product(
            stripe_id='prod_RHNcjbft7nET1G',
            is_active=True,
            type=ProductType.SUBSCRIPTION,
            category=ProductCategory.YEARLY,
            names={
                'ru': 'Mini 🍬',
                'en': 'Mini 🍬',
            },
            descriptions={
                'ru': '',
                'en': '',
            },
            prices={
                Currency.RUB: 1919,
                Currency.USD: 24,
                Currency.XTR: 1440,
            },
            photos={
                'ru': 'payments/subscription_mini_ru.png',
                'en': 'payments/subscription_mini_en.png',
            },
            order=0,
            details={
                'limits': {
                    Quota.CHAT_GPT4_OMNI_MINI: 20,
                    Quota.CHAT_GPT4_OMNI: 10,
                    Quota.CLAUDE_3_HAIKU: 20,
                    Quota.CLAUDE_3_SONNET: 10,
                    Quota.CLAUDE_3_OPUS: 0,
                    Quota.GEMINI_1_FLASH: 20,
                    Quota.GEMINI_1_PRO: 10,
                    Quota.GEMINI_1_ULTRA: 0,
                    Quota.CHAT_GPT_O_1_MINI: 10,
                    Quota.CHAT_GPT_O_1_PREVIEW: 0,
                    Quota.DALL_E: 5,
                    Quota.MIDJOURNEY: 5,
                    Quota.STABLE_DIFFUSION: 5,
                    Quota.FLUX: 5,
                    Quota.FACE_SWAP: 5,
                    Quota.PHOTOSHOP_AI: 5,
                    Quota.MUSIC_GEN: 5,
                    Quota.SUNO: 5,
                    Quota.ADDITIONAL_CHATS: 2,
                    Quota.ACCESS_TO_CATALOG: True,
                    Quota.FAST_MESSAGES: True,
                    Quota.VOICE_MESSAGES: True,
                },
                'discount': 10,
            },
        )
        mini_subscriptions = await get_subscriptions_by_type(SubscriptionType.MINI)
        for mini_subscription in mini_subscriptions:
            if mini_subscription.period == SubscriptionPeriod.MONTHS12:
                await update_subscription(mini_subscription.id, {
                    'product_id': mini_yearly_product.id,
                })
            else:
                await update_subscription(mini_subscription.id, {
                    'product_id': mini_monthly_product.id,
                })
        mini_transactions = await get_transactions(service=ServiceType.MINI)
        for mini_transaction in mini_transactions:
            await update_transaction(mini_transaction.id, {
                'product_id': mini_monthly_product.id,
            })
        mini_users = await get_users_by_subscription_type(SubscriptionType.MINI)
        for mini_user in mini_users:
            current_subscription = await get_last_subscription_by_user_id(mini_user.id)
            await update_user(mini_user.id, {
                'subscription_id': current_subscription.id,
            })
        mini_promo_codes = await get_promo_codes_by_subscription_type(SubscriptionType.MINI)
        for mini_promo_code in mini_promo_codes:
            mini_promo_code.details['product_id'] = mini_monthly_product.id,
            await update_promo_code(mini_promo_code.id, {
                'details': mini_promo_code.details,
            })

        await send_message_to_admins_and_developers(bot, '<b>MINI migration was successful!</b> 🎉')

        # STANDARD
        standard_monthly_product = await write_product(
            stripe_id='prod_RHNcJ9uGDFTOrc',
            is_active=True,
            type=ProductType.SUBSCRIPTION,
            category=ProductCategory.MONTHLY,
            names={
                'ru': 'Standard ⭐',
                'en': 'Standard ⭐',
            },
            descriptions={
                'ru': '',
                'en': '',
            },
            prices={
                Currency.RUB: 299,
                Currency.USD: 5,
                Currency.XTR: 250,
            },
            photos={
                'ru': 'payments/subscription_standard_ru.png',
                'en': 'payments/subscription_standard_en.png',
            },
            order=1,
            details={
                'limits': {
                    Quota.CHAT_GPT4_OMNI_MINI: 100,
                    Quota.CHAT_GPT4_OMNI: 20,
                    Quota.CLAUDE_3_HAIKU: 100,
                    Quota.CLAUDE_3_SONNET: 20,
                    Quota.CLAUDE_3_OPUS: 10,
                    Quota.GEMINI_1_FLASH: 100,
                    Quota.GEMINI_1_PRO: 20,
                    Quota.GEMINI_1_ULTRA: 10,
                    Quota.CHAT_GPT_O_1_MINI: 20,
                    Quota.CHAT_GPT_O_1_PREVIEW: 10,
                    Quota.DALL_E: 10,
                    Quota.MIDJOURNEY: 10,
                    Quota.STABLE_DIFFUSION: 10,
                    Quota.FLUX: 10,
                    Quota.FACE_SWAP: 10,
                    Quota.PHOTOSHOP_AI: 10,
                    Quota.MUSIC_GEN: 10,
                    Quota.SUNO: 10,
                    Quota.ADDITIONAL_CHATS: 5,
                    Quota.ACCESS_TO_CATALOG: True,
                    Quota.FAST_MESSAGES: True,
                    Quota.VOICE_MESSAGES: True,
                },
                'discount': 20,
            },
        )
        standard_yearly_product = await write_product(
            stripe_id='prod_RHNcJ9uGDFTOrc',
            is_active=True,
            type=ProductType.SUBSCRIPTION,
            category=ProductCategory.YEARLY,
            names={
                'ru': 'Standard ⭐',
                'en': 'Standard ⭐',
            },
            descriptions={
                'ru': '',
                'en': '',
            },
            prices={
                Currency.RUB: 2879,
                Currency.USD: 48,
                Currency.XTR: 2400,
            },
            photos={
                'ru': 'payments/subscription_standard_ru.png',
                'en': 'payments/subscription_standard_en.png',
            },
            order=1,
            details={
                'limits': {
                    Quota.CHAT_GPT4_OMNI_MINI: 100,
                    Quota.CHAT_GPT4_OMNI: 20,
                    Quota.CLAUDE_3_HAIKU: 100,
                    Quota.CLAUDE_3_SONNET: 20,
                    Quota.CLAUDE_3_OPUS: 10,
                    Quota.GEMINI_1_FLASH: 100,
                    Quota.GEMINI_1_PRO: 20,
                    Quota.GEMINI_1_ULTRA: 10,
                    Quota.CHAT_GPT_O_1_MINI: 20,
                    Quota.CHAT_GPT_O_1_PREVIEW: 10,
                    Quota.DALL_E: 10,
                    Quota.MIDJOURNEY: 10,
                    Quota.STABLE_DIFFUSION: 10,
                    Quota.FLUX: 10,
                    Quota.FACE_SWAP: 10,
                    Quota.PHOTOSHOP_AI: 10,
                    Quota.MUSIC_GEN: 10,
                    Quota.SUNO: 10,
                    Quota.ADDITIONAL_CHATS: 5,
                    Quota.ACCESS_TO_CATALOG: True,
                    Quota.FAST_MESSAGES: True,
                    Quota.VOICE_MESSAGES: True,
                },
                'discount': 20,
            },
        )
        standard_subscriptions = await get_subscriptions_by_type(SubscriptionType.STANDARD)
        for standard_subscription in standard_subscriptions:
            if standard_subscription.period == SubscriptionPeriod.MONTHS12:
                await update_subscription(standard_subscription.id, {
                    'product_id': standard_yearly_product.id,
                })
            else:
                await update_subscription(standard_subscription.id, {
                    'product_id': standard_monthly_product.id,
                })
        standard_transactions = await get_transactions(service=ServiceType.STANDARD)
        for standard_transaction in standard_transactions:
            await update_transaction(standard_transaction.id, {
                'product_id': standard_monthly_product.id,
            })
        standard_users = await get_users_by_subscription_type(SubscriptionType.STANDARD)
        for standard_user in standard_users:
            current_subscription = await get_last_subscription_by_user_id(standard_user.id)
            await update_user(standard_user.id, {
                'subscription_id': current_subscription.id,
            })
        standard_promo_codes = await get_promo_codes_by_subscription_type(SubscriptionType.STANDARD)
        for standard_promo_code in standard_promo_codes:
            standard_promo_code.details['product_id'] = standard_monthly_product.id,
            await update_promo_code(standard_promo_code.id, {
                'details': standard_promo_code.details,
            })
        await send_message_to_admins_and_developers(bot, '<b>STANDARD migration was successful!</b> 🎉')

        # VIP
        vip_monthly_product = await write_product(
            stripe_id='prod_RHNcZChkZUanjr',
            is_active=True,
            type=ProductType.SUBSCRIPTION,
            category=ProductCategory.MONTHLY,
            names={
                'ru': 'VIP 🔥',
                'en': 'VIP 🔥',
            },
            descriptions={
                'ru': '',
                'en': '',
            },
            prices={
                Currency.RUB: 749,
                Currency.USD: 10,
                Currency.XTR: 500,
            },
            photos={
                'ru': 'payments/subscription_vip_ru.png',
                'en': 'payments/subscription_vip_en.png',
            },
            order=2,
            details={
                'limits': {
                    Quota.CHAT_GPT4_OMNI_MINI: float('inf'),
                    Quota.CHAT_GPT4_OMNI: 50,
                    Quota.CLAUDE_3_HAIKU: float('inf'),
                    Quota.CLAUDE_3_SONNET: 50,
                    Quota.CLAUDE_3_OPUS: 20,
                    Quota.GEMINI_1_FLASH: float('inf'),
                    Quota.GEMINI_1_PRO: 50,
                    Quota.GEMINI_1_ULTRA: 20,
                    Quota.CHAT_GPT_O_1_MINI: 50,
                    Quota.CHAT_GPT_O_1_PREVIEW: 20,
                    Quota.DALL_E: 15,
                    Quota.MIDJOURNEY: 15,
                    Quota.STABLE_DIFFUSION: 15,
                    Quota.FLUX: 15,
                    Quota.FACE_SWAP: 15,
                    Quota.PHOTOSHOP_AI: 15,
                    Quota.MUSIC_GEN: 20,
                    Quota.SUNO: 20,
                    Quota.ADDITIONAL_CHATS: 10,
                    Quota.ACCESS_TO_CATALOG: True,
                    Quota.FAST_MESSAGES: True,
                    Quota.VOICE_MESSAGES: True,
                },
                'discount': 30,
            },
        )
        vip_yearly_product = await write_product(
            stripe_id='prod_RHNcZChkZUanjr',
            is_active=True,
            type=ProductType.SUBSCRIPTION,
            category=ProductCategory.YEARLY,
            names={
                'ru': 'VIP 🔥',
                'en': 'VIP 🔥',
            },
            descriptions={
                'ru': '',
                'en': '',
            },
            prices={
                Currency.RUB: 7199,
                Currency.USD: 96,
                Currency.XTR: 4800,
            },
            photos={
                'ru': 'payments/subscription_vip_ru.png',
                'en': 'payments/subscription_vip_en.png',
            },
            order=2,
            details={
                'limits': {
                    Quota.CHAT_GPT4_OMNI_MINI: float('inf'),
                    Quota.CHAT_GPT4_OMNI: 50,
                    Quota.CLAUDE_3_HAIKU: float('inf'),
                    Quota.CLAUDE_3_SONNET: 50,
                    Quota.CLAUDE_3_OPUS: 20,
                    Quota.GEMINI_1_FLASH: float('inf'),
                    Quota.GEMINI_1_PRO: 50,
                    Quota.GEMINI_1_ULTRA: 20,
                    Quota.CHAT_GPT_O_1_MINI: 50,
                    Quota.CHAT_GPT_O_1_PREVIEW: 20,
                    Quota.DALL_E: 15,
                    Quota.MIDJOURNEY: 15,
                    Quota.STABLE_DIFFUSION: 15,
                    Quota.FLUX: 15,
                    Quota.FACE_SWAP: 15,
                    Quota.PHOTOSHOP_AI: 15,
                    Quota.MUSIC_GEN: 20,
                    Quota.SUNO: 20,
                    Quota.ADDITIONAL_CHATS: 10,
                    Quota.ACCESS_TO_CATALOG: True,
                    Quota.FAST_MESSAGES: True,
                    Quota.VOICE_MESSAGES: True,
                },
                'discount': 30,
            },
        )
        vip_subscriptions = await get_subscriptions_by_type(SubscriptionType.VIP)
        for vip_subscription in vip_subscriptions:
            if vip_subscription.period == SubscriptionPeriod.MONTHS12:
                await update_subscription(vip_subscription.id, {
                    'product_id': vip_yearly_product.id,
                })
            else:
                await update_subscription(vip_subscription.id, {
                    'product_id': vip_monthly_product.id,
                })
        vip_transactions = await get_transactions(service=ServiceType.VIP)
        for vip_transaction in vip_transactions:
            await update_transaction(vip_transaction.id, {
                'product_id': vip_monthly_product.id,
            })
        vip_users = await get_users_by_subscription_type(SubscriptionType.VIP)
        for vip_user in vip_users:
            current_subscription = await get_last_subscription_by_user_id(vip_user.id)
            await update_user(vip_user.id, {
                'subscription_id': current_subscription.id,
            })
        vip_promo_codes = await get_promo_codes_by_subscription_type(SubscriptionType.VIP)
        for vip_promo_code in vip_promo_codes:
            vip_promo_code.details['product_id'] = vip_monthly_product.id,
            await update_promo_code(vip_promo_code.id, {
                'details': vip_promo_code.details,
            })
        await send_message_to_admins_and_developers(bot, '<b>VIP migration was successful!</b> 🎉')

        # PREMIUM
        premium_monthly_product = await write_product(
            stripe_id='prod_RHNdgOMwE5Wfuy',
            is_active=True,
            type=ProductType.SUBSCRIPTION,
            category=ProductCategory.MONTHLY,
            names={
                'ru': 'Premium 💎',
                'en': 'Premium 💎',
            },
            descriptions={
                'ru': '',
                'en': '',
            },
            prices={
                Currency.RUB: 1999,
                Currency.USD: 20,
                Currency.XTR: 1000,
            },
            photos={
                'ru': 'payments/subscription_premium_ru.png',
                'en': 'payments/subscription_premium_en.png',
            },
            order=3,
            details={
                'limits': {
                    Quota.CHAT_GPT4_OMNI_MINI: float('inf'),
                    Quota.CHAT_GPT4_OMNI: 100,
                    Quota.CLAUDE_3_HAIKU: float('inf'),
                    Quota.CLAUDE_3_SONNET: 100,
                    Quota.CLAUDE_3_OPUS: 50,
                    Quota.GEMINI_1_FLASH: float('inf'),
                    Quota.GEMINI_1_PRO: 100,
                    Quota.GEMINI_1_ULTRA: 50,
                    Quota.CHAT_GPT_O_1_MINI: 100,
                    Quota.CHAT_GPT_O_1_PREVIEW: 50,
                    Quota.DALL_E: 30,
                    Quota.MIDJOURNEY: 30,
                    Quota.STABLE_DIFFUSION: 30,
                    Quota.FLUX: 30,
                    Quota.FACE_SWAP: 30,
                    Quota.PHOTOSHOP_AI: 30,
                    Quota.MUSIC_GEN: 50,
                    Quota.SUNO: 50,
                    Quota.ADDITIONAL_CHATS: 20,
                    Quota.ACCESS_TO_CATALOG: True,
                    Quota.FAST_MESSAGES: True,
                    Quota.VOICE_MESSAGES: True,
                },
                'discount': 50,
            },
        )
        premium_yearly_product = await write_product(
            stripe_id='prod_RHNdgOMwE5Wfuy',
            is_active=True,
            type=ProductType.SUBSCRIPTION,
            category=ProductCategory.YEARLY,
            names={
                'ru': 'Premium 💎',
                'en': 'Premium 💎',
            },
            descriptions={
                'ru': '',
                'en': '',
            },
            prices={
                Currency.RUB: 19199,
                Currency.USD: 192,
                Currency.XTR: 9600,
            },
            photos={
                'ru': 'payments/subscription_premium_ru.png',
                'en': 'payments/subscription_premium_en.png',
            },
            order=3,
            details={
                'limits': {
                    Quota.CHAT_GPT4_OMNI_MINI: float('inf'),
                    Quota.CHAT_GPT4_OMNI: 100,
                    Quota.CLAUDE_3_HAIKU: float('inf'),
                    Quota.CLAUDE_3_SONNET: 100,
                    Quota.CLAUDE_3_OPUS: 50,
                    Quota.GEMINI_1_FLASH: float('inf'),
                    Quota.GEMINI_1_PRO: 100,
                    Quota.GEMINI_1_ULTRA: 50,
                    Quota.CHAT_GPT_O_1_MINI: 100,
                    Quota.CHAT_GPT_O_1_PREVIEW: 50,
                    Quota.DALL_E: 30,
                    Quota.MIDJOURNEY: 30,
                    Quota.STABLE_DIFFUSION: 30,
                    Quota.FLUX: 30,
                    Quota.FACE_SWAP: 30,
                    Quota.PHOTOSHOP_AI: 30,
                    Quota.MUSIC_GEN: 50,
                    Quota.SUNO: 50,
                    Quota.ADDITIONAL_CHATS: 20,
                    Quota.ACCESS_TO_CATALOG: True,
                    Quota.FAST_MESSAGES: True,
                    Quota.VOICE_MESSAGES: True,
                },
                'discount': 50,
            },
        )
        premium_subscriptions = await get_subscriptions_by_type(SubscriptionType.PREMIUM)
        for premium_subscription in premium_subscriptions:
            if premium_subscription.period == SubscriptionPeriod.MONTHS12:
                await update_subscription(premium_subscription.id, {
                    'product_id': premium_yearly_product.id,
                })
            else:
                await update_subscription(premium_subscription.id, {
                    'product_id': premium_monthly_product.id,
                })
        premium_transactions = await get_transactions(service=ServiceType.PREMIUM)
        for premium_transaction in premium_transactions:
            await update_transaction(premium_transaction.id, {
                'product_id': premium_monthly_product.id,
            })
        premium_users = await get_users_by_subscription_type(SubscriptionType.PREMIUM)
        for premium_user in premium_users:
            current_subscription = await get_last_subscription_by_user_id(premium_user.id)
            await update_user(premium_user.id, {
                'subscription_id': current_subscription.id,
            })
        premium_promo_codes = await get_promo_codes_by_subscription_type(SubscriptionType.PREMIUM)
        for premium_promo_code in premium_promo_codes:
            premium_promo_code.details['product_id'] = premium_monthly_product.id,
            await update_promo_code(premium_promo_code.id, {
                'details': premium_promo_code.details,
            })
        await send_message_to_admins_and_developers(bot, '<b>PREMIUM migration was successful!</b> 🎉')

        # UNLIMITED
        unlimited_monthly_product = await write_product(
            stripe_id='prod_RHNdWeHzwmGgCX',
            is_active=True,
            type=ProductType.SUBSCRIPTION,
            category=ProductCategory.MONTHLY,
            names={
                'ru': 'Unlimited ♾️',
                'en': 'Unlimited ♾️',
            },
            descriptions={
                'ru': '',
                'en': '',
            },
            prices={
                Currency.RUB: 4999,
                Currency.USD: 50,
                Currency.XTR: 2500,
            },
            photos={
                'ru': 'payments/subscription_unlimited_ru.png',
                'en': 'payments/subscription_unlimited_en.png',
            },
            order=4,
            details={
                'limits': {
                    Quota.CHAT_GPT4_OMNI_MINI: float('inf'),
                    Quota.CHAT_GPT4_OMNI: float('inf'),
                    Quota.CLAUDE_3_HAIKU: float('inf'),
                    Quota.CLAUDE_3_SONNET: float('inf'),
                    Quota.CLAUDE_3_OPUS: float('inf'),
                    Quota.GEMINI_1_FLASH: float('inf'),
                    Quota.GEMINI_1_PRO: float('inf'),
                    Quota.GEMINI_1_ULTRA: float('inf'),
                    Quota.CHAT_GPT_O_1_MINI: float('inf'),
                    Quota.CHAT_GPT_O_1_PREVIEW: float('inf'),
                    Quota.DALL_E: float('inf'),
                    Quota.MIDJOURNEY: float('inf'),
                    Quota.STABLE_DIFFUSION: float('inf'),
                    Quota.FLUX: float('inf'),
                    Quota.FACE_SWAP: float('inf'),
                    Quota.PHOTOSHOP_AI: float('inf'),
                    Quota.MUSIC_GEN: float('inf'),
                    Quota.SUNO: float('inf'),
                    Quota.ADDITIONAL_CHATS: float('inf'),
                    Quota.ACCESS_TO_CATALOG: True,
                    Quota.FAST_MESSAGES: True,
                    Quota.VOICE_MESSAGES: True,
                },
                'discount': 50,
            },
        )
        unlimited_yearly_product = await write_product(
            stripe_id='prod_RHNdWeHzwmGgCX',
            is_active=True,
            type=ProductType.SUBSCRIPTION,
            category=ProductCategory.YEARLY,
            names={
                'ru': 'Unlimited ♾️',
                'en': 'Unlimited ♾️',
            },
            descriptions={
                'ru': '',
                'en': '',
            },
            prices={
                Currency.RUB: 47999,
                Currency.USD: 480,
                Currency.XTR: 24000,
            },
            photos={
                'ru': 'payments/subscription_unlimited_ru.png',
                'en': 'payments/subscription_unlimited_en.png',
            },
            order=4,
            details={
                'limits': {
                    Quota.CHAT_GPT4_OMNI_MINI: float('inf'),
                    Quota.CHAT_GPT4_OMNI: float('inf'),
                    Quota.CLAUDE_3_HAIKU: float('inf'),
                    Quota.CLAUDE_3_SONNET: float('inf'),
                    Quota.CLAUDE_3_OPUS: float('inf'),
                    Quota.GEMINI_1_FLASH: float('inf'),
                    Quota.GEMINI_1_PRO: float('inf'),
                    Quota.GEMINI_1_ULTRA: float('inf'),
                    Quota.CHAT_GPT_O_1_MINI: float('inf'),
                    Quota.CHAT_GPT_O_1_PREVIEW: float('inf'),
                    Quota.DALL_E: float('inf'),
                    Quota.MIDJOURNEY: float('inf'),
                    Quota.STABLE_DIFFUSION: float('inf'),
                    Quota.FLUX: float('inf'),
                    Quota.FACE_SWAP: float('inf'),
                    Quota.PHOTOSHOP_AI: float('inf'),
                    Quota.MUSIC_GEN: float('inf'),
                    Quota.SUNO: float('inf'),
                    Quota.ADDITIONAL_CHATS: float('inf'),
                    Quota.ACCESS_TO_CATALOG: True,
                    Quota.FAST_MESSAGES: True,
                    Quota.VOICE_MESSAGES: True,
                },
                'discount': 50,
            },
        )
        unlimited_subscriptions = await get_subscriptions_by_type(SubscriptionType.UNLIMITED)
        for unlimited_subscription in unlimited_subscriptions:
            if unlimited_subscription.period == SubscriptionPeriod.MONTHS12:
                await update_subscription(unlimited_subscription.id, {
                    'product_id': unlimited_yearly_product.id,
                })
            else:
                await update_subscription(unlimited_subscription.id, {
                    'product_id': unlimited_monthly_product.id,
                })
        unlimited_transactions = await get_transactions(service=ServiceType.UNLIMITED)
        for unlimited_transaction in unlimited_transactions:
            await update_transaction(unlimited_transaction.id, {
                'product_id': unlimited_monthly_product.id,
            })
        unlimited_users = await get_users_by_subscription_type(SubscriptionType.UNLIMITED)
        for unlimited_user in unlimited_users:
            current_subscription = await get_last_subscription_by_user_id(unlimited_user.id)
            await update_user(unlimited_user.id, {
                'subscription_id': current_subscription.id,
            })
        unlimited_promo_codes = await get_promo_codes_by_subscription_type(SubscriptionType.UNLIMITED)
        for unlimited_promo_code in unlimited_promo_codes:
            unlimited_promo_code.details['product_id'] = unlimited_monthly_product.id,
            await update_promo_code(unlimited_promo_code.id, {
                'details': unlimited_promo_code.details,
            })
        await send_message_to_admins_and_developers(bot, '<b>UNLIMITED migration was successful!</b> 🎉')

        # CHAT_GPT3_TURBO
        chatgpt3_turbo_product = await write_product(
            stripe_id='prod_RHNdnIIXn43za1',
            is_active=False,
            type=ProductType.PACKAGE,
            category=ProductCategory.TEXT,
            names={
                'ru': 'ChatGPT 3.5 Turbo ✉️',
                'en': 'ChatGPT 3.5 Turbo ✉️',
            },
            descriptions={
                'ru': 'Разбудите мощь ChatGPT 3.5 Turbo для остроумных бесед, умных советов и бесконечного веселья! ✉️',
                'en': 'Unleash the power of ChatGPT 3.5 Turbo for witty chats, smart advice, and endless fun! ✉️',
            },
            prices={
                Currency.RUB: 1,
                Currency.USD: 0.01,
                Currency.XTR: 1,
            },
            details={
                'quota': 'gpt3',
            },
        )
        chatgpt3_turbo_packages = await get_packages_by_type('GPT3')
        for chatgpt3_turbo_package in chatgpt3_turbo_packages:
            await update_package(chatgpt3_turbo_package.id, {
                'product_id': chatgpt3_turbo_product.id,
            })
        chatgpt3_turbo_transactions = await get_transactions(service=ServiceType.CHAT_GPT3_TURBO)
        for i in range(0, len(chatgpt3_turbo_transactions), config.BATCH_SIZE):
            batch = firebase.db.batch()
            chatgpt3_turbo_transaction_batch = chatgpt3_turbo_transactions[i:i + config.BATCH_SIZE]
            for chatgpt3_turbo_transaction in chatgpt3_turbo_transaction_batch:
                chatgpt3_turbo_transaction_ref = firebase.db.collection(
                    Transaction.COLLECTION_NAME
                ).document(chatgpt3_turbo_transaction.id)
                batch.update(chatgpt3_turbo_transaction_ref, {
                    'product_id': chatgpt3_turbo_product.id,
                })
            await batch.commit()
        chatgpt3_turbo_promo_codes = await get_promo_codes_by_package_type('GPT3')
        for chatgpt3_turbo_promo_code in chatgpt3_turbo_promo_codes:
            chatgpt3_turbo_promo_code.details['product_id'] = chatgpt3_turbo_product.id,
            await update_promo_code(chatgpt3_turbo_promo_code.id, {
                'details': chatgpt3_turbo_promo_code.details,
            })
        await send_message_to_admins_and_developers(bot, '<b>GPT3 migration was successful!</b> 🎉')
        # CHAT_GPT4_TURBO
        chatgpt4_turbo_product = await write_product(
            stripe_id='prod_RHNdHY5UuRKCWU',
            is_active=False,
            type=ProductType.PACKAGE,
            category=ProductCategory.TEXT,
            names={
                'ru': 'ChatGPT 4.0 Turbo 🧠',
                'en': 'ChatGPT 4.0 Turbo 🧠',
            },
            descriptions={
                'ru': 'Откройте новые горизонты с интеллектом ChatGPT 4.0 Turbo для более глубоких анализов и инновационных диалогов! 🧠',
                'en': 'Discover new horizons with the intelligence of ChatGPT 4.0 Turbo for deeper analyses and innovative dialogues! 🧠',
            },
            prices={
                Currency.RUB: 10,
                Currency.USD: 0.1,
                Currency.XTR: 10,
            },
            details={
                'quota': 'gpt4',
            },
        )
        chatgpt4_turbo_packages = await get_packages_by_type('GPT4')
        for chatgpt4_turbo_package in chatgpt4_turbo_packages:
            await update_package(chatgpt4_turbo_package.id, {
                'product_id': chatgpt4_turbo_product.id,
            })
        chatgpt4_turbo_transactions = await get_transactions(service=ServiceType.CHAT_GPT4_TURBO)
        for i in range(0, len(chatgpt4_turbo_transactions), config.BATCH_SIZE):
            batch = firebase.db.batch()
            chatgpt4_turbo_transaction_batch = chatgpt4_turbo_transactions[i:i + config.BATCH_SIZE]
            for chatgpt4_turbo_transaction in chatgpt4_turbo_transaction_batch:
                chatgpt4_turbo_transaction_ref = firebase.db.collection(
                    Transaction.COLLECTION_NAME
                ).document(chatgpt4_turbo_transaction.id)
                batch.update(chatgpt4_turbo_transaction_ref, {
                    'product_id': chatgpt4_turbo_product.id,
                })
            await batch.commit()
        chatgpt4_turbo_promo_codes = await get_promo_codes_by_package_type('GPT4')
        for chatgpt4_turbo_promo_code in chatgpt4_turbo_promo_codes:
            chatgpt4_turbo_promo_code.details['product_id'] = chatgpt4_turbo_product.id,
            await update_promo_code(chatgpt4_turbo_promo_code.id, {
                'details': chatgpt4_turbo_promo_code.details,
            })
        await send_message_to_admins_and_developers(bot, '<b>GPT4 migration was successful!</b> 🎉')

        # CHAT_GPT4_OMNI_MINI
        chatgpt4_omni_mini_product = await write_product(
            stripe_id='prod_RHNmr3PRsiezOI',
            is_active=True,
            type=ProductType.PACKAGE,
            category=ProductCategory.TEXT,
            names={
                'ru': 'ChatGPT 4.0 Omni Mini ✉️',
                'en': 'ChatGPT 4.0 Omni Mini ✉️',
            },
            descriptions={
                'ru': 'Разбудите мощь ChatGPT 4.0 Omni Mini для остроумных бесед, умных советов и бесконечного веселья! ✉️',
                'en': 'Unleash the power of ChatGPT 4.0 Omni Mini for witty chats, smart advice, and endless fun! ✉️',
            },
            prices={
                Currency.RUB: 1,
                Currency.USD: 0.01,
                Currency.XTR: 1,
            },
            order=0,
            details={
                'quota': Quota.CHAT_GPT4_OMNI_MINI,
            },
        )
        chatgpt4_omni_mini_packages = await get_packages_by_type(PackageType.CHAT_GPT4_OMNI_MINI)
        for chatgpt4_omni_mini_package in chatgpt4_omni_mini_packages:
            await update_package(chatgpt4_omni_mini_package.id, {
                'product_id': chatgpt4_omni_mini_product.id,
            })
        chatgpt4_omni_mini_transactions = await get_transactions(service=ServiceType.CHAT_GPT4_OMNI_MINI)
        for i in range(0, len(chatgpt4_omni_mini_transactions), config.BATCH_SIZE):
            batch = firebase.db.batch()
            chatgpt4_omni_mini_transaction_batch = chatgpt4_omni_mini_transactions[i:i + config.BATCH_SIZE]
            for chatgpt4_omni_mini_transaction in chatgpt4_omni_mini_transaction_batch:
                chatgpt4_omni_mini_transaction_ref = firebase.db.collection(
                    Transaction.COLLECTION_NAME
                ).document(chatgpt4_omni_mini_transaction.id)
                batch.update(chatgpt4_omni_mini_transaction_ref, {
                    'product_id': chatgpt4_omni_mini_product.id,
                })
            await batch.commit()
        chatgpt4_omni_mini_promo_codes = await get_promo_codes_by_package_type(PackageType.CHAT_GPT4_OMNI_MINI)
        for chatgpt4_omni_mini_promo_code in chatgpt4_omni_mini_promo_codes:
            chatgpt4_omni_mini_promo_code.details['product_id'] = chatgpt4_omni_mini_product.id,
            await update_promo_code(chatgpt4_omni_mini_promo_code.id, {
                'details': chatgpt4_omni_mini_promo_code.details,
            })
        await send_message_to_admins_and_developers(bot, '<b>CHAT_GPT4_OMNI_MINI migration was successful!</b> 🎉')
        # CHAT_GPT4_OMNI
        chatgpt4_omni_product = await write_product(
            stripe_id='prod_RHNnfx8kxnkdwC',
            is_active=True,
            type=ProductType.PACKAGE,
            category=ProductCategory.TEXT,
            names={
                'ru': 'ChatGPT 4.0 Omni 💥',
                'en': 'ChatGPT 4.0 Omni 💥',
            },
            descriptions={
                'ru': 'Откройте новые горизонты с интеллектом ChatGPT 4.0 Omni для более глубоких анализов и инновационных диалогов! 💥',
                'en': 'Discover new horizons with the intelligence of ChatGPT 4.0 Omni for deeper analyses and innovative dialogues! 💥',
            },
            prices={
                Currency.RUB: 4,
                Currency.USD: 0.04,
                Currency.XTR: 4,
            },
            order=1,
            details={
                'quota': Quota.CHAT_GPT4_OMNI,
            },
        )
        chatgpt4_omni_packages = await get_packages_by_type(PackageType.CHAT_GPT4_OMNI)
        for chatgpt4_omni_package in chatgpt4_omni_packages:
            await update_package(chatgpt4_omni_package.id, {
                'product_id': chatgpt4_omni_product.id,
            })
        chatgpt4_omni_transactions = await get_transactions(service=ServiceType.CHAT_GPT4_OMNI)
        for i in range(0, len(chatgpt4_omni_transactions), config.BATCH_SIZE):
            batch = firebase.db.batch()
            chatgpt4_omni_transaction_batch = chatgpt4_omni_transactions[i:i + config.BATCH_SIZE]
            for chatgpt4_omni_transaction in chatgpt4_omni_transaction_batch:
                chatgpt4_omni_transaction_ref = firebase.db.collection(
                    Transaction.COLLECTION_NAME
                ).document(chatgpt4_omni_transaction.id)
                batch.update(chatgpt4_omni_transaction_ref, {
                    'product_id': chatgpt4_omni_product.id,
                })
            await batch.commit()
        chatgpt4_omni_promo_codes = await get_promo_codes_by_package_type(PackageType.CHAT_GPT4_OMNI)
        for chatgpt4_omni_promo_code in chatgpt4_omni_promo_codes:
            chatgpt4_omni_promo_code.details['product_id'] = chatgpt4_omni_product.id,
            await update_promo_code(chatgpt4_omni_promo_code.id, {
                'details': chatgpt4_omni_promo_code.details,
            })
        await send_message_to_admins_and_developers(bot, '<b>CHAT_GPT4_OMNI migration was successful!</b> 🎉')
        # CHAT_GPT_O_1_MINI
        chatgpt_o_1_mini_product = await write_product(
            stripe_id='prod_RHNnp9xsxRtJhc',
            is_active=True,
            type=ProductType.PACKAGE,
            category=ProductCategory.TEXT,
            names={
                'ru': 'ChatGPT o1-mini 🧩',
                'en': 'ChatGPT o1-mini 🧩',
            },
            descriptions={
                'ru': 'Откройте новые перспективы с ChatGPT o1-mini, чтобы находить быстрые и точные решения для ваших задач! 🧩',
                'en': 'Unlock new possibilities with ChatGPT o1-mini to find quick and precise solutions for your tasks! 🧩',
            },
            prices={
                Currency.RUB: 4,
                Currency.USD: 0.04,
                Currency.XTR: 4,
            },
            order=2,
            details={
                'quota': Quota.CHAT_GPT_O_1_MINI,
            },
        )
        chatgpt_o_1_mini_packages = await get_packages_by_type(PackageType.CHAT_GPT_O_1_MINI)
        for chatgpt_o_1_mini_package in chatgpt_o_1_mini_packages:
            await update_package(chatgpt_o_1_mini_package.id, {
                'product_id': chatgpt_o_1_mini_product.id,
            })
        chatgpt_o_1_mini_transactions = await get_transactions(service=ServiceType.CHAT_GPT_O_1_MINI)
        for i in range(0, len(chatgpt_o_1_mini_transactions), config.BATCH_SIZE):
            batch = firebase.db.batch()
            chatgpt_o_1_mini_transaction_batch = chatgpt_o_1_mini_transactions[i:i + config.BATCH_SIZE]
            for chatgpt_o_1_mini_transaction in chatgpt_o_1_mini_transaction_batch:
                chatgpt_o_1_mini_transaction_ref = firebase.db.collection(
                    Transaction.COLLECTION_NAME
                ).document(chatgpt_o_1_mini_transaction.id)
                batch.update(chatgpt_o_1_mini_transaction_ref, {
                    'product_id': chatgpt_o_1_mini_product.id,
                })
            await batch.commit()
        chatgpt_o_1_mini_promo_codes = await get_promo_codes_by_package_type(PackageType.CHAT_GPT_O_1_MINI)
        for chatgpt_o_1_mini_promo_code in chatgpt_o_1_mini_promo_codes:
            chatgpt_o_1_mini_promo_code.details['product_id'] = chatgpt_o_1_mini_product.id,
            await update_promo_code(chatgpt_o_1_mini_promo_code.id, {
                'details': chatgpt_o_1_mini_promo_code.details,
            })
        await send_message_to_admins_and_developers(bot, '<b>CHAT_GPT_O_1_MINI migration was successful!</b> 🎉')
        # CHAT_GPT_O_1_PREVIEW
        chatgpt_o_1_preview_product = await write_product(
            stripe_id='prod_RHNoY55CSLKHwP',
            is_active=True,
            type=ProductType.PACKAGE,
            category=ProductCategory.TEXT,
            names={
                'ru': 'ChatGPT o1-preview 🧪',
                'en': 'ChatGPT o1-preview 🧪',
            },
            descriptions={
                'ru': 'Исследуйте будущее с ChatGPT o1-preview, совершая глубокие и логически выверенные открытия! 🧪',
                'en': 'Explore the future with ChatGPT o1-preview, making deep and logically sound discoveries! 🧪',
            },
            prices={
                Currency.RUB: 8,
                Currency.USD: 0.08,
                Currency.XTR: 8,
            },
            order=3,
            details={
                'quota': Quota.CHAT_GPT_O_1_PREVIEW,
            },
        )
        chatgpt_o_1_preview_packages = await get_packages_by_type(PackageType.CHAT_GPT_O_1_PREVIEW)
        for chatgpt_o_1_preview_package in chatgpt_o_1_preview_packages:
            await update_package(chatgpt_o_1_preview_package.id, {
                'product_id': chatgpt_o_1_preview_product.id,
            })
        chatgpt_o_1_preview_transactions = await get_transactions(service=ServiceType.CHAT_GPT_O_1_PREVIEW)
        for i in range(0, len(chatgpt_o_1_preview_transactions), config.BATCH_SIZE):
            batch = firebase.db.batch()
            chatgpt_o_1_preview_transaction_batch = chatgpt_o_1_preview_transactions[i:i + config.BATCH_SIZE]
            for chatgpt_o_1_preview_transaction in chatgpt_o_1_preview_transaction_batch:
                chatgpt_o_1_preview_transaction_ref = firebase.db.collection(
                    Transaction.COLLECTION_NAME
                ).document(chatgpt_o_1_preview_transaction.id)
                batch.update(chatgpt_o_1_preview_transaction_ref, {
                    'product_id': chatgpt_o_1_preview_product.id,
                })
            await batch.commit()
        chatgpt_o_1_preview_promo_codes = await get_promo_codes_by_package_type(PackageType.CHAT_GPT_O_1_PREVIEW)
        for chatgpt_o_1_preview_promo_code in chatgpt_o_1_preview_promo_codes:
            chatgpt_o_1_preview_promo_code.details['product_id'] = chatgpt_o_1_preview_product.id,
            await update_promo_code(chatgpt_o_1_preview_promo_code.id, {
                'details': chatgpt_o_1_preview_promo_code.details,
            })
        await send_message_to_admins_and_developers(bot, '<b>CHAT_GPT_O_1_PREVIEW migration was successful!</b> 🎉')

        # CLAUDE_3_HAIKU
        claude_3_haiku_product = await write_product(
            stripe_id='prod_RHNoE4HCiI0uJi',
            is_active=True,
            type=ProductType.PACKAGE,
            category=ProductCategory.TEXT,
            names={
                'ru': 'Claude 3.5 Haiku 📜',
                'en': 'Claude 3.5 Haiku 📜',
            },
            descriptions={
                'ru': 'Погрузитесь в мир краткости и мудрости с Claude 3.5 Haiku, где лаконичность рождает гениальные идеи! 📜',
                'en': 'Immerse yourself in the world of brevity and wisdom with Claude 3.5 Haiku! 📜',
            },
            prices={
                Currency.RUB: 1,
                Currency.USD: 0.01,
                Currency.XTR: 1,
            },
            order=4,
            details={
                'quota': Quota.CLAUDE_3_HAIKU,
            },
        )
        claude_3_haiku_packages = await get_packages_by_type(PackageType.CLAUDE_3_HAIKU)
        for claude_3_haiku_package in claude_3_haiku_packages:
            await update_package(claude_3_haiku_package.id, {
                'product_id': claude_3_haiku_product.id,
            })
        claude_3_haiku_transactions = await get_transactions(service=ServiceType.CLAUDE_3_HAIKU)
        for i in range(0, len(claude_3_haiku_transactions), config.BATCH_SIZE):
            batch = firebase.db.batch()
            claude_3_haiku_transaction_batch = claude_3_haiku_transactions[i:i + config.BATCH_SIZE]
            for claude_3_haiku_transaction in claude_3_haiku_transaction_batch:
                claude_3_haiku_transaction_ref = firebase.db.collection(
                    Transaction.COLLECTION_NAME
                ).document(claude_3_haiku_transaction.id)
                batch.update(claude_3_haiku_transaction_ref, {
                    'product_id': claude_3_haiku_product.id,
                })
            await batch.commit()
        claude_3_haiku_promo_codes = await get_promo_codes_by_package_type(PackageType.CLAUDE_3_HAIKU)
        for claude_3_haiku_promo_code in claude_3_haiku_promo_codes:
            claude_3_haiku_promo_code.details['product_id'] = claude_3_haiku_product.id,
            await update_promo_code(claude_3_haiku_promo_code.id, {
                'details': claude_3_haiku_promo_code.details,
            })
        await send_message_to_admins_and_developers(bot, '<b>CLAUDE_3_HAIKU migration was successful!</b> 🎉')
        # CLAUDE_3_SONNET
        claude_3_sonnet_product = await write_product(
            stripe_id='prod_RHNoq0gEgqVi59',
            is_active=True,
            type=ProductType.PACKAGE,
            category=ProductCategory.TEXT,
            names={
                'ru': 'Claude 3.5 Sonnet 💫',
                'en': 'Claude 3.5 Sonnet 💫',
            },
            descriptions={
                'ru': 'Исследуйте баланс скорости и интеллекта с Claude 3.5 Sonnet для точных и оперативных решений! 💫',
                'en': 'Explore the balance of speed and intelligence with Claude 3.5 Sonnet for accurate and timely solutions! 💫',
            },
            prices={
                Currency.RUB: 4,
                Currency.USD: 0.04,
                Currency.XTR: 4,
            },
            order=5,
            details={
                'quota': Quota.CLAUDE_3_SONNET,
            },
        )
        claude_3_sonnet_packages = await get_packages_by_type(PackageType.CLAUDE_3_SONNET)
        for claude_3_sonnet_package in claude_3_sonnet_packages:
            await update_package(claude_3_sonnet_package.id, {
                'product_id': claude_3_sonnet_product.id,
            })
        claude_3_sonnet_transactions = await get_transactions(service=ServiceType.CLAUDE_3_SONNET)
        for i in range(0, len(claude_3_sonnet_transactions), config.BATCH_SIZE):
            batch = firebase.db.batch()
            claude_3_sonnet_transaction_batch = claude_3_sonnet_transactions[i:i + config.BATCH_SIZE]
            for claude_3_sonnet_transaction in claude_3_sonnet_transaction_batch:
                claude_3_sonnet_transaction_ref = firebase.db.collection(
                    Transaction.COLLECTION_NAME
                ).document(claude_3_sonnet_transaction.id)
                batch.update(claude_3_sonnet_transaction_ref, {
                    'product_id': claude_3_sonnet_product.id,
                })
            await batch.commit()
        claude_3_sonnet_promo_codes = await get_promo_codes_by_package_type(PackageType.CLAUDE_3_SONNET)
        for claude_3_sonnet_promo_code in claude_3_sonnet_promo_codes:
            claude_3_sonnet_promo_code.details['product_id'] = claude_3_sonnet_product.id,
            await update_promo_code(claude_3_sonnet_promo_code.id, {
                'details': claude_3_sonnet_promo_code.details,
            })
        await send_message_to_admins_and_developers(bot, '<b>CLAUDE_3_SONNET migration was successful!</b> 🎉')
        # CLAUDE_3_OPUS
        claude_3_opus_product = await write_product(
            stripe_id='prod_RHNoEs0MGtCDDs',
            is_active=True,
            type=ProductType.PACKAGE,
            category=ProductCategory.TEXT,
            names={
                'ru': 'Claude 3.0 Opus 🚀',
                'en': 'Claude 3.0 Opus 🚀',
            },
            descriptions={
                'ru': 'Проникнитесь мощью Claude 3.0 Opus для решения самых сложных задач и создания глубоких инсайтов! 🚀',
                'en': 'Experience the power of Claude 3.0 Opus to solve the most complex challenges and create profound insights! 🚀',
            },
            prices={
                Currency.RUB: 8,
                Currency.USD: 0.08,
                Currency.XTR: 8,
            },
            order=6,
            details={
                'quota': Quota.CLAUDE_3_OPUS,
            },
        )
        claude_3_opus_packages = await get_packages_by_type(PackageType.CLAUDE_3_OPUS)
        for claude_3_opus_package in claude_3_opus_packages:
            await update_package(claude_3_opus_package.id, {
                'product_id': claude_3_opus_product.id,
            })
        claude_3_opus_transactions = await get_transactions(service=ServiceType.CLAUDE_3_OPUS)
        for i in range(0, len(claude_3_opus_transactions), config.BATCH_SIZE):
            batch = firebase.db.batch()
            claude_3_opus_transaction_batch = claude_3_opus_transactions[i:i + config.BATCH_SIZE]
            for claude_3_opus_transaction in claude_3_opus_transaction_batch:
                claude_3_opus_transaction_ref = firebase.db.collection(
                    Transaction.COLLECTION_NAME
                ).document(claude_3_opus_transaction.id)
                batch.update(claude_3_opus_transaction_ref, {
                    'product_id': claude_3_opus_product.id,
                })
            await batch.commit()
        claude_3_opus_promo_codes = await get_promo_codes_by_package_type(PackageType.CLAUDE_3_OPUS)
        for claude_3_opus_promo_code in claude_3_opus_promo_codes:
            claude_3_opus_promo_code.details['product_id'] = claude_3_opus_product.id,
            await update_promo_code(claude_3_opus_promo_code.id, {
                'details': claude_3_opus_promo_code.details,
            })
        await send_message_to_admins_and_developers(bot, '<b>CLAUDE_3_OPUS migration was successful!</b> 🎉')

        # GEMINI_1_FLASH
        gemini_1_flash_product = await write_product(
            stripe_id='prod_RHNov6pvSAOxOv',
            is_active=True,
            type=ProductType.PACKAGE,
            category=ProductCategory.TEXT,
            names={
                'ru': 'Gemini 1.5 Flash 🏎',
                'en': 'Gemini 1.5 Flash 🏎',
            },
            descriptions={
                'ru': 'Разбудите мощь Gemini 1.5 Flash для мгновенных решений, быстрых ответов и динамичных взаимодействий! 🏎',
                'en': 'Unleash the power of Gemini 1.5 Flash for instant solutions, quick responses, and dynamic interactions! 🏎',
            },
            prices={
                Currency.RUB: 1,
                Currency.USD: 0.01,
                Currency.XTR: 1,
            },
            order=7,
            details={
                'quota': Quota.GEMINI_1_FLASH,
            },
        )
        gemini_1_flash_packages = await get_packages_by_type(PackageType.GEMINI_1_FLASH)
        for gemini_1_flash_package in gemini_1_flash_packages:
            await update_package(gemini_1_flash_package.id, {
                'product_id': gemini_1_flash_product.id,
            })
        gemini_1_flash_transactions = await get_transactions(service=ServiceType.GEMINI_1_FLASH)
        for i in range(0, len(gemini_1_flash_transactions), config.BATCH_SIZE):
            batch = firebase.db.batch()
            gemini_1_flash_transaction_batch = gemini_1_flash_transactions[i:i + config.BATCH_SIZE]
            for gemini_1_flash_transaction in gemini_1_flash_transaction_batch:
                gemini_1_flash_transaction_ref = firebase.db.collection(
                    Transaction.COLLECTION_NAME
                ).document(gemini_1_flash_transaction.id)
                batch.update(gemini_1_flash_transaction_ref, {
                    'product_id': gemini_1_flash_product.id,
                })
            await batch.commit()
        gemini_1_flash_promo_codes = await get_promo_codes_by_package_type(PackageType.GEMINI_1_FLASH)
        for gemini_1_flash_promo_code in gemini_1_flash_promo_codes:
            gemini_1_flash_promo_code.details['product_id'] = gemini_1_flash_product.id,
            await update_promo_code(gemini_1_flash_promo_code.id, {
                'details': gemini_1_flash_promo_code.details,
            })
        await send_message_to_admins_and_developers(bot, '<b>GEMINI_1_FLASH migration was successful!</b> 🎉')
        # GEMINI_1_PRO
        gemini_1_pro_product = await write_product(
            stripe_id='prod_RHNp2NVU2N00o2',
            is_active=True,
            type=ProductType.PACKAGE,
            category=ProductCategory.TEXT,
            names={
                'ru': 'Gemini 1.5 Pro 💼',
                'en': 'Gemini 1.5 Pro 💼',
            },
            descriptions={
                'ru': 'Разбудите мощь Gemini 1.5 Pro для глубокого анализа, точных решений и максимальной продуктивности! 💼',
                'en': 'Unleash the power of Gemini 1.5 Pro for deep analysis, precise decisions, and maximum productivity! 💼',
            },
            prices={
                Currency.RUB: 4,
                Currency.USD: 0.04,
                Currency.XTR: 4,
            },
            order=8,
            details={
                'quota': Quota.GEMINI_1_PRO,
            },
        )
        gemini_1_pro_packages = await get_packages_by_type(PackageType.GEMINI_1_PRO)
        for gemini_1_pro_package in gemini_1_pro_packages:
            await update_package(gemini_1_pro_package.id, {
                'product_id': gemini_1_pro_product.id,
            })
        gemini_1_pro_transactions = await get_transactions(service=ServiceType.GEMINI_1_PRO)
        for i in range(0, len(gemini_1_pro_transactions), config.BATCH_SIZE):
            batch = firebase.db.batch()
            gemini_1_pro_transaction_batch = gemini_1_pro_transactions[i:i + config.BATCH_SIZE]
            for gemini_1_pro_transaction in gemini_1_pro_transaction_batch:
                gemini_1_pro_transaction_ref = firebase.db.collection(
                    Transaction.COLLECTION_NAME
                ).document(gemini_1_pro_transaction.id)
                batch.update(gemini_1_pro_transaction_ref, {
                    'product_id': gemini_1_pro_product.id,
                })
            await batch.commit()
        gemini_1_pro_promo_codes = await get_promo_codes_by_package_type(PackageType.GEMINI_1_PRO)
        for gemini_1_pro_promo_code in gemini_1_pro_promo_codes:
            gemini_1_pro_promo_code.details['product_id'] = gemini_1_pro_product.id,
            await update_promo_code(gemini_1_pro_promo_code.id, {
                'details': gemini_1_pro_promo_code.details,
            })
        await send_message_to_admins_and_developers(bot, '<b>GEMINI_1_PRO migration was successful!</b> 🎉')
        # GEMINI_1_ULTRA
        gemini_1_ultra_product = await write_product(
            stripe_id='prod_RHNqfsnNOBhwbK',
            is_active=True,
            type=ProductType.PACKAGE,
            category=ProductCategory.TEXT,
            names={
                'ru': 'Gemini 1.0 Ultra 🛡',
                'en': 'Gemini 1.0 Ultra 🛡',
            },
            descriptions={
                'ru': 'Воспользуйтесь силой Gemini 1.0 Ultra для решения самых сложных задач и достижений на новых высотах! 🛡',
                'en': 'Harness the power of Gemini 1.0 Ultra to tackle the most complex challenges and reach new heights! 🛡',
            },
            prices={
                Currency.RUB: 8,
                Currency.USD: 0.08,
                Currency.XTR: 8,
            },
            order=9,
            details={
                'quota': Quota.GEMINI_1_ULTRA,
            },
        )
        gemini_1_ultra_packages = await get_packages_by_type(PackageType.GEMINI_1_ULTRA)
        for gemini_1_ultra_package in gemini_1_ultra_packages:
            await update_package(gemini_1_ultra_package.id, {
                'product_id': gemini_1_ultra_product.id,
            })
        gemini_1_ultra_transactions = await get_transactions(service=ServiceType.GEMINI_1_ULTRA)
        for i in range(0, len(gemini_1_ultra_transactions), config.BATCH_SIZE):
            batch = firebase.db.batch()
            gemini_1_ultra_transaction_batch = gemini_1_ultra_transactions[i:i + config.BATCH_SIZE]
            for gemini_1_ultra_transaction in gemini_1_ultra_transaction_batch:
                gemini_1_ultra_transaction_ref = firebase.db.collection(
                    Transaction.COLLECTION_NAME
                ).document(gemini_1_ultra_transaction.id)
                batch.update(gemini_1_ultra_transaction_ref, {
                    'product_id': gemini_1_ultra_product.id,
                })
            await batch.commit()
        gemini_1_ultra_promo_codes = await get_promo_codes_by_package_type(PackageType.GEMINI_1_ULTRA)
        for gemini_1_ultra_promo_code in gemini_1_ultra_promo_codes:
            gemini_1_ultra_promo_code.details['product_id'] = gemini_1_ultra_product.id,
            await update_promo_code(gemini_1_ultra_promo_code.id, {
                'details': gemini_1_ultra_promo_code.details,
            })
        await send_message_to_admins_and_developers(bot, '<b>GEMINI_1_ULTRA migration was successful!</b> 🎉')

        # DALL_E
        dall_e_product = await write_product(
            stripe_id='prod_RHNqijlBdOxmCP',
            is_active=True,
            type=ProductType.PACKAGE,
            category=ProductCategory.IMAGE,
            names={
                'ru': 'DALL-E 👨‍🎨',
                'en': 'DALL-E 👨‍🎨',
            },
            descriptions={
                'ru': 'Превратите свои идеи в искусство с помощью DALL-E – там, где ваше воображение становится поразительной визуальной реальностью! 👨‍🎨',
                'en': 'Turn ideas into art with DALL-E – where your imagination becomes stunning visual reality! 👨‍🎨',
            },
            prices={
                Currency.RUB: 8,
                Currency.USD: 0.08,
                Currency.XTR: 8,
            },
            order=0,
            details={
                'quota': Quota.DALL_E,
            },
        )
        dall_e_packages = await get_packages_by_type(PackageType.DALL_E)
        for dall_e_package in dall_e_packages:
            await update_package(dall_e_package.id, {
                'product_id': dall_e_product.id,
            })
        dall_e_transactions = await get_transactions(service=ServiceType.DALL_E)
        for i in range(0, len(dall_e_transactions), config.BATCH_SIZE):
            batch = firebase.db.batch()
            dall_e_transaction_batch = dall_e_transactions[i:i + config.BATCH_SIZE]
            for dall_e_transaction in dall_e_transaction_batch:
                dall_e_transaction_ref = firebase.db.collection(
                    Transaction.COLLECTION_NAME
                ).document(dall_e_transaction.id)
                batch.update(dall_e_transaction_ref, {
                    'product_id': dall_e_product.id,
                })
            await batch.commit()
        dall_e_promo_codes = await get_promo_codes_by_package_type(PackageType.DALL_E)
        for dall_e_promo_code in dall_e_promo_codes:
            dall_e_promo_code.details['product_id'] = dall_e_product.id,
            await update_promo_code(dall_e_promo_code.id, {
                'details': dall_e_promo_code.details,
            })
        await send_message_to_admins_and_developers(bot, '<b>DALL_E migration was successful!</b> 🎉')
        # MIDJOURNEY
        midjourney_product = await write_product(
            stripe_id='prod_RHNrVDhpUAvoAF',
            is_active=True,
            type=ProductType.PACKAGE,
            category=ProductCategory.IMAGE,
            names={
                'ru': 'Midjourney 🎨',
                'en': 'Midjourney 🎨',
            },
            descriptions={
                'ru': 'Раскройте свой творческий потенциал с Midjourney – превращайте ваши мысли в великолепные визуальные произведения искусства! 🎨',
                'en': 'Unleash your creativity with Midjourney – transform your thoughts into magnificent visual works of art! 🎨',
            },
            prices={
                Currency.RUB: 8,
                Currency.USD: 0.08,
                Currency.XTR: 8,
            },
            order=1,
            details={
                'quota': Quota.MIDJOURNEY,
                'has_reactions': True,
            },
        )
        midjourney_requests = await get_requests_by_model(model=Model.MIDJOURNEY)
        for midjourney_request in midjourney_requests:
            await update_request(midjourney_request.id, {
                'product_id': midjourney_product.id,
            })
        midjourney_generations = await get_generations_by_model(model=Model.MIDJOURNEY)
        for midjourney_generation in midjourney_generations:
            await update_generation(midjourney_generation.id, {
                'product_id': midjourney_product.id,
            })
        midjourney_packages = await get_packages_by_type(PackageType.MIDJOURNEY)
        for midjourney_package in midjourney_packages:
            await update_package(midjourney_package.id, {
                'product_id': midjourney_product.id,
            })
        midjourney_transactions = await get_transactions(service=ServiceType.MIDJOURNEY)
        for i in range(0, len(midjourney_transactions), config.BATCH_SIZE):
            batch = firebase.db.batch()
            midjourney_transaction_batch = midjourney_transactions[i:i + config.BATCH_SIZE]
            for midjourney_transaction in midjourney_transaction_batch:
                midjourney_transaction_ref = firebase.db.collection(
                    Transaction.COLLECTION_NAME
                ).document(midjourney_transaction.id)
                batch.update(midjourney_transaction_ref, {
                    'product_id': midjourney_product.id,
                })
            await batch.commit()
        midjourney_promo_codes = await get_promo_codes_by_package_type(PackageType.MIDJOURNEY)
        for midjourney_promo_code in midjourney_promo_codes:
            midjourney_promo_code.details['product_id'] = midjourney_product.id,
            await update_promo_code(midjourney_promo_code.id, {
                'details': midjourney_promo_code.details,
            })
        await send_message_to_admins_and_developers(bot, '<b>MIDJOURNEY migration was successful!</b> 🎉')
        # STABLE_DIFFUSION
        stable_diffusion_product = await write_product(
            stripe_id='prod_RHNr4qfz3kJjZB',
            is_active=True,
            type=ProductType.PACKAGE,
            category=ProductCategory.IMAGE,
            names={
                'ru': 'Stable Diffusion 3.5 🎆',
                'en': 'Stable Diffusion 3.5 🎆',
            },
            descriptions={
                'ru': 'Откройте дверь в мир творчества с Stable Diffusion — превращайте свои идеи в изображения, которые поражают воображение! 🎆',
                'en': 'Open the door to a world of creativity with Stable Diffusion — transform your ideas into stunning images! 🎆',
            },
            prices={
                Currency.RUB: 8,
                Currency.USD: 0.08,
                Currency.XTR: 8,
            },
            order=2,
            details={
                'quota': Quota.STABLE_DIFFUSION,
                'has_reactions': True,
            },
        )
        stable_diffusion_requests = await get_requests_by_model(model=Model.STABLE_DIFFUSION)
        for stable_diffusion_request in stable_diffusion_requests:
            await update_request(stable_diffusion_request.id, {
                'product_id': stable_diffusion_product.id,
            })
        stable_diffusion_generations = await get_generations_by_model(model=Model.STABLE_DIFFUSION)
        for stable_diffusion_generation in stable_diffusion_generations:
            await update_generation(stable_diffusion_generation.id, {
                'product_id': stable_diffusion_product.id,
            })
        stable_diffusion_packages = await get_packages_by_type(PackageType.STABLE_DIFFUSION)
        for stable_diffusion_package in stable_diffusion_packages:
            await update_package(stable_diffusion_package.id, {
                'product_id': stable_diffusion_product.id,
            })
        stable_diffusion_transactions = await get_transactions(service=ServiceType.STABLE_DIFFUSION)
        for i in range(0, len(stable_diffusion_transactions), config.BATCH_SIZE):
            batch = firebase.db.batch()
            stable_diffusion_transaction_batch = stable_diffusion_transactions[i:i + config.BATCH_SIZE]
            for stable_diffusion_transaction in stable_diffusion_transaction_batch:
                stable_diffusion_transaction_ref = firebase.db.collection(
                    Transaction.COLLECTION_NAME
                ).document(stable_diffusion_transaction.id)
                batch.update(stable_diffusion_transaction_ref, {
                    'product_id': stable_diffusion_product.id,
                })
            await batch.commit()
        stable_diffusion_promo_codes = await get_promo_codes_by_package_type(PackageType.STABLE_DIFFUSION)
        for stable_diffusion_promo_code in stable_diffusion_promo_codes:
            stable_diffusion_promo_code.details['product_id'] = stable_diffusion_product.id,
            await update_promo_code(stable_diffusion_promo_code.id, {
                'details': stable_diffusion_promo_code.details,
            })
        await send_message_to_admins_and_developers(bot, '<b>STABLE_DIFFUSION migration was successful!</b> 🎉')
        # FLUX
        flux_product = await write_product(
            stripe_id='prod_RHNrAc0WIEbR2h',
            is_active=True,
            type=ProductType.PACKAGE,
            category=ProductCategory.IMAGE,
            names={
                'ru': 'Flux 1.1 Pro 🫐',
                'en': 'Flux 1.1 Pro 🫐',
            },
            descriptions={
                'ru': 'Исследуйте визуальные вариации с Flux — экспериментируйте и создавайте уникальные изображения! 🫐',
                'en': 'Explore visual variations with Flux — experiment and create unique images! 🫐',
            },
            prices={
                Currency.RUB: 8,
                Currency.USD: 0.08,
                Currency.XTR: 8,
            },
            order=3,
            details={
                'quota': Quota.FLUX,
                'has_reactions': True,
            },
        )
        flux_requests = await get_requests_by_model(model=Model.FLUX)
        for flux_request in flux_requests:
            await update_request(flux_request.id, {
                'product_id': flux_product.id,
            })
        flux_generations = await get_generations_by_model(model=Model.FLUX)
        for flux_generation in flux_generations:
            await update_generation(flux_generation.id, {
                'product_id': flux_product.id,
            })
        flux_packages = await get_packages_by_type(PackageType.FLUX)
        for flux_package in flux_packages:
            await update_package(flux_package.id, {
                'product_id': flux_product.id,
            })
        flux_transactions = await get_transactions(service=ServiceType.FLUX)
        for i in range(0, len(flux_transactions), config.BATCH_SIZE):
            batch = firebase.db.batch()
            flux_transaction_batch = flux_transactions[i:i + config.BATCH_SIZE]
            for flux_transaction in flux_transaction_batch:
                flux_transaction_ref = firebase.db.collection(
                    Transaction.COLLECTION_NAME
                ).document(flux_transaction.id)
                batch.update(flux_transaction_ref, {
                    'product_id': flux_product.id,
                })
            await batch.commit()
        flux_promo_codes = await get_promo_codes_by_package_type(PackageType.FLUX)
        for flux_promo_code in flux_promo_codes:
            flux_promo_code.details['product_id'] = flux_product.id,
            await update_promo_code(flux_promo_code.id, {
                'details': flux_promo_code.details,
            })
        await send_message_to_admins_and_developers(bot, '<b>FLUX migration was successful!</b> 🎉')
        # FACE_SWAP
        face_swap_product = await write_product(
            stripe_id='prod_RHNrBTAHqhMreX',
            is_active=True,
            type=ProductType.PACKAGE,
            category=ProductCategory.IMAGE,
            names={
                'ru': 'FaceSwap 📷',
                'en': 'FaceSwap 📷',
            },
            descriptions={
                'ru': 'Погрузитесь в игровой мир замены лиц для смеха и удивления на каждом изображении! 📷',
                'en': 'Enter the playful world of FaceSwap for laughs and surprises in every image! 📷',
            },
            prices={
                Currency.RUB: 8,
                Currency.USD: 0.08,
                Currency.XTR: 8,
            },
            order=4,
            details={
                'quota': Quota.FACE_SWAP,
                'has_reactions': True,
            },
        )
        face_swap_requests = await get_requests_by_model(model=Model.FACE_SWAP)
        for face_swap_request in face_swap_requests:
            await update_request(face_swap_request.id, {
                'product_id': face_swap_product.id,
            })
        face_swap_generations = await get_generations_by_model(model=Model.FACE_SWAP)
        for face_swap_generation in face_swap_generations:
            await update_generation(face_swap_generation.id, {
                'product_id': face_swap_product.id,
            })
        face_swap_packages = await get_packages_by_type(PackageType.FACE_SWAP)
        for face_swap_package in face_swap_packages:
            await update_package(face_swap_package.id, {
                'product_id': face_swap_product.id,
            })
        face_swap_transactions = await get_transactions(service=ServiceType.FACE_SWAP)
        for i in range(0, len(face_swap_transactions), config.BATCH_SIZE):
            batch = firebase.db.batch()
            face_swap_transaction_batch = face_swap_transactions[i:i + config.BATCH_SIZE]
            for face_swap_transaction in face_swap_transaction_batch:
                face_swap_transaction_ref = firebase.db.collection(
                    Transaction.COLLECTION_NAME
                ).document(face_swap_transaction.id)
                batch.update(face_swap_transaction_ref, {
                    'product_id': face_swap_product.id,
                })
            await batch.commit()
        face_swap_promo_codes = await get_promo_codes_by_package_type(PackageType.FACE_SWAP)
        for face_swap_promo_code in face_swap_promo_codes:
            face_swap_promo_code.details['product_id'] = face_swap_product.id,
            await update_promo_code(face_swap_promo_code.id, {
                'details': face_swap_promo_code.details,
            })
        await send_message_to_admins_and_developers(bot, '<b>FACE_SWAP migration was successful!</b> 🎉')
        # PHOTOSHOP_AI
        photoshop_ai_product = await write_product(
            stripe_id='prod_RHNs4YG7pCMIKf',
            is_active=True,
            type=ProductType.PACKAGE,
            category=ProductCategory.IMAGE,
            names={
                'ru': 'Photoshop AI 🪄',
                'en': 'Photoshop AI 🪄',
            },
            descriptions={
                'ru': 'Творите без границ с Photoshop AI, превращая каждую фотографию в шедевр! 🪄',
                'en': 'Create without limits with Photoshop AI, turning every photo into a masterpiece! 🪄',
            },
            prices={
                Currency.RUB: 8,
                Currency.USD: 0.08,
                Currency.XTR: 8,
            },
            order=5,
            details={
                'quota': Quota.PHOTOSHOP_AI,
                'has_reactions': True,
            },
        )
        photoshop_ai_requests = await get_requests_by_model(model=Model.PHOTOSHOP_AI)
        for photoshop_ai_request in photoshop_ai_requests:
            await update_request(photoshop_ai_request.id, {
                'product_id': photoshop_ai_product.id,
            })
        photoshop_ai_generations = await get_generations_by_model(model=Model.PHOTOSHOP_AI)
        for photoshop_ai_generation in photoshop_ai_generations:
            await update_generation(photoshop_ai_generation.id, {
                'product_id': photoshop_ai_product.id,
            })
        photoshop_ai_packages = await get_packages_by_type(PackageType.PHOTOSHOP_AI)
        for photoshop_ai_package in photoshop_ai_packages:
            await update_package(photoshop_ai_package.id, {
                'product_id': photoshop_ai_product.id,
            })
        photoshop_ai_transactions = await get_transactions(service=ServiceType.PHOTOSHOP_AI)
        for i in range(0, len(photoshop_ai_transactions), config.BATCH_SIZE):
            batch = firebase.db.batch()
            photoshop_ai_transaction_batch = photoshop_ai_transactions[i:i + config.BATCH_SIZE]
            for photoshop_ai_transaction in photoshop_ai_transaction_batch:
                photoshop_ai_transaction_ref = firebase.db.collection(
                    Transaction.COLLECTION_NAME
                ).document(photoshop_ai_transaction.id)
                batch.update(photoshop_ai_transaction_ref, {
                    'product_id': photoshop_ai_product.id,
                })
            await batch.commit()
        photoshop_ai_promo_codes = await get_promo_codes_by_package_type(PackageType.PHOTOSHOP_AI)
        for photoshop_ai_promo_code in photoshop_ai_promo_codes:
            photoshop_ai_promo_code.details['product_id'] = photoshop_ai_product.id,
            await update_promo_code(photoshop_ai_promo_code.id, {
                'details': photoshop_ai_promo_code.details,
            })
        await send_message_to_admins_and_developers(bot, '<b>PHOTOSHOP_AI migration was successful!</b> 🎉')

        # MUSIC_GEN
        music_gen_product = await write_product(
            stripe_id='prod_RHNsuN9ktAhJjw',
            is_active=True,
            type=ProductType.PACKAGE,
            category=ProductCategory.MUSIC,
            names={
                'ru': 'MusicGen 🎺',
                'en': 'MusicGen 🎺',
            },
            descriptions={
                'ru': 'Откройте для себя мир, где каждый промпт превращается в уникальную мелодию! 🎺',
                'en': 'Discover a world where every prompt turns into a unique melody! 🎺',
            },
            prices={
                Currency.RUB: 20,
                Currency.USD: 0.20,
                Currency.XTR: 20,
            },
            order=0,
            details={
                'quota': Quota.MUSIC_GEN,
                'has_reactions': True,
            },
        )
        music_gen_requests = await get_requests_by_model(model=Model.MUSIC_GEN)
        for music_gen_request in music_gen_requests:
            await update_request(music_gen_request.id, {
                'product_id': music_gen_product.id,
            })
        music_gen_generations = await get_generations_by_model(model=Model.MUSIC_GEN)
        for music_gen_generation in music_gen_generations:
            await update_generation(music_gen_generation.id, {
                'product_id': music_gen_product.id,
            })
        music_gen_packages = await get_packages_by_type(PackageType.MUSIC_GEN)
        for music_gen_package in music_gen_packages:
            await update_package(music_gen_package.id, {
                'product_id': music_gen_product.id,
            })
        music_gen_transactions = await get_transactions(service=ServiceType.MUSIC_GEN)
        for i in range(0, len(music_gen_transactions), config.BATCH_SIZE):
            batch = firebase.db.batch()
            music_gen_transaction_batch = music_gen_transactions[i:i + config.BATCH_SIZE]
            for music_gen_transaction in music_gen_transaction_batch:
                music_gen_transaction_ref = firebase.db.collection(
                    Transaction.COLLECTION_NAME
                ).document(music_gen_transaction.id)
                batch.update(music_gen_transaction_ref, {
                    'product_id': music_gen_product.id,
                })
            await batch.commit()
        music_gen_promo_codes = await get_promo_codes_by_package_type(PackageType.MUSIC_GEN)
        for music_gen_promo_code in music_gen_promo_codes:
            music_gen_promo_code.details['product_id'] = music_gen_product.id,
            await update_promo_code(music_gen_promo_code.id, {
                'details': music_gen_promo_code.details,
            })
        await send_message_to_admins_and_developers(bot, '<b>MUSIC_GEN migration was successful!</b> 🎉')
        # SUNO
        suno_product = await write_product(
            stripe_id='prod_RHNsxMchoJzawB',
            is_active=True,
            type=ProductType.PACKAGE,
            category=ProductCategory.MUSIC,
            names={
                'ru': 'Suno 4.0 🎸',
                'en': 'Suno 4.0 🎸',
            },
            descriptions={
                'ru': 'Попробуйте мир, где каждый ваш текст превращается в уникальную песню! 🎸',
                'en': 'Discover a world where every text you write is transformed into a unique song! 🎸',
            },
            prices={
                Currency.RUB: 4,
                Currency.USD: 0.04,
                Currency.XTR: 4,
            },
            order=1,
            details={
                'quota': Quota.SUNO,
                'has_reactions': True,
            },
        )
        suno_requests = await get_requests_by_model(model=Model.SUNO)
        for suno_request in suno_requests:
            await update_request(suno_request.id, {
                'product_id': suno_product.id,
            })
        suno_generations = await get_generations_by_model(model=Model.FLUX)
        for suno_generation in suno_generations:
            await update_generation(suno_generation.id, {
                'product_id': suno_product.id,
            })
        suno_packages = await get_packages_by_type(PackageType.SUNO)
        for suno_package in suno_packages:
            await update_package(suno_package.id, {
                'product_id': suno_product.id,
            })
        suno_transactions = await get_transactions(service=ServiceType.SUNO)
        for i in range(0, len(suno_transactions), config.BATCH_SIZE):
            batch = firebase.db.batch()
            suno_transaction_batch = suno_transactions[i:i + config.BATCH_SIZE]
            for suno_transaction in suno_transaction_batch:
                suno_transaction_ref = firebase.db.collection(
                    Transaction.COLLECTION_NAME
                ).document(suno_transaction.id)
                batch.update(suno_transaction_ref, {
                    'product_id': suno_product.id,
                })
            await batch.commit()
        suno_promo_codes = await get_promo_codes_by_package_type(PackageType.SUNO)
        for suno_promo_code in suno_promo_codes:
            suno_promo_code.details['product_id'] = suno_product.id,
            await update_promo_code(suno_promo_code.id, {
                'details': suno_promo_code.details,
            })
        await send_message_to_admins_and_developers(bot, '<b>SUNO migration was successful!</b> 🎉')

        # CHAT
        chat_product = await write_product(
            stripe_id='prod_RHNucovOmmyk60',
            is_active=True,
            type=ProductType.PACKAGE,
            category=ProductCategory.OTHER,
            names={
                'ru': 'Тематические чаты 💬',
                'en': 'Thematic chats 💬',
            },
            descriptions={
                'ru': 'Окунитесь в интересные темы с тематическими чатами, направляемыми AI в мире индивидуальных дискуссий! 💬',
                'en': 'Dive into topics you love with Thematic Chats, guided by AI in a world of tailored discussions! 💬',
            },
            prices={
                Currency.RUB: 10,
                Currency.USD: 0.1,
                Currency.XTR: 10,
            },
            order=0,
            details={
                'quota': Quota.ADDITIONAL_CHATS,
            },
        )
        chat_packages = await get_packages_by_type(PackageType.CHAT)
        for chat_package in chat_packages:
            await update_package(chat_package.id, {
                'product_id': chat_product.id,
            })
        chat_transactions = await get_transactions(service=ServiceType.ADDITIONAL_CHATS)
        for chat_transaction in chat_transactions:
            await update_transaction(chat_transaction.id, {
                'product_id': chat_product.id,
            })
        chat_promo_codes = await get_promo_codes_by_package_type(PackageType.CHAT)
        for chat_promo_code in chat_promo_codes:
            chat_promo_code.details['product_id'] = chat_product.id,
            await update_promo_code(chat_promo_code.id, {
                'details': chat_promo_code.details,
            })
        await send_message_to_admins_and_developers(bot, '<b>CHAT migration was successful!</b> 🎉')
        # ACCESS_TO_CATALOG
        access_to_catalog_product = await write_product(
            stripe_id='prod_RHNu52alX6deIg',
            is_active=True,
            type=ProductType.PACKAGE,
            category=ProductCategory.OTHER,
            names={
                'ru': 'Доступ к каталогу с цифровыми сотрудниками 🎭',
                'en': 'Access to the Digital Staff Catalog 🎭',
            },
            descriptions={
                'ru': 'Откройте вселенную специализированных AI-помощников с доступом к эксклюзивному каталогу, где каждая роль адаптирована под ваши уникальные потребности и задачи! 🎭',
                'en': 'Unlock a universe of specialized AI assistants with access to an exclusive catalog, where every role is tailored to fit your unique needs and tasks! 🎭',
            },
            prices={
                Currency.RUB: 20,
                Currency.USD: 0.2,
                Currency.XTR: 20,
            },
            order=1,
            details={
                'quota': Quota.ACCESS_TO_CATALOG,
                'is_recurring': True,
            },
        )
        access_to_catalog_packages = await get_packages_by_type(PackageType.ACCESS_TO_CATALOG)
        for access_to_catalog_package in access_to_catalog_packages:
            await update_package(access_to_catalog_package.id, {
                'product_id': access_to_catalog_product.id,
            })
        access_to_catalog_transactions = await get_transactions(service=ServiceType.ACCESS_TO_CATALOG)
        for access_to_catalog_transaction in access_to_catalog_transactions:
            await update_transaction(access_to_catalog_transaction.id, {
                'product_id': access_to_catalog_product.id,
            })
        access_to_catalog_promo_codes = await get_promo_codes_by_package_type(PackageType.ACCESS_TO_CATALOG)
        for access_to_catalog_promo_code in access_to_catalog_promo_codes:
            access_to_catalog_promo_code.details['product_id'] = access_to_catalog_product.id,
            await update_promo_code(access_to_catalog_promo_code.id, {
                'details': access_to_catalog_promo_code.details,
            })
        await send_message_to_admins_and_developers(bot, '<b>ACCESS_TO_CATALOG migration was successful!</b> 🎉')
        # VOICE_MESSAGES
        voice_messages_product = await write_product(
            stripe_id='prod_RHNu76DLiwtAYq',
            is_active=True,
            type=ProductType.PACKAGE,
            category=ProductCategory.OTHER,
            names={
                'ru': 'Голосовые ответы и запросы 🎙',
                'en': 'Voice Answers and Requests 🎙',
            },
            descriptions={
                'ru': 'Ощутите удобство и простоту голосового общения с нашим AI: отправляйте и получайте голосовые сообщения для более динамичного и выразительного взаимодействия! 🎙',
                'en': 'Experience the ease and convenience of voice communication with our AI: Send and receive voice messages for a more dynamic and expressive interaction! 🎙',
            },
            prices={
                Currency.RUB: 50,
                Currency.USD: 0.5,
                Currency.XTR: 50,
            },
            order=2,
            details={
                'quota': Quota.VOICE_MESSAGES,
                'is_recurring': True,
            },
        )
        voice_messages_packages = await get_packages_by_type(PackageType.VOICE_MESSAGES)
        for voice_messages_package in voice_messages_packages:
            await update_package(voice_messages_package.id, {
                'product_id': voice_messages_product.id,
            })
        voice_messages_transactions = await get_transactions(service=ServiceType.VOICE_MESSAGES)
        for voice_messages_transaction in voice_messages_transactions:
            await update_transaction(voice_messages_transaction.id, {
                'product_id': voice_messages_product.id,
            })
        voice_messages_promo_codes = await get_promo_codes_by_package_type(PackageType.VOICE_MESSAGES)
        for voice_messages_promo_code in voice_messages_promo_codes:
            voice_messages_promo_code.details['product_id'] = voice_messages_product.id,
            await update_promo_code(voice_messages_promo_code.id, {
                'details': voice_messages_promo_code.details,
            })
        await send_message_to_admins_and_developers(bot, '<b>VOICE_MESSAGES migration was successful!</b> 🎉')
        # FAST_MESSAGES
        fast_messages_product = await write_product(
            stripe_id='prod_RHNuT0Qr4VmKrk',
            is_active=True,
            type=ProductType.PACKAGE,
            category=ProductCategory.OTHER,
            names={
                'ru': 'Быстрые ответы без пауз ⚡',
                'en': 'Fast Answers Without Pauses ⚡',
            },
            descriptions={
                'ru': 'Функция \'Быстрые ответы без пауз\' предлагает мгновенные, точные ответы AI, обеспечивая ваше преимущество в общении! ⚡',
                'en': 'Quick Messages feature offers lightning-fast, accurate AI responses, ensuring you are always a step ahead in communication! ⚡',
            },
            prices={
                Currency.RUB: 20,
                Currency.USD: 0.2,
                Currency.XTR: 20,
            },
            order=3,
            details={
                'quota': Quota.FAST_MESSAGES,
                'is_recurring': True,
            },
        )
        fast_messages_packages = await get_packages_by_type(PackageType.FAST_MESSAGES)
        for fast_messages_package in fast_messages_packages:
            await update_package(fast_messages_package.id, {
                'product_id': fast_messages_product.id,
            })
        fast_messages_transactions = await get_transactions(service=ServiceType.FAST_MESSAGES)
        for fast_messages_transaction in fast_messages_transactions:
            await update_transaction(fast_messages_transaction.id, {
                'product_id': fast_messages_product.id,
            })
        fast_messages_promo_codes = await get_promo_codes_by_package_type(PackageType.FAST_MESSAGES)
        for fast_messages_promo_code in fast_messages_promo_codes:
            fast_messages_promo_code.details['product_id'] = fast_messages_product.id,
            await update_promo_code(fast_messages_promo_code.id, {
                'details': fast_messages_promo_code.details,
            })
        await send_message_to_admins_and_developers(bot, '<b>FAST_MESSAGES migration was successful!</b> 🎉')

        server_transactions = await get_transactions(service=ServiceType.SERVER)
        for server_transaction in server_transactions:
            await update_transaction(server_transaction.id, {
                'product_id': ServiceType.SERVER,
            })
        await send_message_to_admins_and_developers(bot, '<b>SERVER migration was successful!</b> 🎉')
        database_transactions = await get_transactions(service=ServiceType.DATABASE)
        for database_transaction in database_transactions:
            await update_transaction(database_transaction.id, {
                'product_id': ServiceType.SERVER,
            })
        await send_message_to_admins_and_developers(bot, '<b>DATABASE migration was successful!</b> 🎉')
        other_transactions = await get_transactions(service=ServiceType.OTHER)
        for other_transaction in other_transactions:
            await update_transaction(other_transaction.id, {
                'product_id': ServiceType.OTHER,
            })
        await send_message_to_admins_and_developers(bot, '<b>OTHER migration was successful!</b> 🎉')

        await send_message_to_admins_and_developers(bot, '<b>The first database migration was successful!</b> 🎉')
    except Exception as e:
        logging.exception('Error in migration', e)
        await send_message_to_admins_and_developers(
            bot,
            f'The first database migration was not successful! 🚨\n\n{e}',
            parse_mode=None,
        )

    try:
        current_date = datetime.now(timezone.utc)

        await send_message_to_admins_and_developers(bot, '<b>Second migration started!</b>')

        users = await get_users()
        for i in range(0, len(users), config.BATCH_SIZE):
            batch = firebase.db.batch()
            user_batch = users[i:i + config.BATCH_SIZE]

            for user in user_batch:
                user_ref = firebase.db.collection(User.COLLECTION_NAME).document(user.id)

                full_name = user.first_name
                if user.last_name:
                    full_name += f' {user.last_name}'

                # create user in firebase
                try:
                    firebase.auth.get_user(user.id)
                except firebase.auth.UserNotFoundError:
                    try:
                        photo_path = f'users/avatars/{user.id}.jpeg'
                        photo = await firebase.bucket.get_blob(photo_path)
                        photo_url = firebase.get_public_url(photo.name)
                    except aiohttp.ClientResponseError:
                        photo_url = None

                    firebase.auth.create_user(
                        uid=user.id,
                        display_name=full_name,
                        photo_url=photo_url,
                    )
                # create user in stripe
                if not user.stripe_id:
                    stripe_customer = await stripe.Customer.create_async(
                        name=full_name,
                    )
                    user.stripe_id = stripe_customer.id

                # settings
                user.settings[Model.SUNO][UserSettings.VERSION] = SunoVersion.V4

                batch.update(user_ref, {
                    'stripe_id': user.stripe_id,
                    'settings': user.settings,
                    'edited_at': current_date,
                })

            await batch.commit()
        await send_message_to_admins_and_developers(bot, '<b>USERS migration was successful!</b> 🎉')

        carts = await get_carts()
        for i in range(0, len(carts), config.BATCH_SIZE):
            batch = firebase.db.batch()
            cart_batch = carts[i:i + config.BATCH_SIZE]

            for cart in cart_batch:
                cart_ref = firebase.db.collection(Cart.COLLECTION_NAME).document(cart.id)

                batch.update(cart_ref, {
                    'items': [],
                    'edited_at': current_date,
                })

            await batch.commit()
        await send_message_to_admins_and_developers(bot, '<b>CARTS migration was successful!</b> 🎉')

        await send_message_to_admins_and_developers(bot, '<b>The second database migration was successful!</b> 🎉')
    except Exception as e:
        logging.exception('Error in migration', e)
        await send_message_to_admins_and_developers(
            bot,
            f'The second database migration was not successful! 🚨\n\n{e}',
            parse_mode=None,
        )

    # TODO ONLY AFTER RELEASE
    try:
        await send_message_to_admins_and_developers(bot, '<b>Third migration started!</b>')

        subscriptions = await get_subscriptions()
        for subscription in subscriptions:
            await update_subscription(subscription.id, {
                'subscription_type': DELETE_FIELD,
            })
        await send_message_to_admins_and_developers(bot, '<b>SUBSCRIPTIONS migration was successful!</b> 🎉')

        packages = await get_packages()
        for package in packages:
            await update_package(package.id, {
                'package_type': DELETE_FIELD,
            })
        await send_message_to_admins_and_developers(bot, '<b>PACKAGES migration was successful!</b> 🎉')

        promo_codes = await get_promo_codes()
        for promo_code in promo_codes:
            if promo_code.details.get('subscription_type'):
                promo_code.details['subscription_type'] = DELETE_FIELD
            if promo_code.details.get('package_type'):
                promo_code.details['package_type'] = DELETE_FIELD
            await update_promo_code(promo_code.id, {
                'details': promo_code.details,
            })
        await send_message_to_admins_and_developers(bot, '<b>PROMO_CODES migration was successful!</b> 🎉')

        users = await get_users()
        for i in range(0, len(users), config.BATCH_SIZE):
            batch = firebase.db.batch()
            user_batch = users[i:i + config.BATCH_SIZE]

            for user in user_batch:
                user_ref = firebase.db.collection(Generation.COLLECTION_NAME).document(user.id)

                batch.update(user_ref, {
                    'subscription_type': DELETE_FIELD,
                })
            await batch.commit()
        await send_message_to_admins_and_developers(bot, '<b>USERS migration was successful!</b> 🎉')

        requests = await get_requests()
        for i in range(0, len(requests), config.BATCH_SIZE):
            batch = firebase.db.batch()
            request_batch = requests[i:i + config.BATCH_SIZE]

            for request in request_batch:
                request_ref = firebase.db.collection(Generation.COLLECTION_NAME).document(request.id)

                batch.update(request_ref, {
                    'model': DELETE_FIELD,
                })
            await batch.commit()
        await send_message_to_admins_and_developers(bot, '<b>REQUESTS migration was successful!</b> 🎉')

        generations = await get_generations()
        for i in range(0, len(generations), config.BATCH_SIZE):
            batch = firebase.db.batch()
            generation_batch = generations[i:i + config.BATCH_SIZE]

            for generation in generation_batch:
                generation_ref = firebase.db.collection(Generation.COLLECTION_NAME).document(generation.id)

                batch.update(generation_ref, {
                    'model': DELETE_FIELD,
                })
            await batch.commit()
        await send_message_to_admins_and_developers(bot, '<b>GENERATIONS migration was successful!</b> 🎉')

        mini_transactions = await get_transactions(service=ServiceType.MINI)
        for mini_transaction in mini_transactions:
            await update_transaction(mini_transaction.id, {
                'service': DELETE_FIELD,
            })
        standard_transactions = await get_transactions(service=ServiceType.STANDARD)
        for standard_transaction in standard_transactions:
            await update_transaction(standard_transaction.id, {
                'service': DELETE_FIELD,
            })
        vip_transactions = await get_transactions(service=ServiceType.VIP)
        for vip_transaction in vip_transactions:
            await update_transaction(vip_transaction.id, {
                'service': DELETE_FIELD,
            })
        premium_transactions = await get_transactions(service=ServiceType.PREMIUM)
        for premium_transaction in premium_transactions:
            await update_transaction(premium_transaction.id, {
                'service': DELETE_FIELD,
            })
        unlimited_transactions = await get_transactions(service=ServiceType.UNLIMITED)
        for unlimited_transaction in unlimited_transactions:
            await update_transaction(unlimited_transaction.id, {
                'service': DELETE_FIELD,
            })

        chatgpt3_turbo_transactions = await get_transactions(service=ServiceType.CHAT_GPT3_TURBO)
        for i in range(0, len(chatgpt3_turbo_transactions), config.BATCH_SIZE):
            batch = firebase.db.batch()
            chatgpt3_turbo_transaction_batch = chatgpt3_turbo_transactions[i:i + config.BATCH_SIZE]
            for chatgpt3_turbo_transaction in chatgpt3_turbo_transaction_batch:
                chatgpt3_turbo_transaction_ref = firebase.db.collection(
                    Transaction.COLLECTION_NAME
                ).document(chatgpt3_turbo_transaction.id)
                batch.update(chatgpt3_turbo_transaction_ref, {
                    'service': DELETE_FIELD,
                })
            await batch.commit()
        chatgpt4_turbo_transactions = await get_transactions(service=ServiceType.CHAT_GPT4_TURBO)
        for i in range(0, len(chatgpt4_turbo_transactions), config.BATCH_SIZE):
            batch = firebase.db.batch()
            chatgpt4_turbo_transaction_batch = chatgpt4_turbo_transactions[i:i + config.BATCH_SIZE]
            for chatgpt4_turbo_transaction in chatgpt4_turbo_transaction_batch:
                chatgpt4_turbo_transaction_ref = firebase.db.collection(
                    Transaction.COLLECTION_NAME
                ).document(chatgpt4_turbo_transaction.id)
                batch.update(chatgpt4_turbo_transaction_ref, {
                    'service': DELETE_FIELD,
                })
            await batch.commit()
        chatgpt4_omni_mini_transactions = await get_transactions(service=ServiceType.CHAT_GPT4_OMNI_MINI)
        for i in range(0, len(chatgpt4_omni_mini_transactions), config.BATCH_SIZE):
            batch = firebase.db.batch()
            chatgpt4_omni_mini_transaction_batch = chatgpt4_omni_mini_transactions[i:i + config.BATCH_SIZE]
            for chatgpt4_omni_mini_transaction in chatgpt4_omni_mini_transaction_batch:
                chatgpt4_omni_mini_transaction_ref = firebase.db.collection(
                    Transaction.COLLECTION_NAME
                ).document(chatgpt4_omni_mini_transaction.id)
                batch.update(chatgpt4_omni_mini_transaction_ref, {
                    'service': DELETE_FIELD,
                })
            await batch.commit()
        chatgpt4_omni_transactions = await get_transactions(service=ServiceType.CHAT_GPT4_OMNI)
        for i in range(0, len(chatgpt4_omni_transactions), config.BATCH_SIZE):
            batch = firebase.db.batch()
            chatgpt4_omni_transaction_batch = chatgpt4_omni_transactions[i:i + config.BATCH_SIZE]
            for chatgpt4_omni_transaction in chatgpt4_omni_transaction_batch:
                chatgpt4_omni_transaction_ref = firebase.db.collection(
                    Transaction.COLLECTION_NAME
                ).document(chatgpt4_omni_transaction.id)
                batch.update(chatgpt4_omni_transaction_ref, {
                    'service': DELETE_FIELD,
                })
            await batch.commit()
        chatgpt_o_1_mini_transactions = await get_transactions(service=ServiceType.CHAT_GPT_O_1_MINI)
        for i in range(0, len(chatgpt_o_1_mini_transactions), config.BATCH_SIZE):
            batch = firebase.db.batch()
            chatgpt_o_1_mini_transaction_batch = chatgpt_o_1_mini_transactions[i:i + config.BATCH_SIZE]
            for chatgpt_o_1_mini_transaction in chatgpt_o_1_mini_transaction_batch:
                chatgpt_o_1_mini_transaction_ref = firebase.db.collection(
                    Transaction.COLLECTION_NAME
                ).document(chatgpt_o_1_mini_transaction.id)
                batch.update(chatgpt_o_1_mini_transaction_ref, {
                    'service': DELETE_FIELD,
                })
            await batch.commit()
        chatgpt_o_1_preview_transactions = await get_transactions(service=ServiceType.CHAT_GPT_O_1_PREVIEW)
        for i in range(0, len(chatgpt_o_1_preview_transactions), config.BATCH_SIZE):
            batch = firebase.db.batch()
            chatgpt_o_1_preview_transaction_batch = chatgpt_o_1_preview_transactions[i:i + config.BATCH_SIZE]
            for chatgpt_o_1_preview_transaction in chatgpt_o_1_preview_transaction_batch:
                chatgpt_o_1_preview_transaction_ref = firebase.db.collection(
                    Transaction.COLLECTION_NAME
                ).document(chatgpt_o_1_preview_transaction.id)
                batch.update(chatgpt_o_1_preview_transaction_ref, {
                    'service': DELETE_FIELD,
                })
            await batch.commit()
        claude_3_haiku_transactions = await get_transactions(service=ServiceType.CLAUDE_3_HAIKU)
        for i in range(0, len(claude_3_haiku_transactions), config.BATCH_SIZE):
            batch = firebase.db.batch()
            claude_3_haiku_transaction_batch = claude_3_haiku_transactions[i:i + config.BATCH_SIZE]
            for claude_3_haiku_transaction in claude_3_haiku_transaction_batch:
                claude_3_haiku_transaction_ref = firebase.db.collection(
                    Transaction.COLLECTION_NAME
                ).document(claude_3_haiku_transaction.id)
                batch.update(claude_3_haiku_transaction_ref, {
                    'service': DELETE_FIELD,
                })
            await batch.commit()
        claude_3_sonnet_transactions = await get_transactions(service=ServiceType.CLAUDE_3_SONNET)
        for i in range(0, len(claude_3_sonnet_transactions), config.BATCH_SIZE):
            batch = firebase.db.batch()
            claude_3_sonnet_transaction_batch = claude_3_sonnet_transactions[i:i + config.BATCH_SIZE]
            for claude_3_sonnet_transaction in claude_3_sonnet_transaction_batch:
                claude_3_sonnet_transaction_ref = firebase.db.collection(
                    Transaction.COLLECTION_NAME
                ).document(claude_3_sonnet_transaction.id)
                batch.update(claude_3_sonnet_transaction_ref, {
                    'service': DELETE_FIELD,
                })
            await batch.commit()
        claude_3_opus_transactions = await get_transactions(service=ServiceType.CLAUDE_3_OPUS)
        for i in range(0, len(claude_3_opus_transactions), config.BATCH_SIZE):
            batch = firebase.db.batch()
            claude_3_opus_transaction_batch = claude_3_opus_transactions[i:i + config.BATCH_SIZE]
            for claude_3_opus_transaction in claude_3_opus_transaction_batch:
                claude_3_opus_transaction_ref = firebase.db.collection(
                    Transaction.COLLECTION_NAME
                ).document(claude_3_opus_transaction.id)
                batch.update(claude_3_opus_transaction_ref, {
                    'service': DELETE_FIELD,
                })
            await batch.commit()
        gemini_1_flash_transactions = await get_transactions(service=ServiceType.GEMINI_1_FLASH)
        for i in range(0, len(gemini_1_flash_transactions), config.BATCH_SIZE):
            batch = firebase.db.batch()
            gemini_1_flash_transaction_batch = gemini_1_flash_transactions[i:i + config.BATCH_SIZE]
            for gemini_1_flash_transaction in gemini_1_flash_transaction_batch:
                gemini_1_flash_transaction_ref = firebase.db.collection(
                    Transaction.COLLECTION_NAME
                ).document(gemini_1_flash_transaction.id)
                batch.update(gemini_1_flash_transaction_ref, {
                    'service': DELETE_FIELD,
                })
            await batch.commit()
        gemini_1_pro_transactions = await get_transactions(service=ServiceType.GEMINI_1_PRO)
        for i in range(0, len(gemini_1_pro_transactions), config.BATCH_SIZE):
            batch = firebase.db.batch()
            gemini_1_pro_transaction_batch = gemini_1_pro_transactions[i:i + config.BATCH_SIZE]
            for gemini_1_pro_transaction in gemini_1_pro_transaction_batch:
                gemini_1_pro_transaction_ref = firebase.db.collection(
                    Transaction.COLLECTION_NAME
                ).document(gemini_1_pro_transaction.id)
                batch.update(gemini_1_pro_transaction_ref, {
                    'service': DELETE_FIELD,
                })
            await batch.commit()
        gemini_1_ultra_transactions = await get_transactions(service=ServiceType.GEMINI_1_ULTRA)
        for i in range(0, len(gemini_1_ultra_transactions), config.BATCH_SIZE):
            batch = firebase.db.batch()
            gemini_1_ultra_transaction_batch = gemini_1_ultra_transactions[i:i + config.BATCH_SIZE]
            for gemini_1_ultra_transaction in gemini_1_ultra_transaction_batch:
                gemini_1_ultra_transaction_ref = firebase.db.collection(
                    Transaction.COLLECTION_NAME
                ).document(gemini_1_ultra_transaction.id)
                batch.update(gemini_1_ultra_transaction_ref, {
                    'service': DELETE_FIELD,
                })
            await batch.commit()
        dall_e_transactions = await get_transactions(service=ServiceType.DALL_E)
        for i in range(0, len(dall_e_transactions), config.BATCH_SIZE):
            batch = firebase.db.batch()
            dall_e_transaction_batch = dall_e_transactions[i:i + config.BATCH_SIZE]
            for dall_e_transaction in dall_e_transaction_batch:
                dall_e_transaction_ref = firebase.db.collection(
                    Transaction.COLLECTION_NAME
                ).document(dall_e_transaction.id)
                batch.update(dall_e_transaction_ref, {
                    'service': DELETE_FIELD,
                })
            await batch.commit()
        midjourney_transactions = await get_transactions(service=ServiceType.MIDJOURNEY)
        for i in range(0, len(midjourney_transactions), config.BATCH_SIZE):
            batch = firebase.db.batch()
            midjourney_transaction_batch = midjourney_transactions[i:i + config.BATCH_SIZE]
            for midjourney_transaction in midjourney_transaction_batch:
                midjourney_transaction_ref = firebase.db.collection(
                    Transaction.COLLECTION_NAME
                ).document(midjourney_transaction.id)
                batch.update(midjourney_transaction_ref, {
                    'service': DELETE_FIELD,
                })
            await batch.commit()
        stable_diffusion_transactions = await get_transactions(service=ServiceType.STABLE_DIFFUSION)
        for i in range(0, len(stable_diffusion_transactions), config.BATCH_SIZE):
            batch = firebase.db.batch()
            stable_diffusion_transaction_batch = stable_diffusion_transactions[i:i + config.BATCH_SIZE]
            for stable_diffusion_transaction in stable_diffusion_transaction_batch:
                stable_diffusion_transaction_ref = firebase.db.collection(
                    Transaction.COLLECTION_NAME
                ).document(stable_diffusion_transaction.id)
                batch.update(stable_diffusion_transaction_ref, {
                    'service': DELETE_FIELD,
                })
            await batch.commit()
        flux_transactions = await get_transactions(service=ServiceType.FLUX)
        for i in range(0, len(flux_transactions), config.BATCH_SIZE):
            batch = firebase.db.batch()
            flux_transaction_batch = flux_transactions[i:i + config.BATCH_SIZE]
            for flux_transaction in flux_transaction_batch:
                flux_transaction_ref = firebase.db.collection(
                    Transaction.COLLECTION_NAME
                ).document(flux_transaction.id)
                batch.update(flux_transaction_ref, {
                    'service': DELETE_FIELD,
                })
            await batch.commit()
        face_swap_transactions = await get_transactions(service=ServiceType.FACE_SWAP)
        for i in range(0, len(face_swap_transactions), config.BATCH_SIZE):
            batch = firebase.db.batch()
            face_swap_transaction_batch = face_swap_transactions[i:i + config.BATCH_SIZE]
            for face_swap_transaction in face_swap_transaction_batch:
                face_swap_transaction_ref = firebase.db.collection(
                    Transaction.COLLECTION_NAME
                ).document(face_swap_transaction.id)
                batch.update(face_swap_transaction_ref, {
                    'service': DELETE_FIELD,
                })
            await batch.commit()
        photoshop_ai_transactions = await get_transactions(service=ServiceType.PHOTOSHOP_AI)
        for i in range(0, len(photoshop_ai_transactions), config.BATCH_SIZE):
            batch = firebase.db.batch()
            photoshop_ai_transaction_batch = photoshop_ai_transactions[i:i + config.BATCH_SIZE]
            for photoshop_ai_transaction in photoshop_ai_transaction_batch:
                photoshop_ai_transaction_ref = firebase.db.collection(
                    Transaction.COLLECTION_NAME
                ).document(photoshop_ai_transaction.id)
                batch.update(photoshop_ai_transaction_ref, {
                    'service': DELETE_FIELD,
                })
            await batch.commit()
        music_gen_transactions = await get_transactions(service=ServiceType.MUSIC_GEN)
        for i in range(0, len(music_gen_transactions), config.BATCH_SIZE):
            batch = firebase.db.batch()
            music_gen_transaction_batch = music_gen_transactions[i:i + config.BATCH_SIZE]
            for music_gen_transaction in music_gen_transaction_batch:
                music_gen_transaction_ref = firebase.db.collection(
                    Transaction.COLLECTION_NAME
                ).document(music_gen_transaction.id)
                batch.update(music_gen_transaction_ref, {
                    'service': DELETE_FIELD,
                })
            await batch.commit()
        suno_transactions = await get_transactions(service=ServiceType.SUNO)
        for i in range(0, len(suno_transactions), config.BATCH_SIZE):
            batch = firebase.db.batch()
            suno_transaction_batch = suno_transactions[i:i + config.BATCH_SIZE]
            for suno_transaction in suno_transaction_batch:
                suno_transaction_ref = firebase.db.collection(
                    Transaction.COLLECTION_NAME
                ).document(suno_transaction.id)
                batch.update(suno_transaction_ref, {
                    'service': DELETE_FIELD,
                })
            await batch.commit()
        chat_transactions = await get_transactions(service=ServiceType.ADDITIONAL_CHATS)
        for chat_transaction in chat_transactions:
            await update_transaction(chat_transaction.id, {
                'service': DELETE_FIELD,
            })
        access_to_catalog_transactions = await get_transactions(service=ServiceType.ACCESS_TO_CATALOG)
        for access_to_catalog_transaction in access_to_catalog_transactions:
            await update_transaction(access_to_catalog_transaction.id, {
                'service': DELETE_FIELD,
            })
        voice_messages_transactions = await get_transactions(service=ServiceType.VOICE_MESSAGES)
        for voice_messages_transaction in voice_messages_transactions:
            await update_transaction(voice_messages_transaction.id, {
                'service': DELETE_FIELD,
            })
        fast_messages_transactions = await get_transactions(service=ServiceType.FAST_MESSAGES)
        for fast_messages_transaction in fast_messages_transactions:
            await update_transaction(fast_messages_transaction.id, {
                'service': DELETE_FIELD,
            })
        server_transactions = await get_transactions(service=ServiceType.SERVER)
        for server_transaction in server_transactions:
            await update_transaction(server_transaction.id, {
                'service': DELETE_FIELD,
            })
        database_transactions = await get_transactions(service=ServiceType.DATABASE)
        for database_transaction in database_transactions:
            await update_transaction(database_transaction.id, {
                'service': DELETE_FIELD,
            })
        other_transactions = await get_transactions(service=ServiceType.OTHER)
        for other_transaction in other_transactions:
            await update_transaction(other_transaction.id, {
                'service': DELETE_FIELD,
            })

        await send_message_to_admins_and_developers(bot, '<b>TRANSACTIONS migration was successful!</b> 🎉')

        await send_message_to_admins_and_developers(bot, '<b>The third database migration was successful!</b> 🎉')
    except Exception as e:
        logging.exception('Error in migration', e)
        await send_message_to_admins_and_developers(
            bot,
            f'The third database migration was not successful! 🚨\n\n{e}',
            parse_mode=None,
        )
    finally:
        logging.info('END_MIGRATION')
