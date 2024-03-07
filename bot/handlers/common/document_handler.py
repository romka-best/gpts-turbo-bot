from aiogram import Router, F

from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from bot.handlers.common.photo_handler import handle_photo

document_router = Router()


@document_router.message(F.document)
async def handle_document(message: Message, state: FSMContext):
    if message.document.mime_type.startswith('image') and message.document.thumbnail:
        photo_file = await message.bot.get_file(message.document.file_id)
        await handle_photo(message, state, photo_file)
