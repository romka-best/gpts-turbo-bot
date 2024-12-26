from aiogram.fsm.state import StatesGroup, State


class Blast(StatesGroup):
    waiting_for_blast_letter = State()
