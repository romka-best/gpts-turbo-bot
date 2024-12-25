from aiogram.fsm.state import StatesGroup, State


class Chats(StatesGroup):
    waiting_for_chat_name = State()
