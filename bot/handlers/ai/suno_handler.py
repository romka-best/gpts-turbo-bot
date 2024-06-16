import asyncio

from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.chat_action import ChatActionSender

from bot.database.models.common import Model, SunoMode, Quota, SunoVersion
from bot.database.models.generation import GenerationStatus
from bot.database.models.request import RequestStatus
from bot.database.models.subscription import SubscriptionType
from bot.database.models.user import User, UserSettings
from bot.database.operations.generation.getters import get_generations_by_request_id
from bot.database.operations.generation.updaters import update_generation
from bot.database.operations.generation.writers import write_generation
from bot.database.operations.request.getters import get_started_requests_by_user_id_and_model
from bot.database.operations.request.updaters import update_request
from bot.database.operations.request.writers import write_request
from bot.database.operations.user.getters import get_user
from bot.database.operations.user.updaters import update_user
from bot.helpers.senders.send_message_to_admins import send_message_to_admins
from bot.integrations.suno import generate_song, check_song
from bot.keyboards.ai.suno import (
    build_suno_keyboard,
    build_suno_simple_mode_keyboard,
    build_suno_custom_mode_lyrics_keyboard,
    build_suno_custom_mode_genres_keyboard,
)
from bot.keyboards.common.common import build_recommendations_keyboard, build_cancel_keyboard, build_error_keyboard
from bot.locales.main import get_user_language, get_localization
from bot.locales.translate_text import translate_text
from bot.states.suno import Suno

suno_router = Router()

PRICE_SUNO = 0


@suno_router.message(Command("suno"))
async def suno(message: Message, state: FSMContext):
    await state.clear()

    user_id = str(message.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    if user.current_model == Model.SUNO:
        reply_markup = await build_recommendations_keyboard(user.current_model, user_language_code, user.gender)
        await message.answer(
            text=get_localization(user_language_code).ALREADY_SWITCHED_TO_THIS_MODEL,
            reply_markup=reply_markup,
        )
    else:
        user.current_model = Model.SUNO
        await update_user(user_id, {
            "current_model": user.current_model,
        })

        reply_markup = await build_recommendations_keyboard(user.current_model, user_language_code, user.gender)
        await message.answer(
            text=get_localization(user_language_code).SWITCHED_TO_SUNO,
            reply_markup=reply_markup,
            message_effect_id="5104841245755180586",
        )

    await handle_suno(message.bot, str(message.chat.id), state, user_id)


async def handle_suno(bot: Bot, chat_id: str, state: FSMContext, user_id: str):
    user_language_code = await get_user_language(str(user_id), state.storage)

    reply_markup = build_suno_keyboard(user_language_code)
    await bot.send_message(
        chat_id=chat_id,
        text=get_localization(user_language_code).SUNO_INFO,
        reply_markup=reply_markup,
    )


@suno_router.callback_query(lambda c: c.data.startswith('suno:'))
async def handle_suno_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)
    user_language_code = await get_user_language(user_id, state.storage)

    mode = callback_query.data.split(':')[1]

    if mode == SunoMode.SIMPLE:
        reply_markup = build_suno_simple_mode_keyboard(user_language_code)
        await callback_query.message.edit_text(
            text=get_localization(user_language_code).SUNO_SIMPLE_MODE_PROMPT,
            reply_markup=reply_markup,
        )

        await state.set_state(Suno.waiting_for_prompt)
    elif mode == SunoMode.CUSTOM:
        reply_markup = build_suno_custom_mode_lyrics_keyboard(user_language_code)
        await callback_query.message.edit_text(
            text=get_localization(user_language_code).SUNO_CUSTOM_MODE_LYRICS,
            reply_markup=reply_markup,
        )

        await state.set_state(Suno.waiting_for_lyrics)

    await state.update_data(suno_mode=mode)


@suno_router.callback_query(lambda c: c.data.startswith('suno_simple_mode:'))
async def handle_suno_simple_mode_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)
    user_language_code = await get_user_language(user_id, state.storage)

    action = callback_query.data.split(':')[1]

    if action == 'back':
        reply_markup = build_suno_keyboard(user_language_code)
        await callback_query.message.edit_text(
            text=get_localization(user_language_code).SUNO_INFO,
            reply_markup=reply_markup,
        )

        await state.clear()


@suno_router.message(Suno.waiting_for_prompt, ~F.text.startswith('/'))
async def suno_prompt_sent(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    user = await get_user(str(user_id))
    user_language_code = await get_user_language(str(user_id), state.storage)

    prompt = message.text
    if prompt is None:
        await message.reply(
            text=get_localization(user_language_code).SUNO_VALUE_ERROR,
        )
        return

    processing_message = await message.reply(
        text=get_localization(user_language_code).processing_request_music()
    )

    async with ChatActionSender.upload_voice(bot=message.bot, chat_id=message.chat.id):
        quota = user.monthly_limits[Quota.SUNO] + user.additional_usage_quota[Quota.SUNO]
        if quota < 2:
            reply_markup = build_cancel_keyboard(user_language_code)
            await message.answer(
                text=get_localization(user_language_code).REACHED_USAGE_LIMIT,
                reply_markup=reply_markup,
            )
        else:
            user_not_finished_requests = await get_started_requests_by_user_id_and_model(user.id, Model.SUNO)

            if len(user_not_finished_requests):
                await message.reply(
                    text=get_localization(user_language_code).ALREADY_MAKE_REQUEST,
                )
                await processing_message.delete()
                return

            request = await write_request(
                user_id=user.id,
                message_id=processing_message.message_id,
                model=Model.SUNO,
                requested=2,
                details={
                    "mode": SunoMode.SIMPLE,
                    "prompt": prompt,
                    "is_suggestion": False,
                },
            )

            try:
                results = await generate_song(user.settings[Model.SUNO][UserSettings.VERSION], prompt)
                tasks = []
                for (i, result) in enumerate(results):
                    if result is not None:
                        tasks.append(
                            write_generation(
                                id=result,
                                request_id=request.id,
                                model=Model.SUNO,
                                has_error=result is None,
                                details={
                                    "mode": SunoMode.SIMPLE,
                                    "prompt": prompt,
                                    "is_suggestion": False,
                                }
                            )
                        )

                        asyncio.create_task(
                            check_song(
                                bot=message.bot,
                                storage=state.storage,
                                song_id=result,
                            )
                        )

                await asyncio.gather(*tasks)
            except Exception as e:
                if "Too Many Requests" in str(e):
                    await message.answer(
                        text=get_localization(user_language_code).SERVER_OVERLOADED_ERROR,
                    )
                elif "Bad Request" in str(e):
                    await message.answer(
                        text=get_localization(user_language_code).SUNO_TOO_MANY_WORDS,
                    )

                    await handle_suno(message.bot, str(message.chat.id), state, user_id)
                else:
                    reply_markup = build_error_keyboard(user_language_code)
                    await message.answer(
                        text=get_localization(user_language_code).ERROR,
                        reply_markup=reply_markup,
                        parse_mode=None,
                    )

                    await send_message_to_admins(
                        bot=message.bot,
                        message=f"#error\n\nALARM! Ошибка у пользователя при запросе в Suno: {user.id}\nИнформация:\n{e}",
                        parse_mode=None,
                    )

                request.status = RequestStatus.FINISHED
                await update_request(request.id, {
                    "status": request.status
                })

                generations = await get_generations_by_request_id(request.id)
                for generation in generations:
                    generation.status = GenerationStatus.FINISHED,
                    generation.has_error = True
                    await update_generation(
                        generation.id,
                        {
                            "status": generation.status,
                            "has_error": generation.has_error,
                        },
                    )

                await processing_message.delete()


@suno_router.callback_query(lambda c: c.data.startswith('suno_custom_mode_lyrics:'))
async def handle_suno_custom_mode_lyrics_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)
    user_language_code = await get_user_language(user_id, state.storage)

    action = callback_query.data.split(':')[1]

    if action == 'skip':
        reply_markup = build_suno_custom_mode_genres_keyboard(user_language_code)
        await callback_query.message.edit_text(
            text=get_localization(user_language_code).SUNO_CUSTOM_MODE_GENRES,
            reply_markup=reply_markup,
        )

        await state.update_data(suno_lyrics="")
        await state.set_state(Suno.waiting_for_genres)
    elif action == 'back':
        reply_markup = build_suno_keyboard(user_language_code)
        await callback_query.message.edit_text(
            text=get_localization(user_language_code).SUNO_INFO,
            reply_markup=reply_markup,
        )

        await state.clear()


@suno_router.message(Suno.waiting_for_lyrics, ~F.text.startswith('/'))
async def suno_lyrics_sent(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    user_language_code = await get_user_language(str(user_id), state.storage)

    lyrics = message.text
    if lyrics is None:
        await message.reply(
            text=get_localization(user_language_code).SUNO_VALUE_ERROR,
        )
        return

    reply_markup = build_suno_custom_mode_genres_keyboard(user_language_code)
    await message.reply(
        text=get_localization(user_language_code).SUNO_CUSTOM_MODE_GENRES,
        reply_markup=reply_markup,
    )

    await state.update_data(suno_lyrics=lyrics)
    await state.set_state(Suno.waiting_for_genres)


@suno_router.callback_query(lambda c: c.data.startswith('suno_custom_mode_genres:'))
async def handle_suno_custom_mode_genres_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)
    user_language_code = await get_user_language(user_id, state.storage)

    action = callback_query.data.split(':')[1]

    if action == 'start_again':
        reply_markup = build_suno_keyboard(user_language_code)
        await callback_query.message.edit_text(
            text=get_localization(user_language_code).SUNO_INFO,
            reply_markup=reply_markup,
        )

        await state.clear()


@suno_router.message(Suno.waiting_for_genres, ~F.text.startswith('/'))
async def suno_genres_sent(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    user = await get_user(str(user_id))
    user_data = await state.get_data()
    user_language_code = await get_user_language(str(user_id), state.storage)

    lyrics = user_data.get('suno_lyrics', '')
    genres = message.text
    if genres is None:
        await message.reply(
            text=get_localization(user_language_code).SUNO_VALUE_ERROR,
        )
        return

    processing_message = await message.reply(
        text=get_localization(user_language_code).processing_request_music()
    )

    async with ChatActionSender.upload_voice(bot=message.bot, chat_id=message.chat.id):
        quota = user.monthly_limits[Quota.SUNO] + user.additional_usage_quota[Quota.SUNO]

        if quota < 2:
            reply_markup = build_cancel_keyboard(user_language_code)
            await message.answer(
                text=get_localization(user_language_code).REACHED_USAGE_LIMIT,
                reply_markup=reply_markup,
            )
        else:
            user_not_finished_requests = await get_started_requests_by_user_id_and_model(user.id, Model.SUNO)

            if len(user_not_finished_requests):
                await message.reply(
                    text=get_localization(user_language_code).ALREADY_MAKE_REQUEST,
                )
                await processing_message.delete()
                return

            try:
                if user_language_code != 'en':
                    genres = await translate_text(genres, user_language_code, 'en')

                request = await write_request(
                    user_id=user.id,
                    message_id=processing_message.message_id,
                    model=Model.SUNO,
                    requested=2,
                    details={
                        "mode": SunoMode.CUSTOM,
                        "lyrics": lyrics,
                        "genres": genres,
                        "is_suggestion": False,
                    },
                )

                results = await generate_song(
                    user.settings[Model.SUNO][UserSettings.VERSION],
                    lyrics,
                    False,
                    True,
                    genres,
                )
                tasks = []
                for (i, result) in enumerate(results):
                    if result is not None:
                        tasks.append(
                            write_generation(
                                id=result,
                                request_id=request.id,
                                model=Model.SUNO,
                                has_error=result is None,
                                details={
                                    "mode": SunoMode.CUSTOM,
                                    "lyrics": lyrics,
                                    "genres": genres,
                                    "is_suggestion": False,
                                }
                            )
                        )

                        asyncio.create_task(
                            check_song(
                                bot=message.bot,
                                storage=state.storage,
                                song_id=result,
                            )
                        )

                await asyncio.gather(*tasks)
            except Exception as e:
                if "Too Many Requests" in str(e):
                    await message.answer(
                        text=get_localization(user_language_code).SERVER_OVERLOADED_ERROR,
                    )
                elif "Bad Request" in str(e):
                    await message.answer(
                        text=get_localization(user_language_code).SUNO_TOO_MANY_WORDS,
                    )

                    await handle_suno(message.bot, str(message.chat.id), state, user_id)
                else:
                    reply_markup = build_error_keyboard(user_language_code)
                    await message.answer(
                        text=get_localization(user_language_code).ERROR,
                        reply_markup=reply_markup,
                        parse_mode=None,
                    )

                    await send_message_to_admins(
                        bot=message.bot,
                        message=f"#error\n\nALARM! Ошибка у пользователя при запросе в Suno: {user.id}\nИнформация:\n{e}",
                        parse_mode=None,
                    )

                request.status = RequestStatus.FINISHED
                await update_request(request.id, {
                    "status": request.status
                })

                generations = await get_generations_by_request_id(request.id)
                for generation in generations:
                    generation.status = GenerationStatus.FINISHED
                    generation.has_error = True
                    await update_generation(
                        generation.id,
                        {
                            "status": generation.status,
                            "has_error": generation.has_error,
                        },
                    )

                await processing_message.delete()


async def handle_suno_example(user: User, prompt: str, message: Message, state: FSMContext):
    if (
        user.subscription_type == SubscriptionType.FREE and
        user.monthly_limits[Quota.MUSIC_GEN] == 30
    ):
        request = await write_request(
            user_id=user.id,
            message_id=message.message_id,
            model=Model.SUNO,
            requested=2,
            details={
                "mode": SunoMode.SIMPLE,
                "prompt": prompt,
                "is_suggestion": True,
            },
        )

        try:
            results = await generate_song(SunoVersion.V3_5, prompt)
            tasks = []
            for (i, result) in enumerate(results):
                if result is not None:
                    tasks.append(
                        write_generation(
                            id=result,
                            request_id=request.id,
                            model=Model.SUNO,
                            has_error=result is None,
                            details={
                                "mode": SunoMode.SIMPLE,
                                "prompt": prompt,
                                "is_suggestion": True,
                            }
                        )
                    )

                    asyncio.create_task(
                        check_song(
                            bot=message.bot,
                            storage=state.storage,
                            song_id=result,
                        )
                    )

            await asyncio.gather(*tasks)
        except Exception as e:
            await send_message_to_admins(
                bot=message.bot,
                message=f"#error\n\nALARM! Ошибка у пользователя при попытке отправить пример Suno в запросе MusicGen: {user.id}\nИнформация:\n{e}",
                parse_mode=None,
            )

            request.status = RequestStatus.FINISHED
            await update_request(request.id, {
                "status": request.status
            })

            generations = await get_generations_by_request_id(request.id)
            for generation in generations:
                generation.status = GenerationStatus.FINISHED
                generation.has_error = True
                await update_generation(
                    generation.id,
                    {
                        "status": generation.status,
                        "has_error": generation.has_error,
                    },
                )
