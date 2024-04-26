from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.chat_action import ChatActionSender

from bot.database.models.common import Model, Quota, MidjourneyAction
from bot.database.models.user import User
from bot.database.operations.generation.getters import get_generation
from bot.database.operations.generation.writers import write_generation
from bot.database.operations.request.getters import get_started_requests_by_user_id_and_model
from bot.database.operations.request.writers import write_request
from bot.database.operations.user.getters import get_user
from bot.database.operations.user.updaters import update_user
from bot.helpers.senders.send_message_to_admins import send_message_to_admins
from bot.helpers.translate_text import translate_text
from bot.integrations.midjourney import (
    create_midjourney_images,
    create_midjourney_image,
    create_different_midjourney_image, create_different_midjourney_images,
)
from bot.keyboards.common.common import build_recommendations_keyboard
from bot.locales.main import get_localization, get_user_language

midjourney_router = Router()

PRICE_MIDJOURNEY_REQUEST = 0.04


@midjourney_router.message(Command("midjourney"))
async def midjourney(message: Message, state: FSMContext):
    await state.clear()

    user_id = str(message.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    if user.current_model == Model.MIDJOURNEY:
        reply_markup = await build_recommendations_keyboard(user.current_model, user_language_code, user.gender)
        await message.answer(
            text=get_localization(user_language_code).ALREADY_SWITCHED_TO_THIS_MODEL,
            reply_markup=reply_markup,
        )
    else:
        user.current_model = Model.MIDJOURNEY
        await update_user(user_id, {
            "current_model": user.current_model,
        })

        reply_markup = await build_recommendations_keyboard(user.current_model, user_language_code, user.gender)
        await message.answer(
            text=get_localization(user_language_code).SWITCHED_TO_MIDJOURNEY,
            reply_markup=reply_markup,
        )


async def handle_midjourney(
    message: Message,
    state: FSMContext,
    user: User,
    prompt: str,
    action: MidjourneyAction,
    hash_id="",
    choice=0,
):
    await state.update_data(is_processing=True)

    user_language_code = await get_user_language(user.id, state.storage)
    user_data = await state.get_data()

    prompt = user_data.get('recognized_text', prompt)

    processing_message = await message.reply(text=get_localization(user_language_code).processing_request_image())

    async with ChatActionSender.upload_photo(bot=message.bot, chat_id=message.chat.id):
        try:
            quota = user.monthly_limits[Quota.MIDJOURNEY] + user.additional_usage_quota[Quota.MIDJOURNEY]
            if quota < 1:
                await message.reply(get_localization(user_language_code).REACHED_USAGE_LIMIT)
            else:
                user_not_finished_requests = await get_started_requests_by_user_id_and_model(user.id, Model.MIDJOURNEY)

                if len(user_not_finished_requests):
                    await message.reply(
                        text=get_localization(user_language_code).ALREADY_MAKE_REQUEST,
                    )
                    await processing_message.delete()
                    return

                request = await write_request(
                    user_id=user.id,
                    message_id=processing_message.message_id,
                    model=Model.MIDJOURNEY,
                    requested=1,
                    details={
                        "prompt": prompt,
                        "action": action,
                    }
                )

                if user_language_code != 'en':
                    prompt = await translate_text(prompt, user_language_code, 'en')

                if action == MidjourneyAction.UPSCALE:
                    result_id = await create_midjourney_image(hash_id, choice)
                elif action == MidjourneyAction.VARIATION:
                    result_id = await create_different_midjourney_image(hash_id, choice)
                elif action == MidjourneyAction.REROLL:
                    result_id = await create_different_midjourney_images(hash_id)
                else:
                    result_id = await create_midjourney_images(prompt)
                await write_generation(
                    id=result_id,
                    request_id=request.id,
                    model=Model.MIDJOURNEY,
                    has_error=result_id is None,
                    details={
                        "prompt": prompt,
                        "action": action,
                    }
                )
        except Exception as e:
            await message.answer(
                text=get_localization(user_language_code).ERROR,
                parse_mode=None
            )
            await send_message_to_admins(
                bot=message.bot,
                message=f"#error\n\nALARM! Ошибка у пользователя при запросе в MIDJOURNEY: {user.id}\nИнформация:\n{e}",
                parse_mode=None,
            )


@midjourney_router.callback_query(lambda c: c.data.startswith('midjourney:'))
async def handle_midjourney_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)
    user = await get_user(user_id)

    action = callback_query.data.split(':')[1]
    hash_id = callback_query.data.split(':')[2]

    generation = await get_generation(hash_id)

    if action.startswith("u"):
        choice = int(action[1:])
        await handle_midjourney(
            callback_query.message,
            state,
            user,
            generation.details.get('prompt'),
            MidjourneyAction.UPSCALE,
            hash_id,
            choice,
        )
    elif action.startswith("v"):
        choice = int(action[1:])
        await handle_midjourney(
            callback_query.message,
            state,
            user,
            generation.details.get('prompt'),
            MidjourneyAction.VARIATION,
            hash_id,
            choice,
        )
    elif action == "again":
        await handle_midjourney(
            callback_query.message,
            state,
            user,
            generation.details.get('prompt'),
            MidjourneyAction.REROLL,
            hash_id,
        )

    await state.clear()
