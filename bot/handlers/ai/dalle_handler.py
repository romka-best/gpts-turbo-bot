import openai
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender

from bot.database.models.common import Quota, Currency, Model
from bot.database.models.transaction import TransactionType, ServiceType
from bot.database.models.user import UserSettings, User
from bot.database.operations.transaction.writers import write_transaction
from bot.database.operations.user.getters import get_user
from bot.database.operations.user.updaters import update_user
from bot.helpers.senders.send_message_to_admins import send_message_to_admins
from bot.integrations.openAI import get_response_image, get_cost_for_image
from bot.keyboards.common.common import build_recommendations_keyboard
from bot.locales.main import get_localization, get_user_language

dalle_router = Router()

PRICE_DALLE3 = 0.040


@dalle_router.message(Command("dalle3"))
async def dalle3(message: Message, state: FSMContext):
    await state.clear()

    user_id = str(message.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    if user.current_model == Model.DALLE3:
        reply_markup = await build_recommendations_keyboard(user.current_model, user_language_code, user.gender)
        await message.answer(
            text=get_localization(user_language_code).ALREADY_SWITCHED_TO_THIS_MODEL,
            reply_markup=reply_markup,
        )
    else:
        user.current_model = Model.DALLE3
        await update_user(user_id, {
            "current_model": user.current_model,
        })

        reply_markup = await build_recommendations_keyboard(user.current_model, user_language_code, user.gender)
        await message.answer(
            text=get_localization(user_language_code).SWITCHED_TO_DALLE3,
            reply_markup=reply_markup,
        )


async def handle_dalle(message: Message, state: FSMContext, user: User):
    await state.update_data(is_processing=True)

    user_language_code = await get_user_language(user.id, state.storage)
    user_data = await state.get_data()

    text = user_data.get('recognized_text', None)
    if text is None:
        text = message.text

    processing_message = await message.reply(text=get_localization(user_language_code).processing_request_image())

    async with ChatActionSender.upload_photo(bot=message.bot, chat_id=message.chat.id):
        try:
            maximum_generations = user.monthly_limits[Quota.DALLE3] + user.additional_usage_quota[Quota.DALLE3]
            resolution = user.settings[Model.DALLE3][UserSettings.RESOLUTION]
            quality = user.settings[Model.DALLE3][UserSettings.QUALITY]
            cost = get_cost_for_image(quality, resolution)
            if maximum_generations < cost:
                await message.reply(get_localization(user_language_code).REACHED_USAGE_LIMIT)
                return

            response_url = await get_response_image(
                text,
                resolution,
                quality,
            )

            quantity_to_delete = cost
            quantity_deleted = 0
            while quantity_deleted != quantity_to_delete:
                if user.monthly_limits[Quota.DALLE3] != 0:
                    user.monthly_limits[Quota.DALLE3] -= 1
                    quantity_deleted += 1
                elif user.additional_usage_quota[Quota.DALLE3] != 0:
                    user.additional_usage_quota[Quota.DALLE3] -= 1
                    quantity_deleted += 1
                else:
                    break

            await update_user(
                user.id, {
                    "monthly_limits": user.monthly_limits,
                    "additional_usage_quota": user.additional_usage_quota,
                },
            )
            await write_transaction(
                user_id=user.id,
                type=TransactionType.EXPENSE,
                service=ServiceType.DALLE3,
                amount=PRICE_DALLE3 * cost,
                currency=Currency.USD,
                quantity=1,
                details={
                    'text': text,
                },
            )

            footer_text = f'\n\n✉️ {user.monthly_limits[Quota.DALLE3] + user.additional_usage_quota[Quota.DALLE3] + 1}' \
                if user.settings[user.current_model][UserSettings.SHOW_USAGE_QUOTA] else ''
            await message.reply_photo(
                caption=f"{get_localization(user_language_code).IMAGE_SUCCESS}{footer_text}",
                photo=response_url,
            )
        except openai.BadRequestError as e:
            if e.code == 'content_policy_violation':
                await message.reply(
                    text=get_localization(user_language_code).REQUEST_FORBIDDEN_ERROR,
                )
        except Exception as e:
            await message.answer(
                text=get_localization(user_language_code).ERROR,
                parse_mode=None
            )
            await send_message_to_admins(
                bot=message.bot,
                message=f"#error\n\nALARM! Ошибка у пользователя при запросе в DALLE: {user.id}\nИнформация:\n{e}",
                parse_mode=None,
            )
        finally:
            await processing_message.delete()
            await state.update_data(is_processing=False)
