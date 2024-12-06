import logging
from datetime import datetime, timezone

from aiogram import Bot
from google.cloud.firestore_v1 import DELETE_FIELD

from bot.config import config
from bot.database.main import firebase
from bot.database.models.chat import Chat
from bot.database.models.common import (
    Model,
    ModelType,
    Quota,
    AspectRatio,
    SendType,
)
from bot.database.models.user import User, UserSettings
from bot.database.operations.chat.getters import get_chats
from bot.database.operations.product.getters import get_product_by_quota
from bot.database.operations.prompt.writers import write_prompt, write_prompt_category, write_prompt_subcategory
from bot.database.operations.role.getters import get_roles
from bot.database.operations.role.updaters import update_role
from bot.database.operations.user.getters import get_users
from bot.helpers.senders.send_message_to_admins_and_developers import send_message_to_admins_and_developers
from bot.locales.types import LanguageCode


async def migrate(bot: Bot):
    try:
        current_date = datetime.now(timezone.utc)

        roles = await get_roles()
        for role in roles:
            await update_role(role.id, {
                'photo': 'roles/PERSONAL_ASSISTANT.png',
                'name': DELETE_FIELD,
            })

        chats = await get_chats()
        for i in range(0, len(chats), config.BATCH_SIZE):
            batch = firebase.db.batch()
            chat_batch = chats[i:i + config.BATCH_SIZE]

            for chat in chat_batch:
                chat_ref = firebase.db.collection(Chat.COLLECTION_NAME).document(chat.id)
                batch.update(chat_ref, {
                    'role_id': config.DEFAULT_ROLE_ID.get_secret_value(),
                    'role': DELETE_FIELD,
                    'edited_at': current_date,
                })
            await batch.commit()

        users = await get_users()
        for i in range(0, len(users), config.BATCH_SIZE):
            batch = firebase.db.batch()
            user_batch = users[i:i + config.BATCH_SIZE]

            for user in user_batch:
                user_ref = firebase.db.collection(User.COLLECTION_NAME).document(user.id)

                user.settings[Model.DALL_E][UserSettings.ASPECT_RATIO] = AspectRatio.SQUARE
                user.settings[Model.DALL_E][UserSettings.SEND_TYPE] = SendType.IMAGE
                user.settings[Model.MIDJOURNEY][UserSettings.ASPECT_RATIO] = AspectRatio.SQUARE
                user.settings[Model.MIDJOURNEY][UserSettings.SEND_TYPE] = SendType.IMAGE
                user.settings[Model.STABLE_DIFFUSION][UserSettings.SEND_TYPE] = SendType.IMAGE
                user.settings[Model.STABLE_DIFFUSION][UserSettings.ASPECT_RATIO] = AspectRatio.SQUARE
                user.settings[Model.FLUX][UserSettings.SEND_TYPE] = SendType.IMAGE
                user.settings[Model.FLUX][UserSettings.ASPECT_RATIO] = AspectRatio.SQUARE
                user.settings[Model.FACE_SWAP][UserSettings.SEND_TYPE] = SendType.IMAGE
                user.settings[Model.FACE_SWAP][UserSettings.ASPECT_RATIO] = AspectRatio.CUSTOM
                user.settings[Model.PHOTOSHOP_AI][UserSettings.SEND_TYPE] = SendType.DOCUMENT
                user.settings[Model.PHOTOSHOP_AI][UserSettings.ASPECT_RATIO] = AspectRatio.CUSTOM
                batch.update(user_ref, {
                    'settings': user.settings,
                    'edited_at': current_date,
                })
            await batch.commit()

        await send_message_to_admins_and_developers(bot, '<b>First Database Migration Was Successful!</b> 🎉')
    except Exception as e:
        logging.exception(e)
        await send_message_to_admins_and_developers(bot, '<b>First Database Migration Was Not Successful!</b> 🚨')

    try:
        chat_gpt_omni_mini = await get_product_by_quota(Quota.CHAT_GPT4_OMNI_MINI)
        chat_gpt_omni = await get_product_by_quota(Quota.CHAT_GPT4_OMNI_MINI)
        chat_gpt_o1_mini = await get_product_by_quota(Quota.CHAT_GPT_O_1_MINI)
        chat_gpt_o1_preview = await get_product_by_quota(Quota.CHAT_GPT_O_1_PREVIEW)

        claude_3_haiku = await get_product_by_quota(Quota.CLAUDE_3_HAIKU)
        claude_3_sonnet = await get_product_by_quota(Quota.CLAUDE_3_SONNET)
        claude_3_opus = await get_product_by_quota(Quota.CLAUDE_3_OPUS)

        gemini_1_flash = await get_product_by_quota(Quota.GEMINI_1_FLASH)
        gemini_1_pro = await get_product_by_quota(Quota.GEMINI_1_PRO)
        gemini_1_ultra = await get_product_by_quota(Quota.GEMINI_1_ULTRA)

        dall_e = await get_product_by_quota(Quota.DALL_E)
        midjourney = await get_product_by_quota(Quota.MIDJOURNEY)
        stable_diffusion = await get_product_by_quota(Quota.STABLE_DIFFUSION)
        flux = await get_product_by_quota(Quota.FLUX)

        music_gen = await get_product_by_quota(Quota.MUSIC_GEN)
        suno = await get_product_by_quota(Quota.SUNO)

        # Prompts
        # Coding
        coding_category = await write_prompt_category(
            model_type=ModelType.TEXT,
            names={
                LanguageCode.RU: 'Кодинг 🧑‍💻',
                LanguageCode.EN: 'Coding 🧑‍💻',
            },
        )

        coding_frontend_subcategory = await write_prompt_subcategory(
            category_ids=[coding_category.id],
            names={
                LanguageCode.RU: 'Фронтенд Разработка 💻',
                LanguageCode.EN: 'Frontend Development 💻',
            },
        )
        await write_prompt(
            product_ids=[
                chat_gpt_omni_mini.id,
                chat_gpt_omni.id,
                chat_gpt_o1_mini.id,
                chat_gpt_o1_preview.id,
                claude_3_haiku.id,
                claude_3_sonnet.id,
                claude_3_opus.id,
                gemini_1_flash.id,
                gemini_1_pro.id,
                gemini_1_ultra.id,
            ],
            subcategory_ids=[coding_frontend_subcategory.id],
            names={
                LanguageCode.RU: 'JavaScript calculator for financial site',
                LanguageCode.EN: 'JavaScript калькулятор для финансового сайта',
            },
            short_prompts={
                LanguageCode.RU: """
Создай доступный калькулятор на JavaScript для финансового сайта. Включи основные функции, адаптивный дизайн и удобный интерфейс для пользователя.
""".strip(),
                LanguageCode.EN: """
Create an accessible JavaScript calculator for a finance website. Include essential features, responsive design, and user-friendly interface.
""".strip(),
            },
            long_prompts={
                LanguageCode.RU: """
Как Фронтенд Разработчик, тебе поручено создать калькулятор на JavaScript для финансового сайта, принадлежащего [Вашя Компания или Клиент]. Этот калькулятор должен позволять пользователям выполнять финансовые расчёты, такие как выплаты по кредиту, расчёт процентов или оценка роста инвестиций.

Для разработки эффективного калькулятора на JavaScript для финансового сайта включи детали в следующих областях:
- Тип калькулятора: [Определите конкретный тип финансового калькулятора, например, ипотечный калькулятор, калькулятор процентной ставки по сбережениям].
- Необходимые входные данные: [Перечислите данные, которые пользователь должен ввести для расчёта, такие как основная сумма, процентная ставка, срок кредита].
- Логика расчёта: [Опишите математическую формулу или логику, которую будет использовать калькулятор для вычисления результатов].
- Формат вывода: [Укажите, как результаты будут отображаться пользователю, например, в виде таблицы, графика или простого текста].
- Интерактивные элементы: [Опишите интерактивные элементы, такие как ползунки или поля ввода, которые будут у калькулятора].
- Обработка ошибок: [Разработайте механизм обработки ошибок для недопустимых входных данных или ошибок расчёта].
- Стилизация и дизайн: [Опишите аспекты стилизации и дизайна, чтобы калькулятор соответствовал эстетике сайта].
- Функции доступности: [Продумайте, как сделать калькулятор доступным, включая навигацию с клавиатуры и совместимость с программами чтения с экрана].
- Адаптивный дизайн: [Убедитесь, что калькулятор адаптивен и хорошо работает на различных устройствах и экранах].
- Тестирование и проверка: [Определите план тестирования и проверки функциональности калькулятора и его пользовательского интерфейса].

Требования к задаче:
- Определи функционал и тип финансовых расчётов, которые будет выполнять калькулятор.
- Разработай пользовательский интерфейс с полями ввода для необходимых данных.
- Реализуй логику расчётов с использованием JavaScript, обеспечив точность и эффективность.
- Отображай результаты в удобном для понимания формате.
- Добавь интерактивные элементы для повышения вовлечённости пользователей и точности ввода.
- Разработай механизмы обработки ошибок для недействительных или неполных данных.
- Примени CSS для стилизации, чтобы калькулятор визуально интегрировался с дизайном сайта.
- Добавь функции доступности, чтобы калькулятор был удобен для всех пользователей.
- Убедись, что калькулятор адаптивен и работает на разных устройствах.
- Проведи тщательное тестирование функциональности, удобства использования и адаптивности калькулятора.

Чек-лист лучших практик:
- Сделай пользовательский интерфейс простым и интуитивно понятным.
- Убедись, что результаты расчётов отображаются чётко и оперативно.
- Соблюдай лучшие практики веб-доступности и адаптивного дизайна.
- Проверяй ввод данных, чтобы избежать ошибок в расчётах.
- Тестируй калькулятор в разных браузерах и на разных устройствах для обеспечения совместимости.

Результат:
- Разработай полностью функциональный и удобный калькулятор на JavaScript для финансового сайта [Ваша Компании или Клиент]. Калькулятор должен точно выполнять указанные финансовые расчёты, предоставлять адаптивный и доступный пользовательский интерфейс и соответствовать общему дизайну и функциональности сайта.
""".strip(),
                LanguageCode.EN: """
As Frontend Developer, you are tasked with creating a JavaScript calculator for a financial website operated by [Your Company or Client]. This calculator should enable users to perform financial calculations, such as loan repayments, interest calculations, or investment growth estimations.

To develop an effective JavaScript calculator for the financial website, consider including specific details in these areas:
- Calculator Type: [Define the specific type of financial calculator you are developing, e.g., mortgage calculator, savings interest calculator]
- Required Inputs: [List the inputs required from the user to perform the calculations, such as principal amount, interest rate, loan term]
- Calculation Logic: [Describe the mathematical formula or logic that the calculator will use to compute the results]
- Output Format: [Specify how the results will be displayed to the user, such as in a table, graph, or simple text]
- Interactive Elements: [Detail any interactive elements, such as sliders or input fields, that the calculator will have]
- Error Handling: [Plan for error handling to address invalid inputs or calculation errors]
- Styling and Design: [Describe the desired styling and design aspects to ensure the calculator aligns with the website’s aesthetics]
- Accessibility Features: [Consider how to make the calculator accessible, including keyboard navigation and screen reader compatibility]
- Responsive Design: [Ensure the calculator is responsive and functions well on various devices and screen sizes]
- Testing and Validation: [Outline a plan for testing and validating the calculator’s functionality and user interface]

Task Requirements:
- Define the functionality and type of financial calculations the calculator will perform.
- Design a user interface with input fields for required data.
- Implement the calculation logic using JavaScript, ensuring accuracy and efficiency.
- Display the results in a user-friendly format that is easy to understand.
- Include interactive elements to enhance user engagement and input accuracy.
- Develop error handling mechanisms for invalid or incomplete inputs.
- Apply CSS styling to ensure the calculator visually integrates with the rest of the website.
- Incorporate accessibility features to make the calculator usable for all users.
- Ensure the calculator is responsive and functional on different devices.
- Thoroughly test the calculator for functionality, usability, and responsiveness.

Best Practices Checklist:
- Keep the user interface simple and intuitive.
- Ensure calculation results are presented clearly and promptly.
- Follow best practices for web accessibility and responsive design.
- Validate user input to prevent calculation errors.
- Test the calculator across different browsers and devices for compatibility.

Deliverable:
- Develop a fully functional and user-friendly JavaScript calculator for [Your Company or Client]'s financial website. The calculator should accurately perform the designated financial calculations, provide a responsive and accessible user experience, and align with the website's overall design and functionality
""".strip(),
            },
        )
        await write_prompt(
            product_ids=[
                chat_gpt_omni_mini.id,
                chat_gpt_omni.id,
                chat_gpt_o1_mini.id,
                chat_gpt_o1_preview.id,
                claude_3_haiku.id,
                claude_3_sonnet.id,
                claude_3_opus.id,
                gemini_1_flash.id,
                gemini_1_pro.id,
                gemini_1_ultra.id,
            ],
            subcategory_ids=[coding_frontend_subcategory.id],
            names={
                LanguageCode.RU: 'Разработка приложения [Тип Приложения] с адаптивным дизайном',
                LanguageCode.EN: 'Develop an [App Type] Application with Responsive Design',
            },
            short_prompts={
                LanguageCode.RU: """
Разработай адаптивное приложение [Тип Приложения] с понятной целью, приложение должно быть адаптированно для различных устройств. Используй подходящие стек, технологии и фреймворки, чтобы обеспечить оптимальный UX. Составь структурированный график, определи состав команды и бюджет для успешной реализации проекта, учитывая возможные вызовы и пути их решения.
""".strip(),
                LanguageCode.EN: """
Develop a responsive [App Type] application with a clear purpose, tailored for various devices. Leverage the right technologies and frameworks to ensure an optimal user experience. Outline a structured timeline, team composition, and budget to deliver the project successfully, while proactively addressing any potential challenges.
""".strip(),
            },
            long_prompts={
                LanguageCode.RU: """
Подготовь детальное предложение для разработки адаптивного приложения [Тип Приложения]. Включи следующую информацию:

- Обзор приложения: Опиши цель, ключевые функции и целевую аудиторию приложения [Тип Приложения].
- Технические требования: Укажи платформы, языки программирования, фреймворки и библиотеки, которые будут использоваться для разработки приложения.
- Подход к адаптивному дизайну: Объясни стратегию реализации адаптивного дизайна, который обеспечит оптимальный пользовательский опыт на различных устройствах и экранах.
- Ключевые этапы и сроки: Предоставь общий график проекта с основными этапами разработки и развёртывания приложения.
- Состав команды: Опиши роли и обязанности участников команды, включая необходимые навыки и компетенции.
- Оценка бюджета: Предоставь подробное распределение бюджета, включая расходы на разработку, дизайн и дополнительные ресурсы или инструменты.
- Возможные проблемы и стратегии их решения: Определи возможные риски или вызовы, связанные с проектом, и опиши планы по их устранению.
""".strip(),
                LanguageCode.EN: """
Provide a detailed proposal for developing a responsive [App Type] application. Include the following information:

- Application Overview: Describe the purpose, key features, and target audience of the [App Type] application.
- Technical Requirements: Outline the platform(s), programming languages, frameworks, and libraries to be used for the application development.
- Responsive Design Approach: Explain the strategy for implementing a responsive design that provides an optimal user experience across various devices and screen sizes.
- Key Milestones and Timeline: Provide a high-level project timeline with key milestones for the application development and deployment.
- Team Composition: Describe the roles and responsibilities of the project team members, including any specialized skills or expertise required.
- Estimated Budget: Provide a detailed budget breakdown, including development costs, design expenses, and any additional resources or tools required.
- Potential Challenges and Mitigation Strategies: Identify any potential challenges or risks associated with the project and outline your plans to address them.
""".strip(),
            },
        )
        await write_prompt(
            product_ids=[
                chat_gpt_omni_mini.id,
                chat_gpt_omni.id,
                chat_gpt_o1_mini.id,
                chat_gpt_o1_preview.id,
                claude_3_haiku.id,
                claude_3_sonnet.id,
                claude_3_opus.id,
                gemini_1_flash.id,
                gemini_1_pro.id,
                gemini_1_ultra.id,
            ],
            subcategory_ids=[coding_frontend_subcategory.id],
            names={
                LanguageCode.RU: 'Разработка мультиязычной E-Commerce [Категория] платформы с использованием React и i18next',
                LanguageCode.EN: 'Design a Multilingual [Category] E-Commerce Platform with React and i18next',
            },
            short_prompts={
                LanguageCode.RU: """
Design a Multilingual E-Commerce platform for the [Category] industry:

- Leverage React and i18next to create a seamless, user-friendly experience across languages.
- Target a diverse audience with customized content and features for each market.
- Implement a scalable architecture, translation management, and localization strategies.
""".strip(),
                LanguageCode.EN: """
Разработай мультиязычную E-Commerce платформы для индустрии [Категория]:

- Используй React и i18next для создания удобного и плавного опыта на разных языках.
- Ориентируйся на разнообразную аудиторию, предлагая персонализированный контент и функции для каждого рынка.
- Реализуй масштабируемую архитектуру, управление переводами и стратегии локализации.
""".strip(),
            },
            long_prompts={
                LanguageCode.RU: """
Подготовь детальное предложение по созданию мультиязычной e-commerce платформы для индустрии [Категория] с использованием React и библиотеки интернационализации i18next. В предложении должны быть следующие разделы:

Обзор продукта:
- Опиши общую концепцию и ключевые функции мультиязычной e-commerce платформы.
- Объясни, кто является целевой аудиторией и какие основные сценарии использования платформы.

Технический стек и архитектура:
- Перечисли основные технологии и фреймворки, включая React, i18next и другие важные инструменты.
- Опиши предлагаемую архитектуру приложения, включая использование React-компонентов, управление состоянием и интеграцию с API.

Мультиязычная функциональность:
- Детализируй подход к реализации поддержки нескольких языков с использованием i18next, включая автоматическое определение языка, управление переводами и локализацию контента.
- Объясни, как платформа будет обрабатывать перевод информации о продуктах, пользовательского контента и административных интерфейсов.

Пользовательский опыт и дизайн:
- Опиши пользовательский интерфейс и особенности взаимодействия, подчёркивая многоязычные функции и удобство использования.
- Расскажи о подходе, который обеспечит последовательный и интуитивно понятный опыт для разных языковых версий платформы.

План проекта и сроки:
- Предоставь общий план проекта, включая основные этапы и сроки разработки и развёртывания.
- Укажи ключевые ресурсы и роли, необходимые для реализации проекта.
""".strip(),
                LanguageCode.EN: """
Provide a detailed proposal for building a multilingual E-Commerce platform for the [Category] industry using React and the i18next internationalization library. The proposal should include the following:

Product Overview:
- Describe the overall vision and key features of the multilingual e-commerce platform.
- Explain the target audience and primary use cases for the platform.

Tech Stack and Architecture:
- Outline the core technologies and frameworks to be used, including React, i18next, and any other relevant tools.
- Describe the proposed application architecture, including the use of React components, state management, and API integration.

Multilingual Functionality:
- Detail the approach to implementing multilingual support using i18next, including language detection, translation management, and content localization.
- Explain how the platform will handle translation of product information, customer-facing content, and administrative interfaces.

User Experience and Design:
- Describe the user interface and interaction design, highlighting the multilingual features and user-friendly experience.
- Discuss the approach to ensuring a consistent and intuitive experience across different language versions of the platform.

Project Plan and Timeline:
- Provide a high-level project plan, including major milestones and a timeline for development and deployment.
- Outline the key resources and roles required for the project implementation.
""".strip(),
            },
        )

        coding_backend_subcategory = await write_prompt_subcategory(
            category_ids=[coding_category.id],
            names={
                LanguageCode.RU: 'Бэкенд Разработка 💾',
                LanguageCode.EN: 'Backend Development 💾',
            },
        )
        await write_prompt(
            product_ids=[
                chat_gpt_omni_mini.id,
                chat_gpt_omni.id,
                chat_gpt_o1_mini.id,
                chat_gpt_o1_preview.id,
                claude_3_haiku.id,
                claude_3_sonnet.id,
                claude_3_opus.id,
                gemini_1_flash.id,
                gemini_1_pro.id,
                gemini_1_ultra.id,
            ],
            subcategory_ids=[coding_backend_subcategory.id],
            names={
                LanguageCode.RU: 'Создание [Приложение], используя возможности Python',
                LanguageCode.EN: 'Build a [Application] Using Python\'s Power',
            },
            short_prompts={
                LanguageCode.RU: """
Краткий обзор [Приложения] на Python:
- Описание: Представь [Приложение] и его основное назначение.
- Преимущества Python: Подчеркни, почему разработка на Python делает его мощным и гибким.
- Необходимые библиотеки: Укажи ключевые модули и библиотеки Python, которые будут использоваться.
""".strip(),
                LanguageCode.EN: """
Concise Python [Application] Overview:
- Introduce the [Application] and its key purpose.
- Highlight the benefits of developing it using Python.
- List the essential Python modules and libraries required.
""".strip(),
            },
            long_prompts={
                LanguageCode.RU: """
Обзор продукта:
- Дай краткое введение о [Приложение] и его назначении
- Подчеркни преимущества и выгоды разработки этого приложения на Python

Необходимые модули и библиотеки Python:
- Перечисли ключевые модули и библиотеки Python, необходимые для разработки [Приложение]
- Объясни назначение и функционал каждого модуля/библиотеки.

Пошаговое руководство по реализации:
- Опиши основные шаги разработки [Приложение] с использованием Python
- Предоставь подробные фрагменты кода и объяснения для каждого этапа
- Освети такие темы, как обработка данных, реализация алгоритмов и разработка UI/UX

Развёртывание и тестирование:
- Опиши процесс развёртывания [Приложение] и его доступности для пользователей.
- Объясни, как тестировать функциональность и производительность приложения.

Кастомизация и расширяемость:
- Предложи способы кастомизации [Приложение] для удовлетворения специфических потребностей пользователей.
- Дай рекомендации по расширению функциональности и возможностей приложения.
""".strip(),
                LanguageCode.EN: """
Product Overview:
- Provide a brief introduction to the [Application] and its purpose
- Highlight the benefits and advantages of creating this application using Python

Required Python Modules and Libraries:
- List the essential Python modules and libraries needed for building the [Application]
- Explain the purpose and functionality of each module/library

Step-by-Step Implementation Guide:
- Outline the key steps involved in building the [Application] using Python
- Provide detailed code snippets and explanations for each step
- Cover topics such as data processing, algorithm implementation, and UI/UX development

Deployment and Testing:
- Describe the process of deploying the [Application] and making it accessible
- Explain how to test the application's functionality and performance

Customization and Extensibility:
- Suggest ways to customize the [Application] to suit specific user requirements
- Provide guidance on extending the application's features and capabilities
""".strip(),
            },
        )
        await write_prompt(
            product_ids=[
                chat_gpt_omni_mini.id,
                chat_gpt_omni.id,
                chat_gpt_o1_mini.id,
                chat_gpt_o1_preview.id,
                claude_3_haiku.id,
                claude_3_sonnet.id,
                claude_3_opus.id,
                gemini_1_flash.id,
                gemini_1_pro.id,
                gemini_1_ultra.id,
            ],
            subcategory_ids=[coding_backend_subcategory.id],
            names={
                LanguageCode.RU: 'Скрипт автоматизации для социальных сетей на Python',
                LanguageCode.EN: 'Social media automation Python script',
            },
            short_prompts={
                LanguageCode.RU: """
Напиши скрипт на Python для автоматизации публикации в социальных сетях для бизнеса. Скрипт должен поддерживать Twitter (X), Facebook и Instagram. Он должен уметь планировать и публиковать текст, изображения и ссылки. Также скрипт должен обрабатывать аутентификацию и вести журнал ошибок
""".strip(),
                LanguageCode.EN: """
Write a Python script for automating social media posting for a business. The script should support Twitter (X), Facebook, and Instagram. It should be able to schedule and post text, images, and links. The script should also be able to handle authentication and error logging
""".strip(),
            },
            long_prompts={
                LanguageCode.RU: """
Как Backend Разработчику, тебе поручено создать скрипт на Python для автоматизации публикации контента в социальных сетях для [Название Компании, Бренда]. Этот скрипт должен уметь планировать и публиковать контент на указанных платформах в заранее определённое время.

Для разработки скрипта автоматизации публикаций в социальных сетях, предоставь подробности по следующим аспектам:
- Платформы социальных сетей: [Укажи, какие платформы должен поддерживать скрипт, например, Twitter, Facebook, Instagram и т. д.]
- Типы контента: [Определи, какие типы контента будут публиковаться, например, текст, изображения, видео или ссылки.]
- Требования к расписанию: [Опиши, как должно работать расписание, включая часовые пояса, частоту публикаций и точное время постов.]
- Источник контента: [Определи, откуда будет поступать контент, например, из базы данных, CSV-файла, API или вводиться вручную.]
- Опции настройки: [Укажи, какие опции настройки нужны для постов, например, теги, подписи или предпочтения по форматированию.]
- Аутентификация и безопасность: [Подробно опиши процесс аутентификации для каждой платформы социальных сетей, включая использование API-ключей, токенов доступа и протоколов безопасности.]
- Обработка ошибок и логирование: [Опиши, как скрипт должен обрабатывать и записывать ошибки, например, неудачные попытки публикации или проблемы с аутентификацией.]
- Пользовательский интерфейс (если требуется): [Опиши любые требования к пользовательскому интерфейсу, такие как графический интерфейс или ввод через командную строку.]
- Вывод скрипта: [Укажи, какой результат или подтверждение должен предоставлять скрипт после успешной публикации поста.]

Требования к задаче:
- Определи и интегрируй API или SDK для указанных платформ социальных сетей.
- Разработай систему для планирования и автоматизации публикаций в соответствии с заданными требованиями.
- Реализуй метод для получения и форматирования контента для публикации.
- Добавь необходимые опции настройки для каждого поста.
- Настрой безопасные процессы аутентификации для доступа к аккаунтам социальных сетей.
- Создай надёжные механизмы обработки ошибок и логирования.
- Если требуется пользовательский интерфейс, разработай и реализуй его для удобства использования.
- Убедись, что скрипт предоставляет чёткий вывод или подтверждение после успешной публикации.

Чек-лист лучших практик:
- Соблюдай лучшие практики безопасности и конфиденциальности при доступе к аккаунтам социальных сетей.
- Пиши чистый, модульный и хорошо документированный код на Python.
- Проведи тщательное тестирование скрипта в различных сценариях и на разных платформах.
- Обеспечь удобство использования скрипта для пользователей без технических навыков, если это требуется.
- Регулярно обновляй скрипт, чтобы он соответствовал изменениям в API и функциональности социальных сетей.

Результат:
- Создай скрипт на Python для автоматизации публикаций в социальных сетях для [Название Компании, Бренда]. Скрипт должен соответствовать всем заданным требованиям по типам контента, расписанию, настройкам и интеграции с платформами, обеспечивая эффективное управление социальными сетями.
""".strip(),
                LanguageCode.EN: """
As a Backend Engineer, you are tasked with creating a Python script to automate the posting of content on social media platforms for [Name of the Company, Brand, or Personal Use]. This script should be able to schedule and post content on specified platforms at predetermined times.

To develop the Python script for automating social media posts, please provide specific details in the following areas:
- Social Media Platforms: [Identify which social media platforms the script should support, such as Twitter, Facebook, Instagram, etc.]
- Content Types: [Specify the types of content to be posted, such as text, images, videos, or links]
- Scheduling Requirements: [Define how the scheduling should work, including time zones, frequency, and specific timing for posts]
- Content Source: [Describe where the content will be sourced from, e.g., a database, a CSV file, an API, or manually entered]
- Customization Options: [Mention any customization options needed for posts, like tags, captions, or formatting preferences]
- Authentication and Security: [Detail the authentication process for each social media platform, considering API keys, access tokens, and security protocols]
- Error Handling and Logging: [Specify how the script should handle and log errors, such as failed post attempts or authentication issues]
- User Interface (if applicable): [Describe any user interface requirements for the script, such as a GUI or command-line inputs]
- Script Output: [State what output or confirmation the script should provide once a post is successfully made]

Task Requirements:
- Identify and integrate APIs or SDKs for the specified social media platforms.
- Develop a system for scheduling and automating the posts according to the specified requirements.
- Implement a method for sourcing and formatting the content to be posted.
- Include necessary customization options for each post.
- Establish secure authentication processes for accessing social media accounts.
- Create robust error handling and logging mechanisms.
- If a user interface is required, design and implement it for ease of use.
- Ensure the script provides clear output or confirmation upon successful posting.

Best Practices Checklist:
- Follow best practices for security and privacy in handling access to social media accounts.
- Write clean, modular, and well-documented Python code.
- Test the script thoroughly across different scenarios and platforms.
- Ensure the script is user-friendly and accessible for non-technical users if required.
- Regularly update the script to accommodate changes in social media APIs and features.

Deliverable:
- Develop a Python script for automating social media posts for [Name of the Company, Brand, or Personal Use]. The script should meet all specified requirements for content types, scheduling, customization, and platform integration, enabling efficient and automated social media management
""".strip(),
            },
        )
        await write_prompt(
            product_ids=[
                chat_gpt_omni_mini.id,
                chat_gpt_omni.id,
                chat_gpt_o1_mini.id,
                chat_gpt_o1_preview.id,
                claude_3_haiku.id,
                claude_3_sonnet.id,
                claude_3_opus.id,
                gemini_1_flash.id,
                gemini_1_pro.id,
                gemini_1_ultra.id,
            ],
            subcategory_ids=[coding_backend_subcategory.id],
            names={
                LanguageCode.RU: 'Код для системы обнаружения аномалий',
                LanguageCode.EN: 'Code for anomaly detection system',
            },
            short_prompts={
                LanguageCode.RU: """
Создай систему обнаружения аномалий, которая определяет необычные шаблоны или выбросы в наборе данных. Реализуй код, используя подходящий метод, и оцени его производительность с помощью релевантных метрик
""".strip(),
                LanguageCode.EN: """
Create an anomaly detection system that identifies unusual patterns or outliers in a dataset. Implement the code using a suitable method and evaluate its performance using relevant metrics
""".strip(),
            },
            long_prompts={
                LanguageCode.RU: """
Тебе поручено разработать код для системы обнаружения аномалий, которая определяет необычные шаблоны или выбросы в заданном наборе данных. Система должна быть надёжной, эффективной и адаптируемой для различных типов данных и сценариев использования.

Для создания системы обнаружения аномалий учитывай следующие аспекты:
- Характеристики данных: [Опиши особенности данных, которые будут анализироваться, включая формат данных, размер, количество измерений, а также известные аномалии или шаблоны]
- Метод обнаружения: [Укажи метод или алгоритм обнаружения аномалий, который ты планируешь использовать, например, статистические методы, модели машинного обучения (например, Isolation Forest, One-Class SVM) или Deep Learning]
- Настройка порога: [Определи порог или критерии для идентификации аномалий, включая способы определения и классификации выбросов]
- Генерация признаков: [Опиши техники генерации признаков или этапы предобработки данных, необходимые для подготовки данных к обнаружению аномалий, например, нормализацию, уменьшение размерности или выбор признаков]
- Оценка модели: [Определи метрики оценки и методы, которые ты будешь использовать для анализа производительности системы обнаружения аномалий, включая точность, полноту, F1-оценку]
- Масштабируемость и эффективность: [Продумай масштабируемость и эффективность кода, особенно для больших наборов данных или приложений в реальном времени. Опиши стратегии оптимизации производительности и снижения вычислительной нагрузки]

Требования к задаче:
- Реализуй код для системы обнаружения аномалий, используя подходящие языки программирования и библиотеки (например, Python с использованием scikit-learn, TensorFlow, PyTorch и т. д.).
- Обеспечь хорошую документацию, модульность и понятность кода, с чёткими объяснениями каждой компоненты и функции.
- Протестируй код на примерах наборов данных и оцени его производительность с использованием соответствующих метрик и методов.
- Оптимизируй код для повышения эффективности и масштабируемости, учитывая сложность выполнения, использование памяти и вычислительные ресурсы.
- Предоставь инструкции или рекомендации по использованию системы обнаружения аномалий, включая способы ввода данных, интерпретацию результатов и настройку параметров.

Чек-лист лучших практик:
- Ознакомься с различными методами и алгоритмами обнаружения аномалий, чтобы выбрать наиболее подходящий подход для своего случая.
- Оцени производительность системы с использованием перекрёстной проверки, анализа временных рядов или других подходящих методов.
- Учитывай интерпретируемость и объяснимость результатов системы обнаружения аномалий, особенно в сценариях, где требуется человеческое вмешательство или принятие решений.
- Реализуй обработку ошибок и управление исключениями для корректной работы с неожиданными входными данными, ошибками и крайними случаями.
- Документируй предположения, ограничения или особенности системы, чтобы предоставить пользователям и заинтересованным сторонам контекст.

Результат:
- Предоставь код системы обнаружения аномалий вместе с документацией, которая включает объяснения реализации, результаты оценки и инструкции по использованию.
""".strip(),
                LanguageCode.EN: """
You're tasked with developing code for an anomaly detection system to identify unusual patterns or outliers in a given dataset. The anomaly detection system should be robust, efficient, and adaptable to different types of data and use cases.

To create the code for the anomaly detection system, consider the following aspects:
- Data Characteristics: [Describe the characteristics of the data you'll be analyzing, such as data format, size, dimensionality, and any known anomalies or patterns]
- Detection Method: [Specify the anomaly detection method or algorithm you plan to implement, such as statistical methods, machine learning models (e.g., Isolation Forest, One-Class SVM), or deep learning techniques]
- Threshold Setting: [Define the threshold or criteria for identifying anomalies in the data, including how outliers will be defined and classified]
- Feature Engineering: [Discuss any feature engineering techniques or preprocessing steps needed to prepare the data for anomaly detection, such as normalization, dimensionality reduction, or feature selection]
- Model Evaluation: [Outline the evaluation metrics and techniques you'll use to assess the performance of the anomaly detection system, including measures of accuracy, precision, recall, and F1-score]
- Scalability and Efficiency: [Consider the scalability and efficiency of the code, especially for large datasets or real-time applications, and discuss strategies for optimizing performance and reducing computational overhead]

Task Requirements:
- Implement the code for the anomaly detection system using appropriate programming languages and libraries (e.g., Python with scikit-learn, TensorFlow, PyTorch, etc.).
- Ensure that the code is well-documented, modular, and easy to understand, with clear explanations of each component and function.
- Test the code with sample datasets and evaluate its performance using relevant evaluation metrics and techniques.
- Optimize the code for efficiency and scalability, considering factors such as runtime complexity, memory usage, and computational resources.
- Provide instructions or guidelines for using the anomaly detection system, including how to input data, interpret results, and adjust parameters if needed.

Best Practices Checklist:
- Familiarize yourself with different anomaly detection methods and algorithms to choose the most suitable approach for your specific use case.
- Validate the performance of the anomaly detection system using cross-validation, time-series analysis, or other appropriate validation techniques.
- Consider the interpretability and explainability of the anomaly detection results, especially in applications where human intervention or decision-making is involved.
- Implement error handling and exception management to handle unexpected inputs, errors, and edge cases gracefully.
- Document any assumptions, limitations, or constraints associated with the anomaly detection system to provide context for users and stakeholders.

Deliverable:
- Submit the code for the anomaly detection system along with documentation that includes explanations of the implementation details, evaluation results, and usage instructions
""".strip(),
            },
        )

        coding_devops_subcategory = await write_prompt_subcategory(
            category_ids=[coding_category.id],
            names={
                LanguageCode.RU: 'Архитектура и Инфраструктура 🏗️',
                LanguageCode.EN: 'Architecture and Infrastructure 🏗️',
            },
        )
        await write_prompt(
            product_ids=[
                chat_gpt_omni_mini.id,
                chat_gpt_omni.id,
                chat_gpt_o1_mini.id,
                chat_gpt_o1_preview.id,
                claude_3_haiku.id,
                claude_3_sonnet.id,
                claude_3_opus.id,
                gemini_1_flash.id,
                gemini_1_pro.id,
                gemini_1_ultra.id,
            ],
            subcategory_ids=[coding_devops_subcategory.id],
            names={
                LanguageCode.RU: 'Интеграция [Облачный Сервис] в существующее приложение',
                LanguageCode.EN: 'Integrate [Cloud Service] into an Existing Application',
            },
            short_prompts={
                LanguageCode.RU: """
Интегрируй [Облачный Сервис] в моё приложение:

- Изучи функции [Облачный Сервис] и определи требования.
- Настрой необходимые учётные записи, программное обеспечение и конфигурации.
- Следуй пошаговым инструкциям для плавной интеграции [Облачный Сервис].
- Используй ресурсы для поддержки и лучших практик.
""".strip(),
                LanguageCode.EN: """
Integrate [Cloud Service] with my app:

- Explore [Cloud Service] features and understand your requirements.
- Set up necessary accounts, software, and configurations.
- Follow step-by-step instructions to integrate [Cloud Service] seamlessly.
- Refer to resources for support and best practices.
""".strip(),
            },
            long_prompts={
                LanguageCode.RU: """
Создай пошаговое руководство по интеграции [Облачный Сервис] в существующее приложение. Руководство должно включать:

- Обзор [Облачный Сервис] и его ключевых функций
- Требования для интеграции, включая необходимое программное обеспечение, учетные записи и конфигурации
- Подробные инструкции по настройке интеграции [Облачный Сервис] в существующем приложении
- Примеры кода или конфигураций для демонстрации процесса интеграции
- Советы и лучшие практики для обеспечения бесшовной и эффективной интеграции
- Возможные проблемы или ограничения, которые могут возникнуть в процессе интеграции
- Ресурсы и документацию для получения дополнительной информации или поддержки

Форматирование:
- Используй ясный и лаконичный язык, избегая сложного технического жаргона
- Организуй руководство в логической последовательности с соответствующими подзаголовками
- Вставляй примеры кода или конфигурации в форматированных блоках кода
- Проверь руководство на наличие грамматических, орфографических ошибок и на общую ясность текста.
""".strip(),
                LanguageCode.EN: """
Provide a step-by-step guide for integrating the [Cloud Service] into an existing application. The guide should cover the following:

- Overview of the [Cloud Service] and its key features
- Prerequisites for integration, including any software, accounts, or configurations required
- Detailed instructions for setting up the [Cloud Service] integration within the existing application
- Code samples or configuration examples to demonstrate the integration process
- Tips and best practices for ensuring a seamless and efficient integration
- Potential challenges or limitations to be aware of during the integration
- Resources and documentation for further information or support

Formatting:
- Use clear and concise language, avoiding technical jargon where possible
- Organize the guide in a logical flow with relevant subheadings
- Provide code snippets or configuration examples in a formatted code block
- Proofread the guide for grammar, spelling, and overall clarity
""".strip(),
            },
        )
        await write_prompt(
            product_ids=[
                chat_gpt_omni_mini.id,
                chat_gpt_omni.id,
                chat_gpt_o1_mini.id,
                chat_gpt_o1_preview.id,
                claude_3_haiku.id,
                claude_3_sonnet.id,
                claude_3_opus.id,
                gemini_1_flash.id,
                gemini_1_pro.id,
                gemini_1_ultra.id,
            ],
            subcategory_ids=[coding_devops_subcategory.id],
            names={
                LanguageCode.RU: 'Разработка и Деплой масштабируемой архитектуры микросервисов для [Сервис]',
                LanguageCode.EN: 'Design and Deploy a Scalable [Service] Microservices Architecture',
            },
            short_prompts={
                LanguageCode.RU: """
Разработай масштабируемую, модульную и отказоустойчивую архитектуру микросервисов для приложения [Сервис], ориентированного на [Целевая Индустрия] и предполагаемую пользовательскую базу. Используй контейнеризацию и инструменты оркестрации для обеспечения высокой доступности и бесшовного развертывания.
""".strip(),
                LanguageCode.EN: """
Design a scalable, modular, and fault-tolerant microservices architecture for a [Service] application, catering to the [Target Industry] and its anticipated user base. Leverage containerization and orchestration tools to ensure high availability and seamless deployment.
""".strip(),
            },
            long_prompts={
                LanguageCode.RU: """
Создай детальный план разработки и развертывания масштабируемой архитектуры микросервисов для приложения [Сервис]. Архитектура должна быть модульной, отказоустойчивой и легко масштабируемой для обработки растущего пользовательского трафика и увеличивающихся требований к обработке данных.

Детали продукта:
- Название сервиса: [Сервис]
- Целевая индустрия: [Целевая Индустрия]
- Ключевые функции: [Ключевые Функции]
- Предполагаемая пользовательская база: [Предполагаемая Пользовательская База]
- Ожидаемый рост трафика: [Ожидаемый Рост Трафика]

Проектирование архитектуры микросервисов:
- Определи и опиши основные микросервисы, необходимые для приложения [Сервис].
- Охарактеризуй протоколы коммуникации и точки интеграции между микросервисами.
- Объясни стратегию хранения и управления данными для каждого микросервиса.
- Детализируй меры безопасности и механизмы аутентификации для архитектуры.
- Предложи решение для балансировки нагрузки и мониторинга, чтобы обеспечить высокую доступность.
- Укажи инструменты контейнеризации и оркестрации, которые будут использоваться для развертывания.

Стратегия развертывания:
- Опиши инфраструктурные требования (облачные платформы, конфигурации виртуальных машин и т.д.).
- Опиши конвейер CI/CD для автоматической сборки, тестирования и развертывания.
- Детализируй процедуры восстановления после сбоев и резервного копирования для микросервисов.
- Предоставь график выполнения и поэтапный план развертывания архитектуры.
- Оцени общие затраты, связанные с развертыванием микросервисов.
""".strip(),
                LanguageCode.EN: """
Provide a detailed plan for designing and deploying a scalable microservices architecture for a [Service] application. The architecture should be modular, fault-tolerant, and easily scalable to handle increased user traffic and data processing requirements.

Product Details:
- Service Name: [Service Name]
- Target Industry: [Target Industry]
- Key Features: [Key Features]
- Anticipated User Base: [Anticipated User Base]
- Projected Traffic Growth: [Projected Traffic Growth]

Microservices Architecture Design:
- Identify and define the core microservices required for the [Service] application
- Describe the communication protocols and integration points between microservices
- Explain the data storage and management strategy for each microservice
- Detail the security measures and authentication mechanisms for the architecture
- Propose a load balancing and monitoring solution to ensure high availability
- Specify the containerization and orchestration tools to be used for deployment

Deployment Strategy:
- Outline the infrastructure requirements (cloud platforms, VM configurations, etc.)
- Describe the CI/CD pipeline for automated build, testing, and deployment
- Detail the disaster recovery and backup procedures for the microservices
- Provide a timeline and phased rollout plan for the architecture implementation
- Estimate the overall costs associated with the microservices deployment
""".strip(),
            },
        )
        await write_prompt(
            product_ids=[
                chat_gpt_omni_mini.id,
                chat_gpt_omni.id,
                chat_gpt_o1_mini.id,
                chat_gpt_o1_preview.id,
                claude_3_haiku.id,
                claude_3_sonnet.id,
                claude_3_opus.id,
                gemini_1_flash.id,
                gemini_1_pro.id,
                gemini_1_ultra.id,
            ],
            subcategory_ids=[coding_devops_subcategory.id],
            names={
                LanguageCode.RU: 'Реализация системы рекомендаций для [Контент] платформы',
                LanguageCode.EN: 'Implement a Recommendation System for a [Content] Platform',
            },
            short_prompts={
                LanguageCode.RU: """
Разработай персонализированную систему рекомендаций для [Контент] платформы, используя данные пользователей, метаданные контента и продвинутые алгоритмы для предоставления индивидуальных рекомендаций, которые увеличивают вовлечённость и удовлетворённость пользователей.

Опиши ключевые компоненты, включая сбор данных, профилирование пользователей, индексирование контента и алгоритмы рекомендаций, чтобы создать надёжную и адаптивную систему, которая развивается на основе обратной связи пользователей.

Предложи метрики производительности и план для непрерывной оптимизации, чтобы измерять и улучшать эффективность системы рекомендаций со временем.
""".strip(),
                LanguageCode.EN: """
Design a personalized recommendation system for a [Сontent] platform, leveraging user data, content metadata, and advanced algorithms to provide tailored suggestions that enhance user engagement and satisfaction.

Outline the key components, such as data collection, user profiling, content indexing, and recommendation algorithms, ensuring a robust and adaptive system that evolves with user feedback.

Propose performance metrics and a plan for continuous optimization to measure and improve the recommendation system's effectiveness over time.
""".strip(),
            },
            long_prompts={
                LanguageCode.RU: """
Разработай детальное предложение по реализации системы рекомендаций на [Контент] платформе. Система должна предоставлять персонализированные рекомендации пользователям на основе их предпочтений и истории просмотра. Включи следующие ключевые разделы:

Введение
- Дай общий обзор [Контент] платформы и обоснуй необходимость внедрения системы рекомендаций.
- Подчеркни преимущества реализации персонализированной системы рекомендаций.

Архитектура системы рекомендаций
- Опиши высокоуровневую архитектуру системы рекомендаций.
- Перечисли ключевые компоненты, такие как сбор данных, профилирование пользователей, индексирование контента и алгоритмы рекомендаций.

Сбор данных и профилирование пользователей
- Расскажи про источники данных и методы сбора информации о поведении и предпочтениях пользователей.
- Детализируй техники профилирования для понимания интересов и предпочтений отдельных пользователей.

Индексирование контента и метаданные
- Опиши процесс индексирования и категоризации [Контент] активов.
- Продумай использование метаданных контента, тегов и других атрибутов для улучшения работы системы рекомендаций.

Алгоритмы рекомендаций
- Предложи один или несколько алгоритмов рекомендаций для внедрения (например, коллаборативная фильтрация, контентная фильтрация, гибридные подходы).
- Дай высокоуровневое описание работы этих алгоритмов и обоснуй выбор.

Персонализация и настройка
- Опиши функции и возможности, которые позволят пользователям настраивать свои рекомендации.
- Объясни, как система будет адаптироваться и эволюционировать на основе обратной связи и взаимодействий пользователей.

Реализация и развертывание
- Опиши ключевые шаги и временные рамки для реализации и развертывания системы рекомендаций.
- Укажи возможные трудности или риски и предложи стратегии их минимизации.

Оценка и метрики
- Предложи ключевые показатели эффективности (KPI) и метрики для измерения эффективности системы рекомендаций.
- Опиши подход к непрерывному мониторингу и оптимизации работы системы.
""".strip(),
                LanguageCode.EN: """
Develop a detailed proposal for implementing a recommendation system on a [Content] platform. The system should provide personalized content suggestions to users based on their preferences and browsing history. Include the following key sections:

Introduction
- Provide an overview of the [Content] platform and the need for a recommendation system.
- Highlight the benefits of implementing a personalized recommendation system.

Recommendation System Architecture
- Outline the high-level architecture of the recommendation system.
- Describe the key components, such as data collection, user profiling, content indexing, and recommendation algorithms.

Data Collection and User Profiling
- Explain the data sources and methods for collecting user behavior and preference data.
- Detail the user profiling techniques to understand individual user interests and preferences.

Content Indexing and Metadata
- Describe the process of indexing and categorizing the [Content] assets.
- Discuss the use of content metadata, tags, and other relevant attributes for powering the recommendation system.

Recommendation Algorithms
- Propose one or more recommendation algorithms to be implemented (e.g., collaborative filtering, content-based filtering, hybrid approaches).
- Provide a high-level overview of how these algorithms will work and the rationale behind the choices.

Personalization and Customization
- Outline the features and functionality that will allow users to customize their recommendations.
- Explain how the system will adapt and evolve based on user feedback and interactions.

Implementation and Deployment
- Discuss the key steps and timeline for implementing and deploying the recommendation system.
- Identify any potential challenges or risks and propose mitigation strategies.

Evaluation and Metrics
- Suggest key performance indicators (KPIs) and metrics to measure the effectiveness of the recommendation system.
- Outline the approach for continuously monitoring and optimizing the system's performance.
""".strip(),
            },
        )

        # Social Media
        # Подкатегории: Посты, Видео, Сторизы, Контент-Маркетинг
        social_media_category = await write_prompt_category(
            model_type=ModelType.TEXT,
            names={
                LanguageCode.RU: 'Социальные Сети 🌐',
                LanguageCode.EN: 'Social Media 🌐',
            },
        )
        social_media_posts_subcategory = await write_prompt_subcategory(
            category_ids=[social_media_category.id],
            names={
                LanguageCode.RU: 'Посты 📝',
                LanguageCode.EN: 'Posts 📝',
            },
        )
        await write_prompt(
            product_ids=[
                chat_gpt_omni_mini.id,
                chat_gpt_omni.id,
                claude_3_haiku.id,
                claude_3_sonnet.id,
                claude_3_opus.id,
                gemini_1_flash.id,
                gemini_1_pro.id,
                gemini_1_ultra.id,
            ],
            subcategory_ids=[social_media_posts_subcategory.id],
            names={
                LanguageCode.RU: 'Создание Неотразимого [Тип Контента] для [Целевая Аудитория]',
                LanguageCode.EN: 'Crafting Irresistible [Content Type] for a [Target Audience]',
            },
            short_prompts={
                LanguageCode.RU: """
Создай увлекательный [Тип Контента] для [Целевая Аудитория]. Придумай захватывающий заголовок, зацепи читателя интригующим интро и раскрой ключевые темы. Используй тон и стиль, которые откликаются у аудитории, добавь визуальные элементы и заверши сильным призывом к действию
""".strip(),
                LanguageCode.EN: """
Create a captivating [Content Type] for [Target Audience]. Craft a compelling title, hook them with an intro, and cover key topics. Use a tone and style that resonates, enhance with visuals, and include a strong call-to-action
""".strip(),
            },
            long_prompts={
                LanguageCode.RU: """
Разработай увлекательный, информативный и вовлекающий [Тип Контента], ориентированный на [Целевая Аудитория]. Этот [Тип Контента] должен эффективно привлекать внимание аудитории, предоставлять ценные инсайты и стимулировать значимое взаимодействие.

Определи структуру [Тип Контента], рассмотрев следующие аспекты:
- Заголовок: Придумай броский заголовок, который чётко передаёт цель [Тип Контента] и привлекает целевую аудиторию.
- Введение: Начни с захватывающего вступления, которое зацепит читателя и задаст тон для [Тип Контента].
- Ключевые темы/разделы: Определи основные темы, пункты или разделы, которые нужно охватить в [Тип Контента]. Кратко опиши или подведи итог для каждого.
- Тон и стиль: Выбери подходящий тон, язык и стиль написания, который будет резонировать с [Целевая Аудитория].
- Визуальные элементы и форматирование: Опиши любые визуальные элементы, такие как изображения, графики или форматирование, которые улучшат общую привлекательность и эффективность [Тип Контента].
- Призыв к действию: Включи чёткий и убедительный призыв к действию, который побудит [Целевая Аудитория] к дальнейшему взаимодействию с контентом.
""".strip(),
                LanguageCode.EN: """
Develop a compelling, engaging, and informative [Content Type] targeted towards [Target Audience]. The [Content Type] should effectively capture the audience's attention, provide valuable insights, and encourage meaningful interaction.

Outline the [content type] by addressing the following:
- Title: Craft an attention-grabbing title that clearly conveys the [Content Type]'s purpose and appeal to the target audience.
- Introduction: Begin with an introduction that hooks the reader and sets the tone for the [Content Type].
- Key Topics/Sections: Identify the main topics, points, or sections to be covered in the [Content Type]. Provide a brief outline or summary for each.
- Tone and Style: Determine the appropriate tone, language, and writing style to best resonate with the [Target Audience].
- Visuals and Formatting: Describe any visual elements, such as images, graphics, or formatting, that will enhance the [Content Type]'s overall appeal and effectiveness.
- Call-to-Action: Include a clear and compelling call-to-action to encourage the [Target Audience] to engage further with the content.
""".strip(),
            },
        )
        await write_prompt(
            product_ids=[
                chat_gpt_omni_mini.id,
                chat_gpt_omni.id,
                claude_3_haiku.id,
                claude_3_sonnet.id,
                claude_3_opus.id,
                gemini_1_flash.id,
                gemini_1_pro.id,
                gemini_1_ultra.id,
            ],
            subcategory_ids=[social_media_posts_subcategory.id],
            names={
                LanguageCode.RU: 'Раскрытие силы убедительного контента для [Цель Контента]',
                LanguageCode.EN: 'Unleashing the Power of Persuasive [Content Purpose] Content',
            },
            short_prompts={
                LanguageCode.RU: """
Создай увлекательный пост для [Цель Контента], адаптированный под мою целевую аудиторию [Целевая Аудитория]. Разработай убедительные сообщения, подходящий тон и ясный формат, чтобы заинтересовать и вдохновить. Убедись, что контент оптимизирован для поисковых систем и социальных сетей
""".strip(),
                LanguageCode.EN: """
Create a captivating [Content Purpose] post tailored to my target audience [Target Audience]. Craft compelling messaging, a suitable tone, and a clear format to engage and inspire. Ensure the content is optimized for search and social media
""".strip(),
            },
            long_prompts={
                LanguageCode.RU: """
Создай убедительный и воздействующий пост для [Цель Контента], который будет резонировать с моей целевой аудиторией. Подготовь детальный обзор материала, включая ключевые сообщения, тон и рекомендации по форматированию.

Детали контента:
- Заголовок: [Убедительный Заголовок]
- Цель контента: [Цель Контента, например, маркетинг, обучение, экспертное мнение]
- Целевая аудитория: [Целевая Аудитория]
- Ключевые сообщения: [Основные Идеи, которые нужно донести]
- Формат контента: Блог
- Оценочный объём текста: [Диапазон Слов]
- Тон и стиль: [Желаемый Тон и Стиль Написания]
- Призыв к действию: [Желаемый Призыв к Действию]

Рекомендации по форматированию:
- Используй понятный, лаконичный и убедительный язык.
- Организуй контент в логической последовательности с подходящими подзаголовками.
- Добавь визуальные элементы, статистику или примеры для поддержки ключевых идей.
- Оптимизируй контент для поисковых систем и публикаций в социальных сетях.
- Тщательно проверь текст на грамматику, орфографию и общую ясность.
""".strip(),
                LanguageCode.EN: """
Craft a compelling and persuasive [Content Purpose] post that resonates with my target audience. Provide a detailed overview of the content, including the key messaging, tone, and formatting guidelines.

Content Details:
- Title: [Compelling Title]
- Content Purpose: [Content Purpose, e.g., marketing, educational, thought leadership]
- Target Audience: [Target Audience]
- Key Messaging: [Key Messages to Convey]
- Content Format: Post
- Estimated Word Count: [Word Count Range]
- Tone and Style: [Desired Tone and Writing Style]
- Call-to-Action: [Desired Call-to-Action]

Formatting Guidelines:
- Use clear, concise, and persuasive language
- Organize content in a logical flow with relevant subheadings
- Incorporate compelling visuals, statistics, or examples to support key points
- Optimize content for search engine visibility and social media sharing
- Proofread thoroughly for grammar, spelling, and overall clarity
""".strip(),
            },
        )
        await write_prompt(
            product_ids=[
                chat_gpt_omni_mini.id,
                chat_gpt_omni.id,
                claude_3_haiku.id,
                claude_3_sonnet.id,
                claude_3_opus.id,
                gemini_1_flash.id,
                gemini_1_pro.id,
                gemini_1_ultra.id,
            ],
            subcategory_ids=[social_media_posts_subcategory.id],
            names={
                LanguageCode.RU: 'Создание увлекательного блог-поста для [Индустрия], который одновременно информативный и вовлекающий',
                LanguageCode.EN: 'Write a captivating [Industry] blog post that educates and engages',
            },
            short_prompts={
                LanguageCode.RU: """
Создай увлекательный блог-пост для нашей аудитории в [Индустрия]. Обучи читателей теме [Тема] через захватывающее повествование и глубокий анализ. Включи привлекающее внимание вступление, полезный контент и практические рекомендации для применения.
""".strip(),
                LanguageCode.EN: """
Craft an engaging blog post for our [Industry] audience. Educate readers on [Topic] through compelling storytelling and insightful analysis. Incorporate attention-grabbing introduction, valuable content, and actionable takeaways.
""".strip(),
            },
            long_prompts={
                LanguageCode.RU: """
Создай информативный и увлекательный блог-пост для нашей аудитории в [Индустрия]. Пост должен обучать читателей на актуальную тему, привлекая их внимание через захватывающее повествование и глубокий анализ. Включи следующие элементы:

Тема: [Тема Поста]
Рабочее название: [Рабочее Название]
Целевая аудитория: [Целевая Аудитория]
Длина поста: [Длина Поста] слов

- Привлекающее внимание вступление: Начни с введения, которое сразу зацепит читателя и задаст тон всему посту.
- Обучающий контент: Предоставь ценную, тщательно исследованную информацию, которая обучает читателей теме. Используй комбинацию фактов, статистики и экспертных взглядов.
- Увлекательное повествование: Включи релевантные анекдоты, примеры или истории, чтобы сделать контент более интересным и запоминающимся.
- Уникальные идеи: Предложи уникальные точки зрения, анализ или решения, которые выделят пост на фоне аналогичного контента.
- Визуальная привлекательность: Добавь релевантные изображения, графики или мультимедийные элементы для улучшения визуального восприятия поста.
- Практические рекомендации: Заверши пост с призывами, советами, рекомендациями или следующими шагами для читателей.

Руководство по форматированию:
- Используй ясный, разговорный и профессиональный тон на протяжении всего текста.
- Организуй текст в логической последовательности с использованием релевантных подзаголовков.
- Оптимизируй текст для поисковых систем, включая целевые ключевые слова.
- Тщательно проверь текст на наличие грамматических, орфографических ошибок и на общую ясность.

Дай знать, если есть дополнительные требования.
""".strip(),
                LanguageCode.EN: """
Craft an informative and engaging blog post for our [Industry] audience. The post should educate readers on a relevant topic while captivating their attention through compelling storytelling and insightful analysis. Incorporate the following elements:

Topic: [Post Topic]
Working Title: [Working Title]
Target Audience: [Target Audience]
Post Length: [Post Length] words

- Attention-Grabbing Introduction: Begin with an introduction that immediately hooks the reader and sets the tone for the post.
- Educational Content: Provide valuable, well-researched information that educates readers on the topic. Use a combination of facts, statistics, and expert insights.
- Engaging Storytelling: Incorporate relatable anecdotes, examples, or narratives to make the content more engaging and memorable.
- Unique Insights: Offer unique perspectives, analysis, or solutions that differentiate the post from similar content.
- Compelling Visuals: Include relevant images, graphics, or multimedia elements to enhance the post's visual appeal.
- Actionable Takeaways: Conclude the post with actionable tips, recommendations, or next steps for the reader.

Formatting Guidelines:
- Use a clear, conversational, and professional tone throughout.
- Organize the post in a logical flow with relevant subheadings.
- Optimize the post for search engines by incorporating target keywords.
- Proofread thoroughly for grammar, spelling, and overall clarity.

Let me know if you have any requirements.
""".strip(),
            },
        )

        social_media_videos_subcategory = await write_prompt_subcategory(
            category_ids=[social_media_category.id],
            names={
                LanguageCode.RU: 'Видео 📹',
                LanguageCode.EN: 'Video 📹',
            },
        )
        await write_prompt(
            product_ids=[
                chat_gpt_omni_mini.id,
                chat_gpt_omni.id,
                claude_3_haiku.id,
                claude_3_sonnet.id,
                claude_3_opus.id,
                gemini_1_flash.id,
                gemini_1_pro.id,
                gemini_1_ultra.id,
            ],
            subcategory_ids=[social_media_videos_subcategory.id],
            names={
                LanguageCode.RU: 'YouTube Видео Интро',
                LanguageCode.EN: 'YouTube Video Intro',
            },
            short_prompts={
                LanguageCode.RU: """
Напиши вступление для видео на YouTube

Создай захватывающее вступление для моего видео на тему [Тема Видео]. Включи:
- Мощный позыв, чтобы привлечь внимание.
- Чёткое заявление о теме видео и её значимости для [Целевая Аудитория].
- Краткий обзор того, что зрители узнают из видео.
- Личное представление, которое подчеркнёт мою экспертность.
- Призыв к действию: лайки, подписки или комментарии.
""".strip(),
                LanguageCode.EN: """
Write a YouTube Video Introduction

Create a compelling intro for my YouTube video on [Video Topic]. Include:
- A strong hook to grab attention.
- A clear statement of the topic and its relevance to [Target Audience].
- A brief outline of what viewers can expect.
- A personal introduction that establishes credibility.
- A call-to-action for likes, subscriptions, or comments.
""".strip(),
            },
            long_prompts={
                LanguageCode.RU: """
Как [Твоя Роль], тебе предстоит создать вступление для моего видео на YouTube-канале [Название YouTube-Канала]. Вступление важно, так как оно задаёт тон всему видео и привлекает мою аудиторию с самого начала.

Для написания вступления включи следующие детали:
- Тема видео: [Основная Тема Видео].
- Целевая аудитория: [Описание Целевой Аудитории, их интересов и предпочтений].
- Обзор контента: [Краткое Описание того, что будет освещаться в видео].
- Личное представление: [Представь себя и опиши свою связь с темой видео].
- Призыв к действию: [Добавь призыв для зрителей поставить лайк, подписаться или оставить комментарий].

Требования к задаче:
- Начни с сильного хука, который сразу привлечёт внимание зрителей.
- Чётко обозначь тему видео и объясни, почему она важна для аудитории.
- Кратко опиши, что зрители узнают из видео.
- Представь меня так, чтобы укрепить мою экспертность или связь с темой.
- Поощри взаимодействие зрителей для повышения вовлечённости.

Чек-лист лучших практик:
- Держи вступление кратким и по делу.
- Убедись, что тон вступления соответствует общему стилю видео.
- Создай дружелюбную и гостеприимную атмосферу, чтобы удержать внимание зрителей.
- Используй язык, который откликается у моей целевой аудитории.
- Добавь элементы моей уникальной личности или бренда.

Результат:
- Напиши захватывающее вступление для моего будущего видео на YouTube на тему [Основная Тема Видео]. Это вступление должно эффективно привлечь зрителя, чётко описать содержание видео и поощрить взаимодействие с аудиторией.
""".strip(),
                LanguageCode.EN: """
As [Your Role], you are about to create a YouTube video for my channel [Your YouTube Channel Name]. The introduction to my video is crucial as it sets the tone for the content and engages my audience from the outset.

For writing this YouTube video introduction, include the following specific details:
- Video Topic: [Main Topic or Subject of Your Video]
- Target Audience: [Target Audience, including their interests and preferences]
- Content Overview: [Brief Overview of What the Video Will Cover]
- Personal Introduction: [Introduce yourself and your connection to the video topic]
- Engagement Request: [Include a call-to-action for viewers to like, subscribe, or comment]

Task Requirements:
- Start with a strong hook that immediately engages the viewer.
- Clearly state the topic of the video and why it's relevant to the audience.
- Briefly outline what the viewer can expect from the video.
- Introduce myself in a way that establishes my credibility or connection to the topic.
- Encourage viewer interaction to boost engagement metrics.

Best Practices Checklist:
- Keep the introduction concise and to the point.
- Ensure the tone of the introduction matches the overall style of the video.
- Create an inviting and friendly atmosphere to retain viewer interest.
- Use language that resonates with my target audience.
- Incorporate elements of my unique personality or brand.

Delivarable:
- Write a compelling introduction for my upcoming YouTube video on [Main Topic of Your Video]. This introduction should effectively hook the viewer, provide a clear overview of the video content, and encourage audience interaction
""".strip(),
            },
        )
        await write_prompt(
            product_ids=[
                chat_gpt_omni_mini.id,
                chat_gpt_omni.id,
                claude_3_haiku.id,
                claude_3_sonnet.id,
                claude_3_opus.id,
                gemini_1_flash.id,
                gemini_1_pro.id,
                gemini_1_ultra.id,
            ],
            subcategory_ids=[social_media_videos_subcategory.id],
            names={
                LanguageCode.RU: 'TikTok: Празднование достижения [Событие] на TikTok',
                LanguageCode.EN: 'TikTok: Celebrate [Milestone] Achievements on TikTok',
            },
            short_prompts={
                LanguageCode.RU: """
Создай яркое видео в TikTok, посвящённый моему достижению [Milestone]. Зацепи зрителей увлекательным вступлением и расскажи кратко о пути. Покажи лучший контент и вдохнови подписчиков на взаимодействие
""".strip(),
                LanguageCode.EN: """
Create a lively TikTok celebrating my [Milestone]. Captivate viewers with a compelling intro and brief the journey. Showcase the top content and inspire my followers to engage
""".strip(),
            },
            long_prompts={
                LanguageCode.RU: """
Создай захватывающее TikTok-видео, чтобы отпраздновать моё достижение [Событие]. Видео должно длиться 60–90 секунд и включать:

- Яркое вступление, подчёркивающее моё достижение [Событие].
- Краткий обзор моего пути и ключевых этапов, которые я преодолел.
- Демонстрацию моего лучшего контента на TikTok, достижений и метрик вовлечённости.
- Вдохновляющее послание для подписчиков, чтобы воодушевить и мотивировать их.
- Чёткий призыв к действию, побуждающий зрителей взаимодействовать с моим контентом.

Оптимизируй видео для TikTok, используя релевантные хэштеги, трендовую музыку и привлекательные визуальные элементы. Видео будет в вертикальном формате, сохраняя искренний и разговорный тон на протяжении всего ролика.
""".strip(),
                LanguageCode.EN: """
Craft a compelling TikTok video to celebrate my [Milestone] achievements. The video should be 60-90 seconds long and include:

- An attention-grabbing introduction highlighting my [Milestone] accomplishment
- A brief overview of my journey and the key milestones reached
- Showcase of my top TikTok content, achievements, and engagement metrics
- Inspiring message to encourage my followers and motivate them
- A clear call-to-action prompting viewers to engage with my content

Optimize the video for TikTok by using relevant hashtags, trending audio, and eye-catching visual elements. The video will be in a vertical format and maintain an authentic, conversational tone throughout.
""".strip(),
            },
        )
        await write_prompt(
            product_ids=[
                chat_gpt_omni_mini.id,
                chat_gpt_omni.id,
                claude_3_haiku.id,
                claude_3_sonnet.id,
                claude_3_opus.id,
                gemini_1_flash.id,
                gemini_1_pro.id,
                gemini_1_ultra.id,
            ],
            subcategory_ids=[social_media_videos_subcategory.id],
            names={
                LanguageCode.RU: 'Генеративное искусство и NFT',
                LanguageCode.EN: 'Generative Art and NFTs',
            },
            short_prompts={
                LanguageCode.RU: """
Генеративное искусство и NFT: исследуй революцию в создании и владении цифровым искусством
""".strip(),
                LanguageCode.EN: """
Generative art meets NFTs, explore the revolution in digital art creation and ownership
""".strip(),
            },
            long_prompts={
                LanguageCode.RU: """
Напиши увлекательный сценарий для видео, которое исследует пересечение генеративного искусства и невзаимозаменяемых токенов (NFT). Обсуди, как эти технологии революционизируют мир искусства, позволяя художникам создавать уникальные цифровые произведения и находить связь с глобальной аудиторией. Приведи примеры успешных NFT с генеративным искусством и поделись инсайтами о том, как они могут трансформировать рынок искусства.
""".strip(),
                LanguageCode.EN: """
Create an engaging video script that explores the intersection of generative art and Non-Fungible Tokens (NFTs). Discuss how these technologies are revolutionizing the art world, enabling artists to create unique digital artworks and connect with global audiences. Provide examples of successful generative art NFTs and insights into their potential for transforming the art market.
""".strip(),
            },
        )

        social_media_content_plan_subcategory = await write_prompt_subcategory(
            category_ids=[social_media_category.id],
            names={
                LanguageCode.RU: 'Контент-План 📅',
                LanguageCode.EN: 'Content Plan 📅',
            },
        )
        await write_prompt(
            product_ids=[
                chat_gpt_omni_mini.id,
                chat_gpt_omni.id,
                claude_3_haiku.id,
                claude_3_sonnet.id,
                claude_3_opus.id,
                gemini_1_flash.id,
                gemini_1_pro.id,
                gemini_1_ultra.id,
            ],
            subcategory_ids=[social_media_content_plan_subcategory.id],
            names={
                LanguageCode.RU: 'Подготовка информативного White Paper',
                LanguageCode.EN: 'Write an informative White Paper',
            },
            short_prompts={
                LanguageCode.RU: """
Подготовь информативный White Paper на тему [Тема] для [Целевая Аудитория]. Включи исследования, ключевые разделы, визуализацию данных и практические рекомендации.
""".strip(),
                LanguageCode.EN: """
Write a White Paper on [Topic] for [Target Audience]. Include research, key content sections, data visualization, and actionable recommendations.
""".strip(),
            },
            long_prompts={
                LanguageCode.RU: """
Как эксперт в теме, профессионал индустрии или исследователь, вам поручено написать информативный White Paper на тему [Тема]. Цель White Paper — предоставить ценные идеи, анализ и практические рекомендации для целевой аудитории, интересующейся данной темой.

Для эффективной передачи ключевых концепций, выводов и рекомендаций, я предоставляю информацию по следующим направлениям:
- Тема White Paper: [Тема].
- Целевая аудитория: [Целевая Аудитория].
- Ключевые разделы: [Ключевые Разделы].
- Исследования и анализ: [Исследования и Анализ].
- Визуализация данных и иллюстрации: [Визуализация Данных и Иллюстрации].
- Рекомендации и выводы: [Рекомендации и Выводы].

Требования к задаче:
- Провести тщательное исследование и анализ выбранной темы, чтобы собрать релевантную информацию, идеи и доказательства для White Paper.
- Организовать White Paper в логические разделы, подразделы или главы для улучшения читаемости, понимания и удобной навигации для целевой аудитории.
- Написать ясный, лаконичный и увлекательный текст, эффективно передающий сложные концепции, аргументы и выводы для целевой аудитории.
- Включить визуализацию данных, иллюстрации или мультимедийные элементы для улучшения визуальной привлекательности и понятности White Paper.
- Предоставить рекомендации, идеи или выводы, основанные на достоверных источниках, эмпирических данных или мнениях экспертов.

Чек-лист лучших практик:
- Соблюдать академические стандарты, профессиональные рекомендации или отраслевые нормы при написании и форматировании White Paper.
- Использовать ясную и последовательную терминологию, определения и ссылки для поддержания согласованности и понятности текста.
- Цитировать релевантные источники, ссылки или цитаты для подтверждения утверждений, выводов или фактов, представленных в White Paper.
- Проверить и отредактировать документ на предмет точности, согласованности и читаемости, чтобы он соответствовал потребностям и ожиданиям целевой аудитории.
- Получить обратную связь от коллег, экспертов в области или заинтересованных сторон для проверки предположений, усиления аргументов и улучшения общего качества документа.

Результат:
- Предоставь готовый документ White Paper в профессиональном формате, готовый для распространения или публикации для целевой аудитории. Убедись, что документ написан качественно, информативно и убедительно, предоставляя ценные идеи и рекомендации по выбранной теме
""".strip(),
                LanguageCode.EN: """
As a subject matter expert, industry professional, or researcher, you're tasked with writing an informative White Paper on a [Topic]. The White Paper aims to provide valuable insights, analysis, and actionable recommendations to a target audience interested in the subject matter.

To ensure the White Paper effectively communicates key concepts, findings, and recommendations, I provide you details in the following areas:
- White Paper Topic: [Topic].
- Target Audience: [Target Audience]
- Key Content Sections: [Key Content Sections]
- Research and Analysis: [Research and Analysis]
- Data Visualization and Illustrations: [Data Visualization and Illustrations]
- Recommendations and Conclusion: [Recommendations and Conclusion]

Task Requirements:
- Conduct thorough research and analysis on the chosen topic to gather relevant information, insights, and evidence for the White Paper.
- Organize the White Paper into logical sections, subsections, or chapters to facilitate readability, comprehension, and navigation for the target audience.
- Write clear, concise, and engaging content that effectively communicates complex concepts, arguments, and findings to the intended audience.
- Incorporate data visualization, illustrations, or multimedia elements to enhance the visual appeal and clarity of the White Paper.
- Provide evidence-based recommendations, insights, or conclusions supported by credible sources, empirical evidence, or expert opinions.

Best Practices Checklist:
- Adhere to academic standards, professional guidelines, or industry conventions for writing and formatting White Papers.
- Use clear and consistent terminology, definitions, and references to maintain coherence and clarity throughout the document.
- Cite relevant sources, references, or citations to support assertions, claims, or findings presented in the White Paper.
- Review and revise the White Paper for accuracy, coherence, and readability, ensuring that it meets the needs and expectations of the target audience.
- Seek feedback from peers, subject matter experts, or stakeholders to validate assumptions, strengthen arguments, and improve the overall quality of the White Paper.

Deliverable:
- Submit the completed White Paper document in a professional format, ready for distribution or publication to the target audience. Ensure that the White Paper is well-written, informative, and persuasive, providing valuable insights and recommendations on the chosen topic
""".strip(),
            },
        )
        await write_prompt(
            product_ids=[
                chat_gpt_omni_mini.id,
                chat_gpt_omni.id,
                claude_3_haiku.id,
                claude_3_sonnet.id,
                claude_3_opus.id,
                gemini_1_flash.id,
                gemini_1_pro.id,
                gemini_1_ultra.id,
            ],
            subcategory_ids=[social_media_content_plan_subcategory.id],
            names={
                LanguageCode.RU: 'Создание контент-календаря для Instagram',
                LanguageCode.EN: 'Create an Instagram Content Calendar',
            },
            short_prompts={
                LanguageCode.RU: """
Разработай базовый контент-календарь для Instagram для компании [Название Компании] в [Индустрия]
""".strip(),
                LanguageCode.EN: """
Help me develop a basic Instagram content calendar for [Company Name] in the [Industry]
""".strip(),
            },
            long_prompts={
                LanguageCode.RU: """
Разработай контент-календарь для Instagram для компании [Название Компании] в [Индустрия].

Календарь должен включать:
- Чёткие цели и задачи для публикаций (например, увеличение вовлечённости, повышение осведомлённости, продвижение продуктов).
- Типы контента (посты, сторис, рилсы) и их частоту.
- Темы постов, которые будут интересны целевой аудитории.
- Оптимальные дни и время для публикации в зависимости от предпочтений аудитории.
- Идеи для визуального оформления и стиля публикаций.
- Примеры хэштегов, упоминаний и трендовых тем, которые можно использовать для продвижения.
- План регулярного анализа и корректировки контент-стратегии на основе метрик вовлечённости и отзывов аудитории.

Подготовь рекомендации по инструментам для планирования. Укажи, как структурировать контент, чтобы он был последовательным и поддерживал имидж компании [Название Компании].
""".strip(),
                LanguageCode.EN: """
Create an Instagram content calendar for [Company Name] in [Industry].

The calendar should include:
- Clear goals and objectives for posts (e.g., increasing engagement, raising brand awareness, promoting products).
- Types of content (posts, stories, reels) and their frequency.
- Topics for posts that would interest the target audience.
- Optimal days and times for posting based on audience preferences.
- Ideas for visual design and content style.
- Examples of hashtags, mentions, and trending topics that can be used for promotion.
- A plan for regular analysis and adjustment of the content strategy based on engagement metrics and audience feedback.

Provide recommendations for planning tools. Specify how to structure the content to ensure consistency and maintain the image of [Company Name].
""".strip(),
            },
        )
        await write_prompt(
            product_ids=[
                chat_gpt_omni_mini.id,
                chat_gpt_omni.id,
                claude_3_haiku.id,
                claude_3_sonnet.id,
                claude_3_opus.id,
                gemini_1_flash.id,
                gemini_1_pro.id,
                gemini_1_ultra.id,
            ],
            subcategory_ids=[social_media_content_plan_subcategory.id],
            names={
                LanguageCode.RU: 'Twitter (X): Увеличение вовлечённости в Twitter (X) с помощью интерактивных постов на тему [Контент]',
                LanguageCode.EN: 'Twitter (X): Boost Twitter (X) Engagement with Interactive [Content] Posts',
            },
            short_prompts={
                LanguageCode.RU: """
Создай динамичный контент-план для Twitter (X), чтобы увеличить вовлечённость. Используй интерактивный [Контент], который находит отклик у целевой аудитории. Оптимизируй время публикаций, темы и метрики, чтобы добиться значимых взаимодействий.
""".strip(),
                LanguageCode.EN: """
Craft a dynamic Twitter (X) content plan to boost engagement. Leverage interactive [Content] that resonates with your target audience. Optimize timing, themes, and metrics to drive meaningful interactions.
""".strip(),
            },
            long_prompts={
                LanguageCode.RU: """
Разработай комплексную стратегию и контент-план для увеличения вовлечённости в Twitter (X) через создание интерактивных постов на тему [Тема]. Предоставь детальный план, включающий следующие элементы:

Детали продукта:
- Тип контента: [Тип Контента (например, изображения, видео, опросы, анкеты и т. д.)]
- Темы контента: [Тема Контента]
- Основные цели вовлечённости: [Основные Цели Вовлечённости (например, увеличение лайков, ретвитов, комментариев, кликов и т. д.)]
- Целевая аудитория: [Целевая Аудитория]

Описание контента ([Длина Текста] слов):
- Привлекающее внимание введение: Опиши цель и ценность интерактивных постов на тему [Тема] для привлечения внимания аудитории.
- Идеи и темы контента: Определи конкретные идеи, темы и форматы контента, которые будут способствовать вовлечённости.
- Интерактивные элементы: Объясни, какие интерактивные функции (например, опросы, вопросы и ответы, призывы к действию) будут использоваться и как они побудят аудиторию к участию.
- Эмоциональная связь: Расскажи, как контент создаст эмоциональную связь с целевой аудиторией.
- Время и частота: Предоставь расписание публикации интерактивного контента для максимальной вовлечённости.
- Измерение и оптимизация: Опиши метрики для отслеживания вовлечённости и процесс постоянного улучшения.

Руководство по форматированию:
- Используй разговорный, но профессиональный тон.
- Организуй контент-план с чёткими заголовками разделов.
- Включай релевантные ключевые слова и хэштеги для улучшения видимости.
- Соблюдай единообразие форматирования (стиль шрифта, размер, отступы).
- Проверь контент-план на грамматические, орфографические ошибки и общую ясность.
""".strip(),
                LanguageCode.EN: """
Develop a comprehensive strategy and content plan to boost engagement on Twitter (X) by creating interactive [Content] posts. Provide a detailed outline covering the following:

Product Details:
- Content Type: [Content Type (e.g., images, videos, polls, surveys, etc.)]
- Content Topic(s): [Content Topic(s)]
- Key Engagement Goals: [Key Engagement Goals (e.g., increase likes, retweets, comments, click-through rates, etc.)]
- Target Audience: [Target Audience]

Content Description ([Content Length] words):
- Attention-Grabbing Introduction: Describe the purpose and value of the interactive [content] posts in capturing the audience's attention.
- Content Ideation and Themes: Outline the specific content ideas, themes, and formats that will drive engagement.
- Interactive Elements: Explain the interactive features (e.g., polls, Q&A, CTAs) and how they will encourage audience participation.
- Emotional Connection: Discuss how the content will create an emotional connection with the target audience.
- Timing and Frequency: Provide a schedule for posting the interactive [content] to maximize engagement.
- Measurement and Optimization: Describe the metrics to track engagement and the process for continual improvement.

Formatting Guidelines:
- Use a conversational yet professional tone.
- Organize the content plan with clear section headings.
- Incorporate relevant keywords and hashtags to improve discoverability.
- Ensure consistent formatting, including font style, size, and spacing.
- Proofread the content plan for grammar, spelling, and overall clarity.
""".strip(),
            },
        )

        education_category = await write_prompt_category(
            model_type=ModelType.TEXT,
            names={
                LanguageCode.RU: 'Образование 👩‍🏫',
                LanguageCode.EN: 'Education 👩‍🏫',
            },
        )
        education_curriculum_subcategory = await write_prompt_subcategory(
            category_ids=[education_category.id],
            names={
                LanguageCode.RU: 'Учебный План 📅',
                LanguageCode.EN: 'Учебный План 📅',
            },
        )
        await write_prompt(
            product_ids=[
                chat_gpt_omni_mini.id,
                chat_gpt_omni.id,
                claude_3_haiku.id,
                claude_3_sonnet.id,
                claude_3_opus.id,
                gemini_1_flash.id,
                gemini_1_pro.id,
                gemini_1_ultra.id,
            ],
            subcategory_ids=[education_curriculum_subcategory.id],
            names={
                LanguageCode.RU: 'Развитие навыков критического мышления через проектно-ориентированную [Учебный План]',
                LanguageCode.EN: 'Cultivating Critical Thinking Skills through Project-Based [Curriculum]',
            },
            short_prompts={
                LanguageCode.RU: """
Разработай проектно-ориентированную [Учебный План] для развития навыков критического мышления у студентов. Определи ключевые учебные цели с акцентом на решение проблем и аналитическое мышление. Включи 3-5 заданий, направленных на развитие креативности и совместного поиска решений. Оценивай прогресс в критическом мышлении с помощью формативных и итоговых оценочных инструментов
""".strip(),
                LanguageCode.EN: """
Develop a project-based [Curriculum] to cultivate critical thinking skills in students. Outline key learning objectives emphasizing problem-solving and analytical reasoning. Engage students in 3-5 activities fostering creativity and collaborative problem-solving. Assess critical thinking development through formative and summative evaluations.
""".strip(),
            },
            long_prompts={
                LanguageCode.RU: """
Разработай детальный план проектно-ориентированной [Учебный План], которая способствует развитию навыков критического мышления у студентов. Программа должна включать следующие компоненты:

Обзор программы:
- Кратко опиши цели программы, целевую аудиторию и основной фокус на развитие критического мышления.

Учебные цели:
- Определи ключевые учебные цели, которых должны достичь студенты через проектно-ориентированные занятия.
- Убедись, что цели подчеркивают развитие навыков критического мышления, решение проблем и аналитическое мышление.

Проектно-ориентированные занятия:
- Опиши 3-5 занятий, основанных на проектной деятельности, в которых будут участвовать студенты.
- Для каждого занятия предоставь следующие детали: описание проекта, ожидаемые результаты обучения, необходимые ресурсы и рекомендации по реализации.
- Объясни, как эти занятия способствуют развитию критического мышления, креативности и совместного решения проблем.

Оценка и анализ:
- Определи методы оценки, которые будут использоваться для анализа прогресса студентов в развитии критического мышления.
- Включи как формативные, так и итоговые стратегии оценки, такие как презентации проектов, письменные рефлексии и задания, основанные на выполнении практических задач.
- Рекомендации по реализации:

Дай рекомендации по эффективной реализации программы, включая предложенные временные рамки, методы преподавания, возможные трудности и стратегии их преодоления.
""".strip(),
                LanguageCode.EN: """
Develop a detailed project-based [Curriculum] outline that encourages the development of critical thinking skills among students. The curriculum should include the following components:

Curriculum Overview:
- Provide a brief summary of the curriculum's objectives, target audience, and core focus on cultivating critical thinking.

Learning Objectives:
- Outline the key learning objectives students will achieve through the project-based activities.
- Ensure the objectives emphasize the development of critical thinking skills, problem-solving, and analytical reasoning.

Project-Based Activities:
- Describe 3-5 project-based learning activities that students will engage in.
- For each activity, include details such as project description, learning outcomes, required resources, and implementation guidelines.
- Explain how the activities are designed to foster critical thinking, creativity, and collaborative problem-solving.

Assessment and Evaluation:
- Outline the assessment methods that will be used to evaluate students' critical thinking skills development.
- Include both formative and summative assessment strategies, such as project presentations, written reflections, and performance-based tasks.

Implementation Considerations:
- Provide guidance on how the curriculum can be effectively implemented, including suggested timelines, teaching methodologies, and potential challenges and mitigation strategies.
""".strip(),
            },
        )
        await write_prompt(
            product_ids=[
                chat_gpt_omni_mini.id,
                chat_gpt_omni.id,
                claude_3_haiku.id,
                claude_3_sonnet.id,
                claude_3_opus.id,
                gemini_1_flash.id,
                gemini_1_pro.id,
                gemini_1_ultra.id,
            ],
            subcategory_ids=[education_curriculum_subcategory.id],
            names={
                LanguageCode.RU: 'Создание интерактивных модулей для обучения по теме [Тема]',
                LanguageCode.EN: 'Creating Interactive Modules for [Subject] Instruction',
            },
            short_prompts={
                LanguageCode.RU: """
Создай набор интерактивных обучающих модулей, охватывающих ключевые моменты по теме [Тема]. Используй мультимедиа, практические задания и оценки, чтобы заинтересовать студентов. Определи темы модулей, элементы, дизайн и критерии оценки
""".strip(),
                LanguageCode.EN: """
Create a set of interactive learning modules covering key topics in [Subject]. Blend multimedia, hands-on activities, and assessments to engage students. Outline module topics, elements, design, and evaluation criteria
""".strip(),
            },
            long_prompts={
                LanguageCode.RU: """
Разработай полный набор интерактивных обучающих модулей, охватывающих ключевые моменты по теме [Тема]. Каждый модуль должен сочетать мультимедийные элементы, практические задания и инструменты для оценки, чтобы заинтересовать студентов и укрепить их понимание материала. Предоставь подробную информацию по каждому из следующих пунктов:

Темы модулей:
- [Тема модуля 1]
- [Тема модуля 2]
- [Тема модуля 3]
- [Тема модуля 4]
- [Тема модуля 5]

Элементы модулей:
- Учебные цели
- Ключевые концепции и теории
- Интерактивные симуляции или анимации
- Увлекательные видео-лекции или презентации
- Практические задания для применения знаний
- Проверка знаний и инструменты оценки
- Дополнительные ресурсы и ссылки

Дизайн и форматирование модулей:
- Структурированный макет с чёткой навигацией
- Визуально привлекательный и адаптивный дизайн
- Доступность для студентов с различными потребностями
- Единый стиль и брендинг
- Интуитивный пользовательский опыт

Критерии оценки:
- Эффективность в достижении учебных целей
- Качество и актуальность контента
- Интерактивность и увлекательность заданий
- Простота использования и навигации
- Соответствие стандартам учебной программы по теме [Тема]
""".strip(),
                LanguageCode.EN: """
Develop a comprehensive set of interactive learning modules covering the key topics in [Subject]. Each module should blend multimedia elements, hands-on activities, and assessment tools to engage students and reinforce their understanding of the subject matter. Provide detailed information for each of the following:

Module Topics:
- [Module Topic 1]
- [Module Topic 2]
- [Module Topic 3]
- [Module Topic 4]
- [Module Topic 5]

Module Elements:
- Learning Objectives
- Key Concepts and Theories
- Interactive Simulations or Animations
- Engaging Video Lectures or Presentations
- Hands-on Application Exercises
- Knowledge Checks and Assessments
- Additional Resources and References

Module Design and Formatting:
- Structured Layout with Clear Navigation
- Visually Appealing and Responsive Design
- Accessible for Students with Diverse Needs
- Consistent Branding and Styling
- Intuitive User Experience

Evaluation Criteria:
- Effectiveness in Achieving Learning Objectives
- Quality and Relevance of Content
- Interactivity and Engagement of Activities
- Ease of Use and Navigation
- Alignment with [Subject] Curriculum Standards
""".strip(),
            },
        )
        await write_prompt(
            product_ids=[
                chat_gpt_omni_mini.id,
                chat_gpt_omni.id,
                claude_3_haiku.id,
                claude_3_sonnet.id,
                claude_3_opus.id,
                gemini_1_flash.id,
                gemini_1_pro.id,
                gemini_1_ultra.id,
            ],
            subcategory_ids=[education_curriculum_subcategory.id],
            names={
                LanguageCode.RU: 'Разработка учебной программы по [Предмет] для [Уровень Класса]',
                LanguageCode.EN: 'Develop a curriculum for [Subject] at the [Grade Level]',
            },
            short_prompts={
                LanguageCode.RU: """
Краткий план учебной программы по [Предмет] для [Уровень Класса]:
- Определи ключевые учебные цели, увлекательные планы уроков и разнообразные методы оценки.
- Согласуй программу с образовательными стандартами, учитывай потребности разных учащихся и обеспечь эффективное внедрение.
- Предоставь полный набор ресурсов и стратегий для создания содержательной и эффективной программы по [Предмет].
- Корректируй программу по мере необходимости для обеспечения качественного и интуитовного образовательного опыта.
""".strip(),
                LanguageCode.EN: """
Compact curriculum plan for teaching [Subject] at [Grade Level]:
- Outline key learning objectives, engaging lesson plans, and diverse assessments.
- Align to educational standards, accommodate diverse learners, and implement effectively.
- Provide comprehensive resources and strategies for an impactful [Subject] curriculum.
- Refine as needed to ensure a robust and enriching educational experience.
""".strip(),
            },
            long_prompts={
                LanguageCode.RU: """
Предоставь подробный план учебной программы для преподавания [Предмет] для [Уровень Класса] класса. Программа должна включать детализированные планы уроков, учебные цели, методики преподавания, стратегии оценки и любые необходимые материалы или ресурсы.

Основные детали для включения:
- Область предмета: [Предмет]
- Уровень класса: [Уровень Класса]
- Общие учебные цели курса
- Детализированные планы уроков ([Количество Уроков] уроков):
    - Название урока, продолжительность и учебные цели
    - Инструктивные стратегии и методы преподавания
    - Студенческие активности и оценочные задания
    - Необходимые материалы и ресурсы
- Соответствие образовательным стандартам
- Стратегии дифференцированного обучения и инклюзии
- Рекомендуемые форматы итоговой оценки
- График реализации учебной программы

Рекомендации по форматированию:
- Используй понятный и лаконичный язык, соответствующий образовательному контексту.
- Организуй программу в логической и простой для восприятия структуре.
- Включай релевантные образовательные термины и лучшие практики.
- Проверь документ на грамматические ошибки, орфографию и общую ясность.

Дай знать, если тебе нужны дополнительные требования или помощь.
""".strip(),
                LanguageCode.EN: """
Provide a comprehensive curriculum outline for teaching [Subject] at the [Grade Level]. The curriculum should include detailed lesson plans, learning objectives, teaching methodologies, assessment strategies, and any required materials or resources.

Key Details to Include:
- Subject Area: [Subject]
- Grade Level: [Grade Level]
- Overall Learning Objectives for the Course
- Detailed Lesson Plans ([Lessons Count] lessons):
  - Lesson Title, Duration, and Learning Objectives
  - Instructional Strategies and Teaching Methods
  - Student Activities and Assessments
  - Required Materials and Resources
- Alignment to Relevant Educational Standards
- Strategies for Differentiated Instruction and Inclusion
- Suggested Summative Assessment Formats
- Timeline for Curriculum Implementation

Formatting Guidelines:
- Use clear and concise language appropriate for the educational context
- Organize the curriculum in a logical and easy-to-follow structure
- Incorporate relevant educational terminology and best practices
- Proofread the document for grammar, spelling, and overall clarity

Let me know if you have any other requirements or need further assistance
""".strip(),
            },
        )

        architecture_category = await write_prompt_category(
            model_type=ModelType.IMAGE,
            names={
                LanguageCode.RU: 'Архитектура 🏗',
                LanguageCode.EN: 'Architecture 🏗',
            },
        )
        architecture_interior_design_subcategory = await write_prompt_subcategory(
            category_ids=[architecture_category.id],
            names={
                LanguageCode.RU: 'Дизайн Интерьера 🛋',
                LanguageCode.EN: 'Interior Design 🛋',
            },
        )
        await write_prompt(
            product_ids=[
                dall_e.id,
                midjourney.id,
                stable_diffusion.id,
                flux.id,
            ],
            subcategory_ids=[architecture_interior_design_subcategory.id],
            names={
                LanguageCode.RU: 'Современная Гостиная',
                LanguageCode.EN: 'Modern Living Room',
            },
            short_prompts={
                LanguageCode.RU: 'Гостиная с удобным цилиндрическим мягким креслом и пуфом, выполненная в чёрно-красных тонах, профессиональная фотосъёмка',
                LanguageCode.EN: 'Living room with comfortable, cylindrical, plush chair with footstool, black and red, professional photography',
            },
            long_prompts={
                LanguageCode.RU: '',
                LanguageCode.EN: '',
            },
            has_examples=True,
        )
        await write_prompt(
            product_ids=[
                dall_e.id,
                midjourney.id,
                stable_diffusion.id,
                flux.id,
            ],
            subcategory_ids=[architecture_interior_design_subcategory.id],
            names={
                LanguageCode.RU: 'Минималистичное Лобби',
                LanguageCode.EN: 'Minimalist Lobby',
            },
            short_prompts={
                LanguageCode.RU: '2D, минимализм, белый пол с волнами в вестибюле, оттенки светло-голубого, декоративные линии, точные линии, контровой свет, изящные линии, органические материалы',
                LanguageCode.EN: '2D, minimalist, a white floor with waves in the lobby, shades of light blue, decorative lines, precisionist lines, rim light, delicate lines, organic material',
            },
            long_prompts={
                LanguageCode.RU: '',
                LanguageCode.EN: '',
            },
            has_examples=True,
        )
        await write_prompt(
            product_ids=[
                dall_e.id,
                midjourney.id,
                stable_diffusion.id,
                flux.id,
            ],
            subcategory_ids=[architecture_interior_design_subcategory.id],
            names={
                LanguageCode.RU: 'Лауреатная Архитектурная Фотография',
                LanguageCode.EN: 'Award Winning Architectural Photography',
            },
            short_prompts={
                LanguageCode.RU: 'Архитектурная фотография, отмеченная наградами: мягко рассеянный свет в частной резиденции, современное и роскошное офисное пространство, в стиле светящегося неона, V-Ray, колонны и тотемы, вдохновлено индустриальным стилем, яркое фиолетовое и голубое рассеянное освещение, мягко подсвеченный потолок с рассеянным светом, мягко подсвеченная стена, человек',
                LanguageCode.EN: 'Award winning architectural photography: soft diffuse private residence, modern and luxurious office workspace, in the style of glowing neon, vray, columns and totems, industrial-inspired, bright violet and blue diffuse lighting, soft diffuse backlit ceiling, soft diffuse backlit wall, man',
            },
            long_prompts={
                LanguageCode.RU: '',
                LanguageCode.EN: '',
            },
            has_examples=True,
        )

        architecture_exterior_design_subcategory = await write_prompt_subcategory(
            category_ids=[architecture_category.id],
            names={
                LanguageCode.RU: 'Дизайн Экстерьера ⛲️',
                LanguageCode.EN: 'Exterior Design ⛲️',
            },
        )
        await write_prompt(
            product_ids=[
                dall_e.id,
                midjourney.id,
                stable_diffusion.id,
                flux.id,
            ],
            subcategory_ids=[architecture_exterior_design_subcategory.id],
            names={
                LanguageCode.RU: 'Современный Дом',
                LanguageCode.EN: 'Modern House',
            },
            short_prompts={
                LanguageCode.RU: 'Современный дом с высоким современным чёрным забором',
                LanguageCode.EN: 'Modern house with high modern black fense',
            },
            long_prompts={
                LanguageCode.RU: '',
                LanguageCode.EN: '',
            },
            has_examples=True,
        )
        await write_prompt(
            product_ids=[
                dall_e.id,
                midjourney.id,
                stable_diffusion.id,
                flux.id,
            ],
            subcategory_ids=[architecture_exterior_design_subcategory.id],
            names={
                LanguageCode.RU: 'Игровая Площадка',
                LanguageCode.EN: 'Play Ground Area',
            },
            short_prompts={
                LanguageCode.RU: 'Мудборд ландшафтного дизайна с игровой зоной для детей, включающей песочницу и горку, окружённую гравийными клумбами для посадки растений, поднятая зона для отдыха выложена серыми камнями необычной формы или плитами, соединёнными белыми швами, с утопленным кострищем, высажены пальмы, лаванда, иксора, бугенвиллия и газон. По газону проложены серые ступени, а длинная дорожка выложена бежевыми камнями неправильной формы, соединёнными белыми швами, высокая степень реализма',
                LanguageCode.EN: 'Mood board of landscape design having a play ground area for kids with sand and house slide surrounding with gravel garden bed for planting, a raised seating area with grey crazy stones or flagstones joined together with white joints with sun keen fire pit palms lavender exiora jahanamya and grass and grey steeping stones on grass and a long pathway with beige crazy stones random shape joined together with white joints, high realistic',
            },
            long_prompts={
                LanguageCode.RU: '',
                LanguageCode.EN: '',
            },
            has_examples=True,
        )
        await write_prompt(
            product_ids=[
                dall_e.id,
                midjourney.id,
                stable_diffusion.id,
                flux.id,
            ],
            subcategory_ids=[architecture_exterior_design_subcategory.id],
            names={
                LanguageCode.RU: 'Футуристический Голландский Жилой Комплекс',
                LanguageCode.EN: 'Futuristic Dutch Apartment',
            },
            short_prompts={
                LanguageCode.RU: 'Кинематографический вид футуристического голландского жилого комплекса, достигающего облаков, с монолитным блестящим алюминиевым фасадом и стальными балками, завораживающий своей архитектурой. Сады перед зданием, тротуар и дорога, машины на переднем плане, рядом парк, на пруду с камышом. Утренний туман, сквозь который пробиваются солнечные лучи. В стиле Хадид. Архитектурная фотография уровня Architectural Digest, отмеченная наградами. Высокий контраст, хроматическая аберрация, глубина резкости',
                LanguageCode.EN: 'Cinematic view a futuristic dutch apartment complex reaching the clouds made of monolithic shiny aluminum facade and steel beams, a marvel to look at, gardens in front, in the style of Hadid, sidewalk and road, cars in front, next to a park, on the pond with reed, foggy in the morning, sun coming through, architectural digest, award winning photography, high contrast, chromatic abberation, depth of field',
            },
            long_prompts={
                LanguageCode.RU: '',
                LanguageCode.EN: '',
            },
            has_examples=True,
        )

        melodies_category = await write_prompt_category(
            model_type=ModelType.MUSIC,
            names={
                LanguageCode.RU: 'Мелодии 🎶',
                LanguageCode.EN: 'Melodies 🎶',
            },
        )
        melodies_classic_subcategory = await write_prompt_subcategory(
            category_ids=[melodies_category.id],
            names={
                LanguageCode.RU: 'Классическая 🎹',
                LanguageCode.EN: 'Classic 🎹',
            },
        )
        await write_prompt(
            product_ids=[
                music_gen.id,
            ],
            subcategory_ids=[melodies_classic_subcategory.id],
            names={
                LanguageCode.RU: 'Грустная Камерная Музыка',
                LanguageCode.EN: 'Sad Chamber Music',
            },
            short_prompts={
                LanguageCode.RU: 'Дуэт фортепиано и виолончели, играющий грустную камерную музыку',
                LanguageCode.EN: 'Duet of piano and cello, playing sad chamber music',
            },
            long_prompts={
                LanguageCode.RU: '',
                LanguageCode.EN: '',
            },
        )
        await write_prompt(
            product_ids=[
                music_gen.id,
            ],
            subcategory_ids=[melodies_classic_subcategory.id],
            names={
                LanguageCode.RU: 'Ужин при Свечах',
                LanguageCode.EN: 'Candlelit Dinner',
            },
            short_prompts={
                LanguageCode.RU: 'Классическая музыка для ужина при свечах',
                LanguageCode.EN: 'Classical music for a candlelit dinner',
            },
            long_prompts={
                LanguageCode.RU: '',
                LanguageCode.EN: '',
            },
        )
        await write_prompt(
            product_ids=[
                music_gen.id,
            ],
            subcategory_ids=[melodies_classic_subcategory.id],
            names={
                LanguageCode.RU: 'Глубокие Размышления',
                LanguageCode.EN: 'Deep Reflections',
            },
            short_prompts={
                LanguageCode.RU: 'Меланхоличная виолончель для глубоких размышлений',
                LanguageCode.EN: 'Melancholic cello for deep reflections',
            },
            long_prompts={
                LanguageCode.RU: '',
                LanguageCode.EN: '',
            },
        )

        melodies_calm_subcategory = await write_prompt_subcategory(
            category_ids=[melodies_category.id],
            names={
                LanguageCode.RU: 'Спокойная 🎻',
                LanguageCode.EN: 'Calm 🎻',
            },
        )
        await write_prompt(
            product_ids=[
                music_gen.id,
            ],
            subcategory_ids=[melodies_calm_subcategory.id],
            names={
                LanguageCode.RU: 'Релаксация и Умиротворение',
                LanguageCode.EN: 'Relaxation and Peace',
            },
            short_prompts={
                LanguageCode.RU: 'Спокойная медитативная музыка с восточными мотивами для релаксации и умиротворения',
                LanguageCode.EN: 'Calm meditative music with Eastern motifs for relaxation and peace',
            },
            long_prompts={
                LanguageCode.RU: '',
                LanguageCode.EN: '',
            },
        )
        await write_prompt(
            product_ids=[
                music_gen.id,
            ],
            subcategory_ids=[melodies_calm_subcategory.id],
            names={
                LanguageCode.RU: 'Шум Дождя',
                LanguageCode.EN: 'Sound of Rain',
            },
            short_prompts={
                LanguageCode.RU: 'Расслабляющая музыка для сна с шумом дождя',
                LanguageCode.EN: 'Relaxing music for sleep with the sound of rain',
            },
            long_prompts={
                LanguageCode.RU: '',
                LanguageCode.EN: '',
            },
        )
        await write_prompt(
            product_ids=[
                music_gen.id,
            ],
            subcategory_ids=[melodies_calm_subcategory.id],
            names={
                LanguageCode.RU: 'Йога',
                LanguageCode.EN: 'Yoga',
            },
            short_prompts={
                LanguageCode.RU: 'Легкая и воздушная музыка для йоги',
                LanguageCode.EN: 'Light and airy music for yoga',
            },
            long_prompts={
                LanguageCode.RU: '',
                LanguageCode.EN: '',
            },
        )

        songs_category = await write_prompt_category(
            model_type=ModelType.MUSIC,
            names={
                LanguageCode.RU: 'Песни 🎤',
                LanguageCode.EN: 'Songs 🎤',
            },
        )
        songs_person_subcategory = await write_prompt_subcategory(
            category_ids=[songs_category.id],
            names={
                LanguageCode.RU: 'Человек 👤',
                LanguageCode.EN: 'Person 👤',
            },
        )
        await write_prompt(
            product_ids=[
                suno.id,
            ],
            subcategory_ids=[songs_person_subcategory.id],
            names={
                LanguageCode.RU: 'Песня, чтобы Отпраздновать Особенного Человека в Твоей Жизни',
                LanguageCode.EN: 'Song to Celebrate a Special Person in Your Life',
            },
            short_prompts={
                LanguageCode.RU: """
Я праздную [Имя Человека], моего/мою [Кем Он/Она Вам Приходится].
Моё любимое в нём/ней — это [То, Что Вам Больше Всего Нравится], а самое смешное в нём/ней — это [Самое Забавное Качество или Ситуация].
Его/её любимый жанр музыки — это [Жанр].
""".strip(),
                LanguageCode.EN: """
I'm celebrating [Name of Person] my [Relationship to Person].
My favorite thing about them is [Favorite Thing About Them], and the funniest thing about them is [Funniest Thing About Them].
Their favorite genre of music is [Genre].
""".strip(),
            },
            long_prompts={
                LanguageCode.RU: '',
                LanguageCode.EN: '',
            },
        )

        songs_pet_subcategory = await write_prompt_subcategory(
            category_ids=[songs_category.id],
            names={
                LanguageCode.RU: 'Питомец 🐶',
                LanguageCode.EN: 'Pet 🐶',
            },
        )
        await write_prompt(
            product_ids=[
                suno.id,
            ],
            subcategory_ids=[songs_pet_subcategory.id],
            names={
                LanguageCode.RU: 'Песня, чтобы Отпраздновать Вашего Питомца и то, Как Он Делает Вашу Жизнь Лучше',
                LanguageCode.EN: 'Song to Celebrate Your Pet and How They Make Your Life Better',
            },
            short_prompts={
                LanguageCode.RU: """
Моего питомца зовут [Имя Питомца], и это [Тип Питомца].
Он/она [Внешний Вид Питомца], и он/она всегда заставляет меня улыбаться, потому что [То, что Вы в Нём/Ней Любите].
Если бы он/она слушал(а) музыку, его/её любимым жанром был бы [Жанр].
""".strip(),
                LanguageCode.EN: """
My pet's name is [Name of Pet] and they are a [Type of Pet].
They are [Physical Appearance], and they always make me smile because [Thing You Love About Them].
If they listened to music, their favorite genre would be [Genre].
""".strip(),
            },
            long_prompts={
                LanguageCode.RU: '',
                LanguageCode.EN: '',
            },
        )

        await send_message_to_admins_and_developers(bot, '<b>Second Database Migration Was Successful!</b> 🎉')
    except Exception as e:
        logging.exception(e)
        await send_message_to_admins_and_developers(bot, '<b>Second Database Migration Was Not Successful!</b> 🚨')
