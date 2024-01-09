from bot.database.operations.role import get_role_by_name, write_role


class RoleInfo:
    PERSONAL_ASSISTANT = {
        'name': "PERSONAL_ASSISTANT",
        'translated_names': {
            'en': '🤖 Personal assistant',
            'ru': '🤖 Персональный ассистент',
        },
        'translated_descriptions': {
            'en': """
Your go-to for anything and everything!
From answering questions to deep conversations, I'm here to assist you like a trusty sidekick 🌟
Let's tackle life's puzzles together!
""",
            'ru': """
Ваш надёжный помощник во всём и для всего!
От простых ответов до глубоких бесед, я здесь, чтобы помочь вам, как верный спутник 🌟
Давайте вместе решим жизненные головоломки!
"""
        },
        'translated_instructions': {
            'en': 'You are a helpful assistant.',
            'ru': 'Ты полезный личный ассистент',
        },
    }
    TUTOR = {
        'name': "TUTOR",
        'translated_names': {
            'en': '📚 Tutor',
            'ru': '📚 Репетитор',
        },
        'translated_descriptions': {
            'en': """
Unlock the world of knowledge across all subjects!
I'm here to make complex concepts simple and learning enjoyable 📚
Whether it's math, science, or art, let's learn together!
""",
            'ru': """
Откройте для себя мир знаний по всем предметам!
Я здесь, чтобы сделать сложные концепции простыми и обучение увлекательным 📚
Будь то математика, наука или искусство, давайте учиться вместе!
"""
        },
        'translated_instructions': {
            'en': 'You are a helpful tutor.',
            'ru': 'Ты полезный репетитор',
        },
    }
    LANGUAGE_TUTOR = {
        'name': "LANGUAGE_TUTOR",
        'translated_names': {
            'en': '🗣️ Language tutor',
            'ru': '🗣️ Репетитор по иностранным языкам',
        },
        'translated_descriptions': {
            'en': """
Embark on a linguistic adventure!
From basic phrases to fluency, I'll guide you through the nuances of languages with ease and fun 🌐
Let's converse in new tongues!
""",
            'ru': """
Отправляйтесь в лингвистическое приключение!
От основных фраз до свободного владения, я помогу вам изучить языки легко и с удовольствием 🌐
Давайте общаться на новых языках!
"""
        },
        'translated_instructions': {
            'en': 'You are a helpful language tutor.',
            'ru': 'Ты полезный репетитор по иностранным языкам',
        },
    }
    CREATIVE_WRITER = {
        'name': "CREATIVE_WRITER",
        'translated_names': {
            'en': '🖋️ Creative writer',
            'ru': '🖋️ Креативный писатель',
        },
        'translated_descriptions': {
            'en': """
Ready to explore worlds of wonder?
From crafting captivating stories to penning heartfelt poetry, let's unleash our collective creativity 🖋️
Your imagination is the limit!
""",
            'ru': """
Готовы исследовать миры чудес?
От создания захватывающих историй до написания трогательной поэзии, давайте вместе раскроем наше творчество 🖋️
Ваше воображение - это предел!
"""
        },
        'translated_instructions': {
            'en': 'You are a helpful creative writer.',
            'ru': 'Ты полезный креативный писатель',
        },
    }
    TECHNICAL_ADVISOR = {
        'name': "TECHNICAL_ADVISOR",
        'translated_names': {
            'en': '💻 Technical advisor',
            'ru': '💻 Технический консультант',
        },
        'translated_descriptions': {
            'en': """
Navigating the tech maze made easy!
Whether it's understanding new software, fixing bugs, or exploring tech trends, I'm here to simplify technology 💻
Let's decode the digital world together!
""",
            'ru': """
Лёгкий путь через технический лабиринт!
Будь то понимание нового ПО, устранение ошибок или изучение технических тенденций, я здесь, чтобы упростить технологии 💻
Давайте вместе разбираться в цифровом мире!
"""
        },
        'translated_instructions': {
            'en': 'You are a helpful technical advisor.',
            'ru': 'Ты полезный технический консультант',
        },
    }
    MARKETER = {
        'name': "MARKETER",
        'translated_names': {
            'en': '📈 Marketer',
            'ru': '📈 Маркетолог',
        },
        'translated_descriptions': {
            'en': """
Let's elevate your brand and outreach!
From market research to campaign strategies, I'm here to help you navigate the marketing landscape and achieve your business goals 📊
Your success is our target!
""",
            'ru': """
Давайте поднимем ваш бренд и охват!
От исследования рынка до стратегий кампаний, я здесь, чтобы помочь вам в навигации по маркетинговому ландшафту и достижению ваших бизнес-целей 📊
Ваш успех - наша цель!
"""
        },
        'translated_instructions': {
            'en': 'You are a helpful marketer.',
            'ru': 'Ты полезный маркетолог',
        },
    }
    SMM_SPECIALIST = {
        'name': "SMM_SPECIALIST",
        'translated_names': {
            'en': '📱 SMM-Specialist',
            'ru': '📱 SMM-Специалист',
        },
        'translated_descriptions': {
            'en': """
Transform your social media presence!
I'll help you create engaging content, grow your audience, and stay ahead in the ever-evolving social media space 📱
Let's make social media work for you!
""",
            'ru': """
Преобразите ваше присутствие в социальных сетях!
Я помогу вам создать увлекательный контент, расширить вашу аудиторию и оставаться на шаг впереди в постоянно меняющемся мире социальных сетей 📱
Давайте сделаем социальные сети вашим инструментом!
"""
        },
        'translated_instructions': {
            'en': 'You are a helpful SMM-specialist.',
            'ru': 'Ты полезный SMM-Специалист',
        },
    }
    CONTENT_SPECIALIST = {
        'name': "CONTENT_SPECIALIST",
        'translated_names': {
            'en': '📝 Content specialist',
            'ru': '📝 Специалист по контенту',
        },
        'translated_descriptions': {
            'en': """
Content is king, and I'm here to help you rule!
From SEO optimization to compelling copy, let's create content that resonates and engages ✍️
Your message matters!
""",
            'ru': """
Контент - это король, и я здесь, чтобы помочь вам властвовать!
От оптимизации SEO до увлекательных текстов, давайте создадим контент, который будет резонировать и привлекать внимание ✍️
Ваше сообщение имеет значение!
"""
        },
        'translated_instructions': {
            'en': 'You are a helpful content specialist.',
            'ru': 'Ты полезный специалист по контенту',
        },
    }
    DESIGNER = {
        'name': "DESIGNER",
        'translated_names': {
            'en': '🎨 Designer',
            'ru': '🎨 Дизайнер',
        },
        'translated_descriptions': {
            'en': """
Visual storytelling at its best!
Let's design experiences that captivate and communicate, from websites to brand identities 🖌️
Your vision, our canvas!
""",
            'ru': """
Визуальное повествование в лучшем виде!
Давайте создадим дизайн, который завораживает и передаёт идеи, будь то веб-сайты или фирменные стили 🖌️
Ваше видение, наш холст!
"""
        },
        'translated_instructions': {
            'en': 'You are a helpful designer.',
            'ru': 'Ты полезный дизайнер',
        },
    }
    SOCIAL_MEDIA_PRODUCER = {
        'name': "SOCIAL_MEDIA_PRODUCER",
        'translated_names': {
            'en': '📸 Producer in social media',
            'ru': '📸 Продюсер в социальных сетях',
        },
        'translated_descriptions': {
            'en': """
Crafting stories that click and connect on social media!
Let's produce content that stands out and speaks to your audience 🎥
Your story, brilliantly told on social platforms!
""",
            'ru': """
Создаём истории, которые запоминаются и связывают на социальных сетях!
Давайте производим контент, который выделяется и говорит с вашей аудиторией 🎥
Ваша история, блестяще рассказанная в социальных платформах!
"""
        },
        'translated_instructions': {
            'en': 'You are a helpful social media producer.',
            'ru': 'Ты полезный продюсер в социальных сетях',
        },
    }
    LIFE_COACH = {
        'name': "LIFE_COACH",
        'translated_names': {
            'en': '🌱 Life coach',
            'ru': '🌱 Лайф-коуч',
        },
        'translated_descriptions': {
            'en': """
Empowering you to reach your fullest potential!
From setting goals to overcoming obstacles, I'm here to support and inspire you on your journey to personal growth 🌱
Let's grow together!
""",
            'ru': """
Помогаю вам достичь вашего полного потенциала!
От постановки целей до преодоления препятствий, я здесь, чтобы поддержать и вдохновить вас на вашем пути к личностному росту 🌱
Давайте расти вместе!
"""
        },
        'translated_instructions': {
            'en': 'You are a helpful life coach.',
            'ru': 'Ты полезный лайф-коуч',
        },
    }
    ENTREPRENEUR = {
        'name': "ENTREPRENEUR",
        'translated_names': {
            'en': '💼 Entrepreneur',
            'ru': '💼 Предприниматель',
        },
        'translated_descriptions': {
            'en': """
Turning ideas into reality!
Whether it's starting a business or scaling up, let's navigate the entrepreneurial journey with innovative strategies and insights 💡
Your dream, our mission!
""",
            'ru': """
Превращаем идеи в реальность!
Будь то запуск бизнеса или его масштабирование, давайте вместе пройдем предпринимательский путь с инновационными стратегиями и прозрениями 💡
Ваша мечта - наша миссия!
"""
        },
        'translated_instructions': {
            'en': 'You are a helpful entrepreneur.',
            'ru': 'Ты полезный предприниматель',
        },
    }


async def load_roles():
    roles = [
        RoleInfo.PERSONAL_ASSISTANT['name'],
        RoleInfo.TUTOR['name'],
        RoleInfo.LANGUAGE_TUTOR['name'],
        RoleInfo.CREATIVE_WRITER['name'],
        RoleInfo.TECHNICAL_ADVISOR['name'],
        RoleInfo.MARKETER['name'],
        RoleInfo.SMM_SPECIALIST['name'],
        RoleInfo.CONTENT_SPECIALIST['name'],
        RoleInfo.DESIGNER['name'],
        RoleInfo.SOCIAL_MEDIA_PRODUCER['name'],
        RoleInfo.LIFE_COACH['name'],
        RoleInfo.ENTREPRENEUR['name'],
    ]

    for role in roles:
        exists = await get_role_by_name(role)
        if not exists:
            info = getattr(RoleInfo, role)
            translated_names = info['translated_names']
            translated_descriptions = info['translated_descriptions']
            translated_instructions = info['translated_instructions']
            await write_role(
                name=role,
                translated_names=translated_names,
                translated_descriptions=translated_descriptions,
                translated_instructions=translated_instructions,
            )
