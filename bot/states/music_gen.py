from aiogram.fsm.state import StatesGroup, State


class MusicGen(StatesGroup):
    waiting_for_music_gen_duration = State()
