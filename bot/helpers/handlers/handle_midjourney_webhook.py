import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey

from bot.database.models.common import Quota, Currency, Model, MidjourneyAction
from bot.database.models.generation import GenerationStatus, Generation
from bot.database.models.request import Request, RequestStatus
from bot.database.models.transaction import TransactionType, ServiceType
from bot.database.models.user import User, UserSettings
from bot.database.operations.generation.getters import get_generation
from bot.database.operations.generation.updaters import update_generation
from bot.database.operations.request.getters import get_request
from bot.database.operations.request.updaters import update_request
from bot.database.operations.transaction.writers import write_transaction
from bot.database.operations.user.getters import get_user
from bot.database.operations.user.updaters import update_user
from bot.handlers.ai.midjourney_handler import PRICE_MIDJOURNEY_REQUEST
from bot.helpers.senders.send_error_info import send_error_info
from bot.helpers.senders.send_images import send_image
from bot.keyboards.ai.midjourney import build_midjourney_keyboard
from bot.keyboards.common.common import build_reaction_keyboard, build_error_keyboard
from bot.locales.main import get_localization, get_user_language


async def handle_midjourney_webhook(bot: Bot, dp: Dispatcher, body: dict):
    generation = await get_generation(body.get('hash'))
    if not generation:
        return False
    elif generation.status == GenerationStatus.FINISHED:
        return True

    generation_error = body.get("status_reason", False)
    generation_result = body.get("result", {})
    if generation_error or not generation_result:
        generation.status = GenerationStatus.FINISHED
        generation.has_error = True
        generation.details["error"] = generation_error
        await update_generation(generation.id, {
            "status": generation.status,
            "has_error": generation.has_error,
        })
        logging.error(f"Error in midjourney_webhook: {generation_error}")
    else:
        generation.status = GenerationStatus.FINISHED
        generation.result = generation_result.get("url", "")
        await update_generation(generation.id, {
            "status": generation.status,
            "result": generation.result,
        })

    request = await get_request(generation.request_id)
    user = await get_user(request.user_id)

    await handle_midjourney_result(bot, dp, user, request, generation)

    return True


async def handle_midjourney_result(
    bot: Bot,
    dp: Dispatcher,
    user: User,
    request: Request,
    generation: Generation,
):
    is_suggestion = generation.details.get('is_suggestion', False)
    action_type = generation.details.get('action')
    user_language_code = await get_user_language(user.id, dp.storage)
    if not generation.has_error and not is_suggestion:
        reply_markup = build_midjourney_keyboard(generation.id) if action_type != MidjourneyAction.UPSCALE \
            else build_reaction_keyboard(generation.id)
        footer_text = f'\n\n🖼 {user.monthly_limits[Quota.MIDJOURNEY] + user.additional_usage_quota[Quota.MIDJOURNEY]}' \
            if user.settings[Model.MIDJOURNEY][UserSettings.SHOW_USAGE_QUOTA] else ''
        caption = f"{get_localization(user_language_code).IMAGE_SUCCESS}{footer_text}"
        await send_image(bot, user.telegram_chat_id, generation.result, reply_markup, caption)
    elif not generation.has_error and is_suggestion:
        await send_image(
            bot,
            user.telegram_chat_id,
            generation.result,
            None,
            get_localization(user_language_code).MIDJOURNEY_EXAMPLE,
            request.message_id,
        )
    else:
        generation_error = generation.details.get('error')
        if "banned prompt detected" in generation_error:
            if not is_suggestion:
                await bot.send_message(
                    chat_id=user.telegram_chat_id,
                    text=get_localization(user_language_code).REQUEST_FORBIDDEN_ERROR,
                )
        elif "You can request another upscale for this image" in generation_error:
            await bot.send_message(
                chat_id=user.telegram_chat_id,
                text=get_localization(user_language_code).MIDJOURNEY_ALREADY_CHOSE_UPSCALE,
            )
        else:
            if not is_suggestion:
                reply_markup = build_error_keyboard(user_language_code)
                await bot.send_message(
                    chat_id=user.telegram_chat_id,
                    text=get_localization(user_language_code).ERROR,
                    reply_markup=reply_markup,
                )
            await send_error_info(
                bot=bot,
                user_id=user.id,
                info=str(generation_error),
                hashtags=["midjourney"],
            )

    request.status = RequestStatus.FINISHED
    await update_request(request.id, {
        "status": request.status
    })

    if not generation.has_error and user.monthly_limits[Quota.MIDJOURNEY] != 0 and not is_suggestion:
        user.monthly_limits[Quota.MIDJOURNEY] -= 1
    elif not generation.has_error and user.additional_usage_quota[Quota.MIDJOURNEY] != 0 and not is_suggestion:
        user.additional_usage_quota[Quota.MIDJOURNEY] -= 1

    update_tasks = [
        write_transaction(
            user_id=user.id,
            type=TransactionType.EXPENSE,
            service=ServiceType.MIDJOURNEY,
            amount=PRICE_MIDJOURNEY_REQUEST,
            clear_amount=PRICE_MIDJOURNEY_REQUEST,
            currency=Currency.USD,
            quantity=1,
            details={
                "prompt": generation.details.get('prompt'),
                "type": generation.details.get('action'),
                "is_suggestion": generation.details.get('is_suggestion', False),
                "has_error": generation.details.get('has_error', False),
            }
        ),
        update_user(
            user.id,
            {
                "monthly_limits": user.monthly_limits,
                "additional_usage_quota": user.additional_usage_quota,
            },
        ),
    ]

    await asyncio.gather(*update_tasks)

    state = FSMContext(
        storage=dp.storage,
        key=StorageKey(
            chat_id=int(user.telegram_chat_id),
            user_id=int(user.id),
            bot_id=bot.id,
        )
    )
    await state.clear()

    if not is_suggestion:
        await bot.delete_message(user.telegram_chat_id, request.message_id)
