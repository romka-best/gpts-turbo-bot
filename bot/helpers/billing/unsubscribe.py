from aiogram import Bot

from bot.database.models.common import Currency, PaymentMethod
from bot.database.models.subscription import Subscription, SubscriptionStatus
from bot.database.operations.product.getters import get_product
from bot.database.operations.subscription.updaters import update_subscription_in_transaction
from bot.helpers.senders.send_message_to_admins import send_message_to_admins


async def unsubscribe(transaction, old_subscription: Subscription, bot: Bot):
    old_subscription.status = SubscriptionStatus.CANCELED
    await update_subscription_in_transaction(transaction, old_subscription.id, {
        'status': old_subscription.status,
    })

    if old_subscription.payment_method == PaymentMethod.TELEGRAM_STARS:
        await bot.edit_user_star_subscription(
            user_id=int(old_subscription.user_id),
            telegram_payment_charge_id=old_subscription.provider_payment_charge_id,
            is_canceled=True,
        )

    product = await get_product(old_subscription.product_id)

    await send_message_to_admins(
        bot=bot,
        message=f'#payment #subscription #canceled\n\n'
                f'❌ <b>Отмена продления подписки у пользователя: {old_subscription.user_id}</b>\n\n'
                f'ℹ️ ID: {old_subscription.id}\n'
                f'💱 Метод оплаты: {old_subscription.payment_method}\n'
                f'💳 Тип: {product.names.get("ru")}\n'
                f'💰 Сумма: {old_subscription.amount}{Currency.SYMBOLS[old_subscription.currency]}\n'
                f'💸 Чистая сумма: {float(old_subscription.income_amount)}{Currency.SYMBOLS[old_subscription.currency]}\n'
                f'🗓 Период подписки: {old_subscription.start_date.strftime("%d.%m.%Y")}-{old_subscription.end_date.strftime("%d.%m.%Y")}\n\n'
                f'Грустно, но что поделать 🤷',
    )
