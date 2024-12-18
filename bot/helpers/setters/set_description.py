from aiogram import Bot

from bot.locales.types import LanguageCode


async def set_description(bot: Bot):
    await bot.set_my_short_description(
        short_description="""
🤖 Access to AI: ChatGPT | Claude | Gemini | DALL•E | Midjourney | Stable Diffusion | Suno | Runway
🛟 @roman_danilov
""",
    )
    await bot.set_my_short_description(
        short_description="""
🤖 Доступ к ИИ: ChatGPT | Claude | Gemini | DALL•E | Midjourney | Stable Diffusion | Suno | Runway
🛟 @roman_danilov
""",
        language_code=LanguageCode.RU,
    )

    await bot.set_my_description(
        description="""
Access to AI:

━ 🔤 Text
    ┣ ✉️ ChatGPT 4.0 Omni Mini
    ┣ 💥 ChatGPT 4.0 Omni
    ┣ 🧩 ChatGPT o1-mini
    ┣ 🧪 ChatGPT o1
    ┣ 📜 Claude 3.5 Haiku
    ┣ 💫 Claude 3.5 Sonnet
    ┣ 🚀 Claude 3.0 Opus
    ┣ 🏎 Gemini 1.5 Flash
    ┣ 💼 Gemini 1.5 Pro
    ┣ 🛡️ Gemini 1.0 Ultra
    ┗ 👀️ Eightify

━ 🖼 Image
    ┣ 👨‍🎨 DALL•E
    ┣ 🎨 Midjourney
    ┣ 🎆 Stable Diffusion
    ┣ 🫐 Flux Pro
    ┣ 😜 FaceSwap
    ┗ 🪄 Photoshop AI

━ 🎵 Music
    ┣ 🎺 MusicGen
    ┗ 🎸 Suno

━ 📹 Video
    ┗ 🎥 Runway
""",
    )
    await bot.set_my_description(
        description="""
Доступ к ИИ:

━ 🔤 Текстовые
    ┣ ✉️ ChatGPT 4.0 Omni Mini
    ┣ 💥 ChatGPT 4.0 Omni
    ┣ 🧩 ChatGPT o1-mini
    ┣ 🧪 ChatGPT o1
    ┣ 📜 Claude 3.5 Haiku
    ┣ 💫 Claude 3.5 Sonnet
    ┣ 🚀 Claude 3.0 Opus
    ┣ 🏎 Gemini 1.5 Flash
    ┣ 💼 Gemini 1.5 Pro
    ┣ 🛡️ Gemini 1.0 Ultra
    ┗ 👀️ Eightify

━ 🖼 Графические
    ┣ 👨‍🎨 DALL•E
    ┣ 🎨 Midjourney
    ┣ 🎆 Stable Diffusion
    ┣ 🫐 Flux Pro
    ┣ 😜 FaceSwap
    ┗ 🪄 Photoshop AI

━ 🎵 Музыкальные
    ┣ 🎺 MusicGen
    ┗ 🎸 Suno

━ 📹 Видео
    ┗ 🎥 Runway
""",
        language_code=LanguageCode.RU,
    )
