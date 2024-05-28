from aiogram import Router
from aiogram.filters import Command, CommandStart, ChatMemberUpdatedFilter, KICKED, MEMBER
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ChatMemberUpdated

from bot.database.main import firebase
from bot.database.models.generation import Generation
from bot.database.operations.generation.updaters import update_generation
from bot.database.operations.user.getters import get_user, get_users_by_referral
from bot.database.operations.user.updaters import update_user
from bot.helpers.initialize_user_for_the_first_time import initialize_user_for_the_first_time
from bot.helpers.update_monthly_limits import update_user_monthly_limits
from bot.keyboards.common.common import build_recommendations_keyboard

from bot.locales.main import get_localization, get_user_language, set_user_language

common_router = Router()


@common_router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()

    user_id = str(message.from_user.id)
    user = await get_user(user_id)
    if not user:
        referred_by = None
        referred_by_user = None
        if len(message.text.split()) > 1:
            referred_by = message.text.split()[1]
            referred_by_user = await get_user(referred_by)
            referred_by_user_language_code = await get_user_language(referred_by, state.storage)

            if referred_by_user:
                referred_users = await get_users_by_referral(user_id)
                if len(referred_users) > 50:
                    text = get_localization(referred_by_user_language_code).REFERRAL_LIMIT_ERROR
                    await message.bot.send_message(
                        chat_id=referred_by_user.telegram_chat_id,
                        text=text,
                    )
                else:
                    added_to_balance = 25.00
                    referred_by_user.balance += added_to_balance
                    await update_user(referred_by_user.id, {
                        "balance": referred_by_user.balance,
                    })

                    text = get_localization(referred_by_user_language_code).REFERRAL_SUCCESS
                    await message.bot.send_message(
                        chat_id=referred_by_user.telegram_chat_id,
                        text=text,
                    )

        language_code = message.from_user.language_code
        await set_user_language(user_id, language_code, state.storage)

        chat_title = get_localization(language_code).DEFAULT_CHAT_TITLE
        transaction = firebase.db.transaction()
        await initialize_user_for_the_first_time(
            transaction,
            message.from_user,
            str(message.chat.id),
            chat_title,
            referred_by,
            bool(referred_by_user),
        )

        user = await get_user(str(message.from_user.id))
    elif user and user.is_blocked:
        user.is_blocked = False
        await update_user(user.id, {
            "is_blocked": user.is_blocked,
        })

        batch = firebase.db.batch()
        await update_user_monthly_limits(message.bot, user, batch)
        await batch.commit()

    user_language_code = await get_user_language(user_id, state.storage)

    greeting = get_localization(user_language_code).START
    reply_markup = await build_recommendations_keyboard(user.current_model, user_language_code, user.gender)
    await message.answer(
        text=greeting,
        reply_markup=reply_markup,
    )


@common_router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=KICKED)
)
async def user_blocked_bot(event: ChatMemberUpdated):
    await update_user(str(event.from_user.id), {
        "is_blocked": True,
    })


@common_router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=MEMBER)
)
async def user_unblocked_bot(event: ChatMemberUpdated):
    user = await get_user(str(event.from_user.id))
    user.is_blocked = False
    await update_user(user.id, {
        "is_blocked": user.is_blocked,
    })

    batch = firebase.db.batch()
    await update_user_monthly_limits(event.bot, user, batch)
    await batch.commit()


@common_router.message(Command("help"))
async def handle_help(message: Message, state: FSMContext):
    await state.clear()

    user_id = str(message.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    text = get_localization(user_language_code).COMMANDS
    reply_markup = await build_recommendations_keyboard(user.current_model, user_language_code, user.gender)
    await message.answer(
        text=text,
        reply_markup=reply_markup,
    )


@common_router.message(Command("terms"))
async def terms(message: Message, state: FSMContext):
    await state.clear()

    user_id = str(message.from_user.id)
    user_language_code = await get_user_language(user_id, state.storage)

    await message.answer(text=get_localization(user_language_code).TERMS_LINK)


@common_router.callback_query(lambda c: c.data.startswith('reaction:'))
async def reaction_selection(callback_query: CallbackQuery):
    await callback_query.answer()

    reaction, generation_id = callback_query.data.split(':')[1], callback_query.data.split(':')[2]
    await update_generation(generation_id, {
        "reaction": reaction,
    })

    if callback_query.message.caption:
        await callback_query.message.edit_reply_markup(
            reply_markup=None,
        )
    else:
        await callback_query.message.edit_caption(
            caption=Generation.get_reaction_emojis()[reaction],
            reply_markup=None,
        )


@common_router.callback_query(lambda c: c.data.endswith(':close'))
async def handle_close_selection(callback_query: CallbackQuery):
    await callback_query.answer()

    await callback_query.message.delete()


@common_router.callback_query(lambda c: c.data.endswith(':cancel'))
async def handle_cancel_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    await callback_query.message.delete()

    await state.clear()
