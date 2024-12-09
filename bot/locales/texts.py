import random
from typing import Protocol, Union

from bot.database.models.common import Currency, Model, ModelType
from bot.database.models.feedback import FeedbackStatus
from bot.database.models.game import GameType
from bot.database.models.generation import GenerationReaction
from bot.database.models.product import Product, ProductCategory
from bot.database.models.prompt import Prompt
from bot.database.models.subscription import SubscriptionStatus
from bot.database.models.user import UserGender
from bot.helpers.calculate_percentage_difference import calculate_percentage_difference
from bot.locales.types import LanguageCode


class Texts(Protocol):
    START: str
    START_QUICK_GUIDE: str
    START_ADDITIONAL_FEATURES: str
    QUICK_GUIDE: str
    ADDITIONAL_FEATURES: str
    MAINTENANCE_MODE: str

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

    ADMIN_INFO = '👨‍💻 Выберите действие, админ 👩‍💻'
    ADS_INFO = 'Выберите, что хотите сделать:'
    ADS_CREATE = 'Создать рекламную ссылку 📯'
    ADS_GET = 'Получить информацию о рекламной кампании 📯'
    ADS_SEND_LINK = 'Отправьте мне ссылку с рекламной кампанией 📯'
    ADS_CHOOSE_SOURCE = 'Выберите источник рекламной кампании 📯'
    ADS_CHOOSE_MEDIUM = 'Выберите тип трафика рекламной кампании 📯'
    ADS_SEND_NAME = 'Отправьте название рекламной кампании, которое состоит из одного слова без спец. символов 📯'
    ADS_SEND_QUANTITY = 'Отправьте количество создаваемых ссылок 📯'
    BAN_INFO = 'Отправь мне id пользователя, которого вы хотите забанить/разбанить ⛔️'
    BAN_SUCCESS = 'Вы успешно забанили пользователя 📛'
    UNBAN_SUCCESS = 'Вы успешно разбанили пользователя 🔥'

    SERVER: str
    DATABASE: str

    TEXT_MODELS: str
    IMAGE_MODELS: str
    MUSIC_MODELS: str
    VIDEO_MODELS: str

    # Feedback
    FEEDBACK: str
    FEEDBACK_SUCCESS: str
    FEEDBACK_ADMIN_APPROVE = 'Одобрить ✅'
    FEEDBACK_ADMIN_DENY = 'Отклонить ❌'
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
    RENEW_SUBSCRIPTION: str
    RENEW_SUBSCRIPTION_SUCCESS: str
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
    PLAY_DICE_GAME_CHOOSE_1 = '🎲 1️⃣'
    PLAY_DICE_GAME_CHOOSE_2 = '🎲 2️⃣'
    PLAY_DICE_GAME_CHOOSE_3 = '🎲 3️⃣'
    PLAY_DICE_GAME_CHOOSE_4 = '🎲 4️⃣'
    PLAY_DICE_GAME_CHOOSE_5 = '🎲 5️⃣'
    PLAY_DICE_GAME_CHOOSE_6 = '🎲 6️⃣'
    PLAY_CASINO_GAME: str
    PLAY_CASINO_GAME_DESCRIPTION: str
    PLAY_GAME_WON: str
    PLAY_GAME_LOST: str
    PLAY_GAME_REACHED_LIMIT: str
    CASH_OUT: str
    REFERRAL_SUCCESS: str
    REFERRAL_LIMIT_ERROR: str

    # Blast
    BLAST_CHOOSE_USER_TYPE = """
📣 <b>Пора делать рассылку!</b>

Выберите для начала кому вы хотите отправить рассылку:
"""
    BLAST_CHOOSE_LANGUAGE = """
📣 <b>Продолжаем делать рассылку!</b>

Выберите язык для рассылки или отправьте всем сразу:
"""
    BLAST_WRITE_IN_CHOSEN_LANGUAGE = """
✍️ <b>Пора создать ваше послание!</b> 🚀

Вы выбрали язык, теперь пришло время вложить душу в сообщение!

Напишите текст рассылки, который затронет сердца ваших пользователей, развеселит их или даже вдохновит на новые подвиги. Помните, каждое слово – это кисть, а ваш текст – полотно, на котором вы можете нарисовать что угодно. Вперёд, наполните этот мир красками вашего воображения! 🌈✨
"""
    BLAST_WRITE_IN_DEFAULT_LANGUAGE = """
🚀 <b>Время для масштабной рассылки!</b> 🌍

Вы выбрали "Для всех" и это означает, что ваше сообщение достигнет каждого моего уголка, независимо от языковых предпочтений пользователей. Напишите ваше сообщение на русском, и я автоматически переведу его для всех наших пользователей Создайте сообщение, которое вдохновит, развлечет или проинформирует - ведь оно полетит к сердцам и умам людей по всему миру.

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

✨ Выбери тип подписки, на который хочешь дать доступ:
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
    CHATGPT = '💭 ChatGPT'
    CHATGPT3_TURBO = '✉️ ChatGPT 3.5 Turbo'
    CHATGPT4_OMNI_MINI = '✉️ ChatGPT 4.0 Omni Mini'
    CHATGPT4_TURBO = '🧠 ChatGPT 4.0 Turbo'
    CHATGPT4_OMNI = '💥 ChatGPT 4.0 Omni'
    CHAT_GPT_O_1_MINI = '🧩 ChatGPT o1-mini'
    CHAT_GPT_O_1_PREVIEW = '🧪 ChatGPT o1-preview'
    CLAUDE = '📄 Claude'
    CLAUDE_3_HAIKU = '📜 Claude 3.5 Haiku'
    CLAUDE_3_SONNET = '💫 Claude 3.5 Sonnet'
    CLAUDE_3_OPUS = '🚀 Claude 3.0 Opus'
    GEMINI = '✨ Gemini'
    GEMINI_1_FLASH = '🏎 Gemini 1.5 Flash'
    GEMINI_1_PRO = '💼 Gemini 1.5 Pro'
    GEMINI_1_ULTRA = '🛡️ Gemini 1.0 Ultra'
    DALL_E = '👨‍🎨 DALL-E'
    MIDJOURNEY = '🎨 Midjourney'
    STABLE_DIFFUSION = '🎆 Stable Diffusion 3.5'
    FLUX = '🫐 Flux 1.1 Pro'
    PHOTOSHOP_AI = '🪄 Photoshop AI'
    FACE_SWAP = '📷️ FaceSwap'
    MUSIC_GEN = '🎺 MusicGen'
    SUNO = '🎸 Suno'
    MODE: str
    CHOOSE_CHATGPT_MODEL: str
    CHOOSE_CLAUDE_MODEL: str
    CHOOSE_GEMINI_MODEL: str
    SWITCHED_TO_AI_SETTINGS: str
    SWITCHED_TO_AI_INFO: str
    SWITCHED_TO_AI_EXAMPLES: str
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
    FILE_TOO_BIG_ERROR: str

    # Examples
    CHATGPT4_OMNI_EXAMPLE: str
    CLAUDE_3_SONNET_EXAMPLE: str
    GEMINI_1_PRO_EXAMPLE: str
    MIDJOURNEY_EXAMPLE: str
    SUNO_EXAMPLE: str
    EXAMPLE_INFO: str

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
    STRIPE_PAYMENT_METHOD: str
    TELEGRAM_STARS_PAYMENT_METHOD: str
    CRYPTO_PAYMENT_METHOD: str
    CHOOSE_PAYMENT_METHOD: str
    PROCEED_TO_PAY: str
    MONTHLY: str
    YEARLY: str

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
    MIN_ERROR: str
    MAX_ERROR: str
    VALUE_ERROR: str
    PACKAGE_SUCCESS: str
    PACKAGES_SUCCESS: str

    # Catalog
    MANAGE_CATALOG: str
    CATALOG: str
    CATALOG_DIGITAL_EMPLOYEES: str
    CATALOG_DIGITAL_EMPLOYEES_INFO: str
    CATALOG_PROMPTS: str
    CATALOG_PROMPTS_CHOOSE_MODEL_TYPE: str
    CATALOG_PROMPTS_CHOOSE_CATEGORY: str
    CATALOG_PROMPTS_CHOOSE_SUBCATEGORY: str

    @staticmethod
    def catalog_prompts_choose_prompt(prompts: list[Prompt]):
        raise NotImplementedError

    @staticmethod
    def catalog_prompts_info_prompt(prompt: Prompt, products: list[Product]):
        raise NotImplementedError

    CATALOG_PROMPTS_GET_SHORT_PROMPT: str
    CATALOG_PROMPTS_GET_LONG_PROMPT: str
    CATALOG_PROMPTS_GET_EXAMPLES: str
    CATALOG_PROMPTS_COPY: str

    @staticmethod
    def catalog_prompts_examples(products: list[Product]):
        raise NotImplementedError

    CATALOG_FORBIDDEN_ERROR: str
    CATALOG_MANAGE = """
🎭 <b>Управление каталогом ролей</b> 🌟

Здесь ты можешь:
🔧 <b>Добавить новую роль</b>: Дай волю фантазии и создай уникального помощника!
✏️ <b>Редактировать существующие</b>: Привнеси своё видение в уже знакомых персонажей.
🗑️ <b>Удалить ненужное</b>: Иногда прощание - это начало чего-то нового.

Выбери своё приключение в этом мире AI-талантов! 🚀
"""
    CREATE_ROLE = 'Создать роль'
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
    EDIT_ROLE_NAME = 'Изменить имя 🖌'
    EDIT_ROLE_DESCRIPTION = 'Изменить описание 🖌'
    EDIT_ROLE_INSTRUCTION = 'Изменить инструкцию 🖌'
    EDIT_ROLE_PHOTO = 'Изменить фотографию 🖼'
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
    CREATE_PACKAGE = 'Создать новый пакет'
    EDIT_PACKAGE = 'Редактировать существующий пакет'
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
    FACE_SWAP_MANAGE_EDIT_CHOOSE_GENDER = 'Выбери пол:'
    FACE_SWAP_MANAGE_EDIT_CHOOSE_PACKAGE = 'Выбери пакет:'
    FACE_SWAP_MANAGE_EDIT = """
🎨 <b>Время творить! Вы выбрали пакет для редактирования</b> 🖌️

🔧 Возможности редактирования:
- <b>Изменить видимость</b> - Сделайте пакет видимым или скрытым для пользователей.
- <b>Просмотреть картинки</b> - Оцените, какие шедевры уже есть в пакете.
- <b>Добавить новую картинку</b> - Пора внести свежую краску и новые лица!

🚀 Готовы к изменениям? Ваше творчество вдохнет новую жизнь в этот пакет. Пусть каждая генерация будет уникальной и запоминающейся!
"""
    FACE_SWAP_MANAGE_CHANGE_STATUS = 'Изменить видимость 👁'
    FACE_SWAP_MANAGE_SHOW_PICTURES = 'Просмотреть картинки 🖼'
    FACE_SWAP_MANAGE_ADD_NEW_PICTURE = 'Добавить новую картинку 👨‍🎨'
    FACE_SWAP_MANAGE_ADD_NEW_PICTURE_NAME = 'Отправьте мне название будущего изображения на английском языке в CamelCase, например "ContentMaker"'
    FACE_SWAP_MANAGE_ADD_NEW_PICTURE_IMAGE = 'Теперь, отправьте мне фотографию'
    FACE_SWAP_MANAGE_EXAMPLE_PICTURE = 'Пример генерации 🎭'
    FACE_SWAP_MANAGE_EDIT_SUCCESS = """
🌟 <b>Пакет успешно отредактирован!</b> 🎉

👏 Браво, админ! Ваши изменения успешно применены. Пакет FaceSwap теперь обновлён и ещё более прекрасен

🚀 Готовы к новым приключениям? Ваша креативность и умение управлять пакетами делают мир FaceSwap ещё ярче и интереснее. Продолжайте творить и вдохновлять пользователей своими уникальными идеями!
"""
    FACE_SWAP_PUBLIC = 'Видно всем 🔓'
    FACE_SWAP_PRIVATE = 'Видно админам 🔒'

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
    TECH_SUPPORT: str
    BACK: str
    CLOSE: str
    CANCEL: str
    APPROVE: str
    IMAGE: str
    DOCUMENT: str
    AUDIO: str
    VIDEO: str
    SKIP: str

    TERMS_LINK: str

    @staticmethod
    def statistics_users(
        period: str,
        subscription_products: dict[str, str],
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
        count_subscription_users: dict,
        count_subscription_users_before: dict,
    ):
        is_all_time = period == 'всё время'

        subscription_info = ''
        for index, (key, name) in enumerate(subscription_products.items()):
            is_last = index == len(subscription_products) - 1
            left_part = '┣' if not is_last else '┗'
            right_part = '\n' if not is_last else ''
            subscription_info += f'    {left_part} <b>{name}:</b> {count_subscription_users[key]} {calculate_percentage_difference(is_all_time, count_subscription_users[key], count_subscription_users_before[key])}{right_part}'

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
{subscription_info}
━ 6️⃣ <b>{'Заблокировали бота' if is_all_time else 'Заблокировали бота из пришедших'}:</b> {count_blocked_users} {calculate_percentage_difference(is_all_time, count_blocked_users, count_blocked_users_before)}

🔍 Это всё, что нужно знать о пользователей на данный момент 🚀
"""

    @staticmethod
    def statistics_text_models(
        period: str,
        text_products: dict[str, str],
        count_all_transactions: dict,
        count_all_transactions_before: dict,
    ):
        is_all_time = period == 'всё время'

        all_success_requests = 0
        all_success_requests_before = 0
        all_fail_requests = 0
        all_fail_requests_before = 0
        all_example_requests = 0
        all_example_requests_before = 0
        all_requests = 0
        all_requests_before = 0

        text_info = ''
        for index, (text_product_id, text_product_name) in enumerate(text_products.items()):
            all_success_requests += count_all_transactions[text_product_id]['SUCCESS']
            all_success_requests_before += count_all_transactions_before[text_product_id]['SUCCESS']
            all_fail_requests += count_all_transactions[text_product_id]['FAIL']
            all_fail_requests_before += count_all_transactions_before[text_product_id]['FAIL']
            all_example_requests += count_all_transactions[text_product_id]['EXAMPLE']
            all_example_requests_before += count_all_transactions_before[text_product_id]['EXAMPLE']
            all_requests += count_all_transactions[text_product_id]['ALL']
            all_requests_before += count_all_transactions_before[text_product_id]['ALL']

            emoji_number = ''.join(f'{digit}\uFE0F\u20E3' for digit in str(index + 1))
            text_info += f"""━ {emoji_number} <b>{text_product_name}:</b>
    ┣ ✅ Удачных: {count_all_transactions[text_product_id]['SUCCESS']} {calculate_percentage_difference(is_all_time, count_all_transactions[text_product_id]['SUCCESS'], count_all_transactions_before[text_product_id]['SUCCESS'])}
    ┣ ❌ С ошибкой: {count_all_transactions[text_product_id]['FAIL']} {calculate_percentage_difference(is_all_time, count_all_transactions[text_product_id]['FAIL'], count_all_transactions_before[text_product_id]['FAIL'])}
    ┣ 🚀 Примеров: {count_all_transactions[text_product_id]['EXAMPLE']} {calculate_percentage_difference(is_all_time, count_all_transactions[text_product_id]['EXAMPLE'], count_all_transactions_before[text_product_id]['EXAMPLE'])}
    ┗ 📝 Всего: {count_all_transactions[text_product_id]['ALL']} {calculate_percentage_difference(is_all_time, count_all_transactions[text_product_id]['ALL'], count_all_transactions_before[text_product_id]['ALL'])}
"""

        return f"""
#statistics #text_models

📊 <b>Статистика за {period} готова!</b>

🔤 <b>Текстовые модели</b>
{text_info}
━ <b>Резюме:</b>
    ┣ ✅ Удачных: {all_success_requests} {calculate_percentage_difference(is_all_time, all_success_requests, all_success_requests_before)}
    ┣ ❌ С ошибкой: {all_fail_requests} {calculate_percentage_difference(is_all_time, all_fail_requests, all_fail_requests_before)}
    ┣ 🚀 Примеров: {all_example_requests} {calculate_percentage_difference(is_all_time, all_example_requests, all_example_requests_before)}
    ┗ 📝 Всего: {all_requests} {calculate_percentage_difference(is_all_time, all_requests, all_requests_before)}

🔍 Это всё, что нужно знать о текстовых моделях на данный момент 🚀
"""

    @staticmethod
    def statistics_image_models(
        period: str,
        image_products: dict[str, str],
        count_all_transactions: dict,
        count_all_transactions_before: dict,
    ):
        is_all_time = period == 'всё время'

        all_success_requests = 0
        all_success_requests_before = 0
        all_fail_requests = 0
        all_fail_requests_before = 0
        all_example_requests = 0
        all_example_requests_before = 0
        all_requests = 0
        all_requests_before = 0

        image_info = ''
        for index, (image_product_id, image_product_name) in enumerate(image_products.items()):
            all_success_requests += count_all_transactions[image_product_id]['SUCCESS']
            all_success_requests_before += count_all_transactions_before[image_product_id]['SUCCESS']
            all_fail_requests += count_all_transactions[image_product_id]['FAIL']
            all_fail_requests_before += count_all_transactions_before[image_product_id]['FAIL']
            all_example_requests += count_all_transactions[image_product_id]['EXAMPLE']
            all_example_requests_before += count_all_transactions_before[image_product_id]['EXAMPLE']
            all_requests += count_all_transactions[image_product_id]['ALL']
            all_requests_before += count_all_transactions_before[image_product_id]['ALL']

            emoji_number = ''.join(f'{digit}\uFE0F\u20E3' for digit in str(index + 1))
            image_info += f"""━ {emoji_number} <b>{image_product_name}:</b>
    ┣ ✅ Удачных: {count_all_transactions[image_product_id]['SUCCESS']} {calculate_percentage_difference(is_all_time, count_all_transactions[image_product_id]['SUCCESS'], count_all_transactions_before[image_product_id]['SUCCESS'])}
    ┣ ❌ С ошибкой: {count_all_transactions[image_product_id]['FAIL']} {calculate_percentage_difference(is_all_time, count_all_transactions[image_product_id]['FAIL'], count_all_transactions_before[image_product_id]['FAIL'])}
    ┣ 🚀 Примеров: {count_all_transactions[image_product_id]['EXAMPLE']} {calculate_percentage_difference(is_all_time, count_all_transactions[image_product_id]['EXAMPLE'], count_all_transactions_before[image_product_id]['EXAMPLE'])}
    ┗ 📝 Всего: {count_all_transactions[image_product_id]['ALL']} {calculate_percentage_difference(is_all_time, count_all_transactions[image_product_id]['ALL'], count_all_transactions_before[image_product_id]['ALL'])}
"""

        return f"""
#statistics #image_models

📊 <b>Статистика за {period} готова!</b>

🧑‍🎨 <b>Графические модели</b>
{image_info}
━ <b>Резюме:</b>
    ┣ ✅ Удачных: {all_success_requests} {calculate_percentage_difference(is_all_time, all_success_requests, all_success_requests_before)}
    ┣ ❌ С ошибкой: {all_fail_requests} {calculate_percentage_difference(is_all_time, all_fail_requests, all_fail_requests_before)}
    ┣ 🚀 Примеров: {all_example_requests} {calculate_percentage_difference(is_all_time, all_example_requests, all_example_requests_before)}
    ┗ 📝 Всего: {all_requests} {calculate_percentage_difference(is_all_time, all_requests, all_requests_before)}

🔍 Это всё, что нужно знать о графических моделях на данный момент 🚀
"""

    @staticmethod
    def statistics_music_models(
        period: str,
        music_products: dict[str, str],
        count_all_transactions: dict,
        count_all_transactions_before: dict,
    ):
        is_all_time = period == 'всё время'

        all_success_requests = 0
        all_success_requests_before = 0
        all_fail_requests = 0
        all_fail_requests_before = 0
        all_example_requests = 0
        all_example_requests_before = 0
        all_requests = 0
        all_requests_before = 0

        music_info = ''
        for index, (music_product_id, music_product_name) in enumerate(music_products.items()):
            all_success_requests += count_all_transactions[music_product_id]['SUCCESS']
            all_success_requests_before += count_all_transactions_before[music_product_id]['SUCCESS']
            all_fail_requests += count_all_transactions[music_product_id]['FAIL']
            all_fail_requests_before += count_all_transactions_before[music_product_id]['FAIL']
            all_example_requests += count_all_transactions[music_product_id]['EXAMPLE']
            all_example_requests_before += count_all_transactions_before[music_product_id]['EXAMPLE']
            all_requests += count_all_transactions[music_product_id]['ALL']
            all_requests_before += count_all_transactions_before[music_product_id]['ALL']

            emoji_number = ''.join(f'{digit}\uFE0F\u20E3' for digit in str(index + 1))
            music_info += f"""━ {emoji_number} <b>{music_product_name}:</b>
    ┣ ✅ Удачных: {count_all_transactions[music_product_id]['SUCCESS']} {calculate_percentage_difference(is_all_time, count_all_transactions[music_product_id]['SUCCESS'], count_all_transactions_before[music_product_id]['SUCCESS'])}
    ┣ ❌ С ошибкой: {count_all_transactions[music_product_id]['FAIL']} {calculate_percentage_difference(is_all_time, count_all_transactions[music_product_id]['FAIL'], count_all_transactions_before[music_product_id]['FAIL'])}
    ┣ 🚀 Примеров: {count_all_transactions[music_product_id]['EXAMPLE']} {calculate_percentage_difference(is_all_time, count_all_transactions[music_product_id]['EXAMPLE'], count_all_transactions_before[music_product_id]['EXAMPLE'])}
    ┗ 📝 Всего: {count_all_transactions[music_product_id]['ALL']} {calculate_percentage_difference(is_all_time, count_all_transactions[music_product_id]['ALL'], count_all_transactions_before[music_product_id]['ALL'])}
"""

        return f"""
#statistics #music_models

📊 <b>Статистика за {period} готова!</b>

🎺 <b>Музыкальные модели</b>
{music_info}
━ <b>Резюме:</b>
    ┣ ✅ Удачных: {all_success_requests} {calculate_percentage_difference(is_all_time, all_success_requests, all_success_requests_before)}
    ┣ ❌ С ошибкой: {all_fail_requests} {calculate_percentage_difference(is_all_time, all_fail_requests, all_fail_requests_before)}
    ┣ 🚀 Примеров: {all_example_requests} {calculate_percentage_difference(is_all_time, all_example_requests, all_example_requests_before)}
    ┗ 📝 Всего: {all_requests} {calculate_percentage_difference(is_all_time, all_requests, all_requests_before)}

🔍 Это всё, что нужно знать о музыкальных моделях на данный момент 🚀
"""

    @staticmethod
    def statistics_reactions(
        period: str,
        products_with_reactions: dict[str, str],
        count_reactions: dict,
        count_reactions_before: dict,
        count_feedbacks: dict,
        count_feedbacks_before: dict,
        count_games: dict,
        count_games_before: dict,
    ):
        is_all_time = period == 'всё время'

        all_liked = 0
        all_liked_before = 0
        all_disliked = 0
        all_disliked_before = 0
        all_none = 0
        all_none_before = 0

        reaction_info = ''
        for index, (product_with_reaction_id, product_with_reactions_name) in enumerate(
            products_with_reactions.items()):
            all_liked += count_reactions[product_with_reaction_id][GenerationReaction.LIKED]
            all_liked_before += count_reactions_before[product_with_reaction_id][GenerationReaction.LIKED]
            all_disliked += count_reactions[product_with_reaction_id][GenerationReaction.DISLIKED]
            all_disliked_before += count_reactions_before[product_with_reaction_id][GenerationReaction.DISLIKED]
            all_none += count_reactions[product_with_reaction_id][GenerationReaction.NONE]
            all_none_before += count_reactions_before[product_with_reaction_id][GenerationReaction.NONE]

            emoji_number = ''.join(f'{digit}\uFE0F\u20E3' for digit in str(index + 1))
            reaction_info += f"""━ {emoji_number} <b>{product_with_reactions_name}:</b>
    ┣ 👍 {count_reactions[product_with_reaction_id][GenerationReaction.LIKED]} {calculate_percentage_difference(is_all_time, count_reactions[product_with_reaction_id][GenerationReaction.LIKED], count_reactions_before[product_with_reaction_id][GenerationReaction.LIKED])}
    ┣ 👎 {count_reactions[product_with_reaction_id][GenerationReaction.DISLIKED]} {calculate_percentage_difference(is_all_time, count_reactions[product_with_reaction_id][GenerationReaction.DISLIKED], count_reactions_before[product_with_reaction_id][GenerationReaction.DISLIKED])}
    ┗ 🤷 {count_reactions[product_with_reaction_id][GenerationReaction.NONE]} {calculate_percentage_difference(is_all_time, count_reactions[product_with_reaction_id][GenerationReaction.NONE], count_reactions_before[product_with_reaction_id][GenerationReaction.NONE])}
"""

        feedback_statuses = [feedback_status for key, feedback_status in vars(FeedbackStatus).items() if
                             not key.startswith('__')]
        all_feedbacks = 0
        all_feedbacks_before = 0
        for feedback_status in feedback_statuses:
            all_feedbacks += count_feedbacks[feedback_status]
            all_feedbacks_before += count_feedbacks_before[feedback_status]

        game_types = [game_type for key, game_type in vars(GameType).items() if not key.startswith('__')]
        all_games = 0
        all_games_before = 0
        for game_type in game_types:
            all_games += count_games[game_type]
            all_games_before += count_games_before[game_type]

        return f"""
#statistics #reactions

📊 <b>Статистика за {period} готова!</b>

🧐 <b>Реакции</b>
{reaction_info}
━ <b>Резюме:</b>
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
        package_products: dict[str, str],
        count_credits: dict,
        count_credits_before: dict,
        count_all_transactions: dict,
        count_all_transactions_before: dict,
        count_activated_promo_codes: int,
        count_activated_promo_codes_before: int,
    ):
        is_all_time = period == 'всё время'

        all_bonuses = 0
        all_bonuses_before = 0
        credits_info = ''
        for index, (package_product_id, package_product_name) in enumerate(package_products.items()):
            all_bonuses += count_all_transactions[package_product_id]['BONUS']
            all_bonuses_before += count_all_transactions_before[package_product_id]['BONUS']

            is_last = index == len(package_products) - 1
            right_part = '\n' if not is_last else ''
            credits_info += f"    ┣ {package_product_name}: {count_all_transactions[package_product_id]['BONUS']} {calculate_percentage_difference(is_all_time, count_all_transactions[package_product_id]['BONUS'], count_all_transactions_before[package_product_id]['BONUS'])}{right_part}"

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
{credits_info}
    ┗ Всего: {all_bonuses} {calculate_percentage_difference(is_all_time, all_bonuses, all_bonuses_before)}
━ 3️⃣ <b>Промокоды:</b>
    ┗ Активировано: {count_activated_promo_codes} {calculate_percentage_difference(is_all_time, count_activated_promo_codes, count_activated_promo_codes_before)}

🔍 Это всё, что нужно знать о бонусах на данный момент 🚀
"""

    @staticmethod
    def statistics_expenses(
        period: str,
        ai_products: dict[str, str],
        tech_products: dict[str, str],
        subscription_products: dict[str, str],
        count_expense_money: dict,
        count_expense_money_before: dict,
    ):
        is_all_time = period == 'всё время'

        ai_info = ''
        for index, (ai_product_id, ai_product_name) in enumerate(ai_products.items()):
            is_last = index == len(ai_products) - 1
            left_part = '┣' if not is_last else '┗'
            right_part = '\n' if not is_last else ''
            ai_info += f"""    {left_part} {ai_product_name}:
        ┣ 💸 Средняя цена запроса: ${round(count_expense_money[ai_product_id]['AVERAGE_PRICE'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ai_product_id]['AVERAGE_PRICE'], count_expense_money_before[ai_product_id]['AVERAGE_PRICE'])}
        ┗ 💰 Всего: ${round(count_expense_money[ai_product_id]['ALL'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[ai_product_id]['ALL'], count_expense_money_before[ai_product_id]['ALL'])}{right_part}"""
        tech_info = ''
        for index, (tech_product_id, tech_product_name) in enumerate(tech_products.items()):
            is_last = index == len(tech_products) - 1
            left_part = '┣' if not is_last else '┗'
            right_part = '\n' if not is_last else ''
            tech_info += f"    {left_part} {tech_product_name}: ${round(count_expense_money[tech_product_id]['ALL'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[tech_product_id]['ALL'], count_expense_money_before[tech_product_id]['ALL'])}{right_part}"
        subscription_info = ''
        for index, (subscription_product_id, subscription_product_name) in enumerate(subscription_products.items()):
            is_last = index == len(subscription_products) - 1
            left_part = '┣' if not is_last else '┗'
            right_part = '\n' if not is_last else ''
            subscription_info += f"""    {left_part} <b>{subscription_product_name}:</b>
        ┣ 💸 Средняя цена подписчика: ${round(count_expense_money[subscription_product_id]['AVERAGE_PRICE'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[subscription_product_id]['AVERAGE_PRICE'], count_expense_money_before[subscription_product_id]['AVERAGE_PRICE'])}
        ┗ 💰 Всего: ${round(count_expense_money[subscription_product_id]['ALL'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money[subscription_product_id]['ALL'], count_expense_money_before[subscription_product_id]['ALL'])}{right_part}"""

        return f"""
#statistics #expenses

📊 <b>Статистика за {period} готова!</b>

📉 <b>Расходы</b>
━ 1️⃣ <b>AI модели:</b>
{ai_info}
━ 2️⃣ <b>Технические:</b>
{tech_info}
━ 3️⃣ <b>Подписчики:</b>
{subscription_info}
━ <b>Всего:</b> ${round(count_expense_money['ALL'], 4)} {calculate_percentage_difference(is_all_time, count_expense_money['ALL'], count_expense_money_before['ALL'])}

🔍 Это всё, что нужно знать о расходах на данный момент 🚀
"""

    @staticmethod
    def statistics_incomes(
        period: str,
        subscription_products: dict[str, str],
        package_products: dict[str, str],
        count_income_money: dict,
        count_income_money_before: dict,
    ):
        is_all_time = period == 'всё время'

        subscription_info = ''
        for index, (subscription_product_id, subscription_product_name) in enumerate(subscription_products.items()):
            is_last = index == len(subscription_products) - 1
            right_part = '\n' if not is_last else ''
            subscription_info += f"    ┣ {subscription_product_name}: {round(count_income_money[subscription_product_id], 2)}₽ {calculate_percentage_difference(is_all_time, count_income_money[subscription_product_id], count_income_money_before[subscription_product_id])}{right_part}"
        package_info = ''
        for index, (package_product_id, package_product_name) in enumerate(package_products.items()):
            is_last = index == len(package_products) - 1
            right_part = '\n' if not is_last else ''
            package_info += f"    ┣ {package_product_name}: {round(count_income_money[package_product_id], 2)}₽ {calculate_percentage_difference(is_all_time, count_income_money[package_product_id], count_income_money_before[package_product_id])}{right_part}"

        return f"""
#statistics #incomes

📊 <b>Статистика за {period} готова!</b>

📈 <b>Доходы</b>
━ 1️⃣ <b>Подписки:</b>
{subscription_info}
    ┗ Всего: {round(count_income_money['SUBSCRIPTION_ALL'], 2)}₽ {calculate_percentage_difference(is_all_time, count_income_money['SUBSCRIPTION_ALL'], count_income_money_before['SUBSCRIPTION_ALL'])}
━ 2️⃣ <b>Пакеты:</b>
{package_info}
    ┗ Всего: {round(count_income_money['PACKAGES_ALL'], 2)}₽ {calculate_percentage_difference(is_all_time, count_income_money['PACKAGES_ALL'], count_income_money_before['PACKAGES_ALL'])}
━ <b>Средний чек:</b> {round(count_income_money['AVERAGE_PRICE'], 2)}₽ {calculate_percentage_difference(is_all_time, count_income_money['AVERAGE_PRICE'], count_income_money_before['AVERAGE_PRICE'])}
━ <b>Всего:</b> {round(count_income_money['ALL'], 2)}₽ {calculate_percentage_difference(is_all_time, count_income_money['ALL'], count_income_money_before['ALL'])}
━ <b>Вал:</b> {round(count_income_money['VAL'], 2)}₽ {calculate_percentage_difference(is_all_time, count_income_money['VAL'], count_income_money_before['VAL'])}

🔍 Это всё, что нужно знать о доходах на данный момент. Вперёд, к новым достижениям! 🚀
"""

    # Blast
    @staticmethod
    def blast_confirmation(
        blast_letters: dict,
    ):
        letters = ''
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
        role_names: dict,
        role_descriptions: dict,
        role_instructions: dict,
    ):
        names = ''
        for i, (language_code, name) in enumerate(role_names.items()):
            names += f'{language_code}: {name}'
            names += '\n' if i < len(role_names.items()) - 1 else ''
        descriptions = ''
        for i, (language_code, description) in enumerate(role_descriptions.items()):
            descriptions += f'{language_code}: {description}'
            descriptions += '\n' if i < len(role_descriptions.items()) - 1 else ''
        instructions = ''
        for i, (language_code, instruction) in enumerate(role_instructions.items()):
            instructions += f'{language_code}: {instruction}'
            instructions += '\n' if i < len(role_instructions.items()) - 1 else ''

        return f"""
🎩 <b>Вот что вы создали:</b>

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
        role_names: dict[LanguageCode, str],
        role_descriptions: dict[LanguageCode, str],
        role_instructions: dict[LanguageCode, str],
    ):
        names = ''
        for i, (language_code, name) in enumerate(role_names.items()):
            names += f'{language_code}: {name}'
            names += '\n' if i < len(role_names.items()) - 1 else ''
        descriptions = ''
        for i, (language_code, description) in enumerate(role_descriptions.items()):
            descriptions += f'{language_code}: {description}'
            descriptions += '\n' if i < len(role_descriptions.items()) - 1 else ''
        instructions = ''
        for i, (language_code, instruction) in enumerate(role_instructions.items()):
            instructions += f'{language_code}: {instruction}'
            instructions += '\n' if i < len(role_instructions.items()) - 1 else ''

        return f"""
🎨 <b>Настройка роли</b> 🖌️

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
        package_names: dict,
    ):
        names = ''
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
    def purchase_minimal_price(currency: Currency, current_price: str):
        raise NotImplementedError

    @staticmethod
    def profile(
        subscription_name: str,
        subscription_status: SubscriptionStatus,
        gender: UserGender,
        current_model: Model,
        current_model_version: str,
        current_currency: Currency,
        renewal_date,
    ) -> str:
        raise NotImplementedError

    @staticmethod
    def profile_quota(
        subscription_limits: dict,
        daily_limits,
        additional_usage_quota,
        hours_before_limit_update: int,
        minutes_before_limit_update: int,
    ) -> str:
        raise NotImplementedError

    @staticmethod
    def notify_about_quota(
        subscription_limits: dict,
    ) -> str:
        raise NotImplementedError

    # Payment
    @staticmethod
    def payment_description_subscription(user_id: str, name: str):
        raise NotImplementedError

    @staticmethod
    def payment_description_renew_subscription(user_id: str, name: str):
        raise NotImplementedError

    @staticmethod
    def subscribe(subscriptions: list[Product], currency: Currency, user_discount: int) -> str:
        raise NotImplementedError

    @staticmethod
    def cycles_subscribe() -> str:
        raise NotImplementedError

    @staticmethod
    def confirmation_subscribe(
        name: str,
        category: ProductCategory,
        currency: Currency,
        price: Union[str, int, float],
    ) -> str:
        raise NotImplementedError

    @staticmethod
    def payment_description_package(user_id: str, package_name: str, package_quantity: int):
        raise NotImplementedError

    @staticmethod
    def payment_description_cart(user_id: str):
        raise NotImplementedError

    @staticmethod
    def package(currency: Currency, cost: str) -> str:
        raise NotImplementedError

    @staticmethod
    def choose_min(name: str) -> str:
        raise NotImplementedError

    @staticmethod
    async def shopping_cart(currency: Currency, cart_items: list[dict], discount: int):
        raise NotImplementedError

    @staticmethod
    def confirmation_package(package_name: str, package_quantity: int, currency: Currency, price: str) -> str:
        raise NotImplementedError

    @staticmethod
    async def confirmation_cart(cart_items: list[dict], currency: Currency, price: float) -> str:
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
    def switched(model_name: str, model_type: ModelType, model_info: dict):
        raise NotImplementedError

    @staticmethod
    def requests_recommendations() -> list[str]:
        raise NotImplementedError

    @staticmethod
    def image_recommendations() -> list[str]:
        raise NotImplementedError

    @staticmethod
    def music_recommendations() -> list[str]:
        raise NotImplementedError

    @staticmethod
    def photoshop_ai_actions() -> list[str]:
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
            'Вызываю кибернетических уток, чтобы ускорить процесс. Кря-кря, и данные у нас! 🦆💻',
            'Использую тайные заклинания кода, чтобы вызволить вашу статистику из пучины данных. Абракадабра! 🧙‍💾',
            'Таймер установлен, чайник на плите. Пока я готовлю чай, данные собираются сами! ☕📊',
            'Подключаюсь к космическим спутникам, чтобы найти нужную статистику. Вот это звёздный поиск! 🛰️✨',
            'Зову на помощь армию пикселей. Они уже маршируют сквозь строки кода, чтобы доставить вам данные! 🪖🖥️',
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
            return f'https://t.me/share/url?url=https://t.me/GPTsTurboBot?start=referral-{user_id}'
        return f'https://t.me/GPTsTurboBot?start=referral-{user_id}'
