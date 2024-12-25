from datetime import timedelta

import stripe
from aiogram import Bot
from google.cloud import firestore

from bot.database.models.common import Currency, PaymentMethod
from bot.database.models.subscription import Subscription, SubscriptionStatus, SubscriptionPeriod
from bot.database.operations.product.getters import get_product
from bot.database.operations.subscription.updaters import update_subscription_in_transaction
from bot.helpers.senders.send_message_to_admins import send_message_to_admins
from bot.locales.types import LanguageCode


@firestore.async_transactional
async def resubscribe_wrapper(transaction, old_subscription: Subscription, bot: Bot):
    await resubscribe(transaction, old_subscription, bot)


async def resubscribe(transaction, old_subscription: Subscription, bot: Bot):
    is_trial = (old_subscription.end_date - old_subscription.start_date).days <= 3
    if is_trial and old_subscription.period == SubscriptionPeriod.MONTH1:
        old_subscription.end_date = old_subscription.start_date + timedelta(days=30)
    elif is_trial and old_subscription.period == SubscriptionPeriod.MONTHS12:
        old_subscription.end_date = old_subscription.start_date + timedelta(days=365)

    await update_subscription_in_transaction(transaction, old_subscription.id, {
        'status': SubscriptionStatus.TRIAL if is_trial else SubscriptionStatus.ACTIVE,
        'end_date': old_subscription.end_date,
    })

    if old_subscription.payment_method == PaymentMethod.STRIPE:
        await stripe.Subscription.modify_async(
            old_subscription.stripe_id,
            cancel_at_period_end=False
        )
    elif old_subscription.payment_method == PaymentMethod.TELEGRAM_STARS:
        await bot.edit_user_star_subscription(
            user_id=int(old_subscription.user_id),
            telegram_payment_charge_id=old_subscription.provider_payment_charge_id,
            is_canceled=False,
        )

    product = await get_product(old_subscription.product_id)

    if is_trial:
        await send_message_to_admins(
            bot=bot,
            message=f'#payment #trial #subscription #resubscribe\n\n'
                    f'🤑 <b>Возобновление пробного периода подписки у пользователя: {old_subscription.user_id}</b>\n\n'
                    f'ℹ️ ID: {old_subscription.id}\n'
                    f'💱 Метод оплаты: {old_subscription.payment_method}\n'
                    f'💳 Тип: {product.names.get(LanguageCode.RU)}\n'
                    f'💰 Сумма: {old_subscription.amount}{Currency.SYMBOLS[old_subscription.currency]}\n'
                    f'💸 Чистая сумма: {float(old_subscription.income_amount)}{Currency.SYMBOLS[old_subscription.currency]}\n'
                    f'🗓 Период подписки: {old_subscription.start_date.strftime("%d.%m.%Y")}-{old_subscription.end_date.strftime("%d.%m.%Y")}\n\n'
                    f'Вернулся к нам, продолжаем в том же духе 💪',
        )
    else:
        await send_message_to_admins(
            bot=bot,
            message=f'#payment #subscription #resubscribe\n\n'
                    f'🤑 <b>Возобновление продления подписки у пользователя: {old_subscription.user_id}</b>\n\n'
                    f'ℹ️ ID: {old_subscription.id}\n'
                    f'💱 Метод оплаты: {old_subscription.payment_method}\n'
                    f'💳 Тип: {product.names.get(LanguageCode.RU)}\n'
                    f'💰 Сумма: {old_subscription.amount}{Currency.SYMBOLS[old_subscription.currency]}\n'
                    f'💸 Чистая сумма: {float(old_subscription.income_amount)}{Currency.SYMBOLS[old_subscription.currency]}\n'
                    f'🗓 Период подписки: {old_subscription.start_date.strftime("%d.%m.%Y")}-{old_subscription.end_date.strftime("%d.%m.%Y")}\n\n'
                    f'Вернулся к нам, продолжаем в том же духе 💪',
        )
