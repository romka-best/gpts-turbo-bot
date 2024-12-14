from aiogram.fsm.state import StatesGroup, State


class Eightify(StatesGroup):
    waiting_for_link = State()
