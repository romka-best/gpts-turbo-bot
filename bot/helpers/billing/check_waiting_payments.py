import asyncio
from datetime import datetime, timezone, timedelta

from aiogram import Bot

from bot.database.models.common import Currency
from bot.database.models.subscription import SubscriptionStatus
from bot.database.operations.subscription.getters import get_subscriptions_by_status
from bot.database.operations.subscription.updaters import update_subscription
from bot.helpers.senders.send_message_to_admins import send_message_to_admins


async def check_waiting_payments(bot: Bot):
    today_utc_day = datetime.now(timezone.utc)
    yesterday_utc_day = today_utc_day - timedelta(days=1)
    not_finished_subscriptions = await get_subscriptions_by_status(
        yesterday_utc_day,
        today_utc_day - timedelta(hours=1),
        SubscriptionStatus.WAITING,
    )

    tasks = []
    for not_finished_subscription in not_finished_subscriptions:
        status = SubscriptionStatus.DECLINED
        not_finished_subscription.status = status
        tasks.append(
            update_subscription(
                not_finished_subscription.id,
                {
                    'status': not_finished_subscription.status,
                }
            )
        )

        await send_message_to_admins(
            bot=bot,
            message=f'#payment #subscription #declined\n\n'
                    f'❌ <b>Отмена оплаты подписки у пользователя: {not_finished_subscription.user_id}</b>\n\n'
                    f'ℹ️ ID: {not_finished_subscription.id}\n'
                    f'💱 Метод оплаты: {not_finished_subscription.payment_method}\n'
                    f'💳 Тип подписки: {not_finished_subscription.type}\n'
                    f'💰 Сумма: {not_finished_subscription.amount}{Currency.SYMBOLS[not_finished_subscription.currency]}\n\n'
                    f'Грустно, но что поделать 🤷',
        )

    await asyncio.gather(*tasks)
