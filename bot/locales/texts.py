import random
from typing import Protocol, Dict, List

from bot.database.models.common import Currency, Model
from bot.database.models.feedback import FeedbackStatus
from bot.database.models.game import GameType
from bot.database.models.generation import GenerationReaction
from bot.database.models.package import PackageType
from bot.database.models.subscription import Subscription, SubscriptionType, SubscriptionStatus
from bot.database.models.transaction import ServiceType
from bot.database.models.user import UserGender
from bot.helpers.calculate_percentage_difference import calculate_percentage_difference


class Texts(Protocol):
    START: str
    START_QUICK_GUIDE: str
    START_ADDITIONAL_FEATURES: str
    QUICK_GUIDE: str
    ADDITIONAL_FEATURES: str

    COMMANDS: str
    INFO: str
    INFO_TEXT_MODELS: str
    INFO_IMAGE_MODELS: str
    INFO_MUSIC_MODELS: str
    INFO_VIDEO_MODELS: str
    INFO_CHATGPT: str
    INFO_CLAUDE: str
    INFO_GEMINI: str
    INFO_DALL_E: str
    INFO_MIDJOURNEY: str
    INFO_STABLE_DIFFUSION: str
    INFO_FLUX: str
    INFO_FACE_SWAP: str
    INFO_PHOTOSHOP_AI: str
    INFO_MUSIC_GEN: str
    INFO_SUNO: str

    ADMIN_INFO = "👨‍💻 Выберите действие, админ 👩‍💻"
    BAN_INFO = "Отправь мне id пользователя, которого вы хотите забанить/разбанить ⛔️"
    BAN_SUCCESS = "Вы успешно забанили пользователя 📛"
    UNBAN_SUCCESS = "Вы успешно разбанили пользователя 🔥"

    TEXT_MODELS: str
    IMAGE_MODELS: str
    MUSIC_MODELS: str
    VIDEO_MODELS: str

    # Feedback
    FEEDBACK: str
    FEEDBACK_SUCCESS: str
    FEEDBACK_ADMIN_APPROVE = "Одобрить ✅"
    FEEDBACK_ADMIN_DENY = "Отклонить ❌"
    FEEDBACK_APPROVED: str
    FEEDBACK_APPROVED_WITH_LIMIT_ERROR: str
    FEEDBACK_DENIED: str

    # Profile
    SHOW_QUOTA: str
    TELL_ME_YOUR_GENDER: str
    YOUR_GENDER: str
    UNSPECIFIED: str
    MALE: str
    FEMALE: str
    SEND_ME_YOUR_PICTURE: str
    UPLOAD_PHOTO: str
    UPLOADING_PHOTO: str
    NO_FACE_IN_PHOTO: str
    CHANGE_PHOTO: str
    CHANGE_PHOTO_SUCCESS: str
    CHOOSE_GENDER: str
    CHANGE_GENDER: str
    OPEN_SETTINGS: str
    OPEN_BONUS_INFO: str
    OPEN_BUY_SUBSCRIPTIONS_INFO: str
    OPEN_BUY_PACKAGES_INFO: str
    CANCEL_SUBSCRIPTION: str
    CANCEL_SUBSCRIPTION_CONFIRMATION: str
    CANCEL_SUBSCRIPTION_SUCCESS: str
    NO_ACTIVE_SUBSCRIPTION: str

    # Language
    LANGUAGE: str
    CHOOSE_LANGUAGE: str

    # Bonus
    BONUS_ACTIVATED_SUCCESSFUL: str
    BONUS_CHOOSE_PACKAGE: str
    INVITE_FRIEND: str
    LEAVE_FEEDBACK: str
    PLAY: str
    PLAY_GAME: str
    PLAY_GAME_CHOOSE: str
    PLAY_BOWLING_GAME: str
    PLAY_BOWLING_GAME_DESCRIPTION: str
    PLAY_SOCCER_GAME: str
    PLAY_SOCCER_GAME_DESCRIPTION: str
    PLAY_BASKETBALL_GAME: str
    PLAY_BASKETBALL_GAME_DESCRIPTION: str
    PLAY_DARTS_GAME: str
    PLAY_DARTS_GAME_DESCRIPTION: str
    PLAY_DICE_GAME: str
    PLAY_DICE_GAME_CHOOSE: str
    PLAY_DICE_GAME_CHOOSE_1 = "🎲 1️⃣"
    PLAY_DICE_GAME_CHOOSE_2 = "🎲 2️⃣"
    PLAY_DICE_GAME_CHOOSE_3 = "🎲 3️⃣"
    PLAY_DICE_GAME_CHOOSE_4 = "🎲 4️⃣"
    PLAY_DICE_GAME_CHOOSE_5 = "🎲 5️⃣"
    PLAY_DICE_GAME_CHOOSE_6 = "🎲 6️⃣"
    PLAY_CASINO_GAME: str
    PLAY_CASINO_GAME_DESCRIPTION: str
    PLAY_GAME_WON: str
    PLAY_GAME_LOST: str
    PLAY_GAME_REACHED_LIMIT: str
    CASH_OUT: str
    REFERRAL_SUCCESS: str
    REFERRAL_LIMIT_ERROR: str

    # Blast
    BLAST_CHOOSE_LANGUAGE = """
📣 <b>Пора делать рассылку!</b>

Выберите язык для рассылки или отправьте всем сразу:
"""
    BLAST_WRITE_IN_CHOSEN_LANGUAGE = """
✍️ <b>Пора создать ваше послание!</b> 🚀

Вы выбрали язык, теперь пришло время вложить душу в сообщение!

Напишите текст рассылки, который затронет сердца ваших пользователей, развеселит их или даже вдохновит на новые подвиги. Помните, каждое слово – это кисть, а ваш текст – полотно, на котором вы можете нарисовать что угодно. Вперёд, наполните этот мир красками вашего воображения! 🌈✨
"""
    BLAST_WRITE_IN_DEFAULT_LANGUAGE = """
🚀 <b>Время для масштабной рассылки!</b> 🌍

Вы выбрали "Для всех" и это означает, что ваше сообщение достигнет каждого моего уголка, независимо от языковых предпочтений пользователей. Напишите ваше сообщение на русском, и я автоматически переведу его для всех наших пользователей. Создайте сообщение, которое вдохновит, развлечет или проинформирует - ведь оно полетит к сердцам и умам людей по всему миру.

Помните, ваши слова могут изменить чей-то день к лучшему! 🌟
"""
    BLAST_SUCCESS = """
🎉 <b>Рассылка успешно отправлена!</b> 💌

Твоё сообщение уже в пути к пользователям, готово разбудить интерес и вызвать улыбки. Ты сделал настоящий шаг навстречу вовлечённости и общению. Поздравляем, админ-волшебник, твоё творение скоро оценят по достоинству! 🌟

Спасибо, что делаешь меня ярче и интереснее каждым своим действием! ✨
"""

    # Promo code
    PROMO_CODE_ACTIVATE: str
    PROMO_CODE_INFO: str
    PROMO_CODE_INFO_ADMIN = """
🔑 <b>Время создать магию с промокодами!</b> ✨

Выбери, для чего ты хочешь создать промокод:
🌠 <b>Подписка</b> - открой доступ к эксклюзивным функциям и контенту
🎨 <b>Пакет</b> - добавь специальные возможности для использования AI
🪙 <b>Скидка</b> - дай возможность приобрести генерации подешевле

Нажми на нужную кнопку и приступим к созданию! 🚀
"""
    PROMO_CODE_SUCCESS: str
    PROMO_CODE_SUCCESS_ADMIN = """
🌟 <b>Вау!</b>

Твой <b>промокод успешно создан</b> и готов к путешествию в карманы наших пользователей. 🚀
Этот маленький кодик обязательно принесёт радость кому-то там!

🎉 Поздравляю, ты настоящий волшебник промокодов!
"""
    PROMO_CODE_CHOOSE_SUBSCRIPTION_ADMIN = """
🌟 <b>Выбираем подписку для промокода!</b> 🎁

Выбери тип подписки, на который хочешь дать доступ:
- <b>MINI</b> 🍬
- <b>STANDARD</b> ⭐
- <b>VIP</b> 🔥
- <b>PREMIUM</b> 💎
- <b>UNLIMITED</b> 🚀

Выбери и нажми, чтобы создать волшебный ключ доступа! ✨
"""
    PROMO_CODE_CHOOSE_PACKAGE_ADMIN = """
🌟 <b>Выбираем пакет для промокода!</b> 🎁

Выбери для начала пакет 👇
"""
    PROMO_CODE_CHOOSE_DISCOUNT_ADMIN = """
🌟 <b>Выбираем скидку для промокода!</b> 🎁

Напиши мне скидку в диапазоне от 1% до 50%, которую ты хочешь дать пользователям 👇
"""
    PROMO_CODE_CHOOSE_NAME_ADMIN = """
🖋️ <b>Придумай название для промокода</b> ✨

Сейчас ты как настоящий волшебник, создающий заклинание! ✨🧙‍
Напиши уникальное и запоминающееся название для твоего промокода.

🔠 Используй буквы, цифры, но помни о волшебстве краткости. Не бойся экспериментировать и вдохновлять пользователей!
"""
    PROMO_CODE_CHOOSE_DATE = """
📅 <b>Время для волшебства!</b> 🪄

Введи дату, до которой этот промокод будет разносить счастье и удивление!
Помни, нужен формат ДД.ММ.ГГГГ, например, 25.12.2023 - идеально для Рождественского сюрприза! 🎄

Так что вперёд, выбирай дату, когда магия закончится 🌟
"""
    PROMO_CODE_NAME_EXISTS_ERROR = """
🚫 <b>Ой-ой, такой код уже существует!</b> 🤖

Как настоящий инноватор, ты создал код, который уже кто-то придумал! Нужно что-то ещё более уникальное. Попробуй снова, ведь в творчестве нет границ!

Покажи свою оригинальность и креативность. Уверен, на этот раз получится!
"""
    PROMO_CODE_DATE_VALUE_ERROR = """
🚫 <b>Упс!</b>

Кажется, дата заблудилась в календаре и не может найти свой формат 📅

Давай попробуем ещё раз, но на этот раз в формате ДД.ММ.ГГГГ, например, 25.12.2023. Точность — залог успеха!
"""
    PROMO_CODE_ALREADY_HAVE_SUBSCRIPTION: str
    PROMO_CODE_EXPIRED_ERROR: str
    PROMO_CODE_NOT_FOUND_ERROR: str
    PROMO_CODE_ALREADY_USED_ERROR: str

    # Statistics
    STATISTICS_INFO = """
📊 <b>Статистика на подходе!</b>

Пора погрузиться в мир цифр и графиков. Выбери период, и я покажу тебе, как наш бот покорял AI-вершины 🚀:
1️⃣ <b>Статистика за день</b> - Узнай, что происходило сегодня! Были ли рекорды?
2️⃣ <b>Статистика за неделю</b> - Недельная доза данных. Каковы были тренды?
3️⃣ <b>Статистика за месяц</b> - Месяц в цифрах. Сколько достижений мы накопили?
4️⃣ <b>Статистика за всё время</b> - Взгляд в прошлое. Откуда мы начали и куда пришли?
5️⃣ <b>Записать транзакцию</b> - Актуализируй наши данные, чтобы всё было по-честному!

Выбирай кнопку и вперёд, к знаниям! 🕵️‍♂️🔍
"""
    STATISTICS_WRITE_TRANSACTION = """
🧾 <b>Выбери тип транзакции!</b>

Хмм... Кажется, пришло время подвести финансовые итоги! 🕵️‍♂️💼 Теперь перед тобой стоит выбор:
- Нажми на кнопку "📈 Записать доход", если наши казны пополнились и мы богаче на пару золотых монет!
- Или выбери "📉 Записать расход", если пришлось раскошелиться на волшебные ингредиенты или что-то ещё нужное.

Жми на кнопку и вперёд, к финансовым приключениям! 💫🚀
"""
    STATISTICS_CHOOSE_SERVICE = """
🔍 <b>Выбери тип сервиса для транзакции!</b>

Оу, похоже, дело дошло до выбора типа сервиса! 🌟📚 Тут всё, как в магазине чудес

Выбирай, не стесняйся, и пусть финансовые записи будут точны, как у звёздного картографа! 🗺️✨
"""
    STATISTICS_CHOOSE_CURRENCY = """
💰 <b>Время выбирать валюту!</b>

Для полной картины нам нужно узнать валюту этих транзакций. Так что, в какой валюте мы купались, когда совершались эти сделки? Рубли, доллары, а может быть, золотые дублоны? 😄

Выбери кнопку с нужной валютой, чтобы мы занесли всё по книжке точно и без ошибок. Это важно, ведь даже пираты не шутили с учётом своих сокровищ! 💸🏴‍☠️
"""
    STATISTICS_SERVICE_QUANTITY = """
✍️ <b>Пора записывать количество транзакций!</b>

Напиши, пожалуйста, количество транзакций

🔢🚀 Помни, каждая транзакция - это шаг к нашему общему успеху. Не пропусти ни одной!
"""
    STATISTICS_SERVICE_AMOUNT = """
🤑 <b>Давай посчитаем копейки!</b>

Напиши мне, пожалуйста, стоимость транзакции. Но помни, каждая копейка (или цент) на счету! Пожалуйста, используй формат с десятичными дробями через точку. Например, 999.99

Вводи цифры аккуратно, как если бы ты считал золотые монеты на пиратском корабле. В конце концов, точность – вежливость королей... и бухгалтеров! 🏴‍☠️📖
"""
    STATISTICS_SERVICE_DATE = """
📅 <b>Остался последний штрих: Дата транзакции!</b>

Напиши дату, когда происходили эти транзакции. Формат? Просто и ясно: "ДД.ММ.ГГГГ". Например, "01.04.2024" или "25.12.2023". Эта дата - ключ к организации нашего временного сундука с сокровищами.

🕰️✨ Помни, точная дата - это не просто числа, это маркеры нашего пути. По ним мы будем планировать наше будущее!
"""
    STATISTICS_SERVICE_DATE_VALUE_ERROR = """
🤔 <b>Упс, кажется, дата решила пошалить!</b>

Ой-ой, кажется, мы немного запутались в календарных страницах! Введённая дата не соответствует формату "ДД.ММ.ГГГГ". Давай попробуем ещё раз, ведь даже временной машины у нас пока нет, чтобы исправить это в будущем.

🗓️✏️ Итак, давай снова: когда именно происходило это финансовое чудо?
"""
    STATISTICS_WRITE_TRANSACTION_SUCCESSFUL = """
🎉 <b>Транзакция успешно записана! Вот это да, мы в бизнесе!</b>

Ура-ура! Ваши финансовые манёвры были успешно занесены в наши цифровые хроники. Теперь эта транзакция блестит в нашей базе данных, словно звезда на небосклоне бухгалтерии!

📚💰 Благодарю вас за аккуратность и точность. Наши цифровые эльфы уже танцуют радость. Кажется, ваша финансовая мудрость достойна отдельной главы в книге экономических приключений!
"""

    # AI
    CHATGPT = "💭 ChatGPT"
    CHATGPT3_TURBO = "✉️ ChatGPT 3.5 Turbo"
    CHATGPT4_OMNI_MINI = "✉️ ChatGPT 4.0 Omni Mini"
    CHATGPT4_TURBO = "🧠 ChatGPT 4.0 Turbo"
    CHATGPT4_OMNI = "💥 ChatGPT 4.0 Omni"
    CHAT_GPT_O_1_MINI = "🧩 ChatGPT o1-mini"
    CHAT_GPT_O_1_PREVIEW = "🧪 ChatGPT o1-preview"
    CLAUDE = "📄 Claude"
    CLAUDE_3_HAIKU = "📜 Claude 3.0 Haiku"
    CLAUDE_3_SONNET = "💫 Claude 3.5 Sonnet"
    CLAUDE_3_OPUS = "🚀 Claude 3.0 Opus"
    GEMINI = "✨ Gemini"
    GEMINI_1_FLASH = "🏎 Gemini 1.5 Flash"
    GEMINI_1_PRO = "💼 Gemini 1.5 Pro"
    GEMINI_1_ULTRA = "🛡️ Gemini 1.0 Ultra"
    DALL_E = "👨‍🎨 DALL-E"
    MIDJOURNEY = "🎨 Midjourney"
    STABLE_DIFFUSION = "🎆 Stable Diffusion"
    FLUX = "🫐 Flux"
    PHOTOSHOP_AI = "🪄 Photoshop AI"
    FACE_SWAP = "📷️ FaceSwap"
    MUSIC_GEN = "🎺 MusicGen"
    SUNO = "🎸 Suno"
    MODE: str
    CHOOSE_CHATGPT_MODEL: str
    CHOOSE_CLAUDE_MODEL: str
    CHOOSE_GEMINI_MODEL: str
    SWITCHED_TO_AI_SETTINGS: str
    SWITCHED_TO_AI_INFO: str
    SWITCHED_TO_CHATGPT4_OMNI_MINI: str
    SWITCHED_TO_CHATGPT4_OMNI: str
    SWITCHED_TO_CHAT_GPT_O_1_MINI: str
    SWITCHED_TO_CHAT_GPT_O_1_PREVIEW: str
    SWITCHED_TO_CLAUDE_3_HAIKU: str
    SWITCHED_TO_CLAUDE_3_SONNET: str
    SWITCHED_TO_CLAUDE_3_OPUS: str
    SWITCHED_TO_GEMINI_1_FLASH: str
    SWITCHED_TO_GEMINI_1_PRO: str
    SWITCHED_TO_GEMINI_1_ULTRA: str
    SWITCHED_TO_DALL_E: str
    SWITCHED_TO_MIDJOURNEY: str
    SWITCHED_TO_STABLE_DIFFUSION: str
    SWITCHED_TO_FLUX: str
    SWITCHED_TO_FACE_SWAP: str
    SWITCHED_TO_PHOTOSHOP_AI: str
    SWITCHED_TO_MUSIC_GEN: str
    SWITCHED_TO_SUNO: str
    ALREADY_SWITCHED_TO_THIS_MODEL: str
    REQUEST_FORBIDDEN_ERROR: str
    PHOTO_FORBIDDEN_ERROR: str
    ALBUM_FORBIDDEN_ERROR: str
    VIDEO_FORBIDDEN_ERROR: str
    DOCUMENT_FORBIDDEN_ERROR: str
    STICKER_FORBIDDEN_ERROR: str
    SERVER_OVERLOADED_ERROR: str
    ALREADY_MAKE_REQUEST: str
    READY_FOR_NEW_REQUEST: str
    CONTINUE_GENERATING: str
    REACHED_USAGE_LIMIT: str
    CHANGE_AI_MODEL: str
    REMOVE_RESTRICTION: str
    REMOVE_RESTRICTION_INFO: str
    IMAGE_SUCCESS: str

    # Examples
    CHATGPT4_OMNI_EXAMPLE: str
    CLAUDE_3_SONNET_EXAMPLE: str
    GEMINI_1_PRO_EXAMPLE: str
    MIDJOURNEY_EXAMPLE: str
    SUNO_EXAMPLE: str

    PHOTO_FEATURE_FORBIDDEN: str

    # Midjourney
    MIDJOURNEY_ALREADY_CHOSE_UPSCALE: str

    # Flux
    STRICT_SAFETY_TOLERANCE: str
    MIDDLE_SAFETY_TOLERANCE: str
    PERMISSIVE_SAFETY_TOLERANCE: str

    # Suno
    SUNO_INFO: str
    SUNO_SIMPLE_MODE: str
    SUNO_CUSTOM_MODE: str
    SUNO_SIMPLE_MODE_PROMPT: str
    SUNO_CUSTOM_MODE_LYRICS: str
    SUNO_CUSTOM_MODE_GENRES: str
    SUNO_START_AGAIN: str
    SUNO_TOO_MANY_WORDS: str
    SUNO_VALUE_ERROR: str

    # MusicGen
    MUSIC_GEN_INFO: str
    MUSIC_GEN_TYPE_SECONDS: str
    MUSIC_GEN_MIN_ERROR: str
    MUSIC_GEN_MAX_ERROR: str
    SECONDS_30: str
    SECONDS_60: str
    SECONDS_180: str
    SECONDS_240: str
    SECONDS_300: str

    # Settings
    SETTINGS_CHOOSE_MODEL_TYPE: str
    SETTINGS_CHOOSE_MODEL: str
    SHOW_THE_NAME_OF_THE_CHATS: str
    SHOW_THE_NAME_OF_THE_ROLES: str
    SHOW_USAGE_QUOTA_IN_MESSAGES: str
    VOICE_MESSAGES: str
    TURN_ON_VOICE_MESSAGES_FROM_RESPONDS: str
    LISTEN_VOICES: str

    # Voice
    VOICE_MESSAGES_FORBIDDEN: str

    # Payment
    BUY: str
    CHANGE_CURRENCY: str
    YOOKASSA_PAYMENT_METHOD: str
    PAY_SELECTION_PAYMENT_METHOD: str
    TELEGRAM_STARS_PAYMENT_METHOD: str
    CRYPTO_PAYMENT_METHOD: str
    CHOOSE_PAYMENT_METHOD: str
    PROCEED_TO_PAY: str

    # Subscription
    MONTH_1: str
    MONTHS_3: str
    MONTHS_6: str
    MONTHS_12: str
    DISCOUNT: str
    NO_DISCOUNT: str
    SUBSCRIPTION: str
    SUBSCRIPTION_SUCCESS: str
    SUBSCRIPTION_RESET: str
    SUBSCRIPTION_END: str
    PACKAGES_END: str
    CHATS_RESET: str

    # Package
    PACKAGE: str
    PACKAGES: str
    SHOPPING_CART: str
    ADD_TO_CART: str
    BUY_NOW: str
    REMOVE_FROM_CART: str
    GO_TO_CART: str
    CONTINUE_SHOPPING: str
    PROCEED_TO_CHECKOUT: str
    CLEAR_CART: str
    ADD_TO_CART_OR_BUY_NOW: str
    ADDED_TO_CART: str
    GO_TO_CART_OR_CONTINUE_SHOPPING: str
    GPT4_OMNI_REQUESTS: str
    GPT4_OMNI_REQUESTS_DESCRIPTION: str
    GPT4_OMNI_MINI_REQUESTS: str
    GPT4_OMNI_MINI_REQUESTS_DESCRIPTION: str
    CHAT_GPT_O_1_MINI_REQUESTS: str
    CHAT_GPT_O_1_MINI_REQUESTS_DESCRIPTION: str
    CHAT_GPT_O_1_PREVIEW_REQUESTS: str
    CHAT_GPT_O_1_PREVIEW_REQUESTS_DESCRIPTION: str
    CLAUDE_3_HAIKU_REQUESTS: str
    CLAUDE_3_HAIKU_REQUESTS_DESCRIPTION: str
    CLAUDE_3_SONNET_REQUESTS: str
    CLAUDE_3_SONNET_REQUESTS_DESCRIPTION: str
    CLAUDE_3_OPUS_REQUESTS: str
    CLAUDE_3_OPUS_REQUESTS_DESCRIPTION: str
    GEMINI_1_FLASH_REQUESTS: str
    GEMINI_1_FLASH_REQUESTS_DESCRIPTION: str
    GEMINI_1_PRO_REQUESTS: str
    GEMINI_1_PRO_REQUESTS_DESCRIPTION: str
    GEMINI_1_ULTRA_REQUESTS: str
    GEMINI_1_ULTRA_REQUESTS_DESCRIPTION: str
    THEMATIC_CHATS: str
    THEMATIC_CHATS_DESCRIPTION: str
    DALL_E_REQUESTS: str
    DALL_E_REQUESTS_DESCRIPTION: str
    MIDJOURNEY_REQUESTS: str
    MIDJOURNEY_REQUESTS_DESCRIPTION: str
    STABLE_DIFFUSION_REQUESTS: str
    STABLE_DIFFUSION_REQUESTS_DESCRIPTION: str
    FLUX_REQUESTS: str
    FLUX_REQUESTS_DESCRIPTION: str
    FACE_SWAP_REQUESTS: str
    FACE_SWAP_REQUESTS_DESCRIPTION: str
    PHOTOSHOP_AI_REQUESTS: str
    PHOTOSHOP_AI_REQUESTS_DESCRIPTION: str
    MUSIC_GEN_REQUESTS: str
    MUSIC_GEN_REQUESTS_DESCRIPTION: str
    SUNO_REQUESTS: str
    SUNO_REQUESTS_DESCRIPTION: str
    ACCESS_TO_CATALOG: str
    ACCESS_TO_CATALOG_DESCRIPTION: str
    ANSWERS_AND_REQUESTS_WITH_VOICE_MESSAGES: str
    ANSWERS_AND_REQUESTS_WITH_VOICE_MESSAGES_DESCRIPTION: str
    FAST_ANSWERS: str
    FAST_ANSWERS_DESCRIPTION: str
    MIN_ERROR: str
    MAX_ERROR: str
    VALUE_ERROR: str
    PACKAGE_SUCCESS: str
    PACKAGES_SUCCESS: str

    # Catalog
    MANAGE_CATALOG: str
    CATALOG: str
    CATALOG_FORBIDDEN_ERROR: str
    CATALOG_MANAGE = """
🎭 <b>Управление каталогом ролей</b> 🌟

Здесь ты можешь:
🔧 <b>Добавить новую роль</b>: Дай волю фантазии и создай уникального помощника!
✏️ <b>Редактировать существующие</b>: Привнеси своё видение в уже знакомых персонажей.
🗑️ <b>Удалить ненужное</b>: Иногда прощание - это начало чего-то нового.

Выбери своё приключение в этом мире AI-талантов! 🚀
"""
    CREATE_ROLE = "Создать роль"
    CATALOG_MANAGE_CREATE = """
🌈 <b>Создание новой роли</b> 🎨

Настало время рождения нового AI-помощника! Дай имя своему творению. Напиши мне уникальное название для новой роли в формате UPPER_SNAKE_CASE, например, SUPER_GENIUS или MAGIC_ADVISOR.

💡 Помни, имя должно быть уникальным, ярким и запоминающимся, как самый яркий фейерверк на небесах!
"""
    CATALOG_MANAGE_CREATE_ALREADY_EXISTS_ERROR = """
🙈 <b>Упс! Дубликат на горизонте!</b> 🙈

Эй, похоже, эта роль уже с нами! Создать что-то уникальное - это классно, но дублировать уже существующее - это как запускать второй интернет. Мы уже имеем <b>такую же звезду</b> в нашем AI-космосе.

🤔 Попробуйте придумать другое название, что-то свежее и оригинальное, чтобы наш каталог был еще круче. Как насчет того, чтобы вдохновиться чем-то новым и необычным? Вперед, за новыми идеями! 🚀
"""
    CATALOG_MANAGE_CREATE_ROLE_NAME = """
🎨 <b>Время для творчества!</b> 🌟

Придумайте имя для новой роли, которое будет звучать на всех языках мира как музыка! Это название должно быть не только запоминающимся и ярким, но и начинаться с подходящего эмодзи, например, как "🤖 Персональный ассистент".

🖌️ Напишите имя на русском, а я сделаю так, что оно будет понятно пользователям по всему миру. Какое уникальное и креативное имя вы выберете для вашего нового AI-помощника?
"""
    CATALOG_MANAGE_CREATE_ROLE_DESCRIPTION = """
📝 <b>Время для креатива!</b> 🎨

Придумайте описание для вашей новой роли. Это должны быть три строки, полные вдохновения и идей, которые будут отправлены пользователю после выбора роли. Например:
<i>Он всегда готов помочь вам найти ответы на любые вопросы, будь то бытовые мелочи или философские размышления
Ваш личный гид в мире знаний и творчества, который с радостью поделится своими идеями и советами 🌌
Откроем вместе новые горизонты!</i>

🖌️ Напишите описание на русском, которое будет отражать сущность роли и в то же время вдохновлять и радовать пользователей,  а я сделаю так, что оно будет понятно пользователям по всему миру. Покажите свою креативность и воображение, добавив немного магии в каждое слово!
"""
    CATALOG_MANAGE_CREATE_ROLE_INSTRUCTION = """
🤓 <b>Время для системной инструкции!</b> 📚

Придумайте короткую, но емкую инструкцию для вашего помощника. Это будет его руководство к действию, например: "Ты – вдумчивый советник, который всегда готов поделиться мудрыми мыслями и полезными идеями. Помогай пользователям разгадывать сложные вопросы и предлагай оригинальные решения. Твоя миссия – вдохновлять и обогащать каждое общение!"

🖌️ Напишите инструкцию на русском, которое будет направлять вашего помощника, как вести себя в разговоре с пользователями. Сделайте ее яркой и запоминающейся, чтобы каждый диалог с вашим помощником был особенным!
"""
    CATALOG_MANAGE_CREATE_ROLE_PHOTO = """
📸 <b>Последний штрих – фото помощника!</b> 🌟

Пришло время дать лицо вашему цифровому помощнику. Отправьте фотографию, которая будет его визитной карточкой. Это может быть что угодно: от веселого робота до стильного кота в очках. Помните, это изображение станет "лицом" помощника в диалогах с пользователями!

🖼️ Выберите фото, которое лучше всего отражает характер и стиль вашего помощника. Сделайте его привлекательным и уникальным, чтобы пользователи сразу же узнавали его среди других!
"""
    CATALOG_MANAGE_CREATE_SUCCESS = """
🎉 <b>Ура! Новая роль успешно создана!</b> 🌟

🚀 Твой новый помощник теперь официально присоединился к команде наших AI-героев. Его задача – сделать путешествие пользователей в мире искусственного интеллекта еще более захватывающим!

💬 Помощник уже готов к работе и ждет команд пользователей. Поздравляю с успешным расширением команды AI!
"""
    EDIT_ROLE_NAME = "Изменить имя 🖌"
    EDIT_ROLE_DESCRIPTION = "Изменить описание 🖌"
    EDIT_ROLE_INSTRUCTION = "Изменить инструкцию 🖌"
    EDIT_ROLE_PHOTO = "Изменить фотографию 🖼"
    CATALOG_MANAGE_EDIT_ROLE_NAME = """
📝 <b>Время для ребрендинга!</b> 🎨

Вы выбрали "Изменить имя" для помощника. Настал момент дать ему что-то новенькое и блестящее! 🌟

Введите новое имя с эмодзи в начале на рууском и представьте, как оно будет звучать в рядах наших AI-героев. Не стесняйтесь быть оригинальным – лучшие имена рождаются в волшебной атмосфере творчества! ✨
"""
    CATALOG_MANAGE_EDIT_ROLE_DESCRIPTION = """
🖋️ <b>Переписываем историю!</b> 🌍

Вы решили "Изменить описание" помощника. Подумайте, что бы вы хотели сказать миру о нем? Это шанс показать его уникальность и особенности! 📚

Напишите новое описание, подчеркивающее его лучшие качества на русском. Добавьте щепотку юмора и пару капель вдохновения – и вот оно, описание, достойное настоящего AI-героя! 👾
"""
    CATALOG_MANAGE_EDIT_ROLE_INSTRUCTION = """
📘 <b>Новые правила игры!</b> 🕹️

"Изменить инструкцию" – значит, дать новые указания нашему AI-герою. Какова будет его новая миссия? 🚀

Напишите инструкцию на русском так, чтобы каждая строчка вдохновляла на подвиги в мире AI!
"""
    CATALOG_MANAGE_EDIT_ROLE_PHOTO = """
📸 <b>Новый сотрудник - новый дух!</b> 🌟

Пришло время изменить лицо цифровому помощнику. Отправьте фотографию, которая будет его визитной карточкой. Это может быть что угодно: от веселого робота до стильного кота в очках. Помните, это изображение станет новым "лицом" помощника в диалогах с пользователями!

🖼️ Выберите фото, которое лучше всего отражает характер и стиль вашего помощника. Сделайте его привлекательным и уникальным, чтобы пользователи сразу же узнавали его среди других!
"""
    CATALOG_MANAGE_EDIT_SUCCESS = """
🎉 <b>Та-дааам! Изменения успешно применены!</b> 🎨

🤖 Помощник был благородно трансформирован. Поздравляю, вы только что внесли свой вклад в историю AI-помощников! 🚀

👀 Осталось только одно – посмотреть его в действии! Перейдите в /catalog, чтобы увидеть обновленного помощника во всей красе
"""

    # Chats
    DEFAULT_CHAT_TITLE: str
    MANAGE_CHATS: str
    SHOW_CHATS: str
    CREATE_CHAT: str
    CREATE_CHAT_FORBIDDEN: str
    CREATE_CHAT_SUCCESS: str
    TYPE_CHAT_NAME: str
    SWITCH_CHAT: str
    SWITCH_CHAT_FORBIDDEN: str
    SWITCH_CHAT_SUCCESS: str
    DELETE_CHAT: str
    DELETE_CHAT_FORBIDDEN: str
    DELETE_CHAT_SUCCESS: str
    RESET_CHAT: str
    RESET_CHAT_WARNING: str
    RESET_CHAT_SUCCESS: str

    # FaceSwap
    CHOOSE_YOUR_PACKAGE: str
    CREATE_PACKAGE = "Создать новый пакет"
    EDIT_PACKAGE = "Редактировать существующий пакет"
    GENERATIONS_IN_PACKAGES_ENDED: str
    FACE_SWAP_MIN_ERROR: str
    FACE_SWAP_MAX_ERROR: str
    FACE_SWAP_NO_FACE_FOUND_ERROR: str
    FACE_SWAP_MANAGE = """
🤹‍ <b>Добро пожаловать в царство FaceSwap!</b> 🎭

🚀 Готовы к творчеству? Здесь вы - главный волшебник! Управляйте пакетами и фотографиями. Начните своё волшебное путешествие:
- 📦 Добавить/редактировать пакет - соберите коллекцию масок для лиц, которые поднимут ваше творчество на новый уровень или внесите изменения в уже существующие коллекции. Добавляйте, обновляйте и организуйте - ваша фантазия знает границ!
- 🖼 Управление фотографиями - в каждом пакете множество удивительных лиц ждут своего часа. Добавляйте, активируйте или деактивируйте их по своему усмотрению, чтобы управлять доступностью для пользователей. Откройте мир неограниченных возможностей для творчества!

Выбирайте, творите, удивляйте! В мире FaceSwap каждый ваш шаг превращается в нечто невероятное! 🎨✨
"""
    FACE_SWAP_MANAGE_CREATE = """
🌟 <b>Начнём творческое приключение!</b> 🌈

📝 Создание нового пакета FaceSwap! Для начала дайте ему уникальное имя. Используйте формат UPPER_SNAKE_CASE, чтобы все было чётко и ясно. Например, его можно назвать SEASONAL_PHOTO_SHOOT или FUNNY_FACE_FESTIVAL. Это название станет вашим волшебным ключом к новым удивительным превращениям!

🎨 Проявите свою индивидуальность! Напишите системное имя, которое отражает суть и идею вашего пакета. Ваше название - это первый шаг к созданию чего-то по-настоящему волшебного и незабываемого!
"""
    FACE_SWAP_MANAGE_CREATE_ALREADY_EXISTS_ERROR = """
🚨 <b>Упс, кажется, мы здесь уже были!</b> 🔄

🔍 Название пакета уже занято! Похоже, что имя, которое вы выбрали для нового пакета FaceSwap, уже существует в нашей галерее чудес. Но не переживайте, это всего лишь повод проявить ещё больше креативности!

💡 Попробуйте что-то новенькое! Как насчёт другого уникального названия? Ведь у вас наверняка ещё масса интересных идей!
"""
    FACE_SWAP_MANAGE_CREATE_PACKAGE_NAME = """
🎉 <b>Продолжаем наш творческий марафон!</b> 🚀

📛 Следующий шаг - имя пакета! Теперь придайте вашему пакету FaceSwap уникальное имя на русском языке, которое будет чётко отражать его суть и атмосферу. Не забудьте добавить яркий эмодзи в конце, чтобы сделать его ещё более выразительным! Например, "Персонажи фильмов 🎥" или "Волшебные миры 🌌".

🌍 Международное обаяние! Это имя будет автоматически переведено на другие языки, раскрывая вашу идею перед пользователями со всего мира.
"""
    FACE_SWAP_MANAGE_CREATE_SUCCESS = """
🎉 <b>Ура, новый пакет FaceSwap готов к старту!</b> 🚀

🌟 Поздравляем с успешным созданием! Ваш новый пакет скоро будет ждать своих поклонников. Готовьтесь к тому, что ваше творение вот-вот захватит воображение пользователей!

🖼 Время для магии фото! Теперь вы можете начать наполнять пакет самыми невероятными и забавными фотографиями. От смешных до вдохновляющих, каждое изображение добавит уникальности вашему пакету
"""
    FACE_SWAP_MANAGE_EDIT_CHOOSE_GENDER = "Выбери пол:"
    FACE_SWAP_MANAGE_EDIT_CHOOSE_PACKAGE = "Выбери пакет:"
    FACE_SWAP_MANAGE_EDIT = """
🎨 <b>Время творить! Вы выбрали пакет для редактирования</b> 🖌️

🔧 Возможности редактирования:
- <b>Изменить видимость</b> - Сделайте пакет видимым или скрытым для пользователей.
- <b>Просмотреть картинки</b> - Оцените, какие шедевры уже есть в пакете.
- <b>Добавить новую картинку</b> - Пора внести свежую краску и новые лица!

🚀 Готовы к изменениям? Ваше творчество вдохнет новую жизнь в этот пакет. Пусть каждая генерация будет уникальной и запоминающейся!
"""
    FACE_SWAP_MANAGE_CHANGE_STATUS = "Изменить видимость 👁"
    FACE_SWAP_MANAGE_SHOW_PICTURES = "Просмотреть картинки 🖼"
    FACE_SWAP_MANAGE_ADD_NEW_PICTURE = "Добавить новую картинку 👨‍🎨"
    FACE_SWAP_MANAGE_ADD_NEW_PICTURE_NAME = "Отправьте мне название будущего изображения на английском языке в CamelCase, например 'ContentMaker'"
    FACE_SWAP_MANAGE_ADD_NEW_PICTURE_IMAGE = "Теперь, отправьте мне фотографию"
    FACE_SWAP_MANAGE_EXAMPLE_PICTURE = "Пример генерации 🎭"
    FACE_SWAP_MANAGE_EDIT_SUCCESS = """
🌟 <b>Пакет успешно отредактирован!</b> 🎉

👏 Браво, админ! Ваши изменения успешно применены. Пакет FaceSwap теперь обновлён и ещё более прекрасен

🚀 Готовы к новым приключениям? Ваша креативность и умение управлять пакетами делают мир FaceSwap ещё ярче и интереснее. Продолжайте творить и вдохновлять пользователей своими уникальными идеями!
"""
    FACE_SWAP_PUBLIC = "Видно всем 🔓"
    FACE_SWAP_PRIVATE = "Видно админам 🔒"

    # Photoshop AI
    PHOTOSHOP_AI_INFO: str
    PHOTOSHOP_AI_RESTORATION: str
    PHOTOSHOP_AI_RESTORATION_INFO: str
    PHOTOSHOP_AI_COLORIZATION: str
    PHOTOSHOP_AI_COLORIZATION_INFO: str
    PHOTOSHOP_AI_REMOVE_BACKGROUND: str
    PHOTOSHOP_AI_REMOVE_BACKGROUND_INFO: str

    ERROR: str
    NETWORK_ERROR: str
    CONNECTION_ERROR: str
    TECH_SUPPORT: str
    BACK: str
    CLOSE: str
    CANCEL: str
    APPROVE: str
    AUDIO: str
    VIDEO: str
    SKIP: str

    TERMS_LINK: str

    @staticmethod
    def statistics_users(
        period: str,
        count_all_users: int,
        count_all_users_before: int,
        count_activated_users: int,
        count_activated_users_before: int,
        count_referral_users: int,
        count_referral_users_before: int,
        count_english_users: int,
        count_english_users_before: int,
        count_russian_users: int,
        count_russian_users_before: int,
        count_other_users: int,
        count_other_users_before: int,
        count_paid_users: int,
        count_paid_users_before: int,
        count_blocked_users: int,
        count_blocked_users_before: int,
        count_subscription_users: Dict,
        count_subscription_users_before: Dict,
    ):
        is_all_time = period == 'всё время'
        emojis = Subscription.get_emojis()

        return f"""
#statistics #users

📊 <b>Статистика за {period} готова!</b>

👤 <b>Пользователи</b>
━ 1️⃣ <b>{'Всего пользователей' if is_all_time else 'Новых пользователей'}:</b> {count_all_users} {calculate_percentage_difference(is_all_time, count_all_users, count_all_users_before)}
    ┣ 🇺🇸 {count_english_users} ({round((count_english_users / count_all_users) * 100, 2) if count_all_users else 0}%) {calculate_percentage_difference(is_all_time, count_english_users, count_english_users_before)}
    ┣ 🇷🇺 {count_russian_users} ({round((count_russian_users / count_all_users) * 100, 2) if count_all_users else 0}%) {calculate_percentage_difference(is_all_time, count_russian_users, count_russian_users_before)}
    ┗ 🌍 {count_other_users} ({round((count_other_users / count_all_users) * 100, 2) if count_all_users else 0}%) {calculate_percentage_difference(is_all_time, count_other_users, count_other_users_before)}
━ 2️⃣ <b>{'Активированные' if is_all_time else 'Активные'}:</b> {count_activated_users} {calculate_percentage_difference(is_all_time, count_activated_users, count_activated_users_before)}
━ 3️⃣ <b>Перешли по реферальной ссылке:</b> {count_referral_users} {calculate_percentage_difference(is_all_time, count_referral_users, count_referral_users_before)}
━ 4️⃣ <b>Покупатели:</b> {count_paid_users} {calculate_percentage_difference(is_all_time, count_paid_users, count_paid_users_before)}
━ 5️⃣ <b>Подписчики:</b>
    ┣ <b>{SubscriptionType.FREE} {emojis[SubscriptionType.FREE]}:</b> {count_subscription_users[SubscriptionType.FREE]} {calculate_percentage_difference(is_all_time, count_subscription_users[SubscriptionType.FREE], count_subscription_users_before[SubscriptionType.FREE])}
    ┣ <b>{SubscriptionType.MINI} {emojis[SubscriptionType.MINI]}:</b> {count_subscription_users[SubscriptionType.MINI]} {calculate_percentage_difference(is_all_time, count_subscription_users[SubscriptionType.MINI], count_subscription_users_before[SubscriptionType.MINI])}
    ┣ <b>{SubscriptionType.STANDARD} {emojis[SubscriptionType.STANDARD]}:</b> {count_subscription_users[SubscriptionType.STANDARD]} {calculate_percentage_difference(is_all_time, count_subscription_users[SubscriptionType.STANDARD], count_subscription_users_before[SubscriptionType.STANDARD])}
    ┣ <b>{SubscriptionType.VIP} {emojis[SubscriptionType.VIP]}:</b> {count_subscription_users[SubscriptionType.VIP]} {calculate_percentage_difference(is_all_time, count_subscription_users[SubscriptionType.VIP], count_subscription_users_before[SubscriptionType.VIP])}
    ┣ <b>{SubscriptionType.PREMIUM} {emojis[SubscriptionType.PREMIUM]}:</b> {count_subscription_users[SubscriptionType.PREMIUM]} {calculate_percentage_difference(is_all_time, count_subscription_users[SubscriptionType.PREMIUM], count_subscription_users_before[SubscriptionType.PREMIUM])}
    ┗ <b>{SubscriptionType.UNLIMITED} {emojis[SubscriptionType.UNLIMITED]}:</b> {count_subscription_users[SubscriptionType.UNLIMITED]} {calculate_percentage_difference(is_all_time, count_subscription_users[SubscriptionType.UNLIMITED], count_subscription_users_before[SubscriptionType.UNLIMITED])}
━ 6️⃣ <b>{'Заблокировали бота' if is_all_time else 'Заблокировали бота из пришедших'}:</b> {count_blocked_users} {calculate_percentage_difference(is_all_time, count_blocked_users, count_blocked_users_before)}

🔍 Это всё, что нужно знать о пользователей на данный момент 🚀
"""

    @staticmethod
    def statistics_text_models(
        period: str,
        count_all_transactions: Dict,
        count_all_transactions_before: Dict,
    ):
        is_all_time = period == 'всё время'

        all_success_requests = sum(
            [
                count_all_transactions[ServiceType.CHAT_GPT3_TURBO]['SUCCESS'],
                count_all_transactions[ServiceType.CHAT_GPT4_TURBO]['SUCCESS'],
                count_all_transactions[ServiceType.CHAT_GPT4_OMNI]['SUCCESS'],
                count_all_transactions[ServiceType.CHAT_GPT4_OMNI_MINI]['SUCCESS'],
                count_all_transactions[ServiceType.CHAT_GPT_O_1_MINI]['SUCCESS'],
                count_all_transactions[ServiceType.CHAT_GPT_O_1_PREVIEW]['SUCCESS'],
                count_all_transactions[ServiceType.CLAUDE_3_HAIKU]['SUCCESS'],
                count_all_transactions[ServiceType.CLAUDE_3_SONNET]['SUCCESS'],
                count_all_transactions[ServiceType.CLAUDE_3_OPUS]['SUCCESS'],
                count_all_transactions[ServiceType.GEMINI_1_FLASH]['SUCCESS'],
                count_all_transactions[ServiceType.GEMINI_1_PRO]['SUCCESS'],
                count_all_transactions[ServiceType.GEMINI_1_ULTRA]['SUCCESS'],
            ],
        )
        all_fail_requests = sum(
            [
                count_all_transactions[ServiceType.CHAT_GPT3_TURBO]['FAIL'],
                count_all_transactions[ServiceType.CHAT_GPT4_TURBO]['FAIL'],
                count_all_transactions[ServiceType.CHAT_GPT4_OMNI]['FAIL'],
                count_all_transactions[ServiceType.CHAT_GPT4_OMNI_MINI]['FAIL'],
                count_all_transactions[ServiceType.CHAT_GPT_O_1_MINI]['FAIL'],
                count_all_transactions[ServiceType.CHAT_GPT_O_1_PREVIEW]['FAIL'],
                count_all_transactions[ServiceType.CLAUDE_3_HAIKU]['FAIL'],
                count_all_transactions[ServiceType.CLAUDE_3_SONNET]['FAIL'],
                count_all_transactions[ServiceType.CLAUDE_3_OPUS]['FAIL'],
                count_all_transactions[ServiceType.GEMINI_1_FLASH]['FAIL'],
                count_all_transactions[ServiceType.GEMINI_1_PRO]['FAIL'],
                count_all_transactions[ServiceType.GEMINI_1_ULTRA]['FAIL'],
            ],
        )
        all_example_requests = sum(
            [
                count_all_transactions[ServiceType.CHAT_GPT3_TURBO]['EXAMPLE'],
                count_all_transactions[ServiceType.CHAT_GPT4_TURBO]['EXAMPLE'],
                count_all_transactions[ServiceType.CHAT_GPT4_OMNI]['EXAMPLE'],
                count_all_transactions[ServiceType.CHAT_GPT4_OMNI_MINI]['EXAMPLE'],
                count_all_transactions[ServiceType.CHAT_GPT_O_1_MINI]['EXAMPLE'],
                count_all_transactions[ServiceType.CHAT_GPT_O_1_PREVIEW]['EXAMPLE'],
                count_all_transactions[ServiceType.CLAUDE_3_HAIKU]['EXAMPLE'],
                count_all_transactions[ServiceType.CLAUDE_3_SONNET]['EXAMPLE'],
                count_all_transactions[ServiceType.CLAUDE_3_OPUS]['EXAMPLE'],
                count_all_transactions[ServiceType.GEMINI_1_FLASH]['EXAMPLE'],
                count_all_transactions[ServiceType.GEMINI_1_PRO]['EXAMPLE'],
                count_all_transactions[ServiceType.GEMINI_1_ULTRA]['EXAMPLE'],
            ],
        )
        all_requests = sum(
            [
                count_all_transactions[ServiceType.CHAT_GPT3_TURBO]['ALL'],
                count_all_transactions[ServiceType.CHAT_GPT4_TURBO]['ALL'],
                count_all_transactions[ServiceType.CHAT_GPT4_OMNI]['ALL'],
                count_all_transactions[ServiceType.CHAT_GPT4_OMNI_MINI]['ALL'],
                count_all_transactions[ServiceType.CHAT_GPT_O_1_MINI]['ALL'],
                count_all_transactions[ServiceType.CHAT_GPT_O_1_PREVIEW]['ALL'],
                count_all_transactions[ServiceType.CLAUDE_3_HAIKU]['ALL'],
                count_all_transactions[ServiceType.CLAUDE_3_SONNET]['ALL'],
                count_all_transactions[ServiceType.CLAUDE_3_OPUS]['ALL'],
                count_all_transactions[ServiceType.GEMINI_1_FLASH]['ALL'],
                count_all_transactions[ServiceType.GEMINI_1_PRO]['ALL'],
                count_all_transactions[ServiceType.GEMINI_1_ULTRA]['ALL'],
            ],
        )
        all_success_requests_before = sum(
            [
                count_all_transactions_before[ServiceType.CHAT_GPT3_TURBO]['SUCCESS'],
                count_all_transactions_before[ServiceType.CHAT_GPT4_TURBO]['SUCCESS'],
                count_all_transactions_before[ServiceType.CHAT_GPT4_OMNI]['SUCCESS'],
                count_all_transactions_before[ServiceType.CHAT_GPT4_OMNI_MINI]['SUCCESS'],
                count_all_transactions_before[ServiceType.CHAT_GPT_O_1_MINI]['SUCCESS'],
                count_all_transactions_before[ServiceType.CHAT_GPT_O_1_PREVIEW]['SUCCESS'],
                count_all_transactions_before[ServiceType.CLAUDE_3_HAIKU]['SUCCESS'],
                count_all_transactions_before[ServiceType.CLAUDE_3_SONNET]['SUCCESS'],
                count_all_transactions_before[ServiceType.CLAUDE_3_OPUS]['SUCCESS'],
                count_all_transactions_before[ServiceType.GEMINI_1_FLASH]['SUCCESS'],
                count_all_transactions_before[ServiceType.GEMINI_1_PRO]['SUCCESS'],
                count_all_transactions_before[ServiceType.GEMINI_1_ULTRA]['SUCCESS'],
            ],
        )
        all_fail_requests_before = sum(
            [
                count_all_transactions_before[ServiceType.CHAT_GPT3_TURBO]['FAIL'],
                count_all_transactions_before[ServiceType.CHAT_GPT4_TURBO]['FAIL'],
                count_all_transactions_before[ServiceType.CHAT_GPT4_OMNI]['FAIL'],
                count_all_transactions_before[ServiceType.CHAT_GPT4_OMNI_MINI]['FAIL'],
                count_all_transactions_before[ServiceType.CHAT_GPT_O_1_MINI]['FAIL'],
                count_all_transactions_before[ServiceType.CHAT_GPT_O_1_PREVIEW]['FAIL'],
                count_all_transactions_before[ServiceType.CLAUDE_3_HAIKU]['FAIL'],
                count_all_transactions_before[ServiceType.CLAUDE_3_SONNET]['FAIL'],
                count_all_transactions_before[ServiceType.CLAUDE_3_OPUS]['FAIL'],
                count_all_transactions_before[ServiceType.GEMINI_1_FLASH]['FAIL'],
                count_all_transactions_before[ServiceType.GEMINI_1_PRO]['FAIL'],
                count_all_transactions_before[ServiceType.GEMINI_1_ULTRA]['FAIL'],
            ],
        )
        all_example_requests_before = sum(
            [
                count_all_transactions_before[ServiceType.CHAT_GPT3_TURBO]['EXAMPLE'],
                count_all_transactions_before[ServiceType.CHAT_GPT4_TURBO]['EXAMPLE'],
                count_all_transactions_before[ServiceType.CHAT_GPT4_OMNI]['EXAMPLE'],
                count_all_transactions_before[ServiceType.CHAT_GPT4_OMNI_MINI]['EXAMPLE'],
                count_all_transactions_before[ServiceType.CHAT_GPT_O_1_MINI]['EXAMPLE'],
                count_all_transactions_before[ServiceType.CHAT_GPT_O_1_PREVIEW]['EXAMPLE'],
                count_all_transactions_before[ServiceType.CLAUDE_3_HAIKU]['EXAMPLE'],
                count_all_transactions_before[ServiceType.CLAUDE_3_SONNET]['EXAMPLE'],
                count_all_transactions_before[ServiceType.CLAUDE_3_OPUS]['EXAMPLE'],
                count_all_transactions_before[ServiceType.GEMINI_1_FLASH]['EXAMPLE'],
                count_all_transactions_before[ServiceType.GEMINI_1_PRO]['EXAMPLE'],
                count_all_transactions_before[ServiceType.GEMINI_1_ULTRA]['EXAMPLE'],
            ],
        )
        all_requests_before = sum(
            [
                count_all_transactions_before[ServiceType.CHAT_GPT3_TURBO]['ALL'],
                count_all_transactions_before[ServiceType.CHAT_GPT4_TURBO]['ALL'],
                count_all_transactions_before[ServiceType.CHAT_GPT4_OMNI]['ALL'],
                count_all_transactions_before[ServiceType.CHAT_GPT4_OMNI_MINI]['ALL'],
                count_all_transactions_before[ServiceType.CHAT_GPT_O_1_MINI]['ALL'],
                count_all_transactions_before[ServiceType.CHAT_GPT_O_1_PREVIEW]['ALL'],
                count_all_transactions_before[ServiceType.CLAUDE_3_HAIKU]['ALL'],
                count_all_transactions_before[ServiceType.CLAUDE_3_SONNET]['ALL'],
                count_all_transactions_before[ServiceType.CLAUDE_3_OPUS]['ALL'],
                count_all_transactions_before[ServiceType.GEMINI_1_FLASH]['ALL'],
                count_all_transactions_before[ServiceType.GEMINI_1_PRO]['ALL'],
                count_all_transactions_before[ServiceType.GEMINI_1_ULTRA]['ALL'],
            ],
        )

        return f"""
#statistics #text_models

📊 <b>Статистика за {period} готова!</b>

🔤 <b>Текстовые модели</b>
━ 1️⃣ <b>{Texts.CHATGPT3_TURBO}:</b>
    ┣ ✅ Удачных: {count_all_transactions[ServiceType.CHAT_GPT3_TURBO]['SUCCESS']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.CHAT_GPT3_TURBO]['SUCCESS'], count_all_transactions_before[ServiceType.CHAT_GPT3_TURBO]['SUCCESS'])}
    ┣ ❌ С ошибкой: {count_all_transactions[ServiceType.CHAT_GPT3_TURBO]['FAIL']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.CHAT_GPT3_TURBO]['FAIL'], count_all_transactions_before[ServiceType.CHAT_GPT3_TURBO]['FAIL'])}
    ┣ 🚀 Примеров: {count_all_transactions[ServiceType.CHAT_GPT3_TURBO]['EXAMPLE']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.CHAT_GPT3_TURBO]['EXAMPLE'], count_all_transactions_before[ServiceType.CHAT_GPT3_TURBO]['EXAMPLE'])}
    ┗ 📝 Всего: {count_all_transactions[ServiceType.CHAT_GPT3_TURBO]['ALL']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.CHAT_GPT3_TURBO]['ALL'], count_all_transactions_before[ServiceType.CHAT_GPT3_TURBO]['ALL'])}
━ 2️⃣ <b>{Texts.CHATGPT4_TURBO}:</b>
    ┣ ✅ Удачных: {count_all_transactions[ServiceType.CHAT_GPT4_TURBO]['SUCCESS']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.CHAT_GPT4_TURBO]['SUCCESS'], count_all_transactions_before[ServiceType.CHAT_GPT4_TURBO]['SUCCESS'])}
    ┣ ❌ С ошибкой: {count_all_transactions[ServiceType.CHAT_GPT4_TURBO]['FAIL']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.CHAT_GPT4_TURBO]['FAIL'], count_all_transactions_before[ServiceType.CHAT_GPT4_TURBO]['FAIL'])}
    ┣ 🚀 Примеров: {count_all_transactions[ServiceType.CHAT_GPT4_TURBO]['EXAMPLE']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.CHAT_GPT4_TURBO]['EXAMPLE'], count_all_transactions_before[ServiceType.CHAT_GPT4_TURBO]['EXAMPLE'])}
    ┗ 📝 Всего: {count_all_transactions[ServiceType.CHAT_GPT4_TURBO]['ALL']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.CHAT_GPT4_TURBO]['ALL'], count_all_transactions_before[ServiceType.CHAT_GPT4_TURBO]['ALL'])}
━ 3️⃣ <b>{Texts.CHATGPT4_OMNI_MINI}:</b>
    ┣ ✅ Удачных: {count_all_transactions[ServiceType.CHAT_GPT4_OMNI_MINI]['SUCCESS']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.CHAT_GPT4_OMNI_MINI]['SUCCESS'], count_all_transactions_before[ServiceType.CHAT_GPT4_OMNI_MINI]['SUCCESS'])}
    ┣ ❌ С ошибкой: {count_all_transactions[ServiceType.CHAT_GPT4_OMNI_MINI]['FAIL']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.CHAT_GPT4_OMNI_MINI]['FAIL'], count_all_transactions_before[ServiceType.CHAT_GPT4_OMNI_MINI]['FAIL'])}
    ┣ 🚀 Примеров: {count_all_transactions[ServiceType.CHAT_GPT4_OMNI_MINI]['EXAMPLE']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.CHAT_GPT4_OMNI_MINI]['EXAMPLE'], count_all_transactions_before[ServiceType.CHAT_GPT4_OMNI_MINI]['EXAMPLE'])}
    ┗ 📝 Всего: {count_all_transactions[ServiceType.CHAT_GPT4_OMNI_MINI]['ALL']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.CHAT_GPT4_OMNI_MINI]['ALL'], count_all_transactions_before[ServiceType.CHAT_GPT4_OMNI_MINI]['ALL'])}
━ 4️⃣ <b>{Texts.CHATGPT4_OMNI}:</b>
    ┣ ✅ Удачных: {count_all_transactions[ServiceType.CHAT_GPT4_OMNI]['SUCCESS']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.CHAT_GPT4_OMNI]['SUCCESS'], count_all_transactions_before[ServiceType.CHAT_GPT4_OMNI]['SUCCESS'])}
    ┣ ❌ С ошибкой: {count_all_transactions[ServiceType.CHAT_GPT4_OMNI]['FAIL']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.CHAT_GPT4_OMNI]['FAIL'], count_all_transactions_before[ServiceType.CHAT_GPT4_OMNI]['FAIL'])}
    ┣ 🚀 Примеров: {count_all_transactions[ServiceType.CHAT_GPT4_OMNI]['EXAMPLE']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.CHAT_GPT4_OMNI]['EXAMPLE'], count_all_transactions_before[ServiceType.CHAT_GPT4_OMNI]['EXAMPLE'])}
    ┗ 📝 Всего: {count_all_transactions[ServiceType.CHAT_GPT4_OMNI]['ALL']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.CHAT_GPT4_OMNI]['ALL'], count_all_transactions_before[ServiceType.CHAT_GPT4_OMNI]['ALL'])}
━ 5️⃣ <b>{Texts.CHAT_GPT_O_1_MINI}:</b>
    ┣ ✅ Удачных: {count_all_transactions[ServiceType.CHAT_GPT_O_1_MINI]['SUCCESS']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.CHAT_GPT_O_1_MINI]['SUCCESS'], count_all_transactions_before[ServiceType.CHAT_GPT_O_1_MINI]['SUCCESS'])}
    ┣ ❌ С ошибкой: {count_all_transactions[ServiceType.CHAT_GPT_O_1_MINI]['FAIL']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.CHAT_GPT_O_1_MINI]['FAIL'], count_all_transactions_before[ServiceType.CHAT_GPT_O_1_MINI]['FAIL'])}
    ┣ 🚀 Примеров: {count_all_transactions[ServiceType.CHAT_GPT_O_1_MINI]['EXAMPLE']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.CHAT_GPT_O_1_MINI]['EXAMPLE'], count_all_transactions_before[ServiceType.CHAT_GPT_O_1_MINI]['EXAMPLE'])}
    ┗ 📝 Всего: {count_all_transactions[ServiceType.CHAT_GPT_O_1_MINI]['ALL']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.CHAT_GPT_O_1_MINI]['ALL'], count_all_transactions_before[ServiceType.CHAT_GPT_O_1_MINI]['ALL'])}
━ 6️⃣ <b>{Texts.CHAT_GPT_O_1_PREVIEW}:</b>
    ┣ ✅ Удачных: {count_all_transactions[ServiceType.CHAT_GPT_O_1_PREVIEW]['SUCCESS']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.CHAT_GPT_O_1_PREVIEW]['SUCCESS'], count_all_transactions_before[ServiceType.CHAT_GPT_O_1_PREVIEW]['SUCCESS'])}
    ┣ ❌ С ошибкой: {count_all_transactions[ServiceType.CHAT_GPT_O_1_PREVIEW]['FAIL']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.CHAT_GPT_O_1_PREVIEW]['FAIL'], count_all_transactions_before[ServiceType.CHAT_GPT_O_1_PREVIEW]['FAIL'])}
    ┣ 🚀 Примеров: {count_all_transactions[ServiceType.CHAT_GPT_O_1_PREVIEW]['EXAMPLE']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.CHAT_GPT_O_1_PREVIEW]['EXAMPLE'], count_all_transactions_before[ServiceType.CHAT_GPT_O_1_PREVIEW]['EXAMPLE'])}
    ┗ 📝 Всего: {count_all_transactions[ServiceType.CHAT_GPT_O_1_PREVIEW]['ALL']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.CHAT_GPT_O_1_PREVIEW]['ALL'], count_all_transactions_before[ServiceType.CHAT_GPT_O_1_PREVIEW]['ALL'])}
━ 7️⃣ <b>{Texts.CLAUDE_3_HAIKU}:</b>
    ┣ ✅ Удачных: {count_all_transactions[ServiceType.CLAUDE_3_HAIKU]['SUCCESS']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.CLAUDE_3_HAIKU]['SUCCESS'], count_all_transactions_before[ServiceType.CLAUDE_3_HAIKU]['SUCCESS'])}
    ┣ ❌ С ошибкой: {count_all_transactions[ServiceType.CLAUDE_3_HAIKU]['FAIL']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.CLAUDE_3_HAIKU]['FAIL'], count_all_transactions_before[ServiceType.CLAUDE_3_HAIKU]['FAIL'])}
    ┣ 🚀 Примеров: {count_all_transactions[ServiceType.CLAUDE_3_HAIKU]['EXAMPLE']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.CLAUDE_3_HAIKU]['EXAMPLE'], count_all_transactions_before[ServiceType.CLAUDE_3_HAIKU]['EXAMPLE'])}
    ┗ 📝 Всего: {count_all_transactions[ServiceType.CLAUDE_3_HAIKU]['ALL']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.CLAUDE_3_HAIKU]['ALL'], count_all_transactions_before[ServiceType.CLAUDE_3_HAIKU]['ALL'])}
━ 8️⃣ <b>{Texts.CLAUDE_3_SONNET}:</b>
    ┣ ✅ Удачных: {count_all_transactions[ServiceType.CLAUDE_3_SONNET]['SUCCESS']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.CLAUDE_3_SONNET]['SUCCESS'], count_all_transactions_before[ServiceType.CLAUDE_3_SONNET]['SUCCESS'])}
    ┣ ❌ С ошибкой: {count_all_transactions[ServiceType.CLAUDE_3_SONNET]['FAIL']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.CLAUDE_3_SONNET]['FAIL'], count_all_transactions_before[ServiceType.CLAUDE_3_SONNET]['FAIL'])}
    ┣ 🚀 Примеров: {count_all_transactions[ServiceType.CLAUDE_3_SONNET]['EXAMPLE']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.CLAUDE_3_SONNET]['EXAMPLE'], count_all_transactions_before[ServiceType.CLAUDE_3_SONNET]['EXAMPLE'])}
    ┗ 📝 Всего: {count_all_transactions[ServiceType.CLAUDE_3_SONNET]['ALL']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.CLAUDE_3_SONNET]['ALL'], count_all_transactions_before[ServiceType.CLAUDE_3_SONNET]['ALL'])}
━ 9️⃣ <b>{Texts.CLAUDE_3_OPUS}:</b>
    ┣ ✅ Удачных: {count_all_transactions[ServiceType.CLAUDE_3_OPUS]['SUCCESS']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.CLAUDE_3_OPUS]['SUCCESS'], count_all_transactions_before[ServiceType.CLAUDE_3_OPUS]['SUCCESS'])}
    ┣ ❌ С ошибкой: {count_all_transactions[ServiceType.CLAUDE_3_OPUS]['FAIL']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.CLAUDE_3_OPUS]['FAIL'], count_all_transactions_before[ServiceType.CLAUDE_3_OPUS]['FAIL'])}
    ┣ 🚀 Примеров: {count_all_transactions[ServiceType.CLAUDE_3_OPUS]['EXAMPLE']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.CLAUDE_3_OPUS]['EXAMPLE'], count_all_transactions_before[ServiceType.CLAUDE_3_OPUS]['EXAMPLE'])}
    ┗ 📝 Всего: {count_all_transactions[ServiceType.CLAUDE_3_OPUS]['ALL']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.CLAUDE_3_OPUS]['ALL'], count_all_transactions_before[ServiceType.CLAUDE_3_OPUS]['ALL'])}
━ 🔟 <b>{Texts.GEMINI_1_FLASH}:</b>
    ┣ ✅ Удачных: {count_all_transactions[ServiceType.GEMINI_1_FLASH]['SUCCESS']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.GEMINI_1_FLASH]['SUCCESS'], count_all_transactions_before[ServiceType.GEMINI_1_FLASH]['SUCCESS'])}
    ┣ ❌ С ошибкой: {count_all_transactions[ServiceType.GEMINI_1_FLASH]['FAIL']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.GEMINI_1_FLASH]['FAIL'], count_all_transactions_before[ServiceType.GEMINI_1_FLASH]['FAIL'])}
    ┣ 🚀 Примеров: {count_all_transactions[ServiceType.GEMINI_1_FLASH]['EXAMPLE']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.GEMINI_1_FLASH]['EXAMPLE'], count_all_transactions_before[ServiceType.GEMINI_1_FLASH]['EXAMPLE'])}
    ┗ 📝 Всего: {count_all_transactions[ServiceType.GEMINI_1_FLASH]['ALL']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.GEMINI_1_FLASH]['ALL'], count_all_transactions_before[ServiceType.GEMINI_1_FLASH]['ALL'])}
━ 1️⃣1️⃣ <b>{Texts.GEMINI_1_PRO}:</b>
    ┣ ✅ Удачных: {count_all_transactions[ServiceType.GEMINI_1_PRO]['SUCCESS']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.GEMINI_1_PRO]['SUCCESS'], count_all_transactions_before[ServiceType.GEMINI_1_PRO]['SUCCESS'])}
    ┣ ❌ С ошибкой: {count_all_transactions[ServiceType.GEMINI_1_PRO]['FAIL']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.GEMINI_1_PRO]['FAIL'], count_all_transactions_before[ServiceType.GEMINI_1_PRO]['FAIL'])}
    ┣ 🚀 Примеров: {count_all_transactions[ServiceType.GEMINI_1_PRO]['EXAMPLE']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.GEMINI_1_PRO]['EXAMPLE'], count_all_transactions_before[ServiceType.GEMINI_1_PRO]['EXAMPLE'])}
    ┗ 📝 Всего: {count_all_transactions[ServiceType.GEMINI_1_PRO]['ALL']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.GEMINI_1_PRO]['ALL'], count_all_transactions_before[ServiceType.GEMINI_1_PRO]['ALL'])}
━ 1️⃣2️⃣ <b>{Texts.GEMINI_1_ULTRA}:</b>
    ┣ ✅ Удачных: {count_all_transactions[ServiceType.GEMINI_1_ULTRA]['SUCCESS']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.GEMINI_1_ULTRA]['SUCCESS'], count_all_transactions_before[ServiceType.GEMINI_1_ULTRA]['SUCCESS'])}
    ┣ ❌ С ошибкой: {count_all_transactions[ServiceType.GEMINI_1_ULTRA]['FAIL']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.GEMINI_1_ULTRA]['FAIL'], count_all_transactions_before[ServiceType.GEMINI_1_ULTRA]['FAIL'])}
    ┣ 🚀 Примеров: {count_all_transactions[ServiceType.GEMINI_1_ULTRA]['EXAMPLE']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.GEMINI_1_ULTRA]['EXAMPLE'], count_all_transactions_before[ServiceType.GEMINI_1_ULTRA]['EXAMPLE'])}
    ┗ 📝 Всего: {count_all_transactions[ServiceType.GEMINI_1_ULTRA]['ALL']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.GEMINI_1_ULTRA]['ALL'], count_all_transactions_before[ServiceType.GEMINI_1_ULTRA]['ALL'])}
━ 1️⃣3️⃣ <b>Резюме:</b>
    ┣ ✅ Удачных: {all_success_requests} {calculate_percentage_difference(is_all_time, all_success_requests, all_success_requests_before)}
    ┣ ❌ С ошибкой: {all_fail_requests} {calculate_percentage_difference(is_all_time, all_fail_requests, all_fail_requests_before)}
    ┣ 🚀 Примеров: {all_example_requests} {calculate_percentage_difference(is_all_time, all_example_requests, all_example_requests_before)}
    ┗ 📝 Всего: {all_requests} {calculate_percentage_difference(is_all_time, all_requests, all_requests_before)}

🔍 Это всё, что нужно знать о текстовых моделях на данный момент 🚀
"""

    @staticmethod
    def statistics_image_models(
        period: str,
        count_all_transactions: Dict,
        count_all_transactions_before: Dict,
        count_midjourney_usage: Dict,
        count_face_swap_usage: Dict,
        count_photoshop_ai_usage: Dict,
    ):
        is_all_time = period == 'всё время'

        midjourney_info = ""
        for i, (midjourney_key, midjourney_value) in enumerate(count_midjourney_usage.items()):
            if midjourney_key != 'ALL':
                midjourney_info += f"    - <b>{midjourney_key}:</b> {midjourney_value}"
                midjourney_info += '\n' if i < len(count_midjourney_usage.items()) - 1 else ''

        face_swap_info = ""
        for i, (face_swap_key, face_swap_value) in enumerate(count_face_swap_usage.items()):
            if face_swap_key != 'ALL':
                face_swap_info += f"    - <b>{face_swap_key}:</b> {face_swap_value}"
                face_swap_info += '\n' if i < len(count_face_swap_usage.items()) - 1 else ''

        photoshop_ai_info = ""
        for i, (photoshop_ai_key, photoshop_ai_value) in enumerate(count_photoshop_ai_usage.items()):
            if photoshop_ai_key != 'ALL':
                photoshop_ai_info += f"    - <b>{photoshop_ai_key}:</b> {photoshop_ai_value}"
                photoshop_ai_info += '\n' if i < len(count_photoshop_ai_usage.items()) - 1 else ''

        all_success_requests = sum(
            [
                count_all_transactions[ServiceType.DALL_E]['SUCCESS'],
                count_all_transactions[ServiceType.MIDJOURNEY]['SUCCESS'],
                count_all_transactions[ServiceType.STABLE_DIFFUSION]['SUCCESS'],
                count_all_transactions[ServiceType.FLUX]['SUCCESS'],
                count_all_transactions[ServiceType.FACE_SWAP]['SUCCESS'],
                count_all_transactions[ServiceType.PHOTOSHOP_AI]['SUCCESS'],
            ],
        )
        all_fail_requests = sum(
            [
                count_all_transactions[ServiceType.DALL_E]['FAIL'],
                count_all_transactions[ServiceType.MIDJOURNEY]['FAIL'],
                count_all_transactions[ServiceType.STABLE_DIFFUSION]['FAIL'],
                count_all_transactions[ServiceType.FLUX]['FAIL'],
                count_all_transactions[ServiceType.FACE_SWAP]['FAIL'],
                count_all_transactions[ServiceType.PHOTOSHOP_AI]['FAIL'],
            ],
        )
        all_example_requests = sum(
            [
                count_all_transactions[ServiceType.DALL_E]['EXAMPLE'],
                count_all_transactions[ServiceType.MIDJOURNEY]['EXAMPLE'],
                count_all_transactions[ServiceType.STABLE_DIFFUSION]['EXAMPLE'],
                count_all_transactions[ServiceType.FLUX]['EXAMPLE'],
                count_all_transactions[ServiceType.FACE_SWAP]['EXAMPLE'],
                count_all_transactions[ServiceType.PHOTOSHOP_AI]['EXAMPLE'],
            ],
        )
        all_requests = sum(
            [
                count_all_transactions[ServiceType.DALL_E]['ALL'],
                count_all_transactions[ServiceType.MIDJOURNEY]['ALL'],
                count_all_transactions[ServiceType.STABLE_DIFFUSION]['ALL'],
                count_all_transactions[ServiceType.FLUX]['ALL'],
                count_all_transactions[ServiceType.FACE_SWAP]['ALL'],
                count_all_transactions[ServiceType.PHOTOSHOP_AI]['ALL'],
            ],
        )
        all_success_requests_before = sum(
            [
                count_all_transactions_before[ServiceType.DALL_E]['SUCCESS'],
                count_all_transactions_before[ServiceType.MIDJOURNEY]['SUCCESS'],
                count_all_transactions_before[ServiceType.STABLE_DIFFUSION]['SUCCESS'],
                count_all_transactions_before[ServiceType.FLUX]['SUCCESS'],
                count_all_transactions_before[ServiceType.FACE_SWAP]['SUCCESS'],
                count_all_transactions_before[ServiceType.PHOTOSHOP_AI]['SUCCESS'],
            ],
        )
        all_fail_requests_before = sum(
            [
                count_all_transactions_before[ServiceType.DALL_E]['FAIL'],
                count_all_transactions_before[ServiceType.MIDJOURNEY]['FAIL'],
                count_all_transactions_before[ServiceType.STABLE_DIFFUSION]['FAIL'],
                count_all_transactions_before[ServiceType.FLUX]['FAIL'],
                count_all_transactions_before[ServiceType.FACE_SWAP]['FAIL'],
                count_all_transactions_before[ServiceType.PHOTOSHOP_AI]['FAIL'],
            ],
        )
        all_example_requests_before = sum(
            [
                count_all_transactions_before[ServiceType.DALL_E]['EXAMPLE'],
                count_all_transactions_before[ServiceType.MIDJOURNEY]['EXAMPLE'],
                count_all_transactions_before[ServiceType.STABLE_DIFFUSION]['EXAMPLE'],
                count_all_transactions_before[ServiceType.FLUX]['EXAMPLE'],
                count_all_transactions_before[ServiceType.FACE_SWAP]['EXAMPLE'],
                count_all_transactions_before[ServiceType.PHOTOSHOP_AI]['EXAMPLE'],
            ],
        )
        all_requests_before = sum(
            [
                count_all_transactions_before[ServiceType.DALL_E]['ALL'],
                count_all_transactions_before[ServiceType.MIDJOURNEY]['ALL'],
                count_all_transactions_before[ServiceType.STABLE_DIFFUSION]['ALL'],
                count_all_transactions_before[ServiceType.FLUX]['ALL'],
                count_all_transactions_before[ServiceType.FACE_SWAP]['ALL'],
                count_all_transactions_before[ServiceType.PHOTOSHOP_AI]['ALL'],
            ],
        )

        return f"""
#statistics #image_models

📊 <b>Статистика за {period} готова!</b>

🧑‍🎨 <b>Графические модели</b>
━ 1️⃣ <b>{Texts.DALL_E}:</b>
    ┣ ✅ Удачных: {count_all_transactions[ServiceType.DALL_E]['SUCCESS']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.DALL_E]['SUCCESS'], count_all_transactions_before[ServiceType.DALL_E]['SUCCESS'])}
    ┣ ❌ С ошибкой: {count_all_transactions[ServiceType.DALL_E]['FAIL']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.DALL_E]['FAIL'], count_all_transactions_before[ServiceType.DALL_E]['FAIL'])}
    ┣ 🚀 Примеров: {count_all_transactions[ServiceType.DALL_E]['EXAMPLE']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.DALL_E]['EXAMPLE'], count_all_transactions_before[ServiceType.DALL_E]['EXAMPLE'])}
    ┗ 📝 Всего: {count_all_transactions[ServiceType.DALL_E]['ALL']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.DALL_E]['ALL'], count_all_transactions_before[ServiceType.DALL_E]['ALL'])}
━ 2️⃣ <b>{Texts.MIDJOURNEY}:</b>
    ┣ ✅ Удачных: {count_all_transactions[ServiceType.MIDJOURNEY]['SUCCESS']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.MIDJOURNEY]['SUCCESS'], count_all_transactions_before[ServiceType.MIDJOURNEY]['SUCCESS'])}
    ┣ ❌ С ошибкой: {count_all_transactions[ServiceType.MIDJOURNEY]['FAIL']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.MIDJOURNEY]['FAIL'], count_all_transactions_before[ServiceType.MIDJOURNEY]['FAIL'])}
    ┣ 🚀 Примеров: {count_all_transactions[ServiceType.MIDJOURNEY]['EXAMPLE']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.MIDJOURNEY]['EXAMPLE'], count_all_transactions_before[ServiceType.MIDJOURNEY]['EXAMPLE'])}
    ┗ 📝 Всего: {count_all_transactions[ServiceType.MIDJOURNEY]['ALL']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.MIDJOURNEY]['ALL'], count_all_transactions_before[ServiceType.MIDJOURNEY]['ALL'])}

    <b>Генерации:</b>
{midjourney_info}
━ 3️⃣ <b>{Texts.STABLE_DIFFUSION}:</b>
    ┣ ✅ Удачных: {count_all_transactions[ServiceType.STABLE_DIFFUSION]['SUCCESS']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.STABLE_DIFFUSION]['SUCCESS'], count_all_transactions_before[ServiceType.STABLE_DIFFUSION]['SUCCESS'])}
    ┣ ❌ С ошибкой: {count_all_transactions[ServiceType.STABLE_DIFFUSION]['FAIL']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.STABLE_DIFFUSION]['FAIL'], count_all_transactions_before[ServiceType.STABLE_DIFFUSION]['FAIL'])}
    ┣ 🚀 Примеров: {count_all_transactions[ServiceType.STABLE_DIFFUSION]['EXAMPLE']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.STABLE_DIFFUSION]['EXAMPLE'], count_all_transactions_before[ServiceType.STABLE_DIFFUSION]['EXAMPLE'])}
    ┗ 📝 Всего: {count_all_transactions[ServiceType.STABLE_DIFFUSION]['ALL']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.STABLE_DIFFUSION]['ALL'], count_all_transactions_before[ServiceType.STABLE_DIFFUSION]['ALL'])}
━ 4️⃣ <b>{Texts.FLUX}:</b>
    ┣ ✅ Удачных: {count_all_transactions[ServiceType.FLUX]['SUCCESS']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.FLUX]['SUCCESS'], count_all_transactions_before[ServiceType.FLUX]['SUCCESS'])}
    ┣ ❌ С ошибкой: {count_all_transactions[ServiceType.FLUX]['FAIL']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.FLUX]['FAIL'], count_all_transactions_before[ServiceType.FLUX]['FAIL'])}
    ┣ 🚀 Примеров: {count_all_transactions[ServiceType.FLUX]['EXAMPLE']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.FLUX]['EXAMPLE'], count_all_transactions_before[ServiceType.FLUX]['EXAMPLE'])}
    ┗ 📝 Всего: {count_all_transactions[ServiceType.FLUX]['ALL']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.FLUX]['ALL'], count_all_transactions_before[ServiceType.FLUX]['ALL'])}
━ 5️⃣ <b>{Texts.FACE_SWAP}:</b>
    ┣ ✅ Удачных: {count_all_transactions[ServiceType.FACE_SWAP]['SUCCESS']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.FACE_SWAP]['SUCCESS'], count_all_transactions_before[ServiceType.FACE_SWAP]['SUCCESS'])}
    ┣ ❌ С ошибкой: {count_all_transactions[ServiceType.FACE_SWAP]['FAIL']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.FACE_SWAP]['FAIL'], count_all_transactions_before[ServiceType.FACE_SWAP]['FAIL'])}
    ┣ 🚀 Примеров: {count_all_transactions[ServiceType.FACE_SWAP]['EXAMPLE']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.FACE_SWAP]['EXAMPLE'], count_all_transactions_before[ServiceType.FACE_SWAP]['EXAMPLE'])}
    ┗ 📝 Всего: {count_all_transactions[ServiceType.FACE_SWAP]['ALL']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.FACE_SWAP]['ALL'], count_all_transactions_before[ServiceType.FACE_SWAP]['ALL'])}
━ 6️⃣ <b>{Texts.PHOTOSHOP_AI}:</b>
    ┣ ✅ Удачных: {count_all_transactions[ServiceType.PHOTOSHOP_AI]['SUCCESS']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.PHOTOSHOP_AI]['SUCCESS'], count_all_transactions_before[ServiceType.PHOTOSHOP_AI]['SUCCESS'])}
    ┣ ❌ С ошибкой: {count_all_transactions[ServiceType.PHOTOSHOP_AI]['FAIL']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.PHOTOSHOP_AI]['FAIL'], count_all_transactions_before[ServiceType.PHOTOSHOP_AI]['FAIL'])}
    ┣ 🚀 Примеров: {count_all_transactions[ServiceType.PHOTOSHOP_AI]['EXAMPLE']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.PHOTOSHOP_AI]['EXAMPLE'], count_all_transactions_before[ServiceType.PHOTOSHOP_AI]['EXAMPLE'])}
    ┗ 📝 Всего: {count_all_transactions[ServiceType.PHOTOSHOP_AI]['ALL']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.PHOTOSHOP_AI]['ALL'], count_all_transactions_before[ServiceType.PHOTOSHOP_AI]['ALL'])}

    <b>Генерации:</b>
{photoshop_ai_info}
━ 7️⃣ <b>Резюме:</b>
    ┣ ✅ Удачных: {all_success_requests} {calculate_percentage_difference(is_all_time, all_success_requests, all_success_requests_before)}
    ┣ ❌ С ошибкой: {all_fail_requests} {calculate_percentage_difference(is_all_time, all_fail_requests, all_fail_requests_before)}
    ┣ 🚀 Примеров: {all_example_requests} {calculate_percentage_difference(is_all_time, all_example_requests, all_example_requests_before)}
    ┗ 📝 Всего: {all_requests} {calculate_percentage_difference(is_all_time, all_requests, all_requests_before)}

🔍 Это всё, что нужно знать о графических моделях на данный момент 🚀
"""

    @staticmethod
    def statistics_music_models(
        period: str,
        count_all_transactions: Dict,
        count_all_transactions_before: Dict,
        count_suno_usage: Dict,
    ):
        is_all_time = period == 'всё время'

        suno_info = ""
        for i, (suno_key, suno_value) in enumerate(count_suno_usage.items()):
            if suno_key != 'ALL':
                suno_info += f"    - <b>{suno_key}:</b> {suno_value}"
                suno_info += '\n' if i < len(count_suno_usage.items()) - 1 else ''

        all_success_requests = sum(
            [
                count_all_transactions[ServiceType.MUSIC_GEN]['SUCCESS'],
                count_all_transactions[ServiceType.SUNO]['SUCCESS'],
            ],
        )
        all_fail_requests = sum(
            [
                count_all_transactions[ServiceType.MUSIC_GEN]['FAIL'],
                count_all_transactions[ServiceType.SUNO]['FAIL'],
            ],
        )
        all_example_requests = sum(
            [
                count_all_transactions[ServiceType.MUSIC_GEN]['EXAMPLE'],
                count_all_transactions[ServiceType.SUNO]['EXAMPLE'],
            ],
        )
        all_requests = sum(
            [
                count_all_transactions[ServiceType.MUSIC_GEN]['ALL'],
                count_all_transactions[ServiceType.SUNO]['ALL'],
            ],
        )
        all_success_requests_before = sum(
            [
                count_all_transactions_before[ServiceType.MUSIC_GEN]['SUCCESS'],
                count_all_transactions_before[ServiceType.SUNO]['SUCCESS'],
            ],
        )
        all_fail_requests_before = sum(
            [
                count_all_transactions_before[ServiceType.MUSIC_GEN]['FAIL'],
                count_all_transactions_before[ServiceType.SUNO]['FAIL'],
            ],
        )
        all_example_requests_before = sum(
            [
                count_all_transactions_before[ServiceType.MUSIC_GEN]['EXAMPLE'],
                count_all_transactions_before[ServiceType.SUNO]['EXAMPLE'],
            ],
        )
        all_requests_before = sum(
            [
                count_all_transactions_before[ServiceType.MUSIC_GEN]['ALL'],
                count_all_transactions_before[ServiceType.SUNO]['ALL'],
            ],
        )

        return f"""
#statistics #music_models

📊 <b>Статистика за {period} готова!</b>

🎺 <b>Музыкальные модели</b>
━ 1️⃣ <b>{Texts.MUSIC_GEN}:</b>
    ┣ ✅ Удачных: {count_all_transactions[ServiceType.MUSIC_GEN]['SUCCESS']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.MUSIC_GEN]['SUCCESS'], count_all_transactions_before[ServiceType.MUSIC_GEN]['SUCCESS'])}
    ┣ ❌ С ошибкой: {count_all_transactions[ServiceType.MUSIC_GEN]['FAIL']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.MUSIC_GEN]['FAIL'], count_all_transactions_before[ServiceType.MUSIC_GEN]['FAIL'])}
    ┣ 🚀 Примеров: {count_all_transactions[ServiceType.MUSIC_GEN]['EXAMPLE']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.MUSIC_GEN]['EXAMPLE'], count_all_transactions_before[ServiceType.MUSIC_GEN]['EXAMPLE'])}
    ┗ 📝 Всего: {count_all_transactions[ServiceType.MUSIC_GEN]['ALL']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.MUSIC_GEN]['ALL'], count_all_transactions_before[ServiceType.MUSIC_GEN]['ALL'])}
━ 2️⃣ <b>{Texts.SUNO}:</b>
    ┣ ✅ Удачных: {count_all_transactions[ServiceType.SUNO]['SUCCESS']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.SUNO]['SUCCESS'], count_all_transactions_before[ServiceType.SUNO]['SUCCESS'])}
    ┣ ❌ С ошибкой: {count_all_transactions[ServiceType.SUNO]['FAIL']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.SUNO]['FAIL'], count_all_transactions_before[ServiceType.SUNO]['FAIL'])}
    ┣ 🚀 Примеров: {count_all_transactions[ServiceType.SUNO]['EXAMPLE']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.SUNO]['EXAMPLE'], count_all_transactions_before[ServiceType.SUNO]['EXAMPLE'])}
    ┗ 📝 Всего: {count_all_transactions[ServiceType.SUNO]['ALL']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.SUNO]['ALL'], count_all_transactions_before[ServiceType.SUNO]['ALL'])}

<b>Генерации:</b>
{suno_info}
━ 3️⃣ <b>Резюме:</b>
    ┣ ✅ Удачных: {all_success_requests} {calculate_percentage_difference(is_all_time, all_success_requests, all_success_requests_before)}
    ┣ ❌ С ошибкой: {all_fail_requests} {calculate_percentage_difference(is_all_time, all_fail_requests, all_fail_requests_before)}
    ┣ 🚀 Примеров: {all_example_requests} {calculate_percentage_difference(is_all_time, all_example_requests, all_example_requests_before)}
    ┗ 📝 Всего: {all_requests} {calculate_percentage_difference(is_all_time, all_requests, all_requests_before)}

🔍 Это всё, что нужно знать о музыкальных моделях на данный момент 🚀
"""

    @staticmethod
    def statistics_reactions(
        period: str,
        count_reactions: Dict,
        count_reactions_before: Dict,
        count_feedbacks: Dict,
        count_feedbacks_before: Dict,
        count_games: Dict,
        count_games_before: Dict,
    ):
        is_all_time = period == 'всё время'

        all_liked = sum(
            [
                count_reactions[ServiceType.MIDJOURNEY][GenerationReaction.LIKED],
                count_reactions[ServiceType.STABLE_DIFFUSION][GenerationReaction.LIKED],
                count_reactions[ServiceType.FLUX][GenerationReaction.LIKED],
                count_reactions[ServiceType.FACE_SWAP][GenerationReaction.LIKED],
                count_reactions[ServiceType.PHOTOSHOP_AI][GenerationReaction.LIKED],
                count_reactions[ServiceType.MUSIC_GEN][GenerationReaction.LIKED],
                count_reactions[ServiceType.SUNO][GenerationReaction.LIKED],
            ]
        )
        all_disliked = sum(
            [
                count_reactions[ServiceType.MIDJOURNEY][GenerationReaction.DISLIKED],
                count_reactions[ServiceType.STABLE_DIFFUSION][GenerationReaction.DISLIKED],
                count_reactions[ServiceType.FLUX][GenerationReaction.DISLIKED],
                count_reactions[ServiceType.FACE_SWAP][GenerationReaction.DISLIKED],
                count_reactions[ServiceType.PHOTOSHOP_AI][GenerationReaction.DISLIKED],
                count_reactions[ServiceType.MUSIC_GEN][GenerationReaction.DISLIKED],
                count_reactions[ServiceType.SUNO][GenerationReaction.DISLIKED],
            ]
        )
        all_none = sum(
            [
                count_reactions[ServiceType.MIDJOURNEY][GenerationReaction.NONE],
                count_reactions[ServiceType.STABLE_DIFFUSION][GenerationReaction.NONE],
                count_reactions[ServiceType.FLUX][GenerationReaction.NONE],
                count_reactions[ServiceType.FACE_SWAP][GenerationReaction.NONE],
                count_reactions[ServiceType.PHOTOSHOP_AI][GenerationReaction.NONE],
                count_reactions[ServiceType.MUSIC_GEN][GenerationReaction.NONE],
                count_reactions[ServiceType.SUNO][GenerationReaction.NONE],
            ]
        )

        all_liked_before = sum(
            [
                count_reactions_before[ServiceType.MIDJOURNEY][GenerationReaction.LIKED],
                count_reactions_before[ServiceType.STABLE_DIFFUSION][GenerationReaction.LIKED],
                count_reactions_before[ServiceType.FLUX][GenerationReaction.LIKED],
                count_reactions_before[ServiceType.FACE_SWAP][GenerationReaction.LIKED],
                count_reactions_before[ServiceType.PHOTOSHOP_AI][GenerationReaction.LIKED],
                count_reactions_before[ServiceType.MUSIC_GEN][GenerationReaction.LIKED],
                count_reactions_before[ServiceType.SUNO][GenerationReaction.LIKED],
            ]
        )
        all_disliked_before = sum(
            [
                count_reactions_before[ServiceType.MIDJOURNEY][GenerationReaction.DISLIKED],
                count_reactions_before[ServiceType.STABLE_DIFFUSION][GenerationReaction.DISLIKED],
                count_reactions_before[ServiceType.FLUX][GenerationReaction.DISLIKED],
                count_reactions_before[ServiceType.FACE_SWAP][GenerationReaction.DISLIKED],
                count_reactions_before[ServiceType.PHOTOSHOP_AI][GenerationReaction.DISLIKED],
                count_reactions_before[ServiceType.MUSIC_GEN][GenerationReaction.DISLIKED],
                count_reactions_before[ServiceType.SUNO][GenerationReaction.DISLIKED],
            ]
        )
        all_none_before = sum(
            [
                count_reactions_before[ServiceType.MIDJOURNEY][GenerationReaction.NONE],
                count_reactions_before[ServiceType.STABLE_DIFFUSION][GenerationReaction.NONE],
                count_reactions_before[ServiceType.FLUX][GenerationReaction.NONE],
                count_reactions_before[ServiceType.FACE_SWAP][GenerationReaction.NONE],
                count_reactions_before[ServiceType.PHOTOSHOP_AI][GenerationReaction.NONE],
                count_reactions_before[ServiceType.MUSIC_GEN][GenerationReaction.NONE],
                count_reactions_before[ServiceType.SUNO][GenerationReaction.NONE],
            ]
        )

        all_feedbacks = sum(
            [
                count_feedbacks[FeedbackStatus.APPROVED],
                count_feedbacks[FeedbackStatus.DENIED],
                count_feedbacks[FeedbackStatus.WAITING],
            ]
        )
        all_feedbacks_before = sum(
            [
                count_feedbacks_before[FeedbackStatus.APPROVED],
                count_feedbacks_before[FeedbackStatus.DENIED],
                count_feedbacks_before[FeedbackStatus.WAITING],
            ]
        )

        all_games = sum(
            [
                count_games[GameType.BOWLING],
                count_games[GameType.SOCCER],
                count_games[GameType.BASKETBALL],
                count_games[GameType.DARTS],
                count_games[GameType.DICE],
                count_games[GameType.CASINO],
            ]
        )
        all_games_before = sum(
            [
                count_games_before[GameType.BOWLING],
                count_games_before[GameType.SOCCER],
                count_games_before[GameType.BASKETBALL],
                count_games_before[GameType.DARTS],
                count_games_before[GameType.DICE],
                count_games_before[GameType.CASINO],
            ]
        )

        return f"""
#statistics #reactions

📊 <b>Статистика за {period} готова!</b>

🧐 <b>Реакции</b>
━ 1️⃣ <b>{Texts.MIDJOURNEY}:</b>
    ┣ 👍 {count_reactions[ServiceType.MIDJOURNEY][GenerationReaction.LIKED]} {calculate_percentage_difference(is_all_time, count_reactions[ServiceType.MIDJOURNEY][GenerationReaction.LIKED], count_reactions_before[ServiceType.MIDJOURNEY][GenerationReaction.LIKED])}
    ┣ 👎 {count_reactions[ServiceType.MIDJOURNEY][GenerationReaction.DISLIKED]} {calculate_percentage_difference(is_all_time, count_reactions[ServiceType.MIDJOURNEY][GenerationReaction.DISLIKED], count_reactions_before[ServiceType.MIDJOURNEY][GenerationReaction.DISLIKED])}
    ┗ 🤷 {count_reactions[ServiceType.MIDJOURNEY][GenerationReaction.NONE]} {calculate_percentage_difference(is_all_time, count_reactions[ServiceType.MIDJOURNEY][GenerationReaction.NONE], count_reactions_before[ServiceType.MIDJOURNEY][GenerationReaction.NONE])}
━ 2️⃣ <b>{Texts.STABLE_DIFFUSION}:</b>
    ┣ 👍 {count_reactions[ServiceType.STABLE_DIFFUSION][GenerationReaction.LIKED]} {calculate_percentage_difference(is_all_time, count_reactions[ServiceType.STABLE_DIFFUSION][GenerationReaction.LIKED], count_reactions_before[ServiceType.STABLE_DIFFUSION][GenerationReaction.LIKED])}
    ┣ 👎 {count_reactions[ServiceType.STABLE_DIFFUSION][GenerationReaction.DISLIKED]} {calculate_percentage_difference(is_all_time, count_reactions[ServiceType.STABLE_DIFFUSION][GenerationReaction.DISLIKED], count_reactions_before[ServiceType.STABLE_DIFFUSION][GenerationReaction.DISLIKED])}
    ┗ 🤷 {count_reactions[ServiceType.STABLE_DIFFUSION][GenerationReaction.NONE]} {calculate_percentage_difference(is_all_time, count_reactions[ServiceType.STABLE_DIFFUSION][GenerationReaction.NONE], count_reactions_before[ServiceType.STABLE_DIFFUSION][GenerationReaction.NONE])}
━ 3️⃣ <b>{Texts.FLUX}:</b>
    ┣ 👍 {count_reactions[ServiceType.FLUX][GenerationReaction.LIKED]} {calculate_percentage_difference(is_all_time, count_reactions[ServiceType.FLUX][GenerationReaction.LIKED], count_reactions_before[ServiceType.FLUX][GenerationReaction.LIKED])}
    ┣ 👎 {count_reactions[ServiceType.FLUX][GenerationReaction.DISLIKED]} {calculate_percentage_difference(is_all_time, count_reactions[ServiceType.FLUX][GenerationReaction.DISLIKED], count_reactions_before[ServiceType.FLUX][GenerationReaction.DISLIKED])}
    ┗ 🤷 {count_reactions[ServiceType.FLUX][GenerationReaction.NONE]} {calculate_percentage_difference(is_all_time, count_reactions[ServiceType.FLUX][GenerationReaction.NONE], count_reactions_before[ServiceType.FLUX][GenerationReaction.NONE])}
━ 4️⃣ <b>{Texts.FACE_SWAP}:</b>
    ┣ 👍 {count_reactions[ServiceType.FACE_SWAP][GenerationReaction.LIKED]} {calculate_percentage_difference(is_all_time, count_reactions[ServiceType.FACE_SWAP][GenerationReaction.LIKED], count_reactions_before[ServiceType.FACE_SWAP][GenerationReaction.LIKED])}
    ┣ 👎 {count_reactions[ServiceType.FACE_SWAP][GenerationReaction.DISLIKED]} {calculate_percentage_difference(is_all_time, count_reactions[ServiceType.FACE_SWAP][GenerationReaction.DISLIKED], count_reactions_before[ServiceType.FACE_SWAP][GenerationReaction.DISLIKED])}
    ┗ 🤷 {count_reactions[ServiceType.FACE_SWAP][GenerationReaction.NONE]} {calculate_percentage_difference(is_all_time, count_reactions[ServiceType.FACE_SWAP][GenerationReaction.NONE], count_reactions_before[ServiceType.FACE_SWAP][GenerationReaction.NONE])}
━ 5️⃣ <b>{Texts.PHOTOSHOP_AI}:</b>
    ┣ 👍 {count_reactions[ServiceType.PHOTOSHOP_AI][GenerationReaction.LIKED]} {calculate_percentage_difference(is_all_time, count_reactions[ServiceType.PHOTOSHOP_AI][GenerationReaction.LIKED], count_reactions_before[ServiceType.PHOTOSHOP_AI][GenerationReaction.LIKED])}
    ┣ 👎 {count_reactions[ServiceType.PHOTOSHOP_AI][GenerationReaction.DISLIKED]} {calculate_percentage_difference(is_all_time, count_reactions[ServiceType.PHOTOSHOP_AI][GenerationReaction.DISLIKED], count_reactions_before[ServiceType.PHOTOSHOP_AI][GenerationReaction.DISLIKED])}
    ┗ 🤷 {count_reactions[ServiceType.PHOTOSHOP_AI][GenerationReaction.NONE]} {calculate_percentage_difference(is_all_time, count_reactions[ServiceType.PHOTOSHOP_AI][GenerationReaction.NONE], count_reactions_before[ServiceType.PHOTOSHOP_AI][GenerationReaction.NONE])}
━ 6️⃣ <b>{Texts.MUSIC_GEN}:</b>
    ┣ 👍 {count_reactions[ServiceType.MUSIC_GEN][GenerationReaction.LIKED]} {calculate_percentage_difference(is_all_time, count_reactions[ServiceType.MUSIC_GEN][GenerationReaction.LIKED], count_reactions_before[ServiceType.MUSIC_GEN][GenerationReaction.LIKED])}
    ┣ 👎 {count_reactions[ServiceType.MUSIC_GEN][GenerationReaction.DISLIKED]} {calculate_percentage_difference(is_all_time, count_reactions[ServiceType.MUSIC_GEN][GenerationReaction.DISLIKED], count_reactions_before[ServiceType.MUSIC_GEN][GenerationReaction.DISLIKED])}
    ┗ 🤷 {count_reactions[ServiceType.MUSIC_GEN][GenerationReaction.NONE]} {calculate_percentage_difference(is_all_time, count_reactions[ServiceType.MUSIC_GEN][GenerationReaction.NONE], count_reactions_before[ServiceType.MUSIC_GEN][GenerationReaction.NONE])}
━ 7️⃣ <b>{Texts.SUNO}:</b>
    ┣ 👍 {count_reactions[ServiceType.SUNO][GenerationReaction.LIKED]} {calculate_percentage_difference(is_all_time, count_reactions[ServiceType.SUNO][GenerationReaction.LIKED], count_reactions_before[ServiceType.SUNO][GenerationReaction.LIKED])}
    ┣ 👎 {count_reactions[ServiceType.SUNO][GenerationReaction.DISLIKED]} {calculate_percentage_difference(is_all_time, count_reactions[ServiceType.SUNO][GenerationReaction.DISLIKED], count_reactions_before[ServiceType.SUNO][GenerationReaction.DISLIKED])}
    ┗ 🤷 {count_reactions[ServiceType.SUNO][GenerationReaction.NONE]} {calculate_percentage_difference(is_all_time, count_reactions[ServiceType.SUNO][GenerationReaction.NONE], count_reactions_before[ServiceType.SUNO][GenerationReaction.NONE])}
━ 8️⃣ <b>Резюме:</b>
    ┣ 👍 {all_liked} {calculate_percentage_difference(is_all_time, all_liked, all_liked_before)}
    ┣ 👎 {all_disliked} {calculate_percentage_difference(is_all_time, all_disliked, all_disliked_before)}
    ┗ 🤷 {all_none} {calculate_percentage_difference(is_all_time, all_none, all_none_before)}

📡 <b>Обратная связь:</b>
━ 1️⃣ <b>Одобрено:</b> {count_feedbacks[FeedbackStatus.APPROVED]} {calculate_percentage_difference(is_all_time, count_feedbacks[FeedbackStatus.APPROVED], count_feedbacks_before[FeedbackStatus.APPROVED])}
━ 2️⃣ <b>Отклонено:</b> {count_feedbacks[FeedbackStatus.DENIED]} {calculate_percentage_difference(is_all_time, count_feedbacks[FeedbackStatus.DENIED], count_feedbacks_before[FeedbackStatus.DENIED])}
━ 3️⃣ <b>В ожидании:</b> {count_feedbacks[FeedbackStatus.WAITING]} {calculate_percentage_difference(is_all_time, count_feedbacks[FeedbackStatus.WAITING], count_feedbacks_before[FeedbackStatus.WAITING])}
━ 4️⃣ <b>Всего:</b> {all_feedbacks} {calculate_percentage_difference(is_all_time, all_feedbacks, all_feedbacks_before)}

🎮 <b>Игр сыграно:</b>
━ 🎳 <b>Боулинг:</b> {count_games[GameType.BOWLING]} {calculate_percentage_difference(is_all_time, count_games[GameType.BOWLING], count_games_before[GameType.BOWLING])}
━ ⚽️ <b>Футбол:</b> {count_games[GameType.SOCCER]} {calculate_percentage_difference(is_all_time, count_games[GameType.SOCCER], count_games_before[GameType.SOCCER])}
━ 🏀 <b>Баскетбол:</b> {count_games[GameType.BASKETBALL]} {calculate_percentage_difference(is_all_time, count_games[GameType.BASKETBALL], count_games_before[GameType.BASKETBALL])}
━ 🎯 <b>Дартс:</b> {count_games[GameType.DARTS]} {calculate_percentage_difference(is_all_time, count_games[GameType.DARTS], count_games_before[GameType.DARTS])}
━ 🎲 <b>Кубик:</b> {count_games[GameType.DICE]} {calculate_percentage_difference(is_all_time, count_games[GameType.DICE], count_games_before[GameType.DICE])}
━ 🎰 <b>Казино:</b> {count_games[GameType.CASINO]} {calculate_percentage_difference(is_all_time, count_games[GameType.CASINO], count_games_before[GameType.CASINO])}
━ 🕹 <b>Всего:</b> {all_games} {calculate_percentage_difference(is_all_time, all_games, all_games_before)}

🔍 Это всё, что нужно знать о реакциях и обратной связи на данный момент 🚀
"""

    @staticmethod
    def statistics_bonuses(
        period: str,
        count_credits: Dict,
        count_credits_before: Dict,
        count_all_transactions: Dict,
        count_all_transactions_before: Dict,
        count_activated_promo_codes: int,
        count_activated_promo_codes_before: int,
    ):
        is_all_time = period == 'всё время'

        all_bonuses = sum(
            [
                count_all_transactions[ServiceType.CHAT_GPT3_TURBO]['BONUS'],
                count_all_transactions[ServiceType.CHAT_GPT4_TURBO]['BONUS'],
                count_all_transactions[ServiceType.CHAT_GPT4_OMNI_MINI]['BONUS'],
                count_all_transactions[ServiceType.CHAT_GPT4_OMNI]['BONUS'],
                count_all_transactions[ServiceType.CHAT_GPT_O_1_MINI]['BONUS'],
                count_all_transactions[ServiceType.CHAT_GPT_O_1_PREVIEW]['BONUS'],
                count_all_transactions[ServiceType.CLAUDE_3_HAIKU]['BONUS'],
                count_all_transactions[ServiceType.CLAUDE_3_SONNET]['BONUS'],
                count_all_transactions[ServiceType.CLAUDE_3_OPUS]['BONUS'],
                count_all_transactions[ServiceType.GEMINI_1_FLASH]['BONUS'],
                count_all_transactions[ServiceType.GEMINI_1_PRO]['BONUS'],
                count_all_transactions[ServiceType.GEMINI_1_ULTRA]['BONUS'],
                count_all_transactions[ServiceType.DALL_E]['BONUS'],
                count_all_transactions[ServiceType.MIDJOURNEY]['BONUS'],
                count_all_transactions[ServiceType.STABLE_DIFFUSION]['BONUS'],
                count_all_transactions[ServiceType.FLUX]['BONUS'],
                count_all_transactions[ServiceType.FACE_SWAP]['BONUS'],
                count_all_transactions[ServiceType.PHOTOSHOP_AI]['BONUS'],
                count_all_transactions[ServiceType.MUSIC_GEN]['BONUS'],
                count_all_transactions[ServiceType.SUNO]['BONUS'],
                count_all_transactions[ServiceType.ADDITIONAL_CHATS]['BONUS'],
                count_all_transactions[ServiceType.ACCESS_TO_CATALOG]['BONUS'],
                count_all_transactions[ServiceType.VOICE_MESSAGES]['BONUS'],
                count_all_transactions[ServiceType.FAST_MESSAGES]['BONUS'],
            ]
        )
        all_bonuses_before = sum(
            [
                count_all_transactions_before[ServiceType.CHAT_GPT3_TURBO]['BONUS'],
                count_all_transactions_before[ServiceType.CHAT_GPT4_TURBO]['BONUS'],
                count_all_transactions_before[ServiceType.CHAT_GPT4_OMNI_MINI]['BONUS'],
                count_all_transactions_before[ServiceType.CHAT_GPT4_OMNI]['BONUS'],
                count_all_transactions_before[ServiceType.CHAT_GPT_O_1_MINI]['BONUS'],
                count_all_transactions_before[ServiceType.CHAT_GPT_O_1_PREVIEW]['BONUS'],
                count_all_transactions_before[ServiceType.CLAUDE_3_HAIKU]['BONUS'],
                count_all_transactions_before[ServiceType.CLAUDE_3_SONNET]['BONUS'],
                count_all_transactions_before[ServiceType.CLAUDE_3_OPUS]['BONUS'],
                count_all_transactions_before[ServiceType.GEMINI_1_FLASH]['BONUS'],
                count_all_transactions_before[ServiceType.GEMINI_1_PRO]['BONUS'],
                count_all_transactions_before[ServiceType.GEMINI_1_ULTRA]['BONUS'],
                count_all_transactions_before[ServiceType.DALL_E]['BONUS'],
                count_all_transactions_before[ServiceType.MIDJOURNEY]['BONUS'],
                count_all_transactions_before[ServiceType.STABLE_DIFFUSION]['BONUS'],
                count_all_transactions_before[ServiceType.FLUX]['BONUS'],
                count_all_transactions_before[ServiceType.FACE_SWAP]['BONUS'],
                count_all_transactions_before[ServiceType.PHOTOSHOP_AI]['BONUS'],
                count_all_transactions_before[ServiceType.MUSIC_GEN]['BONUS'],
                count_all_transactions_before[ServiceType.SUNO]['BONUS'],
                count_all_transactions_before[ServiceType.ADDITIONAL_CHATS]['BONUS'],
                count_all_transactions_before[ServiceType.ACCESS_TO_CATALOG]['BONUS'],
                count_all_transactions_before[ServiceType.VOICE_MESSAGES]['BONUS'],
                count_all_transactions_before[ServiceType.FAST_MESSAGES]['BONUS'],
            ]
        )

        return f"""
#statistics #bonuses

📊 <b>Статистика за {period} готова!</b>

🎁 <b>Бонусы</b>
━ 1️⃣ <b>Кредитов приобретено:</b>
    ┣ 👤 За приглашения друзей: {count_credits['INVITE_FRIENDS']} {calculate_percentage_difference(is_all_time, count_credits['INVITE_FRIENDS'], count_credits_before['INVITE_FRIENDS'])}
    ┣ 📡 За обратную связь: {count_credits['LEAVE_FEEDBACKS']} {calculate_percentage_difference(is_all_time, count_credits['LEAVE_FEEDBACKS'], count_credits_before['LEAVE_FEEDBACKS'])}
    ┣ 🎮 За игры: {count_credits['PLAY_GAMES']} {calculate_percentage_difference(is_all_time, count_credits['PLAY_GAMES'], count_credits_before['PLAY_GAMES'])}
    ┗ 🪙 Всего: {count_credits['ALL']} {calculate_percentage_difference(is_all_time, count_credits['ALL'], count_credits_before['ALL'])}
━ 2️⃣ <b>Кредитов потрачено на:</b>
    ┣ {Texts.CHATGPT3_TURBO}: {count_all_transactions[ServiceType.CHAT_GPT3_TURBO]['BONUS']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.CHAT_GPT3_TURBO]['BONUS'], count_all_transactions_before[ServiceType.CHAT_GPT3_TURBO]['BONUS'])}
    ┣ {Texts.CHATGPT4_TURBO}: {count_all_transactions[ServiceType.CHAT_GPT4_TURBO]['BONUS']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.CHAT_GPT4_TURBO]['BONUS'], count_all_transactions_before[ServiceType.CHAT_GPT4_TURBO]['BONUS'])}
    ┣ {Texts.CHATGPT4_OMNI_MINI}: {count_all_transactions[ServiceType.CHAT_GPT4_OMNI_MINI]['BONUS']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.CHAT_GPT4_OMNI_MINI]['BONUS'], count_all_transactions_before[ServiceType.CHAT_GPT4_OMNI_MINI]['BONUS'])}
    ┣ {Texts.CHATGPT4_OMNI}: {count_all_transactions[ServiceType.CHAT_GPT4_OMNI]['BONUS']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.CHAT_GPT4_OMNI]['BONUS'], count_all_transactions_before[ServiceType.CHAT_GPT4_OMNI]['BONUS'])}
    ┣ {Texts.CHAT_GPT_O_1_MINI}: {count_all_transactions[ServiceType.CHAT_GPT_O_1_MINI]['BONUS']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.CHAT_GPT_O_1_MINI]['BONUS'], count_all_transactions_before[ServiceType.CHAT_GPT_O_1_MINI]['BONUS'])}
    ┣ {Texts.CHAT_GPT_O_1_PREVIEW}: {count_all_transactions[ServiceType.CHAT_GPT_O_1_PREVIEW]['BONUS']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.CHAT_GPT_O_1_PREVIEW]['BONUS'], count_all_transactions_before[ServiceType.CHAT_GPT_O_1_PREVIEW]['BONUS'])}
    ┣ {Texts.CLAUDE_3_HAIKU}: {count_all_transactions[ServiceType.CLAUDE_3_HAIKU]['BONUS']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.CLAUDE_3_HAIKU]['BONUS'], count_all_transactions_before[ServiceType.CLAUDE_3_HAIKU]['BONUS'])}
    ┣ {Texts.CLAUDE_3_SONNET}: {count_all_transactions[ServiceType.CLAUDE_3_SONNET]['BONUS']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.CLAUDE_3_SONNET]['BONUS'], count_all_transactions_before[ServiceType.CLAUDE_3_SONNET]['BONUS'])}
    ┣ {Texts.CLAUDE_3_OPUS}: {count_all_transactions[ServiceType.CLAUDE_3_OPUS]['BONUS']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.CLAUDE_3_OPUS]['BONUS'], count_all_transactions_before[ServiceType.CLAUDE_3_OPUS]['BONUS'])}
    ┣ {Texts.GEMINI_1_FLASH}: {count_all_transactions[ServiceType.GEMINI_1_FLASH]['BONUS']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.GEMINI_1_FLASH]['BONUS'], count_all_transactions_before[ServiceType.GEMINI_1_FLASH]['BONUS'])}
    ┣ {Texts.GEMINI_1_PRO}: {count_all_transactions[ServiceType.GEMINI_1_PRO]['BONUS']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.GEMINI_1_PRO]['BONUS'], count_all_transactions_before[ServiceType.GEMINI_1_PRO]['BONUS'])}
    ┣ {Texts.GEMINI_1_ULTRA}: {count_all_transactions[ServiceType.GEMINI_1_ULTRA]['BONUS']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.GEMINI_1_ULTRA]['BONUS'], count_all_transactions_before[ServiceType.GEMINI_1_ULTRA]['BONUS'])}
    ┣ {Texts.DALL_E}: {count_all_transactions[ServiceType.DALL_E]['BONUS']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.DALL_E]['BONUS'], count_all_transactions_before[ServiceType.DALL_E]['BONUS'])}
    ┣ {Texts.MIDJOURNEY}: {count_all_transactions[ServiceType.MIDJOURNEY]['BONUS']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.MIDJOURNEY]['BONUS'], count_all_transactions_before[ServiceType.MIDJOURNEY]['BONUS'])}
    ┣ {Texts.STABLE_DIFFUSION}: {count_all_transactions[ServiceType.STABLE_DIFFUSION]['BONUS']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.STABLE_DIFFUSION]['BONUS'], count_all_transactions_before[ServiceType.STABLE_DIFFUSION]['BONUS'])}
    ┣ {Texts.FLUX}: {count_all_transactions[ServiceType.FLUX]['BONUS']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.FLUX]['BONUS'], count_all_transactions_before[ServiceType.FLUX]['BONUS'])}
    ┣ {Texts.FACE_SWAP}: {count_all_transactions[ServiceType.FACE_SWAP]['BONUS']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.FACE_SWAP]['BONUS'], count_all_transactions_before[ServiceType.FACE_SWAP]['BONUS'])}
    ┣ {Texts.PHOTOSHOP_AI}: {count_all_transactions[ServiceType.PHOTOSHOP_AI]['BONUS']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.PHOTOSHOP_AI]['BONUS'], count_all_transactions_before[ServiceType.PHOTOSHOP_AI]['BONUS'])}
    ┣ {Texts.MUSIC_GEN}: {count_all_transactions[ServiceType.MUSIC_GEN]['BONUS']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.MUSIC_GEN]['BONUS'], count_all_transactions_before[ServiceType.MUSIC_GEN]['BONUS'])}
    ┣ {Texts.SUNO}: {count_all_transactions[ServiceType.SUNO]['BONUS']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.SUNO]['BONUS'], count_all_transactions_before[ServiceType.SUNO]['BONUS'])}
    ┣ 💬 Дополнительные чаты: {count_all_transactions[ServiceType.ADDITIONAL_CHATS]['BONUS']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.ADDITIONAL_CHATS]['BONUS'], count_all_transactions_before[ServiceType.ADDITIONAL_CHATS]['BONUS'])}
    ┣ 🎭 Доступ к каталогу: {count_all_transactions[ServiceType.ACCESS_TO_CATALOG]['BONUS']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.ACCESS_TO_CATALOG]['BONUS'], count_all_transactions_before[ServiceType.ACCESS_TO_CATALOG]['BONUS'])}
    ┣ 🎙 Голосовые запросы/ответы: {count_all_transactions[ServiceType.VOICE_MESSAGES]['BONUS']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.VOICE_MESSAGES]['BONUS'], count_all_transactions_before[ServiceType.VOICE_MESSAGES]['BONUS'])}
    ┣ ⚡ Быстрые сообщения: {count_all_transactions[ServiceType.FAST_MESSAGES]['BONUS']} {calculate_percentage_difference(is_all_time, count_all_transactions[ServiceType.FAST_MESSAGES]['BONUS'], count_all_transactions_before[ServiceType.FAST_MESSAGES]['BONUS'])}
    ┗ Всего: {all_bonuses} {calculate_percentage_difference(is_all_time, all_bonuses, all_bonuses_before)}
━ 3️⃣ <b>Промокоды:</b>
    ┗ Активировано: {count_activated_promo_codes} {calculate_percentage_difference(is_all_time, count_activated_promo_codes, count_activated_promo_codes_before)}

🔍 Это всё, что нужно знать о бонусах на данный момент 🚀
"""

    @staticmethod
    def statistics_expenses(
        period: str,
        count_expense_money: Dict,
        count_expense_money_before: Dict,
    ):
        is_all_time = period == 'всё время'
        emojis = Subscription.get_emojis()

        return f"""
#statistics #expenses

📊 <b>Статистика за {period} готова!</b>

📉 <b>Расходы</b>
━ 1️⃣ <b>AI модели:</b>
    ┣ {Texts.CHATGPT3_TURBO}:
        ┣ 💸 Средняя цена запроса: ${round(count_expense_money[ServiceType.CHAT_GPT3_TURBO]['AVERAGE_PRICE'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.CHAT_GPT3_TURBO]['AVERAGE_PRICE'], count_expense_money_before[ServiceType.CHAT_GPT3_TURBO]['AVERAGE_PRICE'])}
        ┗ 💰 Всего: ${round(count_expense_money[ServiceType.CHAT_GPT3_TURBO]['ALL'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.CHAT_GPT3_TURBO]['ALL'], count_expense_money_before[ServiceType.CHAT_GPT3_TURBO]['ALL'])}
    ┣ {Texts.CHATGPT4_TURBO}:
        ┣ 🎁 Средняя цена примера: ${round(count_expense_money[ServiceType.CHAT_GPT4_TURBO]['AVERAGE_EXAMPLE_PRICE'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.CHAT_GPT4_TURBO]['AVERAGE_EXAMPLE_PRICE'], count_expense_money_before[ServiceType.CHAT_GPT4_TURBO]['AVERAGE_EXAMPLE_PRICE'])}
        ┣ 🚀 Всего за примеры: ${round(count_expense_money[ServiceType.CHAT_GPT4_TURBO]['EXAMPLE_ALL'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.CHAT_GPT4_TURBO]['EXAMPLE_ALL'], count_expense_money_before[ServiceType.CHAT_GPT4_TURBO]['EXAMPLE_ALL'])}
        ┣ 💸 Средняя цена запроса: ${round(count_expense_money[ServiceType.CHAT_GPT4_TURBO]['AVERAGE_PRICE'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.CHAT_GPT4_TURBO]['AVERAGE_PRICE'], count_expense_money_before[ServiceType.CHAT_GPT4_TURBO]['AVERAGE_PRICE'])}
        ┗ 💰 Всего: ${round(count_expense_money[ServiceType.CHAT_GPT4_TURBO]['ALL'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.CHAT_GPT4_TURBO]['ALL'], count_expense_money_before[ServiceType.CHAT_GPT4_TURBO]['ALL'])}
    ┣ {Texts.CHATGPT4_OMNI_MINI}:
        ┣ 💸 Средняя цена запроса: ${round(count_expense_money[ServiceType.CHAT_GPT4_OMNI_MINI]['AVERAGE_PRICE'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.CHAT_GPT4_OMNI_MINI]['AVERAGE_PRICE'], count_expense_money_before[ServiceType.CHAT_GPT4_OMNI_MINI]['AVERAGE_PRICE'])}
        ┗ 💰 Всего: ${round(count_expense_money[ServiceType.CHAT_GPT4_OMNI_MINI]['ALL'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.CHAT_GPT4_OMNI_MINI]['ALL'], count_expense_money_before[ServiceType.CHAT_GPT4_OMNI_MINI]['ALL'])}
    ┣ {Texts.CHATGPT4_OMNI}:
        ┣ 🎁 Средняя цена примера: ${round(count_expense_money[ServiceType.CHAT_GPT4_OMNI]['AVERAGE_EXAMPLE_PRICE'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.CHAT_GPT4_OMNI]['AVERAGE_EXAMPLE_PRICE'], count_expense_money_before[ServiceType.CHAT_GPT4_OMNI]['AVERAGE_EXAMPLE_PRICE'])}
        ┣ 🚀 Всего за примеры: ${round(count_expense_money[ServiceType.CHAT_GPT4_OMNI]['EXAMPLE_ALL'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.CHAT_GPT4_OMNI]['EXAMPLE_ALL'], count_expense_money_before[ServiceType.CHAT_GPT4_OMNI]['EXAMPLE_ALL'])}
        ┣ 💸 Средняя цена запроса: ${round(count_expense_money[ServiceType.CHAT_GPT4_OMNI]['AVERAGE_PRICE'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.CHAT_GPT4_OMNI]['AVERAGE_PRICE'], count_expense_money_before[ServiceType.CHAT_GPT4_OMNI]['AVERAGE_PRICE'])}
        ┗ 💰 Всего: ${round(count_expense_money[ServiceType.CHAT_GPT4_OMNI]['ALL'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.CHAT_GPT4_OMNI]['ALL'], count_expense_money_before[ServiceType.CHAT_GPT4_OMNI]['ALL'])}
    ┣ {Texts.CHAT_GPT_O_1_MINI}:
        ┣ 💸 Средняя цена запроса: ${round(count_expense_money[ServiceType.CHAT_GPT_O_1_MINI]['AVERAGE_PRICE'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.CHAT_GPT_O_1_MINI]['AVERAGE_PRICE'], count_expense_money_before[ServiceType.CHAT_GPT_O_1_MINI]['AVERAGE_PRICE'])}
        ┗ 💰 Всего: ${round(count_expense_money[ServiceType.CHAT_GPT_O_1_MINI]['ALL'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.CHAT_GPT_O_1_MINI]['ALL'], count_expense_money_before[ServiceType.CHAT_GPT_O_1_MINI]['ALL'])}
    ┣ {Texts.CHAT_GPT_O_1_PREVIEW}:
        ┣ 💸 Средняя цена запроса: ${round(count_expense_money[ServiceType.CHAT_GPT_O_1_PREVIEW]['AVERAGE_PRICE'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.CHAT_GPT_O_1_PREVIEW]['AVERAGE_PRICE'], count_expense_money_before[ServiceType.CHAT_GPT_O_1_PREVIEW]['AVERAGE_PRICE'])}
        ┗ 💰 Всего: ${round(count_expense_money[ServiceType.CHAT_GPT_O_1_PREVIEW]['ALL'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.CHAT_GPT_O_1_PREVIEW]['ALL'], count_expense_money_before[ServiceType.CHAT_GPT_O_1_PREVIEW]['ALL'])}
    ┣ {Texts.CLAUDE_3_HAIKU}:
        ┣ 💸 Средняя цена запроса: ${round(count_expense_money[ServiceType.CLAUDE_3_HAIKU]['AVERAGE_PRICE'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.CLAUDE_3_HAIKU]['AVERAGE_PRICE'], count_expense_money_before[ServiceType.CLAUDE_3_HAIKU]['AVERAGE_PRICE'])}
        ┗ 💰 Всего: ${round(count_expense_money[ServiceType.CLAUDE_3_HAIKU]['ALL'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.CLAUDE_3_HAIKU]['ALL'], count_expense_money_before[ServiceType.CLAUDE_3_HAIKU]['ALL'])}
    ┣ {Texts.CLAUDE_3_SONNET}:
        ┣ 🎁 Средняя цена примера: ${round(count_expense_money[ServiceType.CLAUDE_3_SONNET]['AVERAGE_EXAMPLE_PRICE'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.CLAUDE_3_SONNET]['AVERAGE_EXAMPLE_PRICE'], count_expense_money_before[ServiceType.CLAUDE_3_SONNET]['AVERAGE_EXAMPLE_PRICE'])}
        ┣ 🚀 Всего за примеры: ${round(count_expense_money[ServiceType.CLAUDE_3_SONNET]['EXAMPLE_ALL'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.CLAUDE_3_SONNET]['EXAMPLE_ALL'], count_expense_money_before[ServiceType.CLAUDE_3_SONNET]['EXAMPLE_ALL'])}
        ┣ 💸 Средняя цена запроса: ${round(count_expense_money[ServiceType.CLAUDE_3_SONNET]['AVERAGE_PRICE'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.CLAUDE_3_SONNET]['AVERAGE_PRICE'], count_expense_money_before[ServiceType.CLAUDE_3_SONNET]['AVERAGE_PRICE'])}
        ┗ 💰 Всего: ${round(count_expense_money[ServiceType.CLAUDE_3_SONNET]['ALL'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.CLAUDE_3_SONNET]['ALL'], count_expense_money_before[ServiceType.CLAUDE_3_SONNET]['ALL'])}
    ┣ {Texts.CLAUDE_3_OPUS}:
        ┣ 🎁 Средняя цена примера: ${round(count_expense_money[ServiceType.CLAUDE_3_OPUS]['AVERAGE_EXAMPLE_PRICE'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.CLAUDE_3_OPUS]['AVERAGE_EXAMPLE_PRICE'], count_expense_money_before[ServiceType.CLAUDE_3_OPUS]['AVERAGE_EXAMPLE_PRICE'])}
        ┣ 🚀 Всего за примеры: ${round(count_expense_money[ServiceType.CLAUDE_3_OPUS]['EXAMPLE_ALL'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.CLAUDE_3_OPUS]['EXAMPLE_ALL'], count_expense_money_before[ServiceType.CLAUDE_3_OPUS]['EXAMPLE_ALL'])}
        ┣ 💸 Средняя цена запроса: ${round(count_expense_money[ServiceType.CLAUDE_3_OPUS]['AVERAGE_PRICE'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.CLAUDE_3_OPUS]['AVERAGE_PRICE'], count_expense_money_before[ServiceType.CLAUDE_3_OPUS]['AVERAGE_PRICE'])}
        ┗ 💰 Всего: ${round(count_expense_money[ServiceType.CLAUDE_3_OPUS]['ALL'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.CLAUDE_3_OPUS]['ALL'], count_expense_money_before[ServiceType.CLAUDE_3_OPUS]['ALL'])}
    ┣ {Texts.GEMINI_1_FLASH}:
        ┣ 💸 Средняя цена запроса: ${round(count_expense_money[ServiceType.GEMINI_1_FLASH]['AVERAGE_PRICE'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.GEMINI_1_FLASH]['AVERAGE_PRICE'], count_expense_money_before[ServiceType.GEMINI_1_FLASH]['AVERAGE_PRICE'])}
        ┗ 💰 Всего: ${round(count_expense_money[ServiceType.GEMINI_1_FLASH]['ALL'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.GEMINI_1_FLASH]['ALL'], count_expense_money_before[ServiceType.GEMINI_1_FLASH]['ALL'])}
    ┣ {Texts.GEMINI_1_PRO}:
        ┣ 🎁 Средняя цена примера: ${round(count_expense_money[ServiceType.GEMINI_1_PRO]['AVERAGE_EXAMPLE_PRICE'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.GEMINI_1_PRO]['AVERAGE_EXAMPLE_PRICE'], count_expense_money_before[ServiceType.GEMINI_1_PRO]['AVERAGE_EXAMPLE_PRICE'])}
        ┣ 🚀 Всего за примеры: ${round(count_expense_money[ServiceType.GEMINI_1_PRO]['EXAMPLE_ALL'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.GEMINI_1_PRO]['EXAMPLE_ALL'], count_expense_money_before[ServiceType.GEMINI_1_PRO]['EXAMPLE_ALL'])}
        ┣ 💸 Средняя цена запроса: ${round(count_expense_money[ServiceType.GEMINI_1_PRO]['AVERAGE_PRICE'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.GEMINI_1_PRO]['AVERAGE_PRICE'], count_expense_money_before[ServiceType.GEMINI_1_PRO]['AVERAGE_PRICE'])}
        ┗ 💰 Всего: ${round(count_expense_money[ServiceType.GEMINI_1_PRO]['ALL'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.GEMINI_1_PRO]['ALL'], count_expense_money_before[ServiceType.GEMINI_1_PRO]['ALL'])}
    ┣ {Texts.GEMINI_1_ULTRA}:
        ┣ 💸 Средняя цена запроса: ${round(count_expense_money[ServiceType.GEMINI_1_ULTRA]['AVERAGE_PRICE'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.GEMINI_1_ULTRA]['AVERAGE_PRICE'], count_expense_money_before[ServiceType.GEMINI_1_ULTRA]['AVERAGE_PRICE'])}
        ┗ 💰 Всего: ${round(count_expense_money[ServiceType.GEMINI_1_ULTRA]['ALL'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.GEMINI_1_ULTRA]['ALL'], count_expense_money_before[ServiceType.GEMINI_1_ULTRA]['ALL'])}
    ┣ {Texts.DALL_E}:
        ┣ 💸 Средняя цена запроса: ${round(count_expense_money[ServiceType.DALL_E]['AVERAGE_PRICE'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.DALL_E]['AVERAGE_PRICE'], count_expense_money_before[ServiceType.DALL_E]['AVERAGE_PRICE'])}
        ┗ 💰 Всего: ${round(count_expense_money[ServiceType.DALL_E]['ALL'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.DALL_E]['ALL'], count_expense_money_before[ServiceType.DALL_E]['ALL'])}
    ┣ {Texts.MIDJOURNEY}:
        ┣ 🎁 Средняя цена примера: ${round(count_expense_money[ServiceType.MIDJOURNEY]['AVERAGE_EXAMPLE_PRICE'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.MIDJOURNEY]['AVERAGE_EXAMPLE_PRICE'], count_expense_money_before[ServiceType.MIDJOURNEY]['AVERAGE_EXAMPLE_PRICE'])}
        ┣ 🚀 Всего за примеры: ${round(count_expense_money[ServiceType.MIDJOURNEY]['EXAMPLE_ALL'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.MIDJOURNEY]['EXAMPLE_ALL'], count_expense_money_before[ServiceType.MIDJOURNEY]['EXAMPLE_ALL'])}
        ┣ 💸 Средняя цена запроса: ${round(count_expense_money[ServiceType.MIDJOURNEY]['AVERAGE_PRICE'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.MIDJOURNEY]['AVERAGE_PRICE'], count_expense_money_before[ServiceType.MIDJOURNEY]['AVERAGE_PRICE'])}
        ┗ 💰 Всего: ${round(count_expense_money[ServiceType.MIDJOURNEY]['ALL'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.MIDJOURNEY]['ALL'], count_expense_money_before[ServiceType.MIDJOURNEY]['ALL'])}
    ┣ {Texts.STABLE_DIFFUSION}:
        ┣ 💸 Средняя цена запроса: ${round(count_expense_money[ServiceType.STABLE_DIFFUSION]['AVERAGE_PRICE'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.STABLE_DIFFUSION]['AVERAGE_PRICE'], count_expense_money_before[ServiceType.STABLE_DIFFUSION]['AVERAGE_PRICE'])}
        ┗ 💰 Всего: ${round(count_expense_money[ServiceType.STABLE_DIFFUSION]['ALL'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.STABLE_DIFFUSION]['ALL'], count_expense_money_before[ServiceType.STABLE_DIFFUSION]['ALL'])}
    ┣ {Texts.FLUX}:
        ┣ 💸 Средняя цена запроса: ${round(count_expense_money[ServiceType.FLUX]['AVERAGE_PRICE'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.FLUX]['AVERAGE_PRICE'], count_expense_money_before[ServiceType.FLUX]['AVERAGE_PRICE'])}
        ┗ 💰 Всего: ${round(count_expense_money[ServiceType.FLUX]['ALL'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.FLUX]['ALL'], count_expense_money_before[ServiceType.FLUX]['ALL'])}
    ┣ {Texts.FACE_SWAP}:
        ┣ 💸 Средняя цена запроса: ${round(count_expense_money[ServiceType.FACE_SWAP]['AVERAGE_PRICE'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.FACE_SWAP]['AVERAGE_PRICE'], count_expense_money_before[ServiceType.FACE_SWAP]['AVERAGE_PRICE'])}
        ┗ 💰 Всего: ${round(count_expense_money[ServiceType.FACE_SWAP]['ALL'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.FACE_SWAP]['ALL'], count_expense_money_before[ServiceType.FACE_SWAP]['ALL'])}
    ┣ {Texts.PHOTOSHOP_AI}:
        ┣ 💸 Средняя цена запроса: ${round(count_expense_money[ServiceType.PHOTOSHOP_AI]['AVERAGE_PRICE'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.PHOTOSHOP_AI]['AVERAGE_PRICE'], count_expense_money_before[ServiceType.PHOTOSHOP_AI]['AVERAGE_PRICE'])}
        ┗ 💰 Всего: ${round(count_expense_money[ServiceType.PHOTOSHOP_AI]['ALL'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.PHOTOSHOP_AI]['ALL'], count_expense_money_before[ServiceType.PHOTOSHOP_AI]['ALL'])}
    ┣ {Texts.MUSIC_GEN}:
        ┣ 💸 Средняя цена запроса: ${round(count_expense_money[ServiceType.MUSIC_GEN]['AVERAGE_PRICE'], 2)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.MUSIC_GEN]['AVERAGE_PRICE'], count_expense_money_before[ServiceType.MUSIC_GEN]['AVERAGE_PRICE'])}
        ┗ 💰 Всего: ${round(count_expense_money[ServiceType.MUSIC_GEN]['ALL'], 2)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.MUSIC_GEN]['ALL'], count_expense_money_before[ServiceType.MUSIC_GEN]['ALL'])}
    ┗ {Texts.SUNO}:
        ┣ 🎁 Средняя цена примера: ${round(count_expense_money[ServiceType.SUNO]['AVERAGE_EXAMPLE_PRICE'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.SUNO]['AVERAGE_EXAMPLE_PRICE'], count_expense_money_before[ServiceType.SUNO]['AVERAGE_EXAMPLE_PRICE'])}
        ┣ 🚀 Всего за примеры: ${round(count_expense_money[ServiceType.SUNO]['EXAMPLE_ALL'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.SUNO]['EXAMPLE_ALL'], count_expense_money_before[ServiceType.SUNO]['EXAMPLE_ALL'])}
        ┣ 💸 Средняя цена запроса: ${round(count_expense_money[ServiceType.SUNO]['AVERAGE_PRICE'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.SUNO]['AVERAGE_PRICE'], count_expense_money_before[ServiceType.SUNO]['AVERAGE_PRICE'])}
        ┗ 💰 Всего: ${round(count_expense_money[ServiceType.SUNO]['ALL'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.SUNO]['ALL'], count_expense_money_before[ServiceType.SUNO]['ALL'])}
━ 2️⃣ <b>Технические:</b>
    ┣ 🎙 Голосовые запросы/ответы: ${round(count_expense_money[ServiceType.VOICE_MESSAGES]['ALL'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.VOICE_MESSAGES]['ALL'], count_expense_money_before[ServiceType.VOICE_MESSAGES]['ALL'])}
    ┣ 💻 Сервер: ${round(count_expense_money[ServiceType.SERVER]['ALL'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.SERVER]['ALL'], count_expense_money_before[ServiceType.SERVER]['ALL'])}
    ┗ 🗄 База Данных: ${round(count_expense_money[ServiceType.DATABASE]['ALL'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ServiceType.DATABASE]['ALL'], count_expense_money_before[ServiceType.DATABASE]['ALL'])}
━ 3️⃣ <b>Подписчики:</b>
    ┣ <b>{SubscriptionType.FREE} {emojis[SubscriptionType.FREE]}:</b>
        ┣ 💸 Средняя цена подписчика: ${round(count_expense_money[SubscriptionType.FREE]['AVERAGE_PRICE'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[SubscriptionType.FREE]['AVERAGE_PRICE'], count_expense_money_before[SubscriptionType.FREE]['AVERAGE_PRICE'])}
        ┗ 💰 Всего: ${round(count_expense_money[SubscriptionType.FREE]['ALL'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[SubscriptionType.FREE]['ALL'], count_expense_money_before[SubscriptionType.FREE]['ALL'])}
    ┣ <b>{SubscriptionType.MINI} {emojis[SubscriptionType.MINI]}:</b>
        ┣ 💸 Средняя цена подписчика: ${round(count_expense_money[SubscriptionType.MINI]['AVERAGE_PRICE'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[SubscriptionType.MINI]['AVERAGE_PRICE'], count_expense_money_before[SubscriptionType.MINI]['AVERAGE_PRICE'])}
        ┗ 💰 Всего: ${round(count_expense_money[SubscriptionType.MINI]['ALL'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[SubscriptionType.MINI]['ALL'], count_expense_money_before[SubscriptionType.MINI]['ALL'])}
    ┣ <b>{SubscriptionType.STANDARD} {emojis[SubscriptionType.STANDARD]}:</b>
        ┣ 💸 Средняя цена подписчика: ${round(count_expense_money[SubscriptionType.STANDARD]['AVERAGE_PRICE'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[SubscriptionType.STANDARD]['AVERAGE_PRICE'], count_expense_money_before[SubscriptionType.STANDARD]['AVERAGE_PRICE'])}
        ┗ 💰 Всего: ${round(count_expense_money[SubscriptionType.STANDARD]['ALL'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[SubscriptionType.STANDARD]['ALL'], count_expense_money_before[SubscriptionType.STANDARD]['ALL'])}
    ┣ <b>{SubscriptionType.VIP} {emojis[SubscriptionType.VIP]}:</b>
        ┣ 💸 Средняя цена подписчика: ${round(count_expense_money[SubscriptionType.VIP]['AVERAGE_PRICE'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[SubscriptionType.VIP]['AVERAGE_PRICE'], count_expense_money_before[SubscriptionType.VIP]['AVERAGE_PRICE'])}
        ┗ 💰 Всего: ${round(count_expense_money[SubscriptionType.VIP]['ALL'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[SubscriptionType.VIP]['ALL'], count_expense_money_before[SubscriptionType.VIP]['ALL'])}
    ┣ <b>{SubscriptionType.PREMIUM} {emojis[SubscriptionType.PREMIUM]}:</b>
        ┣ 💸 Средняя цена подписчика: ${round(count_expense_money[SubscriptionType.PREMIUM]['AVERAGE_PRICE'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[SubscriptionType.PREMIUM]['AVERAGE_PRICE'], count_expense_money_before[SubscriptionType.PREMIUM]['AVERAGE_PRICE'])}
        ┗ 💰 Всего: ${round(count_expense_money[SubscriptionType.PREMIUM]['ALL'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[SubscriptionType.PREMIUM]['ALL'], count_expense_money_before[SubscriptionType.PREMIUM]['ALL'])}
    ┗ <b>{SubscriptionType.UNLIMITED} {emojis[SubscriptionType.UNLIMITED]}:</b>
        ┣ 💸 Средняя цена подписчика: ${round(count_expense_money[SubscriptionType.UNLIMITED]['AVERAGE_PRICE'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[SubscriptionType.UNLIMITED]['AVERAGE_PRICE'], count_expense_money_before[SubscriptionType.UNLIMITED]['AVERAGE_PRICE'])}
        ┗ 💰 Всего: ${round(count_expense_money[SubscriptionType.UNLIMITED]['ALL'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[SubscriptionType.UNLIMITED]['ALL'], count_expense_money_before[SubscriptionType.UNLIMITED]['ALL'])}
━ <b>Всего:</b> ${round(count_expense_money['ALL'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money['ALL'], count_expense_money_before['ALL'])}

🔍 Это всё, что нужно знать о расходах на данный момент 🚀
"""

    @staticmethod
    def statistics_incomes(
        period: str,
        count_income_money: Dict,
        count_income_money_before: Dict,
    ):
        is_all_time = period == 'всё время'
        emojis = Subscription.get_emojis()

        return f"""
#statistics #incomes

📊 <b>Статистика за {period} готова!</b>

📈 <b>Доходы</b>
━ 1️⃣ <b>Подписки:</b>
    ┣ {ServiceType.MINI} {emojis[ServiceType.MINI]}: {round(count_income_money[ServiceType.MINI], 2)}₽ {calculate_percentage_difference(is_all_time, count_income_money[ServiceType.MINI], count_income_money_before[ServiceType.MINI])}
    ┣ {ServiceType.STANDARD} {emojis[ServiceType.STANDARD]}: {round(count_income_money[ServiceType.STANDARD], 2)}₽ {calculate_percentage_difference(is_all_time, count_income_money[ServiceType.STANDARD], count_income_money_before[ServiceType.STANDARD])}
    ┣ {ServiceType.VIP} {emojis[ServiceType.VIP]}: {round(count_income_money[ServiceType.VIP], 2)}₽ {calculate_percentage_difference(is_all_time, count_income_money[ServiceType.VIP], count_income_money_before[ServiceType.VIP])}
    ┣ {ServiceType.PREMIUM} {emojis[ServiceType.PREMIUM]}: {round(count_income_money[ServiceType.PREMIUM], 2)}₽ {calculate_percentage_difference(is_all_time, count_income_money[ServiceType.PREMIUM], count_income_money_before[ServiceType.PREMIUM])}
    ┣ {ServiceType.UNLIMITED} {emojis[ServiceType.UNLIMITED]}: {round(count_income_money[ServiceType.UNLIMITED], 2)}₽ {calculate_percentage_difference(is_all_time, count_income_money[ServiceType.UNLIMITED], count_income_money_before[ServiceType.UNLIMITED])}
    ┗ Всего: {round(count_income_money['SUBSCRIPTION_ALL'], 2)}₽ {calculate_percentage_difference(is_all_time, count_income_money['SUBSCRIPTION_ALL'], count_income_money_before['SUBSCRIPTION_ALL'])}
━ 2️⃣ <b>Пакеты:</b>
    ┣ {Texts.CHATGPT3_TURBO}: {round(count_income_money[ServiceType.CHAT_GPT3_TURBO], 2)}₽ {calculate_percentage_difference(is_all_time, count_income_money[ServiceType.CHAT_GPT3_TURBO], count_income_money_before[ServiceType.CHAT_GPT3_TURBO])}
    ┣ {Texts.CHATGPT4_TURBO}: {round(count_income_money[ServiceType.CHAT_GPT4_TURBO], 2)}₽ {calculate_percentage_difference(is_all_time, count_income_money[ServiceType.CHAT_GPT4_TURBO], count_income_money_before[ServiceType.CHAT_GPT4_TURBO])}
    ┣ {Texts.CHATGPT4_OMNI_MINI}: {round(count_income_money[ServiceType.CHAT_GPT4_OMNI_MINI], 2)}₽ {calculate_percentage_difference(is_all_time, count_income_money[ServiceType.CHAT_GPT4_OMNI_MINI], count_income_money_before[ServiceType.CHAT_GPT4_OMNI_MINI])}
    ┣ {Texts.CHATGPT4_OMNI}: {round(count_income_money[ServiceType.CHAT_GPT4_OMNI], 2)}₽ {calculate_percentage_difference(is_all_time, count_income_money[ServiceType.CHAT_GPT4_OMNI], count_income_money_before[ServiceType.CHAT_GPT4_OMNI])}
    ┣ {Texts.CHAT_GPT_O_1_MINI}: {round(count_income_money[ServiceType.CHAT_GPT_O_1_MINI], 2)}₽ {calculate_percentage_difference(is_all_time, count_income_money[ServiceType.CHAT_GPT_O_1_MINI], count_income_money_before[ServiceType.CHAT_GPT_O_1_MINI])}
    ┣ {Texts.CHAT_GPT_O_1_PREVIEW}: {round(count_income_money[ServiceType.CHAT_GPT_O_1_PREVIEW], 2)}₽ {calculate_percentage_difference(is_all_time, count_income_money[ServiceType.CHAT_GPT_O_1_PREVIEW], count_income_money_before[ServiceType.CHAT_GPT_O_1_PREVIEW])}
    ┣ {Texts.CLAUDE_3_HAIKU}: {round(count_income_money[ServiceType.CLAUDE_3_HAIKU], 2)}₽ {calculate_percentage_difference(is_all_time, count_income_money[ServiceType.CLAUDE_3_HAIKU], count_income_money_before[ServiceType.CLAUDE_3_HAIKU])}
    ┣ {Texts.CLAUDE_3_SONNET}: {round(count_income_money[ServiceType.CLAUDE_3_SONNET], 2)}₽ {calculate_percentage_difference(is_all_time, count_income_money[ServiceType.CLAUDE_3_SONNET], count_income_money_before[ServiceType.CLAUDE_3_SONNET])}
    ┣ {Texts.CLAUDE_3_OPUS}: {round(count_income_money[ServiceType.CLAUDE_3_OPUS], 2)}₽ {calculate_percentage_difference(is_all_time, count_income_money[ServiceType.CLAUDE_3_OPUS], count_income_money_before[ServiceType.CLAUDE_3_OPUS])}
    ┣ {Texts.GEMINI_1_FLASH}: {round(count_income_money[ServiceType.GEMINI_1_FLASH], 2)}₽ {calculate_percentage_difference(is_all_time, count_income_money[ServiceType.GEMINI_1_FLASH], count_income_money_before[ServiceType.GEMINI_1_FLASH])}
    ┣ {Texts.GEMINI_1_PRO}: {round(count_income_money[ServiceType.GEMINI_1_PRO], 2)}₽ {calculate_percentage_difference(is_all_time, count_income_money[ServiceType.GEMINI_1_PRO], count_income_money_before[ServiceType.GEMINI_1_PRO])}
    ┣ {Texts.GEMINI_1_ULTRA}: {round(count_income_money[ServiceType.GEMINI_1_ULTRA], 2)}₽ {calculate_percentage_difference(is_all_time, count_income_money[ServiceType.GEMINI_1_ULTRA], count_income_money_before[ServiceType.GEMINI_1_ULTRA])}
    ┣ {Texts.DALL_E}: {round(count_income_money[ServiceType.DALL_E], 2)}₽ {calculate_percentage_difference(is_all_time, count_income_money[ServiceType.DALL_E], count_income_money_before[ServiceType.DALL_E])}
    ┣ {Texts.MIDJOURNEY}: {round(count_income_money[ServiceType.MIDJOURNEY], 2)}₽ {calculate_percentage_difference(is_all_time, count_income_money[ServiceType.MIDJOURNEY], count_income_money_before[ServiceType.MIDJOURNEY])}
    ┣ {Texts.STABLE_DIFFUSION}: {round(count_income_money[ServiceType.STABLE_DIFFUSION], 2)}₽ {calculate_percentage_difference(is_all_time, count_income_money[ServiceType.STABLE_DIFFUSION], count_income_money_before[ServiceType.STABLE_DIFFUSION])}
    ┣ {Texts.FLUX}: {round(count_income_money[ServiceType.FLUX], 2)}₽ {calculate_percentage_difference(is_all_time, count_income_money[ServiceType.FLUX], count_income_money_before[ServiceType.FLUX])}
    ┣ {Texts.FACE_SWAP}: {round(count_income_money[ServiceType.FACE_SWAP], 2)}₽ {calculate_percentage_difference(is_all_time, count_income_money[ServiceType.FACE_SWAP], count_income_money_before[ServiceType.FACE_SWAP])}
    ┣ {Texts.PHOTOSHOP_AI}: {round(count_income_money[ServiceType.PHOTOSHOP_AI], 2)}₽ {calculate_percentage_difference(is_all_time, count_income_money[ServiceType.PHOTOSHOP_AI], count_income_money_before[ServiceType.PHOTOSHOP_AI])}
    ┣ {Texts.MUSIC_GEN}: {round(count_income_money[ServiceType.MUSIC_GEN], 2)}₽ {calculate_percentage_difference(is_all_time, count_income_money[ServiceType.MUSIC_GEN], count_income_money_before[ServiceType.MUSIC_GEN])}
    ┣ {Texts.SUNO}: {round(count_income_money[ServiceType.SUNO], 2)}₽ {calculate_percentage_difference(is_all_time, count_income_money[ServiceType.SUNO], count_income_money_before[ServiceType.SUNO])}
    ┣ 💬 Дополнительные чаты: {round(count_income_money[ServiceType.ADDITIONAL_CHATS], 2)}₽ {calculate_percentage_difference(is_all_time, count_income_money[ServiceType.ADDITIONAL_CHATS], count_income_money_before[ServiceType.ADDITIONAL_CHATS])}
    ┣ 🎭 Доступ к каталогу: {round(count_income_money[ServiceType.ACCESS_TO_CATALOG], 2)}₽ {calculate_percentage_difference(is_all_time, count_income_money[ServiceType.ACCESS_TO_CATALOG], count_income_money_before[ServiceType.ACCESS_TO_CATALOG])}
    ┣ 🎙 Голосовые запросы/ответы: {round(count_income_money[ServiceType.VOICE_MESSAGES], 2)}₽ {calculate_percentage_difference(is_all_time, count_income_money[ServiceType.VOICE_MESSAGES], count_income_money_before[ServiceType.VOICE_MESSAGES])}
    ┣ ⚡ Быстрые сообщения: {round(count_income_money[ServiceType.FAST_MESSAGES], 2)}₽ {calculate_percentage_difference(is_all_time, count_income_money[ServiceType.FAST_MESSAGES], count_income_money_before[ServiceType.FAST_MESSAGES])}
    ┗ Всего: {round(count_income_money['PACKAGES_ALL'], 2)}₽ {calculate_percentage_difference(is_all_time, count_income_money['PACKAGES_ALL'], count_income_money_before['PACKAGES_ALL'])}
━ <b>Средний чек:</b> {round(count_income_money['AVERAGE_PRICE'], 2)}₽ {calculate_percentage_difference(is_all_time, count_income_money['AVERAGE_PRICE'], count_income_money_before['AVERAGE_PRICE'])}
━ <b>Всего:</b> {round(count_income_money['ALL'], 2)}₽ {calculate_percentage_difference(is_all_time, count_income_money['ALL'], count_income_money_before['ALL'])}
━ <b>Вал:</b> {round(count_income_money['VAL'], 2)}₽ {calculate_percentage_difference(is_all_time, count_income_money['VAL'], count_income_money_before['VAL'])}

🔍 Это всё, что нужно знать о доходах на данный момент. Вперёд, к новым достижениям! 🚀
"""

    # Blast
    @staticmethod
    def blast_confirmation(
        blast_letters: Dict,
    ):
        letters = ""
        for i, (language_code, letter) in enumerate(blast_letters.items()):
            letters += f'{language_code}:\n{letter}'
            letters += '\n' if i < len(blast_letters.items()) - 1 else ''

        return f"""
📢 <b>Последний шаг перед великим запуском!</b> 🚀

🤖 Текст рассылки:
{letters}

Если все выглядит идеально, нажмите "Подтвердить", а если нужны правки, выберите "Отменить" 🌟
"""

    @staticmethod
    def catalog_manage_create_role_confirmation(
        role_system_name: str,
        role_names: Dict,
        role_descriptions: Dict,
        role_instructions: Dict,
    ):
        names = ""
        for i, (language_code, name) in enumerate(role_names.items()):
            names += f'{language_code}: {name}'
            names += '\n' if i < len(role_names.items()) - 1 else ''
        descriptions = ""
        for i, (language_code, description) in enumerate(role_descriptions.items()):
            descriptions += f'{language_code}: {description}'
            descriptions += '\n' if i < len(role_descriptions.items()) - 1 else ''
        instructions = ""
        for i, (language_code, instruction) in enumerate(role_instructions.items()):
            instructions += f'{language_code}: {instruction}'
            instructions += '\n' if i < len(role_instructions.items()) - 1 else ''

        return f"""
🎩 <b>Вот что вы создали:</b>

🤖 Системное название:
{role_system_name}

🌍 Имена:
{names}

💬 Описания:
{descriptions}

📜 Инструкции:
{instructions}

Если все выглядит идеально, нажмите "Подтвердить", а если нужны правки, выберите "Отменить" 🌟
"""

    @staticmethod
    def catalog_manage_role_edit(
        role_system_name: str,
        role_names: Dict,
        role_descriptions: Dict,
        role_instructions: Dict,
    ):
        names = ""
        for i, (language_code, name) in enumerate(role_names.items()):
            names += f'{language_code}: {name}'
            names += '\n' if i < len(role_names.items()) - 1 else ''
        descriptions = ""
        for i, (language_code, description) in enumerate(role_descriptions.items()):
            descriptions += f'{language_code}: {description}'
            descriptions += '\n' if i < len(role_descriptions.items()) - 1 else ''
        instructions = ""
        for i, (language_code, instruction) in enumerate(role_instructions.items()):
            instructions += f'{language_code}: {instruction}'
            instructions += '\n' if i < len(role_instructions.items()) - 1 else ''

        return f"""
🎨 <b>Настройка роли</b> 🖌️

🔧 Вы решили отполировать <b>{role_system_name}</b>! Настало время превратить его в настоящую звезду AI-мира 🌟

🌍 <b>Имена:</b>
{names}

💬 <b>Описания:</b>
{descriptions}

📜 <b>Инструкции:</b>
{instructions}

🛠️ Теперь ваша очередь внести магию! Выберите, что хотите изменить:
- "Изменить имя" 📝
- "Изменить описание" 📖
- "Изменить инструкцию" 🗒️
- "Изменить фотографию" 🖼
- "Назад" 🔙
"""

    @staticmethod
    def face_swap_manage_create_package_confirmation(
        package_system_name: str,
        package_names: Dict,
    ):
        names = ""
        for i, (language_code, name) in enumerate(package_names.items()):
            names += f'{language_code}: {name}'
            names += '\n' if i < len(package_names.items()) - 1 else ''

        return f"""
🌟 <b>Вот и всё! Ваш новый пакет FaceSwap почти готов к дебюту!</b> 🎉

📝 Проверьте все детали:
- 🤖 <b>Системное название:</b>
{package_system_name}

- 🌍 <b>Имена:</b>
{names}

🔍 Убедитесь, что все верно. Это ваше творение, и оно должно быть идеальным!

👇 Выберите действие
"""

    @staticmethod
    def purchase_minimal_price(currency: Currency):
        raise NotImplementedError

    @staticmethod
    def profile(
        subscription_type: SubscriptionType,
        subscription_status: SubscriptionStatus,
        gender: UserGender,
        current_model: Model,
        current_model_version: str,
        renewal_date,
    ) -> str:
        raise NotImplementedError

    @staticmethod
    def profile_quota(
        subscription_type: SubscriptionType,
        daily_limits,
        additional_usage_quota,
        hours_before_limit_update: int,
        minutes_before_limit_update: int,
    ) -> str:
        raise NotImplementedError

    # Payment
    @staticmethod
    def payment_description_subscription(user_id: str, subscription_type: SubscriptionType):
        raise NotImplementedError

    @staticmethod
    def payment_description_renew_subscription(user_id: str, subscription_type: SubscriptionType):
        raise NotImplementedError

    @staticmethod
    def subscribe(currency: Currency, min_prices: Dict) -> str:
        raise NotImplementedError

    @staticmethod
    def choose_how_many_months_to_subscribe(subscription_type: SubscriptionType) -> str:
        raise NotImplementedError

    @staticmethod
    def cycles_subscribe() -> str:
        raise NotImplementedError

    @staticmethod
    def confirmation_subscribe(subscription_type: SubscriptionType, currency: Currency, price: float) -> str:
        raise NotImplementedError

    @staticmethod
    def payment_description_package(user_id: str, package_name: str, package_quantity: int):
        raise NotImplementedError

    @staticmethod
    def payment_description_cart(user_id: str):
        raise NotImplementedError

    @staticmethod
    def package(currency: Currency, page: int) -> str:
        raise NotImplementedError

    @staticmethod
    def get_package_name_and_quantity_by_package_type(package_type: PackageType):
        raise NotImplementedError

    @staticmethod
    def choose_min(package_type: PackageType) -> str:
        raise NotImplementedError

    @staticmethod
    def shopping_cart(currency: Currency, cart_items: List[Dict], discount: int):
        raise NotImplementedError

    @staticmethod
    def confirmation_package(package_name: str, package_quantity: int, currency: Currency, price: float) -> str:
        raise NotImplementedError

    @staticmethod
    def confirmation_cart(cart_items: List[Dict], currency: Currency, price: float) -> str:
        raise NotImplementedError

    # Chats
    @staticmethod
    def chats(current_chat_name: str, total_chats: int, available_to_create_chats: int) -> str:
        raise NotImplementedError

    # FaceSwap
    @staticmethod
    def choose_face_swap_package(name: str, available_images: int, total_images: int, used_images: int) -> str:
        raise NotImplementedError

    @staticmethod
    def face_swap_package_forbidden(available_images: int) -> str:
        raise NotImplementedError

    # MusicGen
    @staticmethod
    def music_gen_forbidden(available_seconds: int) -> str:
        raise NotImplementedError

    # AI
    @staticmethod
    def switched(model: Model, model_version: str):
        raise NotImplementedError

    @staticmethod
    def requests_recommendations() -> List[str]:
        raise NotImplementedError

    @staticmethod
    def image_recommendations() -> List[str]:
        raise NotImplementedError

    @staticmethod
    def music_recommendations() -> List[str]:
        raise NotImplementedError

    @staticmethod
    def photoshop_ai_actions() -> List[str]:
        raise NotImplementedError

    @staticmethod
    def wait_for_another_request(seconds: int) -> str:
        raise NotImplementedError

    @staticmethod
    def processing_request_text() -> str:
        raise NotImplementedError

    @staticmethod
    def processing_request_image() -> str:
        raise NotImplementedError

    @staticmethod
    def processing_request_face_swap() -> str:
        raise NotImplementedError

    @staticmethod
    def processing_request_music() -> str:
        raise NotImplementedError

    @staticmethod
    def processing_statistics() -> str:
        texts = [
            "Вызываю кибернетических уток, чтобы ускорить процесс. Кря-кря, и данные у нас! 🦆💻",
            "Использую тайные заклинания кода, чтобы вызволить вашу статистику из пучины данных. Абракадабра! 🧙‍💾",
            "Таймер установлен, чайник на плите. Пока я готовлю чай, данные собираются сами! ☕📊",
            "Подключаюсь к космическим спутникам, чтобы найти нужную статистику. Вот это звёздный поиск! 🛰️✨",
            "Зову на помощь армию пикселей. Они уже маршируют сквозь строки кода, чтобы доставить вам данные! 🪖🖥️",
        ]

        return random.choice(texts)

    # Settings
    @staticmethod
    def settings(human_model: str, current_model: Model, dall_e_cost=1) -> str:
        raise NotImplementedError

    # Bonus
    @staticmethod
    def bonus(user_id: str, balance: float, referred_count: int, feedback_count: int, play_count: int) -> str:
        raise NotImplementedError

    @staticmethod
    def referral_link(user_id: str, is_share: bool) -> str:
        if is_share:
            return f"https://t.me/share/url?url=https://t.me/GPTsTurboBot?start=referral-{user_id}"
        return f"https://t.me/GPTsTurboBot?start=referral-{user_id}"
