import asyncio
import logging

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey, BaseStorage
from aiogram.utils.markdown import hlink

from bot.database.models.common import Quota, Currency, Model, SunoSendType
from bot.database.models.generation import GenerationStatus, Generation
from bot.database.models.request import RequestStatus, Request
from bot.database.models.transaction import TransactionType
from bot.database.models.user import UserSettings, User
from bot.database.operations.generation.getters import get_generation, get_generations_by_request_id
from bot.database.operations.generation.updaters import update_generation
from bot.database.operations.product.getters import get_product_by_quota
from bot.database.operations.request.getters import get_request
from bot.database.operations.request.updaters import update_request
from bot.database.operations.transaction.writers import write_transaction
from bot.database.operations.user.getters import get_user
from bot.database.operations.user.updaters import update_user
from bot.helpers.senders.send_audio import send_audio
from bot.helpers.senders.send_video import send_video
from bot.helpers.updaters.update_user_usage_quota import get_user_with_updated_quota
from bot.keyboards.ai.suno import build_suno_keyboard
from bot.keyboards.common.common import build_reaction_keyboard
from bot.locales.main import get_user_language, get_localization


async def handle_suno_webhook(bot: Bot, storage: BaseStorage, body: dict):
    generation = await get_generation(body.get('id'))
    if not generation:
        return False
    elif generation.status == GenerationStatus.FINISHED:
        return True

    generation_status, generation_result = body.get('status', 'error'), body.get('audio_url', '')
    is_suggestion = generation.details.get('is_suggestion', False)
    metadata = body.get('metadata', {})

    generation.status = GenerationStatus.FINISHED
    if generation_status == 'error' or not generation_result or '/None.mp3' in generation_result:
        generation.has_error = True
        await update_generation(generation.id, {
            'status': generation.status,
            'has_error': generation.has_error,
        })

        error_type, error_message = metadata.get('error_type'), metadata.get('error_message')
        logging.error(f'Error in suno_webhook: {error_type}: {error_message}')
    else:
        generation.result = generation_result
        new_details = {
            'title': body.get('title'),
            'audio_url': body.get('audio_url'),
            'video_url': body.get('video_url'),
            'image_url': body.get('image_large_url'),
        }
        generation.details = {**generation.details, **new_details}
        await update_generation(generation.id, {
            'status': generation.status,
            'result': generation.result,
            'details': generation.details,
        })

    request = await get_request(generation.request_id)
    user = await get_user(request.user_id)
    user_language_code = await get_user_language(user.id, storage)

    if generation_result and '/None.mp3' not in generation_result and not is_suggestion:
        (
            duration,
            video_url,
            audio_url,
            title,
        ) = (
            int(metadata.get('duration', 0)),
            body.get('video_url'),
            body.get('audio_url'),
            body.get('title', '🎸'),
        )

        reply_markup = build_reaction_keyboard(generation.id)
        if user.settings[Model.SUNO][UserSettings.SEND_TYPE] == SunoSendType.VIDEO and video_url:
            await send_video(
                bot,
                user.telegram_chat_id,
                video_url,
                hlink(get_localization(user_language_code).AUDIO, audio_url),
                title,
                duration,
                reply_markup,
            )
        elif user.settings[Model.SUNO][UserSettings.SEND_TYPE] == SunoSendType.AUDIO and video_url:
            await send_audio(
                bot,
                user.telegram_chat_id,
                generation.result,
                hlink(get_localization(user_language_code).VIDEO, video_url),
                title,
                duration,
                reply_markup,
            )
        else:
            await send_audio(
                bot,
                user.telegram_chat_id,
                generation.result,
                hlink(get_localization(user_language_code).AUDIO, audio_url),
                title,
                duration,
                reply_markup,
            )
    elif generation_result and '/None.mp3' not in generation_result and is_suggestion:
        asyncio.create_task(
            send_suno_example(
                bot=bot,
                user=user,
                user_language_code=user_language_code,
                generation=generation,
                request=request,
                body=body,
                duration=int(metadata.get('duration', 0)),
            )
        )

    current_count = await storage.redis.incr(request.id)
    if current_count == request.requested and request.status != RequestStatus.FINISHED:
        request.status = RequestStatus.FINISHED
        await update_request(request.id, {
            'status': request.status
        })

        request_generations = await get_generations_by_request_id(request.id)
        success_generations = []
        for request_generation in request_generations:
            if request_generation.result:
                success_generations.append(request_generation.result)

        total_result = len(success_generations)

        if total_result != len(request_generations):
            error_type, error_message = metadata.get('error_type'), metadata.get('error_message')
            if error_type == 'moderation_failure':
                if not is_suggestion:
                    await bot.send_message(
                        chat_id=user.telegram_chat_id,
                        text=get_localization(user_language_code).REQUEST_FORBIDDEN_ERROR,
                    )

        quantity_to_delete = total_result
        user = get_user_with_updated_quota(user, Quota.SUNO, quantity_to_delete)

        product = await get_product_by_quota(Quota.SUNO)
        update_tasks = [
            write_transaction(
                user_id=user.id,
                type=TransactionType.EXPENSE,
                product_id=product.id,
                amount=0,
                clear_amount=0,
                currency=Currency.USD,
                quantity=quantity_to_delete,
                details={
                    'mode': request.details.get('mode'),
                    'is_suggestion': request.details.get('is_suggestion', False),
                    'has_error': generation.has_error,
                }
            ),
            update_user(user.id, {
                'daily_limits': user.daily_limits,
                'additional_usage_quota': user.additional_usage_quota
            }),
        ]

        await asyncio.gather(*update_tasks)

        state = FSMContext(
            storage=storage,
            key=StorageKey(
                chat_id=int(user.telegram_chat_id),
                user_id=int(user.id),
                bot_id=bot.id,
            )
        )
        await state.clear()
        user_language_code = await get_user_language(str(user.id), state.storage)

        if not is_suggestion and user.current_model == Model.SUNO:
            reply_markup = build_suno_keyboard(user_language_code)
            await bot.send_message(
                chat_id=user.telegram_chat_id,
                text=get_localization(user_language_code).SUNO_INFO,
                reply_markup=reply_markup,
            )
        if not is_suggestion:
            await bot.delete_message(user.telegram_chat_id, request.message_id)

    return True


async def send_suno_example(
    bot: Bot,
    user: User,
    user_language_code: str,
    generation: Generation,
    request: Request,
    body: dict,
    duration: int,
):
    await asyncio.sleep(60)

    if body.get('video_url'):
        is_okay = await send_video(
            bot=bot,
            chat_id=user.telegram_chat_id,
            result=body.get('video_url'),
            caption=get_localization(user_language_code).SUNO_EXAMPLE,
            filename=body.get('title', '🎸'),
            duration=duration,
            reply_to_message_id=request.message_id,
        )

        if not is_okay:
            await send_audio(
                bot=bot,
                chat_id=user.telegram_chat_id,
                result=generation.result,
                caption=get_localization(user_language_code).SUNO_EXAMPLE,
                filename=body.get('title', '🎸'),
                duration=duration,
                reply_to_message_id=request.message_id,
            )
    else:
        await send_audio(
            bot=bot,
            chat_id=user.telegram_chat_id,
            result=generation.result,
            caption=get_localization(user_language_code).SUNO_EXAMPLE,
            filename=body.get('title', '🎸'),
            duration=duration,
            reply_to_message_id=request.message_id,
        )
