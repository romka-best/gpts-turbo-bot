from typing import Protocol, TypedDict, Dict

from bot.database.models.common import Currency, RoleName
from bot.database.models.package import PackageType
from bot.database.models.subscription import SubscriptionType, SubscriptionPeriod, Subscription
from bot.database.models.transaction import TransactionType, ServiceType
from bot.database.models.user import UserGender


class Role(TypedDict):
    name: str
    description: str
    instruction: str


class Texts(Protocol):
    START: str
    COMMANDS: str
    COMMANDS_ADMIN = """
----------

👨‍💻👩‍💻 <b>Команды для админа</b>:
😇 /create_promo_code - <b>Создать промокод</b>
📊 /statistics - <b>Просмотр статистики</b>
"""

    # Feedback
    FEEDBACK: str
    FEEDBACK_SUCCESS: str

    # Profile
    TELL_ME_YOUR_GENDER: str
    YOUR_GENDER: str
    UNSPECIFIED: str
    MALE: str
    FEMALE: str
    SEND_ME_YOUR_PICTURE: str
    CHANGE_PHOTO: str
    CHANGE_PHOTO_SUCCESS: str
    CHANGE_GENDER: str

    # Language
    LANGUAGE: str
    CHOOSE_LANGUAGE: str

    # Promo code
    PROMO_CODE_INFO: str
    PROMO_CODE_INFO_ADMIN = """
🔑 <b>Время создать магию с промокодами!</b> ✨

Выбери, для чего ты хочешь создать промокод:
🌠 <b>Подписка</b> - открой доступ к эксклюзивным функциям и контенту.
🎨 <b>Пакет</b> - добавь специальные возможности для использования AI.

Нажми на нужную кнопку и приступим к созданию! 🚀
"""
    PROMO_CODE_SUCCESS: str
    PROMO_CODE_SUCCESS_ADMIN = """
🌟 Вау!

Твой <b>промокод успешно создан</b> и готов к путешествию в карманы наших пользователей. 🚀
Этот маленький кодик обязательно принесёт радость кому-то там!

🎉 Поздравляю, ты настоящий волшебник промокодов!
"""
    PROMO_CODE_CHOOSE_SUBSCRIPTION_ADMIN = """
🌟 <b>Выбираем подписку для промокода!</b> 🎁

Выбери тип подписки, на который хочешь дать доступ:
- <b>STANDARD</b> ⭐
- <b>VIP</b> 🔥
- <b>PLATINUM</b> 💎

Выбери и нажми, чтобы создать волшебный ключ доступа! ✨
"""
    PROMO_CODE_CHOOSE_PACKAGE_ADMIN = """
TODO
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

Выбирай кнопку и вперёд, к знаниям! 🕵️‍♂️🔍
"""

    # AI
    MODE: str
    INFO: str
    ALREADY_MAKE_REQUEST: str
    READY_FOR_NEW_REQUEST: str
    CONTINUE_GENERATING: str
    REACHED_USAGE_LIMIT: str
    IMAGE_SUCCESS: str

    # Settings
    SETTINGS: str
    SHOW_NAME_OF_THE_CHAT: str
    SHOW_USAGE_QUOTA_IN_MESSAGES: str
    TURN_ON_VOICE_MESSAGES_FROM_RESPONDS: str

    # Voice
    VOICE_MESSAGES_FORBIDDEN: str

    # Subscription
    MONTH_1: str
    MONTHS_3: str
    MONTHS_6: str
    DISCOUNT: str
    NO_DISCOUNT: str
    SUBSCRIPTION_SUCCESS: str
    SUBSCRIPTION_RESET: str
    SUBSCRIPTION_END: str

    # Package
    GPT3_REQUESTS: str
    GPT3_REQUESTS_DESCRIPTION: str
    GPT4_REQUESTS: str
    GPT4_REQUESTS_DESCRIPTION: str
    THEMATIC_CHATS: str
    THEMATIC_CHATS_DESCRIPTION: str
    DALLE3_REQUESTS: str
    DALLE3_REQUESTS_DESCRIPTION: str
    FACE_SWAP_REQUESTS: str
    FACE_SWAP_REQUESTS_DESCRIPTION: str
    ACCESS_TO_CATALOG: str
    ACCESS_TO_CATALOG_DESCRIPTION: str
    ANSWERS_AND_REQUESTS_WITH_VOICE_MESSAGES: str
    ANSWERS_AND_REQUESTS_WITH_VOICE_MESSAGES_DESCRIPTION: str
    FAST_ANSWERS: str
    FAST_ANSWERS_DESCRIPTION: str
    MIN_ERROR: str
    VALUE_ERROR: str
    PACKAGE_SUCCESS: str

    # Catalog
    CATALOG: str
    CATALOG_FORBIDDEN_ERROR: str
    PERSONAL_ASSISTANT: Role
    TUTOR: Role
    LANGUAGE_TUTOR: Role
    CREATIVE_WRITER: Role
    TECHNICAL_ADVISOR: Role
    MARKETER: Role
    SMM_SPECIALIST: Role
    CONTENT_SPECIALIST: Role
    DESIGNER: Role
    SOCIAL_MEDIA_PRODUCER: Role
    LIFE_COACH: Role
    ENTREPRENEUR: Role

    # Chats
    DEFAULT_CHAT_TITLE: str
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

    # Face swap
    CHOOSE_YOUR_PACKAGE: str
    GENERATIONS_IN_PACKAGES_ENDED: str
    FACE_SWAP_MIN_ERROR: str
    FACE_SWAP_MAX_ERROR: str

    ERROR: str
    BACK: str
    CLOSE: str
    CANCEL: str

    @staticmethod
    def statistics(period: str,
                   count_all_users: int,
                   count_activated_users: int,
                   count_subscription_users: Dict,
                   count_income_transactions: Dict,
                   count_expense_transactions: Dict,
                   count_income_transactions_total: int,
                   count_expense_transactions_total: int,
                   count_transactions_total: int,
                   count_expense_money: Dict,
                   count_income_money: Dict,
                   count_income_subscriptions_total_money: float,
                   count_income_packages_total_money: float,
                   count_income_total_money: float,
                   count_expense_total_money: float,
                   count_total_money: float,
                   count_chats_usage: Dict,
                   count_face_swap_usage: Dict) -> str:
        emojis = Subscription.get_emojis()
        face_swap_info = ""
        for face_swap_key, face_swap_value in count_face_swap_usage.items():
            if face_swap_key != 'ALL':
                face_swap_info += f"\n    - <b>{face_swap_key}:</b> {face_swap_value}"

        return f"""
📈 <b>Статистика за {period} готова!</b>

👤 <b>Пользователи</b>
1️⃣ <b>{'Всего пользователей' if period == 'всё время' else 'Новых пользователей'}:</b> {count_all_users}
2️⃣ <b>Из них, пользователи, оплатившие хоть раз:</b> {count_activated_users}
3️⃣ <b>Из них, пользователи-подписчики:</b>
    - <b>{SubscriptionType.FREE}:</b> {count_subscription_users[SubscriptionType.FREE]}
    - <b>{SubscriptionType.STANDARD} {emojis[SubscriptionType.STANDARD]}:</b> {count_subscription_users[SubscriptionType.STANDARD]}
    - <b>{SubscriptionType.VIP} {emojis[SubscriptionType.VIP]}:</b> {count_subscription_users[SubscriptionType.VIP]}
    - <b>{SubscriptionType.PLATINUM} {emojis[SubscriptionType.PLATINUM]}:</b> {count_subscription_users[SubscriptionType.PLATINUM]}

💰 <b>Финансы</b>
<span class="tg-spoiler">
4️⃣ <b>Транзакции:</b>
    ➖ <b>{TransactionType.EXPENSE}:</b> {count_expense_transactions_total}
    - <b>{ServiceType.GPT3}:</b> {count_expense_transactions[ServiceType.GPT3]}
    - <b>{ServiceType.GPT4}:</b> {count_expense_transactions[ServiceType.GPT4]}
    - <b>{ServiceType.DALLE3}:</b> {count_expense_transactions[ServiceType.DALLE3]}
    - <b>{ServiceType.FACE_SWAP}:</b> {count_expense_transactions[ServiceType.FACE_SWAP]}
    - <b>{ServiceType.VOICE_MESSAGES}:</b> {count_expense_transactions[ServiceType.VOICE_MESSAGES]}

    ➕ <b>{TransactionType.INCOME}:</b> {count_income_transactions_total}
    - <b>{ServiceType.GPT3}:</b> {count_income_transactions[ServiceType.GPT3]}
    - <b>{ServiceType.GPT4}:</b> {count_income_transactions[ServiceType.GPT4]}
    - <b>{ServiceType.DALLE3}:</b> {count_income_transactions[ServiceType.DALLE3]}
    - <b>{ServiceType.FACE_SWAP}:</b> {count_income_transactions[ServiceType.FACE_SWAP]}
    - <b>{ServiceType.ADDITIONAL_CHATS}:</b> {count_income_transactions[ServiceType.ADDITIONAL_CHATS]}
    - <b>{ServiceType.ACCESS_TO_CATALOG}:</b> {count_income_transactions[ServiceType.ACCESS_TO_CATALOG]}
    - <b>{ServiceType.VOICE_MESSAGES}:</b> {count_income_transactions[ServiceType.VOICE_MESSAGES]}
    - <b>{ServiceType.FAST_MESSAGES}:</b> {count_income_transactions[ServiceType.FAST_MESSAGES]}
    - <b>{ServiceType.STANDARD}:</b> {count_income_transactions[ServiceType.STANDARD]}
    - <b>{ServiceType.VIP}:</b> {count_income_transactions[ServiceType.VIP]}
    - <b>{ServiceType.PLATINUM}:</b> {count_income_transactions[ServiceType.PLATINUM]}

    - <b>Всего:</b> {count_transactions_total}
5️⃣ <b>Расходы:</b>
   - <b>{ServiceType.GPT3}:</b> {count_expense_money[ServiceType.GPT3]}$
   - <b>{ServiceType.GPT4}:</b> {count_expense_money[ServiceType.GPT4]}$
   - <b>{ServiceType.DALLE3}:</b> {count_expense_money[ServiceType.DALLE3]}$
   - <b>{ServiceType.FACE_SWAP}:</b> {count_expense_money[ServiceType.FACE_SWAP]}$
   - <b>{ServiceType.VOICE_MESSAGES}:</b> {count_expense_money[ServiceType.VOICE_MESSAGES]}$
   - <b>Всего:</b> {count_expense_total_money}$
6️⃣ <b>Доходы:</b>
    💳 <b>Подписки:</b> {count_income_subscriptions_total_money}₽
    - <b>{ServiceType.STANDARD} {emojis[ServiceType.STANDARD]}:</b> {count_income_money[ServiceType.STANDARD]}₽
    - <b>{ServiceType.VIP} {emojis[ServiceType.VIP]}:</b> {count_income_money[ServiceType.VIP]}₽
    - <b>{ServiceType.PLATINUM} {emojis[ServiceType.PLATINUM]}:</b> {count_income_money[ServiceType.PLATINUM]}₽

    💵 <b>Пакеты:</b> {count_income_packages_total_money}₽
    - <b>{ServiceType.GPT3}:</b> {count_income_money[ServiceType.GPT3]}₽
    - <b>{ServiceType.GPT4}:</b> {count_income_money[ServiceType.GPT4]}₽
    - <b>{ServiceType.DALLE3}:</b> {count_income_money[ServiceType.DALLE3]}₽
    - <b>{ServiceType.FACE_SWAP}:</b> {count_income_money[ServiceType.FACE_SWAP]}₽
    - <b>{ServiceType.ADDITIONAL_CHATS}:</b> {count_income_money[ServiceType.ADDITIONAL_CHATS]}₽
    - <b>{ServiceType.ACCESS_TO_CATALOG}:</b> {count_income_money[ServiceType.ACCESS_TO_CATALOG]}₽
    - <b>{ServiceType.VOICE_MESSAGES}:</b> {count_income_money[ServiceType.VOICE_MESSAGES]}₽
    - <b>{ServiceType.FAST_MESSAGES}:</b> {count_income_money[ServiceType.FAST_MESSAGES]}₽

    - <b>Всего:</b> {count_income_total_money}₽
7️⃣ <b>Вал:</b> {count_total_money}₽
</span>
💬 <b>Созданные чаты</b>
    - <b>{RoleName.PERSONAL_ASSISTANT}:</b> {count_chats_usage[RoleName.PERSONAL_ASSISTANT]}
    - <b>{RoleName.TUTOR}:</b> {count_chats_usage[RoleName.TUTOR]}
    - <b>{RoleName.LANGUAGE_TUTOR}:</b> {count_chats_usage[RoleName.LANGUAGE_TUTOR]}
    - <b>{RoleName.TECHNICAL_ADVISOR}:</b> {count_chats_usage[RoleName.TECHNICAL_ADVISOR]}
    - <b>{RoleName.MARKETER}:</b> {count_chats_usage[RoleName.MARKETER]}
    - <b>{RoleName.SMM_SPECIALIST}:</b> {count_chats_usage[RoleName.SMM_SPECIALIST]}
    - <b>{RoleName.CONTENT_SPECIALIST}:</b> {count_chats_usage[RoleName.CONTENT_SPECIALIST]}
    - <b>{RoleName.DESIGNER}:</b> {count_chats_usage[RoleName.DESIGNER]}
    - <b>{RoleName.SOCIAL_MEDIA_PRODUCER}:</b> {count_chats_usage[RoleName.SOCIAL_MEDIA_PRODUCER]}
    - <b>{RoleName.LIFE_COACH}:</b> {count_chats_usage[RoleName.LIFE_COACH]}
    - <b>{RoleName.ENTREPRENEUR}:</b> {count_chats_usage[RoleName.ENTREPRENEUR]}

    - <b>Всего:</b> {count_chats_usage['ALL']}
🎭 <b>Выбранные Face Swap</b>
    {face_swap_info}

    - <b>Всего:</b> {count_face_swap_usage['ALL']}

🔍 Это всё, что тебе нужно знать о текущем положении дел. Вперёд, к новым достижениям! 🚀
"""

    @staticmethod
    def profile(subscription_type: SubscriptionType,
                gender: UserGender,
                current_model: str,
                monthly_limits,
                additional_usage_quota) -> str:
        raise NotImplementedError

    # Subscription
    @staticmethod
    def subscribe(currency: Currency) -> str:
        raise NotImplementedError

    @staticmethod
    def choose_how_many_months_to_subscribe(subscription_type: SubscriptionType) -> str:
        raise NotImplementedError

    @staticmethod
    def cycles_subscribe() -> str:
        raise NotImplementedError

    @staticmethod
    def confirmation_subscribe(subscription_type: SubscriptionType, subscription_period: SubscriptionPeriod) -> str:
        raise NotImplementedError

    # Package
    @staticmethod
    def buy() -> str:
        raise NotImplementedError

    @staticmethod
    def choose_min(package_type: PackageType) -> str:
        raise NotImplementedError

    # Chats
    @staticmethod
    def chats(current_chat_name: str, total_chats: int, available_to_create_chats: int) -> str:
        raise NotImplementedError

    # Face swap
    @staticmethod
    def choose_face_swap_package(name: str, available_images: int, total_images: int, used_images: int) -> str:
        raise NotImplementedError

    @staticmethod
    def face_swap_package_forbidden(available_images: int) -> str:
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
