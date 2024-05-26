from aiogram import Bot


async def set_description(bot: Bot):
    await bot.set_my_short_description(
        short_description="""
🤖 Access to AI models: ChatGPT, Claude, DALL•E, Midjourney, FaceSwap, MusicGen, Suno
🛟 Support: @roman_danilov
""",
    )
    await bot.set_my_short_description(
        short_description="""
🤖 Доступ к ИИ моделям: ChatGPT, Claude, DALL•E, Midjourney, FaceSwap, MusicGen, Suno
🛟 Поддержка: @roman_danilov
""",
        language_code='ru',
    )

    await bot.set_my_description(
        description="""
Access to neural networks and AI:
✉️ ChatGPT-3.5 Turbo
🧠 ChatGPT-4.0 Turbo
💥 ChatGPT-4.0 Omni
💫 Claude 3 Sonnet
🚀 Claude 3 Opus
🖼 DALL•E
🎨 Midjourney
😜 FaceSwap
🎵 MusicGen
🎸 Suno

Created by Stanford students 🏫
""",
    )
    await bot.set_my_description(
        description="""
Доступ к нейронным сетям и ИИ:
✉️ ChatGPT-3.5 Turbo
🧠 ChatGPT-4.0 Turbo
💥 ChatGPT-4.0 Omni
💫 Claude 3 Sonnet
🚀 Claude 3 Opus
🖼 DALL•E
🎨 Midjourney
😜 FaceSwap
🎵 MusicGen
🎸 Suno

Создан студентами Stanford 🏫
""",
        language_code='ru',
    )
