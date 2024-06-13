import asyncio
import logging
from datetime import datetime, timezone

from aiogram import Bot

from bot.config import config
from bot.database.main import firebase
from bot.database.models.common import Currency, Model, FaceSwapVersion, MusicGenVersion, SunoVersion, PaymentMethod
from bot.database.models.package import Package
from bot.database.models.subscription import Subscription
from bot.database.models.transaction import Transaction, TransactionType
from bot.database.models.user import UserSettings, User
from bot.database.operations.package.getters import get_packages
from bot.database.operations.subscription.getters import get_subscriptions
from bot.database.operations.transaction.getters import get_transactions
from bot.database.operations.user.getters import get_users
from bot.helpers.senders.send_message_to_admins import send_message_to_admins
from bot.helpers.setters.set_commands import set_commands_for_user


async def migrate(bot: Bot):
    logging.info("START_MIGRATION")

    try:
        tasks = []
        current_date = datetime.now(timezone.utc)

        users = await get_users()
        for i in range(0, len(users), config.USER_BATCH_SIZE):
            batch = firebase.db.batch()
            user_batch = users[i:i + config.USER_BATCH_SIZE]

            for user in user_batch:
                user_ref = firebase.db.collection(User.COLLECTION_NAME).document(user.id)

                if user.language_code == "ru":
                    user.interface_language_code = user.language_code
                    user.currency = Currency.RUB
                else:
                    user.interface_language_code = "en"
                    user.currency = Currency.USD

                user.settings[Model.FACE_SWAP][UserSettings.VERSION] = FaceSwapVersion.LATEST
                user.settings[Model.MUSIC_GEN][UserSettings.VERSION] = MusicGenVersion.LATEST
                user.settings[Model.SUNO][UserSettings.VERSION] = SunoVersion.V3_5

                batch.update(user_ref, {
                    "interface_language_code": user.interface_language_code,
                    "currency": user.currency,
                    "settings": user.settings,
                    "edited_at": current_date,
                })

                tasks.append(
                    set_commands_for_user(
                        bot,
                        user.telegram_chat_id,
                        user.interface_language_code,
                    )
                )

            await batch.commit()

        subscriptions = await get_subscriptions()
        for i in range(0, len(subscriptions), config.USER_BATCH_SIZE):
            batch = firebase.db.batch()
            subscription_batch = subscriptions[i:i + config.USER_BATCH_SIZE]

            for subscription in subscription_batch:
                subscription_ref = firebase.db.collection(Subscription.COLLECTION_NAME).document(subscription.id)

                subscription.income_amount = subscription.amount - (subscription.amount * (3.5 / 100))
                subscription.provider_auto_payment_charge_id = ""
                if subscription.amount == 0:
                    subscription.payment_method = PaymentMethod.GIFT
                else:
                    subscription.payment_method = PaymentMethod.YOOKASSA

                batch.update(subscription_ref, {
                    "income_amount": subscription.income_amount,
                    "payment_method": subscription.payment_method,
                    "provider_auto_payment_charge_id": subscription.provider_auto_payment_charge_id,
                    "edited_at": current_date,
                })

            await batch.commit()

        packages = await get_packages()
        for i in range(0, len(packages), config.USER_BATCH_SIZE):
            batch = firebase.db.batch()
            package_batch = packages[i:i + config.USER_BATCH_SIZE]

            for package in package_batch:
                package_ref = firebase.db.collection(Package.COLLECTION_NAME).document(package.id)

                package.income_amount = package.amount - (package.amount * (3.5 / 100))
                if package.amount == 0:
                    package.payment_method = PaymentMethod.GIFT
                else:
                    package.payment_method = PaymentMethod.YOOKASSA

                batch.update(package_ref, {
                    "income_amount": package.income_amount,
                    "payment_method": package.payment_method,
                })

            await batch.commit()

        transactions = await get_transactions()
        for i in range(0, len(transactions), config.USER_BATCH_SIZE):
            batch = firebase.db.batch()
            transaction_batch = transactions[i:i + config.USER_BATCH_SIZE]

            for transaction in transaction_batch:
                transaction_ref = firebase.db.collection(Transaction.COLLECTION_NAME).document(transaction.id)

                if transaction.type == TransactionType.EXPENSE:
                    transaction.clear_amount = transaction.amount
                elif transaction.type == TransactionType.INCOME:
                    if transaction.amount == 0:
                        transaction.clear_amount = 0
                        transaction.details['payment_method'] = PaymentMethod.GIFT
                    else:
                        transaction.clear_amount = transaction.amount - (transaction.amount * (3.5 / 100))
                        transaction.details['payment_method'] = PaymentMethod.YOOKASSA

                batch.update(transaction_ref, {
                    "clear_amount": transaction.clear_amount,
                    "details": transaction.details,
                    "edited_at": current_date,
                })

            await batch.commit()

        await asyncio.gather(*tasks)

        await send_message_to_admins(bot, "<b>The database migration was successful!</b> 🎉")
    except Exception as e:
        logging.exception("Error in migration", e)
        await send_message_to_admins(bot, "<b>The database migration was not successful!</b> 🚨")
    finally:
        logging.info("END_MIGRATION")
