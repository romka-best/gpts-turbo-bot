from datetime import datetime, timezone

import stripe
from aiogram import Bot
from google.cloud import firestore

from bot.database.models.common import Currency, PaymentMethod
from bot.database.models.subscription import Subscription, SubscriptionStatus
from bot.database.operations.product.getters import get_product
from bot.database.operations.subscription.updaters import update_subscription_in_transaction
from bot.helpers.senders.send_message_to_admins import send_message_to_admins
from bot.locales.types import LanguageCode


@firestore.async_transactional
async def unsubscribe_wrapper(transaction, old_subscription: Subscription, bot: Bot):
    await unsubscribe(transaction, old_subscription, bot)


async def unsubscribe(transaction, old_subscription: Subscription, bot: Bot):
    current_date = datetime.now(timezone.utc)

    await update_subscription_in_transaction(transaction, old_subscription.id, {
        'status': SubscriptionStatus.CANCELED,
        'end_date': current_date if old_subscription.status == SubscriptionStatus.TRIAL else old_subscription.end_date,
    })

    if old_subscription.payment_method == PaymentMethod.STRIPE:
        await stripe.Subscription.modify_async(
            old_subscription.stripe_id,
            cancel_at_period_end=True,
        )
    elif old_subscription.payment_method == PaymentMethod.TELEGRAM_STARS:
        await bot.edit_user_star_subscription(
            user_id=int(old_subscription.user_id),
            telegram_payment_charge_id=old_subscription.provider_payment_charge_id,
            is_canceled=True,
        )

    product = await get_product(old_subscription.product_id)

    if old_subscription.status == SubscriptionStatus.TRIAL:
        await send_message_to_admins(
            bot=bot,
            message=f'#payment #trial #subscription #canceled\n\n'
                    f'❌ <b>Отмена продления пробного периода подписки у пользователя: {old_subscription.user_id}</b>\n\n'
                    f'ℹ️ ID: {old_subscription.id}\n'
                    f'💱 Метод оплаты: {old_subscription.payment_method}\n'
                    f'💳 Тип: {product.names.get(LanguageCode.RU)}\n'
                    f'💰 Сумма: {old_subscription.amount}{Currency.SYMBOLS[old_subscription.currency]}\n'
                    f'💸 Чистая сумма: {float(old_subscription.income_amount)}{Currency.SYMBOLS[old_subscription.currency]}\n'
                    f'🗓 Период подписки: {old_subscription.start_date.strftime("%d.%m.%Y")}-{current_date.strftime("%d.%m.%Y")}\n\n'
                    f'Грустно, но что поделать 🤷',
        )
    else:
        await send_message_to_admins(
            bot=bot,
            message=f'#payment #subscription #canceled\n\n'
                    f'❌ <b>Отмена продления подписки у пользователя: {old_subscription.user_id}</b>\n\n'
                    f'ℹ️ ID: {old_subscription.id}\n'
                    f'💱 Метод оплаты: {old_subscription.payment_method}\n'
                    f'💳 Тип: {product.names.get(LanguageCode.RU)}\n'
                    f'💰 Сумма: {old_subscription.amount}{Currency.SYMBOLS[old_subscription.currency]}\n'
                    f'💸 Чистая сумма: {float(old_subscription.income_amount)}{Currency.SYMBOLS[old_subscription.currency]}\n'
                    f'🗓 Период подписки: {old_subscription.start_date.strftime("%d.%m.%Y")}-{old_subscription.end_date.strftime("%d.%m.%Y")}\n\n'
                    f'Грустно, но что поделать 🤷',
        )
