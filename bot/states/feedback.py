from aiogram.fsm.state import StatesGroup, State


class Feedback(StatesGroup):
    waiting_for_feedback = State()
