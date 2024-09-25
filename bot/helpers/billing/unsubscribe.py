from aiogram import Bot

from bot.database.models.common import Currency
from bot.database.models.subscription import Subscription, SubscriptionStatus
from bot.database.operations.subscription.updaters import update_subscription_in_transaction
from bot.helpers.senders.send_message_to_admins_and_developers import send_message_to_admins_and_developers


async def unsubscribe(transaction, old_subscription: Subscription, bot: Bot):
    old_subscription.status = SubscriptionStatus.CANCELED
    await update_subscription_in_transaction(transaction, old_subscription.id, {
        'status': SubscriptionStatus.CANCELED,
    })

    await send_message_to_admins_and_developers(
        bot=bot,
        message=f'#payment #subscription #canceled\n\n'
                f'❌ <b>Отмена подписки у пользователя: {old_subscription.user_id}</b>\n\n'
                f'ℹ️ ID: {old_subscription.id}\n'
                f'💱 Метод оплаты: {old_subscription.payment_method}\n'
                f'💳 Тип подписки: {old_subscription.type}\n'
                f'💰 Сумма: {old_subscription.amount}{Currency.SYMBOLS[old_subscription.currency]}\n'
                f'💸 Чистая сумма: {float(old_subscription.income_amount)}{Currency.SYMBOLS[old_subscription.currency]}\n'
                f'🗓 Период подписки: {old_subscription.start_date.strftime("%d.%m.%Y")}-{old_subscription.end_date.strftime("%d.%m.%Y")}\n\n'
                f'Грустно, но что поделать 🤷',
    )
