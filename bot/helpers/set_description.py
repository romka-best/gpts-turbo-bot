from aiogram import Bot


async def set_description(bot: Bot):
    await bot.set_my_short_description(
        short_description="""
🤖 Access to neural networks and AI: ChatGPT-3.5 , ChatGPT-4.0, DALL•E 3, FaceSwap, MusicGen
🛟 Support: @roman_danilov
""",
    )
    await bot.set_my_short_description(
        short_description="""
🤖 Доступ к нейронным сетям и ИИ: ChatGPT-3.5 , ChatGPT-4.0, DALL•E 3, FaceSwap, MusicGen
🛟 Поддержка: @roman_danilov
""",
        language_code='ru',
    )

    await bot.set_my_description(
        description="""
Access to neural networks and AI:
✉️ ChatGPT-3.5
🧠 ChatGPT-4.0
🎨 DALL•E 3
😜 FaceSwap
🎵 MusicGen
""",
    )
    await bot.set_my_description(
        description="""
Доступ к нейронным сетям и ИИ:
✉️ ChatGPT-3.5
🧠 ChatGPT-4.0
🎨 DALL•E 3
😜 FaceSwap
🎵 MusicGen
""",
        language_code='ru',
    )
