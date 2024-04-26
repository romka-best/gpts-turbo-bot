import asyncio
import logging

from aiogram import Bot

from bot.database.models.common import Model, GPTVersion, DALLEVersion, MidjourneyVersion, Quota
from bot.database.models.package import PackageType
from bot.database.models.request import RequestStatus
from bot.database.models.subscription import SubscriptionType
from bot.database.models.transaction import ServiceType
from bot.database.models.user import UserSettings
from bot.database.operations.package.getters import get_packages
from bot.database.operations.package.updaters import update_package
from bot.database.operations.request.getters import get_started_requests_by_user_id_and_model
from bot.database.operations.request.updaters import update_request
from bot.database.operations.transaction.getters import get_transactions
from bot.database.operations.transaction.updaters import update_transaction
from bot.database.operations.user.getters import get_users
from bot.database.operations.user.updaters import update_user
from bot.helpers.senders.send_message_to_admins import send_message_to_admins
from bot.helpers.setters.set_commands import set_commands_for_user


async def migrate(bot: Bot):
    logging.info("START_MIGRATION")

    try:
        tasks = []

        users = await get_users()
        for user in users:
            # ChatGPT
            old_gpt3 = 'gpt-3.5-turbo-0125'
            old_gpt4 = 'gpt-4-vision-preview'
            if user.settings.get(old_gpt3):
                old_gpt3_settings = user.settings.get(old_gpt3)
                user.settings[Model.CHAT_GPT] = old_gpt3_settings
                if user.current_model == old_gpt3:
                    user.settings[Model.CHAT_GPT][UserSettings.VERSION] = GPTVersion.V3
                    user.current_model = Model.CHAT_GPT
                del user.settings[old_gpt3]
            if user.settings.get(old_gpt4):
                old_gpt4_settings = user.settings.get(old_gpt4)
                user.settings[Model.CHAT_GPT] = old_gpt4_settings
                if user.current_model == old_gpt4:
                    user.settings[Model.CHAT_GPT][UserSettings.VERSION] = GPTVersion.V4
                    user.current_model = Model.CHAT_GPT
                del user.settings[old_gpt4]
            if (
                user.settings[Model.CHAT_GPT].get(UserSettings.VERSION) != GPTVersion.V3 and
                user.settings[Model.CHAT_GPT].get(UserSettings.VERSION) != GPTVersion.V4
            ):
                user.settings[Model.CHAT_GPT][UserSettings.VERSION] = GPTVersion.V3

            # DALL-E
            old_dall_e = 'dall-e-3'
            if user.settings.get(old_dall_e):
                old_dall_e_settings = user.settings.get(old_dall_e)
                user.settings[Model.DALL_E] = old_dall_e_settings
                if user.current_model == old_dall_e:
                    user.current_model = Model.DALL_E
                del user.settings[old_dall_e]
            if user.additional_usage_quota.get('dalle3', -1) >= 0:
                old_dall_e_additional_usage_quota = user.additional_usage_quota.get('dalle3')
                user.additional_usage_quota[Quota.DALL_E] = old_dall_e_additional_usage_quota
                del user.additional_usage_quota['dalle3']
            if user.monthly_limits.get('dalle3', -1) >= 0:
                old_monthly_limits = user.monthly_limits.get('dalle3')
                user.monthly_limits[Quota.DALL_E] = old_monthly_limits
                del user.monthly_limits['dalle3']
            user.settings[Model.DALL_E][UserSettings.VERSION] = DALLEVersion.V3

            # Midjourney
            user.settings[Model.MIDJOURNEY] = {
                UserSettings.SHOW_USAGE_QUOTA: True,
                UserSettings.VERSION: MidjourneyVersion.V6,
            }
            user.additional_usage_quota[Quota.MIDJOURNEY] = 0
            if user.subscription_type == SubscriptionType.FREE:
                user.additional_usage_quota[Quota.MIDJOURNEY] = 10
                user.monthly_limits[Quota.MIDJOURNEY] = 0
            elif user.subscription_type == SubscriptionType.STANDARD:
                user.monthly_limits[Quota.MIDJOURNEY] = 50
            elif user.subscription_type == SubscriptionType.VIP:
                user.monthly_limits[Quota.MIDJOURNEY] = 100
            elif user.subscription_type == SubscriptionType.PLATINUM:
                user.monthly_limits[Quota.MIDJOURNEY] = 200

            # FaceSwap
            not_finished_requests = await get_started_requests_by_user_id_and_model(user.id, Model.FACE_SWAP)
            had_error_in_face_swap = False
            for not_finished_request in not_finished_requests:
                had_error_in_face_swap = True
                not_finished_request.details['has_error'] = had_error_in_face_swap
                tasks.append(
                    update_request(
                        not_finished_request.id,
                        {
                            "status": RequestStatus.FINISHED,
                            "details": not_finished_request.details,
                        }
                    )
                )
            if had_error_in_face_swap:
                user.additional_usage_quota[Quota.FACE_SWAP] += 20
                if user.language_code == 'ru':
                    await bot.send_message(
                        chat_id=user.telegram_chat_id,
                        text="""
🛠️ Важное обновление по модели FaceSwap!

Уважаемые пользователи, недавно мы обнаружили техническую неполадку в AI модели FaceSwap. Мы рады сообщить, что проблема устранена! В знак признательности за ваше терпение и понимание, мы добавили на ваш аккаунт 20 бесплатных генераций

Спасибо за вашу поддержку и наслаждайтесь творчеством с FaceSwap 💙
                        """,
                    )
                else:
                    await bot.send_message(
                        chat_id=user.telegram_chat_id,
                        text="""
🛠️ Important update on FaceSwap AI model!

Dear users, we recently identified a technical issue with our FaceSwap AI model. We're pleased to announce that the problem has been fixed! As a token of our appreciation for your patience and understanding during this time, we've credited your account with 20 free generations

Thank you for your continued support, and enjoy creating with FaceSwap 💙
""",
                    )

            tasks.append(
                update_user(
                    user.id,
                    {
                        "additional_usage_quota": user.additional_usage_quota,
                        "current_model": user.current_model,
                        "monthly_limits": user.monthly_limits,
                        "settings": user.settings,
                    }
                )
            )
            tasks.append(
                set_commands_for_user(
                    bot,
                    user.telegram_chat_id,
                    user.language_code,
                )
            )

        transactions = await get_transactions()
        for transaction in transactions:
            if transaction.service == "DALLE3":
                transaction.service = ServiceType.DALL_E
                tasks.append(
                    update_transaction(
                        transaction.id,
                        {
                            "service": transaction.service,
                        }
                    )
                )

        packages = await get_packages()
        for package in packages:
            if package.type == "DALLE3":
                package.type = PackageType.DALL_E
                tasks.append(
                    update_package(
                        package.id,
                        {
                            "type": package.type,
                        }
                    )
                )

        await asyncio.gather(*tasks)

        await send_message_to_admins(bot, "<b>The database migration was successful!</b> 🎉")
    except Exception as e:
        logging.exception("Error in migration", e)
        await send_message_to_admins(bot, "<b>The database migration was not successful!</b> 🚨")
    finally:
        logging.info("END_MIGRATION")
