import logging

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import BotCommand, BotCommandScopeChat

from bot.config import config

commands_en = [
    BotCommand(
        command="start",
        description="👋 About this bot",
    ),
    BotCommand(
        command="help",
        description="🛟 Detailed information about commands",
    ),
    BotCommand(
        command="mode",
        description="🤖 Choose AI model",
    ),
    BotCommand(
        command="buy",
        description="💎 Buy a subscription or individual packages",
    ),
    BotCommand(
        command="profile",
        description="👤 Profile",
    ),
    BotCommand(
        command="settings",
        description="🔧 Customize AI model for yourself",
    ),
    BotCommand(
        command="language",
        description="🌍 Change language",
    ),
    BotCommand(
        command="info",
        description="ℹ️ Get info about AI models",
    ),
    BotCommand(
        command="chatgpt",
        description="🧠 Switch to ChatGPT model",
    ),
    BotCommand(
        command="claude",
        description="💥 Switch to Claude model",
    ),
    BotCommand(
        command="dalle",
        description="🖼️ Switch to DALL-E model",
    ),
    BotCommand(
        command="midjourney",
        description="🎨 Switch to Midjourney model",
    ),
    BotCommand(
        command="face_swap",
        description="📷️ Switch to FaceSwap model",
    ),
    BotCommand(
        command="music_gen",
        description="🎵 Switch to MusicGen model",
    ),
    BotCommand(
        command="suno",
        description="🎸 Switch to Suno model",
    ),
    BotCommand(
        command="bonus",
        description="🎁 Bonus balance",
    ),
    BotCommand(
        command="promo_code",
        description="🔑 Type promo code to get magic",
    ),
    BotCommand(
        command="feedback",
        description="📡 Give a feedback",
    ),
    BotCommand(
        command="terms",
        description="📄 Terms of Service",
    ),
]

commands_ru = [
    BotCommand(
        command="start",
        description="👋 Что умеет этот бот",
    ),
    BotCommand(
        command="help",
        description="🛟 Детальная информация про команды",
    ),
    BotCommand(
        command="mode",
        description="🤖 Выбрать модель ИИ",
    ),
    BotCommand(
        command="buy",
        description="💎 Приобрести подписку или индивидуальные пакеты",
    ),
    BotCommand(
        command="profile",
        description="👤 Профиль",
    ),
    BotCommand(
        command="settings",
        description="🔧 Настроить модель ИИ под себя",
    ),
    BotCommand(
        command="language",
        description="🌍 Изменить язык",
    ),
    BotCommand(
        command="info",
        description="ℹ️ Получить информацию про модели ИИ",
    ),
    BotCommand(
        command="chatgpt",
        description="🧠 Переключиться на ChatGPT модель",
    ),
    BotCommand(
        command="claude",
        description="💥 Переключиться на Claude модель",
    ),
    BotCommand(
        command="dalle",
        description="🖼️ Перключиться на DALL-E модель",
    ),
    BotCommand(
        command="midjourney",
        description="🎨 Перключиться на Midjourney модель",
    ),
    BotCommand(
        command="face_swap",
        description="📷️ Переключиться на FaceSwap модель",
    ),
    BotCommand(
        command="music_gen",
        description="🎵 Переключиться на MusicGen модель",
    ),
    BotCommand(
        command="suno",
        description="🎸 Переключиться на Suno модель",
    ),
    BotCommand(
        command="bonus",
        description="🎁 Бонусный баланс",
    ),
    BotCommand(
        command="promo_code",
        description="🔑 Написать промокод для получения магии",
    ),
    BotCommand(
        command="feedback",
        description="📡 Оставить обратную связь",
    ),
    BotCommand(
        command="terms",
        description="📄 Пользовательское соглашение",
    ),
]

commands_admin = commands_ru + [
    BotCommand(command="admin", description="👨‍💻 Админка"),
]


async def set_commands(bot: Bot):
    await bot.set_my_commands(commands=commands_en)
    await bot.set_my_commands(commands=commands_ru, language_code='ru')

    for chat_id in list(set(id for ids in [config.ADMIN_IDS, config.DEVELOPER_IDS] for id in ids)):
        try:
            await bot.set_my_commands(commands=commands_admin, scope=BotCommandScopeChat(chat_id=chat_id))
        except TelegramBadRequest as error:
            logging.error(error)


async def set_commands_for_user(bot: Bot, chat_id: str, language='en'):
    if language == 'ru':
        await bot.set_my_commands(commands=commands_ru, scope=BotCommandScopeChat(chat_id=chat_id))
    else:
        await bot.set_my_commands(commands=commands_en, scope=BotCommandScopeChat(chat_id=chat_id))
