from aiogram.fsm.state import StatesGroup, State


class Bonus(StatesGroup):
    waiting_for_package_quantity = State()
