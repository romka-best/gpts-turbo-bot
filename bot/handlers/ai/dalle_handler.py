import asyncio

import openai
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender

from bot.config import config, MessageEffect
from bot.database.models.common import Quota, Currency, Model
from bot.database.models.transaction import TransactionType, ServiceType
from bot.database.models.user import UserSettings, User
from bot.database.operations.transaction.writers import write_transaction
from bot.database.operations.user.getters import get_user
from bot.database.operations.user.updaters import update_user
from bot.handlers.ai.midjourney_handler import handle_midjourney_example
from bot.helpers.senders.send_error_info import send_error_info
from bot.helpers.updaters.update_user_usage_quota import update_user_usage_quota
from bot.integrations.openAI import get_response_image, get_cost_for_image
from bot.keyboards.common.common import build_recommendations_keyboard, build_error_keyboard
from bot.locales.main import get_localization, get_user_language

dall_e_router = Router()

PRICE_DALL_E = 0.040


@dall_e_router.message(Command('dalle'))
async def dall_e(message: Message, state: FSMContext):
    await state.clear()

    user_id = str(message.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    if user.current_model == Model.DALL_E:
        reply_markup = await build_recommendations_keyboard(user.current_model, user_language_code, user.gender)
        await message.answer(
            text=get_localization(user_language_code).ALREADY_SWITCHED_TO_THIS_MODEL,
            reply_markup=reply_markup,
        )
    else:
        user.current_model = Model.DALL_E
        await update_user(user_id, {
            'current_model': user.current_model,
        })

        reply_markup = await build_recommendations_keyboard(user.current_model, user_language_code, user.gender)
        await message.answer(
            text=get_localization(user_language_code).SWITCHED_TO_DALL_E,
            reply_markup=reply_markup,
            message_effect_id=config.MESSAGE_EFFECTS.get(MessageEffect.FIRE),
        )


async def handle_dall_e(message: Message, state: FSMContext, user: User):
    await state.update_data(is_processing=True)

    user_language_code = await get_user_language(user.id, state.storage)
    user_data = await state.get_data()

    text = user_data.get('recognized_text', None)
    if text is None:
        text = message.text

    processing_message = await message.reply(text=get_localization(user_language_code).processing_request_image())

    async with ChatActionSender.upload_photo(bot=message.bot, chat_id=message.chat.id):
        try:
            maximum_generations = user.daily_limits[Quota.DALL_E] + user.additional_usage_quota[Quota.DALL_E]
            model_version = user.settings[Model.DALL_E][UserSettings.VERSION]
            resolution = user.settings[Model.DALL_E][UserSettings.RESOLUTION]
            quality = user.settings[Model.DALL_E][UserSettings.QUALITY]
            cost = get_cost_for_image(quality, resolution)
            if maximum_generations < cost:
                await message.reply(get_localization(user_language_code).REACHED_USAGE_LIMIT)
                return

            response_url = await get_response_image(
                model_version,
                text,
                resolution,
                quality,
            )

            await update_user_usage_quota(user, Quota.DALL_E, cost)

            total_price = PRICE_DALL_E * cost
            await write_transaction(
                user_id=user.id,
                type=TransactionType.EXPENSE,
                service=ServiceType.DALL_E,
                amount=total_price,
                clear_amount=total_price,
                currency=Currency.USD,
                quantity=1,
                details={
                    'text': text,
                    'has_error': False,
                },
            )

            footer_text = f'\n\n🖼 {user.daily_limits[Quota.DALL_E] + user.additional_usage_quota[Quota.DALL_E] + 1}' \
                if user.settings[user.current_model][UserSettings.SHOW_USAGE_QUOTA] and \
                   user.daily_limits[Quota.DALL_E] != float('inf') else ''
            await message.reply_photo(
                caption=f'{get_localization(user_language_code).IMAGE_SUCCESS}{footer_text}',
                photo=response_url,
            )
        except openai.BadRequestError as e:
            if e.code == 'content_policy_violation':
                await message.reply(
                    text=get_localization(user_language_code).REQUEST_FORBIDDEN_ERROR,
                )
        except Exception as e:
            reply_markup = build_error_keyboard(user_language_code)
            await message.answer(
                text=get_localization(user_language_code).ERROR,
                reply_markup=reply_markup,
                parse_mode=None,
            )
            await send_error_info(
                bot=message.bot,
                user_id=user.id,
                info=str(e),
                hashtags=['dalle'],
            )
        finally:
            await processing_message.delete()
            await state.update_data(is_processing=False)

    asyncio.create_task(
        handle_midjourney_example(
            user=user,
            user_language_code=user_language_code,
            prompt=text,
            message=message,
        )
    )
