from aiogram.fsm.state import StatesGroup, State


class Ban(StatesGroup):
    waiting_for_user_id = State()
