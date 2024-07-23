import asyncio
import random
from typing import List

import aiohttp
from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    CallbackQuery,
    URLInputFile,
)
from aiogram.utils.chat_action import ChatActionSender

from bot.database.main import firebase
from bot.database.models.common import Quota, Model
from bot.database.models.generation import GenerationStatus
from bot.database.models.request import RequestStatus
from bot.database.models.user import UserGender, User
from bot.database.operations.face_swap_package.writers import write_used_face_swap_package
from bot.database.operations.generation.getters import get_generations_by_request_id
from bot.database.operations.generation.updaters import update_generation
from bot.database.operations.generation.writers import write_generation
from bot.database.operations.request.getters import get_started_requests_by_user_id_and_model
from bot.database.operations.request.updaters import update_request
from bot.database.operations.request.writers import write_request
from bot.database.operations.user.getters import get_user
from bot.database.operations.user.updaters import update_user
from bot.helpers.senders.send_message_to_admins import send_message_to_admins
from bot.integrations.replicateAI import create_face_swap_images
from bot.keyboards.ai.face_swap import (
    build_face_swap_choose_keyboard,
    build_face_swap_package_keyboard,
)
from bot.keyboards.common.common import build_cancel_keyboard, build_recommendations_keyboard, build_error_keyboard
from bot.keyboards.common.profile import build_profile_gender_keyboard
from bot.locales.main import get_localization, get_user_language
from bot.states.profile import Profile
from bot.states.gfpgan import GFPGAN


gfpgan_router = Router()

PRICE_GFPGAN = 0.0014


@gfpgan_router.message(Command("gfpgan"))
async def gfpgan(message: Message, state: FSMContext):
    await state.clear()

    user_id = str(message.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    if user.current_model == Model.GFPGAN:
        await message.answer(
            text=get_localization(user_language_code).ALREADY_SWITCHED_TO_THIS_MODEL,
        )
        await message.answer(
            text=get_localization(user_language_code).GFPGAN_START,
        )
    else:
        user.current_model = Model.GFPGAN
        await update_user(user_id, {
            "current_model": user.current_model,
        })

        await message.answer(
            text=get_localization(user_language_code).SWITCHED_TO_GFPGAN,
            message_effect_id="5104841245755180586",
        )
