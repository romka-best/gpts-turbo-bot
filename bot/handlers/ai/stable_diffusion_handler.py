import asyncio

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender

from bot.config import config, MessageEffect
from bot.database.models.common import Model
from bot.database.models.generation import GenerationStatus
from bot.database.models.request import RequestStatus
from bot.database.models.user import User
from bot.database.operations.generation.getters import get_generations_by_request_id
from bot.database.operations.generation.updaters import update_generation
from bot.database.operations.generation.writers import write_generation
from bot.database.operations.request.getters import get_started_requests_by_user_id_and_model
from bot.database.operations.request.updaters import update_request
from bot.database.operations.request.writers import write_request
from bot.database.operations.user.getters import get_user
from bot.database.operations.user.updaters import update_user
from bot.handlers.ai.midjourney_handler import handle_midjourney_example
from bot.helpers.senders.send_error_info import send_error_info
from bot.integrations.replicateAI import create_stable_diffusion_image
from bot.keyboards.common.common import build_recommendations_keyboard, build_error_keyboard
from bot.locales.main import get_user_language, get_localization
from bot.locales.translate_text import translate_text

stable_diffusion_router = Router()

PRICE_STABLE_DIFFUSION = 0.0014


@stable_diffusion_router.message(Command('stable_diffusion'))
async def stable_diffusion(message: Message, state: FSMContext):
    await state.clear()

    user_id = str(message.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    if user.current_model == Model.STABLE_DIFFUSION:
        reply_markup = await build_recommendations_keyboard(user.current_model, user_language_code, user.gender)
        await message.answer(
            text=get_localization(user_language_code).ALREADY_SWITCHED_TO_THIS_MODEL,
            reply_markup=reply_markup,
        )
    else:
        user.current_model = Model.STABLE_DIFFUSION
        await update_user(user_id, {
            'current_model': user.current_model,
        })

        reply_markup = await build_recommendations_keyboard(user.current_model, user_language_code, user.gender)
        await message.answer(
            text=get_localization(user_language_code).SWITCHED_TO_STABLE_DIFFUSION,
            reply_markup=reply_markup,
            message_effect_id=config.MESSAGE_EFFECTS.get(MessageEffect.FIRE),
        )


async def handle_stable_diffusion(message: Message, state: FSMContext, user: User):
    user_language_code = await get_user_language(user.id, state.storage)
    user_data = await state.get_data()

    prompt = user_data.get('recognized_text', None)
    if prompt is None:
        prompt = message.text

    processing_message = await message.reply(text=get_localization(user_language_code).processing_request_image())

    async with ChatActionSender.upload_photo(bot=message.bot, chat_id=message.chat.id):
        user_not_finished_requests = await get_started_requests_by_user_id_and_model(user.id, Model.STABLE_DIFFUSION)

        if len(user_not_finished_requests):
            await message.reply(
                text=get_localization(user_language_code).ALREADY_MAKE_REQUEST,
            )
            await processing_message.delete()
            return

        request = await write_request(
            user_id=user.id,
            message_id=processing_message.message_id,
            model=Model.STABLE_DIFFUSION,
            requested=1,
        )

        try:
            if user_language_code != 'en':
                prompt = await translate_text(prompt, user_language_code, 'en')
            result_id = await create_stable_diffusion_image(prompt)

            await write_generation(
                id=result_id,
                request_id=request.id,
                model=Model.STABLE_DIFFUSION,
                has_error=result_id is None,
                details={
                    'prompt': prompt,
                }
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
                hashtags=['stable_diffusion'],
            )

            request.status = RequestStatus.FINISHED
            await update_request(request.id, {
                'status': request.status
            })

            generations = await get_generations_by_request_id(request.id)
            for generation in generations:
                generation.status = GenerationStatus.FINISHED,
                generation.has_error = True
                await update_generation(
                    generation.id,
                    {
                        'status': generation.status,
                        'has_error': generation.has_error,
                    },
                )

    asyncio.create_task(
        handle_midjourney_example(
            user=user,
            user_language_code=user_language_code,
            prompt=prompt,
            message=message,
        )
    )
