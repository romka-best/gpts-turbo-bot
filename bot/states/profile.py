from aiogram.fsm.state import StatesGroup, State


class Profile(StatesGroup):
    waiting_for_photo = State()
