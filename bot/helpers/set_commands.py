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
        description="💵 Buy a subscription or individual packages",
    ),
    BotCommand(
        command="profile",
        description="👤 Your profile",
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
        command="dalle3",
        description="🖼️ Switch to DALL-E 3 model",
    ),
    BotCommand(
        command="face_swap",
        description="📷️ Switch to Face Swap model",
    ),
    BotCommand(
        command="music_gen",
        description="🎵 Switch to MusicGen model",
    ),
    BotCommand(
        command="bonus",
        description="🎁 Invite friends to get bonus",
    ),
    BotCommand(
        command="promo_code",
        description="🔑 Type promo code to get magic",
    ),
    BotCommand(
        command="feedback",
        description="📡 Give a feedback",
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
        description="💵 Приобрести подписку или индивидуальные пакеты",
    ),
    BotCommand(
        command="profile",
        description="👤 Ваш профиль",
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
        description="🧠 Переключаться на ChatGPT модель",
    ),
    BotCommand(
        command="dalle3",
        description="🖼️ Перключиться на DALL-E 3 модель",
    ),
    BotCommand(
        command="face_swap",
        description="📷️ Переключиться на Face Swap модель",
    ),
    BotCommand(
        command="music_gen",
        description="🎵 Переключиться на MusicGen модель",
    ),
    BotCommand(
        command="bonus",
        description="🎁 Пригласить друзей и получить бонус",
    ),
    BotCommand(
        command="promo_code",
        description="🔑 Написать промокод для получения магии",
    ),
    BotCommand(
        command="feedback",
        description="📡 Оставить фидбек",
    ),
]

commands_admin = commands_ru + [
    BotCommand(command="create_promo_code", description="😇 Создать промокод"),
    BotCommand(command="manage_face_swap", description="📸 Управление контентом в Face Swap"),
    BotCommand(command="manage_catalog", description="🎩 Управление ролями в чатах"),
    BotCommand(command="statistics", description="📊 Просмотр статистики"),
    BotCommand(command="blast", description="📣 Сделать рассылку"),
]


async def set_commands(bot: Bot):
    await bot.set_my_commands(commands=commands_en)
    await bot.set_my_commands(commands=commands_ru, language_code='ru')

    for chat_id in config.ADMIN_CHAT_IDS:
        try:
            await bot.set_my_commands(commands=commands_admin, scope=BotCommandScopeChat(chat_id=chat_id))
        except TelegramBadRequest as error:
            logging.error(error)


async def set_commands_for_user(bot: Bot, chat_id: str, language='en'):
    if language == 'ru':
        await bot.set_my_commands(commands=commands_ru, scope=BotCommandScopeChat(chat_id=chat_id))
    else:
        await bot.set_my_commands(commands=commands_en, scope=BotCommandScopeChat(chat_id=chat_id))
