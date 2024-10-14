from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender

from bot.config import config, MessageEffect
from bot.database.models.common import Model
from bot.database.models.generation import GenerationStatus
from bot.database.models.request import RequestStatus
from bot.database.models.user import User, UserSettings
from bot.database.operations.generation.getters import get_generations_by_request_id
from bot.database.operations.generation.updaters import update_generation
from bot.database.operations.generation.writers import write_generation
from bot.database.operations.request.getters import get_started_requests_by_user_id_and_model
from bot.database.operations.request.updaters import update_request
from bot.database.operations.request.writers import write_request
from bot.database.operations.user.getters import get_user
from bot.database.operations.user.updaters import update_user
from bot.helpers.senders.send_error_info import send_error_info
from bot.integrations.replicateAI import create_flux_image
from bot.keyboards.ai.mode import build_switched_to_ai_keyboard
from bot.keyboards.common.common import build_error_keyboard
from bot.locales.main import get_user_language, get_localization
from bot.locales.translate_text import translate_text

flux_router = Router()

PRICE_FLUX = 0.04


@flux_router.message(Command('flux'))
async def flux(message: Message, state: FSMContext):
    await state.clear()

    user_id = str(message.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    if user.current_model == Model.FLUX:
        reply_markup = build_switched_to_ai_keyboard(user_language_code, Model.FLUX)
        await message.answer(
            text=get_localization(user_language_code).ALREADY_SWITCHED_TO_THIS_MODEL,
            reply_markup=reply_markup,
        )
    else:
        user.current_model = Model.FLUX
        await update_user(user_id, {
            'current_model': user.current_model,
        })

        reply_markup = build_switched_to_ai_keyboard(user_language_code, Model.FLUX)
        await message.answer(
            text=get_localization(user_language_code).SWITCHED_TO_FLUX,
            reply_markup=reply_markup,
            message_effect_id=config.MESSAGE_EFFECTS.get(MessageEffect.FIRE),
        )


async def handle_flux(message: Message, state: FSMContext, user: User):
    user_language_code = await get_user_language(user.id, state.storage)
    user_data = await state.get_data()

    prompt = user_data.get('recognized_text', None)
    if prompt is None:
        prompt = message.text

    processing_message = await message.reply(
        text=get_localization(user_language_code).processing_request_image(),
        allow_sending_without_reply=True,
    )

    async with ChatActionSender.upload_photo(bot=message.bot, chat_id=message.chat.id):
        user_not_finished_requests = await get_started_requests_by_user_id_and_model(user.id, Model.FLUX)

        if len(user_not_finished_requests):
            await message.reply(
                text=get_localization(user_language_code).ALREADY_MAKE_REQUEST,
                allow_sending_without_reply=True,
            )
            await processing_message.delete()
            return

        request = await write_request(
            user_id=user.id,
            message_id=processing_message.message_id,
            model=Model.FLUX,
            requested=1,
        )

        try:
            if user_language_code != 'en':
                prompt = await translate_text(prompt, user_language_code, 'en')
            result_id = await create_flux_image(prompt, user.settings[Model.FLUX][UserSettings.SAFETY_TOLERANCE])

            await write_generation(
                id=result_id,
                request_id=request.id,
                model=Model.FLUX,
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
                hashtags=['flux'],
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
