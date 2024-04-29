from typing import List

from aiogram import Router, F

from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from bot.handlers.common.photo_handler import handle_photo, handle_album
from bot.middlewares.AlbumMiddleware import AlbumMiddleware

document_router = Router()
document_router.message.middleware(AlbumMiddleware())


@document_router.message(F.document)
async def handle_document(message: Message, state: FSMContext, album: List[Message]):
    if len(album):
        await handle_album(message, state, album)
    elif message.document.mime_type.startswith('image') and message.document.thumbnail:
        photo_file = await message.bot.get_file(message.document.file_id)
        await handle_photo(message, state, photo_file)
