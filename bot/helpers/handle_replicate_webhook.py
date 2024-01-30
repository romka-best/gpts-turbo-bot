import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey

from bot.database.main import firebase
from bot.database.models.common import Model, Currency, Quota
from bot.database.models.generation import GenerationStatus
from bot.database.models.request import RequestStatus
from bot.database.models.transaction import TransactionType, ServiceType
from bot.database.operations.face_swap_package import update_used_face_swap_package, get_used_face_swap_package
from bot.database.operations.generation import get_generation, update_generation, get_generations_by_request_id
from bot.database.operations.request import get_request, update_request
from bot.database.operations.transaction import write_transaction
from bot.database.operations.user import get_user, update_user
from bot.handlers.face_swap_handler import PRICE_FACE_SWAP, handle_face_swap
from bot.helpers.send_images import send_image
from bot.keyboards.face_swap import build_face_swap_reaction_keyboard


async def handle_replicate_webhook(bot: Bot, dp: Dispatcher, prediction: dict):
    generation = await get_generation(prediction.get("id"))
    if not generation:
        return False
    elif generation.status == GenerationStatus.FINISHED:
        return True

    generation_error, generation_result = prediction.get("error", False), prediction.get("output", {}).get("image")
    seconds = prediction.get("metrics", {}).get("predict_time")
    if generation_error or not generation_result:
        generation.has_error = True
        await update_generation(generation.id, {
            "status": GenerationStatus.FINISHED,
            "has_error": generation.has_error,
            "seconds": seconds,
        })
        logging.error(f"Error in replicate_webhook: {prediction.get('logs')}")
    else:
        generation.status = GenerationStatus.FINISHED
        generation.result = generation_result
        generation.seconds = seconds
        await update_generation(generation.id, {
            "status": generation.status,
            "result": generation.result,
            "seconds": generation.seconds,
        })

    await firebase.counter.increment_counter(firebase.db.collection('requests').document(generation.request_id))
    executed = await firebase.counter.get_count(firebase.db.collection('requests').document(generation.request_id))
    request = await get_request(generation.request_id)
    user = await get_user(request.user_id)

    if request.model == Model.FACE_SWAP:
        reply_markup = build_face_swap_reaction_keyboard(
            user.language_code,
            generation.id,
        )
        await send_image(bot, user.telegram_chat_id, generation.result, reply_markup)

    if executed == request.requested and request.status != RequestStatus.FINISHED:
        request.status = RequestStatus.FINISHED
        await update_request(request.id, {
            "status": request.status
        })

        request_generations = await get_generations_by_request_id(request.id)
        success_generations = []
        used_face_swap_package_used_images = []
        total_seconds = 0
        for request_generation in request_generations:
            if request_generation.result:
                success_generations.append(request_generation.result)
            if request_generation.details.get('used_face_swap_package_used_image'):
                used_face_swap_package_used_images.append(
                    request_generation.details.get('used_face_swap_package_used_image')
                )
            total_seconds += request_generation.seconds

        total_result = len(success_generations)

        if request.model == Model.FACE_SWAP:
            used_face_swap_package = await get_used_face_swap_package(
                generation.details.get("used_face_swap_package_id")
            )
            if request.details.get("is_test"):
                update_tasks = [
                    write_transaction(user_id=user.id,
                                      type=TransactionType.EXPENSE,
                                      service=ServiceType.FACE_SWAP,
                                      amount=round(PRICE_FACE_SWAP * total_seconds, 6),
                                      currency=Currency.USD,
                                      quantity=total_result,
                                      details={
                                          'name': request.details.get("face_swap_package_name"),
                                          'images': success_generations,
                                          'seconds': total_seconds,
                                      }),
                ]
            else:
                quantity_to_delete = total_result
                quantity_deleted = 0
                while quantity_deleted != quantity_to_delete:
                    if user.monthly_limits[Quota.FACE_SWAP] != 0:
                        user.monthly_limits[Quota.FACE_SWAP] -= 1
                        quantity_deleted += 1
                    elif user.additional_usage_quota[Quota.FACE_SWAP] != 0:
                        user.additional_usage_quota[Quota.FACE_SWAP] -= 1
                        quantity_deleted += 1
                    else:
                        break

                update_tasks = [
                    write_transaction(user_id=user.id,
                                      type=TransactionType.EXPENSE,
                                      service=ServiceType.FACE_SWAP,
                                      amount=round(PRICE_FACE_SWAP * total_seconds, 6),
                                      currency=Currency.USD,
                                      quantity=quantity_to_delete,
                                      details={
                                          'name': request.details.get("face_swap_package_name"),
                                          'images': success_generations,
                                          'seconds': total_seconds,
                                      }),
                    update_user(user.id, {
                        "monthly_limits": user.monthly_limits,
                        "additional_usage_quota": user.additional_usage_quota
                    }),
                    update_used_face_swap_package(used_face_swap_package.id, {
                        "used_images": used_face_swap_package.used_images + used_face_swap_package_used_images,
                    })
                ]

            await asyncio.gather(*update_tasks)

            state = FSMContext(
                storage=dp.storage,
                key=StorageKey(
                    chat_id=int(user.telegram_chat_id),
                    user_id=int(user.id),
                    bot_id=bot.id)
            )
            await handle_face_swap(bot, user.telegram_chat_id, state, user.id)

            await bot.delete_message(user.telegram_chat_id, request.message_id)

        return True
