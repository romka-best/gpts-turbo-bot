import aiohttp
from aiogram import Bot
from aiogram.fsm.storage.base import BaseStorage
from google.cloud.firestore_v1 import DELETE_FIELD

from bot.database.main import firebase
from bot.database.operations.package.getters import get_packages
from bot.database.operations.package.updaters import update_package
from bot.database.operations.subscription.getters import get_subscriptions
from bot.database.operations.subscription.updaters import update_subscription
from bot.database.operations.user.getters import get_users
from bot.helpers.senders.send_message_to_admins_and_developers import send_message_to_admins_and_developers
from bot.locales.main import get_user_language


async def migrate(bot: Bot, storage: BaseStorage):
    subscriptions = await get_subscriptions()
    for subscription in subscriptions:
        await update_subscription(subscription.id, {
            'type': DELETE_FIELD,
        })

    packages = await get_packages()
    for package in packages:
        await update_package(package.id, {
            'type': DELETE_FIELD,
        })

    users = await get_users()
    count_different_languages = 0
    for user in users:
        full_name = user.first_name
        if user.last_name:
            full_name += f' {user.last_name}'

        try:
            await firebase.get_user(user.id)
        except firebase.auth.UserNotFoundError:
            try:
                photo_path = f'users/avatars/{user.id}.jpeg'
                photo = await firebase.bucket.get_blob(photo_path)
                photo_url = firebase.get_public_url(photo.name)
            except aiohttp.ClientResponseError:
                photo_url = None

            await firebase.create_user(
                uid=user.id,
                display_name=full_name,
                photo_url=photo_url,
            )

        user_language_code = await get_user_language(user.id, storage)
        if user.interface_language_code != user_language_code:
            count_different_languages += 1
    await send_message_to_admins_and_developers(
        bot, '<b>Database Migration Was Successful!</b> 🎉',
    )
    await send_message_to_admins_and_developers(
        bot, f'<b>Found Users With Different Languages in Cache and DB: {count_different_languages}</b>',
    )
