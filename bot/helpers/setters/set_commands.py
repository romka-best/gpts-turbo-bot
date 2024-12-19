import logging

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import BotCommand, BotCommandScopeChat

from bot.config import config
from bot.locales.types import LanguageCode

commands_en = [
    BotCommand(
        command='start',
        description='👋 About this bot',
    ),
    BotCommand(
        command='model',
        description='🤖 Select AI model',
    ),
    BotCommand(
        command='profile',
        description='👤 Profile',
    ),
    BotCommand(
        command='buy',
        description='💎 Buy a subscription or packages',
    ),
    BotCommand(
        command='text',
        description='🔤 Generate Text with: ChatGPT, Claude, Gemini',
    ),
    BotCommand(
        command='summary',
        description='📝 Generate Summary in: YouTube',
    ),
    BotCommand(
        command='image',
        description='🖼 Generate Images with: DALL-E, Midjourney, Stable Diffusion, Flux, FaceSwap, Photoshop AI',
    ),
    BotCommand(
        command='music',
        description='🎵 Generate Music with: MusicGen, Suno',
    ),
    BotCommand(
        command='video',
        description='📹 Generate Videos with: Runway',
    ),
    BotCommand(
        command='info',
        description='ℹ️ Info about AI models',
    ),
    BotCommand(
        command='catalog',
        description='📂 Catalog with prompts and digital employees',
    ),
    BotCommand(
        command='settings',
        description='🔧 Customize AI model for yourself',
    ),
    BotCommand(
        command='language',
        description='🌍 Select language',
    ),
    BotCommand(
        command='bonus',
        description='🎁 Bonus balance',
    ),
    BotCommand(
        command='help',
        description='🛟 Detailed information about commands',
    ),
]

commands_ru = [
    BotCommand(
        command='start',
        description='👋 Что умеет этот бот',
    ),
    BotCommand(
        command='model',
        description='🤖 Выбрать AI модель',
    ),
    BotCommand(
        command='profile',
        description='👤 Профиль',
    ),
    BotCommand(
        command='buy',
        description='💎 Приобрести подписку или пакеты',
    ),
    BotCommand(
        command='text',
        description='🔤 Генерация текста с: ChatGPT, Claude, Gemini',
    ),
    BotCommand(
        command='summary',
        description='📝 Генерация резюме в: YouTube',
    ),
    BotCommand(
        command='image',
        description='🖼 Генерация изображений с: DALL-E, Midjourney, Stable Diffusion, Flux, FaceSwap, Photoshop AI',
    ),
    BotCommand(
        command='music',
        description='🎵 Генерация музыки с: MusicGen, Suno',
    ),
    BotCommand(
        command='video',
        description='📹 Генерация видео с: Runway',
    ),
    BotCommand(
        command='info',
        description='ℹ️ Информация про модели ИИ',
    ),
    BotCommand(
        command='catalog',
        description='📂 Каталог с промптами и цифровыми сотрудниками',
    ),
    BotCommand(
        command='settings',
        description='🔧 Настроить модель под себя',
    ),
    BotCommand(
        command='language',
        description='🌍 Поменять язык',
    ),
    BotCommand(
        command='bonus',
        description='🎁 Бонусный баланс',
    ),
    BotCommand(
        command='help',
        description='🛟 Детальная информация про команды',
    ),
]

commands_admin = commands_ru + [
    BotCommand(command='admin', description='👨‍💻 Админка'),
]


async def set_commands(bot: Bot):
    await bot.set_my_commands(commands=commands_en)
    await bot.set_my_commands(commands=commands_ru, language_code=LanguageCode.RU)

    for chat_id in config.ADMIN_IDS:
        try:
            await bot.set_my_commands(commands=commands_admin, scope=BotCommandScopeChat(chat_id=chat_id))
        except TelegramBadRequest as error:
            if error.message.startswith('Bad Request: chat not found'):
                logging.warning(f'{error.message}: {chat_id}')
            else:
                raise error


async def set_commands_for_user(bot: Bot, chat_id: str, language=LanguageCode):
    try:
        if language == LanguageCode.RU:
            await bot.set_my_commands(commands=commands_ru, scope=BotCommandScopeChat(chat_id=chat_id))
        else:
            await bot.set_my_commands(commands=commands_en, scope=BotCommandScopeChat(chat_id=chat_id))
    except TelegramBadRequest as error:
        if error.message.startswith('Bad Request: chat not found'):
            logging.warning(f'{error.message}: {chat_id}')
        else:
            raise error
