from aiogram import Bot


async def set_description(bot: Bot):
    await bot.set_my_short_description(
        short_description="""
🤖 Access to AI: ChatGPT | Claude | Gemini | DALL•E | Midjourney | Stable Diffusion | Suno
🛟 Support: @roman_danilov
""",
    )
    await bot.set_my_short_description(
        short_description="""
🤖 Доступ к ИИ: ChatGPT | Claude | Gemini | DALL•E | Midjourney | Stable Diffusion | Suno
🛟 Поддержка: @roman_danilov
""",
        language_code='ru',
    )

    await bot.set_my_description(
        description="""
Access to AI:

━ 🔤 Text Models:
    ┣ ✉️ ChatGPT 4.0 Omni Mini
    ┣ 💥 ChatGPT 4.0 Omni
    ┣ 🧩 ChatGPT o1-mini
    ┣ 🧪 ChatGPT o1-preview
    ┣ 📜 Claude 3.0 Haiku
    ┣ 💫 Claude 3.5 Sonnet
    ┣ 🚀 Claude 3.0 Opus
    ┣ 🏎 Gemini 1.5 Flash
    ┣ 💼 Gemini 1.5 Pro
    ┗ 🛡️ Gemini 1.0 Ultra

━ 🖼 Image Models
    ┣ 👨‍🎨 DALL•E 3
    ┣ 🎨 Midjourney 6.1
    ┣ 🎆 Stable Diffusion 3.0
    ┣ 🫐 Flux 1.1 Pro
    ┣ 😜 FaceSwap
    ┗ 🪄 Photoshop AI

━ 🎵 Music Models
    ┣ 🎺 MusicGen
    ┗ 🎸 Suno 3.5
""",
    )
    await bot.set_my_description(
        description="""
Доступ к нейронным сетям:

━ 🔤 Текстовые
    ┣ ✉️ ChatGPT 4.0 Omni Mini
    ┣ 💥 ChatGPT 4.0 Omni
    ┣ 🧩 ChatGPT o1-mini
    ┣ 🧪 ChatGPT o1-preview
    ┣ 📜 Claude 3.0 Haiku
    ┣ 💫 Claude 3.5 Sonnet
    ┣ 🚀 Claude 3.0 Opus
    ┣ 🏎 Gemini 1.5 Flash
    ┣ 💼 Gemini 1.5 Pro
    ┗ 🛡️ Gemini 1.0 Ultra

━ 🖼 Графические
    ┣ 👨‍🎨 DALL•E 3
    ┣ 🎨 Midjourney 6.1
    ┣ 🎆 Stable Diffusion 3.0
    ┣ 🫐 Flux 1.1 Pro
    ┣ 😜 FaceSwap
    ┗ 🪄 Photoshop AI

━ 🎵 Музыкальные
    ┣ 🎺 MusicGen
    ┗ 🎸 Suno 3.5
""",
        language_code='ru',
    )
