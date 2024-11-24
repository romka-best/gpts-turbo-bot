from aiogram import Bot

from bot.database.models.common import Currency
from bot.database.models.subscription import Subscription, SubscriptionStatus
from bot.database.operations.product.getters import get_product
from bot.database.operations.subscription.updaters import update_subscription_in_transaction
from bot.helpers.senders.send_message_to_admins import send_message_to_admins


async def unsubscribe(transaction, old_subscription: Subscription, bot: Bot):
    old_subscription.status = SubscriptionStatus.CANCELED
    await update_subscription_in_transaction(transaction, old_subscription.id, {
        'status': old_subscription.status,
    })

    product = await get_product(old_subscription.product_id)

    await send_message_to_admins(
        bot=bot,
        message=f'#payment #subscription #canceled\n\n'
                f'❌ <b>Отмена подписки у пользователя: {old_subscription.user_id}</b>\n\n'
                f'ℹ️ ID: {old_subscription.id}\n'
                f'💱 Метод оплаты: {old_subscription.payment_method}\n'
                # f'💳 Тип: {product.names.get("ru")}\n'
                f'💰 Сумма: {old_subscription.amount}{Currency.SYMBOLS[old_subscription.currency]}\n'
                f'💸 Чистая сумма: {float(old_subscription.income_amount)}{Currency.SYMBOLS[old_subscription.currency]}\n'
                f'🗓 Период подписки: {old_subscription.start_date.strftime("%d.%m.%Y")}-{old_subscription.end_date.strftime("%d.%m.%Y")}\n\n'
                f'Грустно, но что поделать 🤷',
    )
