import random

from bot.locales.texts import Texts
from bot.database.models.common import Currency, Quota
from bot.database.models.package import PackageType
from bot.database.models.subscription import Subscription, SubscriptionType, SubscriptionPeriod, SubscriptionLimit
from bot.database.models.user import UserGender


class English(Texts):
    START = """
🤖 Welcome to the future of AI with <b>GPTsTurboBot</b> 🎉

The bot allows you to access AI and neural networks.
Embark on a journey through the realms of AI with:
✉️ Unlimited ChatGPT 3 queries... Well, almost! Check out our 'Free' tier
🧠 The wisdom of ChatGPT 4, if you're feeling extra brainy today
🎨 Artistic creations with DALL-E 3 that will make Picasso look twice
😜 And, ever wanted to swap faces with Mona Lisa? Just ask for our Face Swap feature

Here's a quick guide to get you started:
✉️ To get a text response, simply type your request into the chat
🌅 To generate an image, first choose your AI model in /mode, then let your imagination run wild!
🔄 Swap between different neural networks with /mode to suit your creative needs
🔍 Use /info to learn more about what each AI model can do
👁️‍🗨️ Dive into /catalog to pick a specialized assistant tailored to your tasks
📊 Check your usage and subscription details with /profile
🔧 Personalize your experience further in /settings

And there's more! Just tap /commands to see all the magical AI commands at your disposal.
Let AI be your co-pilot in this adventure! 🚀
"""
    COMMANDS = """
🤖 Here's what you can explore:

🚀 /start - *About me*
🌐 /language - Engage with any language, *set system messages*.
🧠 /mode - *Swap neural network models* on the fly with — *ChatGPT3*, *ChatGPT4*, *DALLE-3*, or *Face Swap*!
📜 /info - Curious about what each model can do? Here you'll find all the answers.
💼 /profile - *Check your profile* to see your usage quota and more.
🔧 /settings - *Customize your experience* for a seamless user experience.
💳 /subscribe or /buy - *Learn about our plans and perks* or opt for individual packages.
🎁 /promo\\_code - Unleash exclusive AI features and special offers with your promo code.
🎭 /catalog - *Pick a specialized assistant* for tasks tailored just for you.
💬 /chats - *Create, switch, or delete context-specific chats*.

Just type away or use a command to begin your AI journey! 🌟
"""
    FEEDBACK = """
🌟 *Your opinion matters!* 🌟

Hey there! We're always looking to improve and your feedback is like gold dust to us. 💬✨
- Love something about our bot? Let us know!
- Got a feature request? We're all ears!
- Something bugging you? We're here to squash those bugs 🐞
Just type your thoughts and hit send. It's that simple! Your insights help us grow and get better every day.

And remember, every piece of feedback is a step towards making our bot even more awesome. Can't wait to hear from you! 💌
"""
    FEEDBACK_SUCCESS = """
🌟 *Feedback received!* 🌟

Thank you for sharing your thoughts! 💌
Your input is the secret sauce to our success. We're cooking up some improvements and your feedback is the key ingredient 🍳🔑
Keep an eye out for updates and new features, all inspired by you. Until then, happy chatting! 🚀

Your opinion matters a lot to us! 💖
"""

    # Profile
    CHANGE_PHOTO = "Change photo 📷"
    CHANGE_GENDER = "Change gender 🚹🚺"

    # Language
    LANGUAGE = "Language:"
    CHOOSE_LANGUAGE = "Selected language: English 🇺🇸"

    # Promo code
    PROMO_CODE_INFO = """
🔓 *Unlock the world of AI wonders with your secret code!* 🌟

If you've got a *promo code*, just type it in to reveal hidden features and special surprises 🎁

*No code?* No problem! Simply click 'Exit' to continue exploring the AI universe without it 🚀
"""
    PROMO_CODE_SUCCESS = """
🎉 *Woohoo! You've Struck Gold!* 🌟

Your promo code has been successfully activated! Get ready to dive into a world of AI wonders with your shiny new perks 🚀
Thanks for joining us on this AI-powered adventure. Enjoy the extra goodies and let's make some magic together! ✨

Happy exploring! 🤖🌐
"""
    PROMO_CODE_ALREADY_HAVE_SUBSCRIPTION = """
<b>Whoopsie-daisy!</b> 🙈

Looks like you're already part of our exclusive subscriber's club! 🌟
"""
    PROMO_CODE_EXPIRED_ERROR = """
🕒 *Whoops, time's up on this promo code!*

Looks like this promo code has hit its expiration date 📆. It's like a Cinderella story, but without the glass slipper 🥿
But hey, don't lose heart! You can still explore our other magical offers with /subscribe or /buy. There's always something exciting waiting for you in our AI wonderland! 🎩✨

Stay curious and let the AI adventure continue! 🌟🚀
"""
    PROMO_CODE_NOT_FOUND_ERROR = """
🔍 *Oops, promo code not found!*

It seems like the promo code you entered is playing hide and seek with us 🕵️‍♂️. We couldn't find it in our system 🤔
Double-check for any typos and give it another go. If it's still a no-show, maybe it's time to hunt for another code or check out our /subscribe and /buy options for some neat deals 🛍️

Keep your spirits high, and let's keep the AI fun rolling! 🚀🎈
"""
    PROMO_CODE_ALREADY_USED_ERROR = """
🚫 *Oops, déjà vu!*

Looks like you've already used this promo code. It's a one-time magic spell, and it seems you've already cast it! ✨🧙
No worries, though! You can check out our latest offers with /subscribe or /buy. There's always a new trick up our AI sleeve! 🎉🔮

Keep exploring and let the AI surprises continue! 🤖
"""

    # AI
    MODE = "Mode:"
    INFO = """
🤖 Let's check out what each model can do for you:

✉️ *ChatGPT3: The Versatile Communicator*
- _Small Talk to Deep Conversations_: Ideal for chatting about anything from daily life to sharing jokes.
- _Educational Assistant_: Get help with homework, language learning, or complex topics like coding.
- _Personal Coach_: Get motivation, fitness tips, or even meditation guidance.
- _Creative Writer_: Need a post, story, or even a song? ChatGPT3 can whip it up in seconds.
- _Travel Buddy_: Ask for travel tips, local cuisines, or historical facts about your next destination.
- _Business Helper_: Draft emails, create business plans, or brainstorm marketing ideas.
- _Role Play_: Engage in creative role-playing scenarios for entertainment or storytelling.
- _Quick Summaries_: Summarize long articles or reports into concise text.

🧠 *ChatGPT4: The Advanced Intellect*
- _In-Depth Analysis_: Perfect for detailed research, technical explanations, or exploring hypothetical scenarios.
- _Problem Solver_: Get help with advanced math problems, programming bugs, or scientific queries.
- _Language Expert_: Translate complex texts or practice conversational skills in various languages.
- _Creative Consultant_: Develop plot ideas for your posts, script dialogues, or explore artistic concepts.
- _Health and Wellness_: Discuss wellness and mental health topics in-depth.
- _Personalized Recommendations_: Get book, movie, or travel recommendations based on your interests.

🎨 *DALLE-3: The Creative Genius*
- _Art on Demand_: Generate unique art from descriptions – perfect for illustrators or those seeking inspiration.
- _Ad Creator_: Produce eye-catching images for advertising or social media content.
- _Educational Tool_: Visualize complex concepts for better understanding in education.
- _Interior Design_: Get ideas for room layouts or decoration themes.
- _Fashion Design_: Create clothing designs or fashion illustrations.
- _Personalized Comics_: Create comic strips or cartoon characters from your stories.
- _Product Mockups_: Create mockups for product ideas or inventions.

🤡 *Face Swap: The Entertainment Master*
- _Fun Reimaginations_: See how you'd look in different historical eras or as various movie characters.
- _Personalized Greetings_: Create unique birthday cards or invitations with personalized images.
- _Role Play_: Experiment with different looks for role-playing games or virtual meetings.
- _Memes and Content Creation_: Spice up your social media with funny or imaginative face-swapped pictures.
- _Digital Makeovers_: Experiment with new haircuts or makeup styles.
- _Celebrity Mashups_: Combine your face with celebrities for fun comparisons.

To change a model use /mode 😉
"""
    ALREADY_MAKE_REQUEST = "You've already made a request. Please wait ⚠️"
    READY_FOR_NEW_REQUEST = "You can ask the next request 😌"
    CONTINUE_GENERATING = "Continue generating"
    REACHED_USAGE_LIMIT = """
<b>Oops! 🚨</b>

Your quota for the current model has just done a Houdini and disappeared! 🎩
But don't worry, you've got options:
- Check out /buy or /subscribe for more magical moments, or
- Switch up the fun with a different AI model using /mode

The adventure continues! 🚀✨
"""
    IMAGE_SUCCESS = "✨ Here's your image creation! 🎨"

    # Settings
    SETTINGS = "Settings:"
    SHOW_NAME_OF_THE_CHAT = "Show name of the chat"
    SHOW_USAGE_QUOTA_IN_MESSAGES = "Show usage quota in messages"
    TURN_ON_VOICE_MESSAGES_FROM_RESPONDS = "Turn on voice messages from responds"

    # Voice
    VOICE_MESSAGES_FORBIDDEN = """
🎙 *Oops! Seems like your voice went into the AI void!*

To unlock the magic of voice-to-text, simply wave your wand with /subscribe or /buy.

Let's turn those voice messages into text and keep the conversation flowing! 🌟🔮
"""

    # Subscription
    MONTH_1 = "1 month"
    MONTHS_3 = "3 months"
    MONTHS_6 = "6 months"
    DISCOUNT = "Discount"
    NO_DISCOUNT = "No discount"
    SUBSCRIPTION_SUCCESS = """
🎉 *Hooray! You're all set!* 🚀

Your subscription is now as active as a caffeinated squirrel! 🐿️☕ Welcome to the club of awesomeness. Here's what's going to happen next:
- A world of possibilities just opened up 🌍✨
- Your AI pals are gearing up to assist you 🤖👍
- Get ready to dive into a sea of features and fun 🌊🎉

Thank you for embarking on this fantastic journey with us! Let's make some magic happen! 🪄🌟
"""
    SUBSCRIPTION_RESET = """
🚀 *Subscription quota refreshed!*

Hello there, fellow AI adventurer! 🌟
Guess what? Your subscription quota has just been topped up! It's like a magic refill, but better because it's real. 🧙‍♂️
You've got a whole new month of AI-powered fun ahead of you. Chat, create, explore – the sky's the limit! ✨

Keep unleashing the power of AI and remember, we're here to make your digital dreams come true. Let's rock this month! 🤖💥
"""
    SUBSCRIPTION_END = """
🛑 *Subscription expired!*

Hey there, AI enthusiast! 🌟
Your subscription has come to an end. But don't worry, the AI journey isn't over yet! 🚀
You can renew your magic pass with /subscribe to keep exploring the AI universe. Or, if you prefer, take a peek at /buy for some tailor-made individual packages. 🎁

The AI adventure awaits! Recharge, regroup, and let's continue this exciting journey together. 🤖✨
"""

    # Package
    GPT3_REQUESTS = "✉️ GPT3 requests"
    GPT3_REQUESTS_DESCRIPTION = "Unleash the power of GPT 3 for witty chats, smart advice, and endless fun! 🤖✨"
    GPT4_REQUESTS = "🧠 GPT4 requests"
    GPT4_REQUESTS_DESCRIPTION = "Experience GPT4's advanced intelligence for deeper insights and groundbreaking conversations 🧠🌟"
    THEMATIC_CHATS = "💬 Thematic chats"
    THEMATIC_CHATS_DESCRIPTION = "Dive into topics you love with Thematic Chats, guided by AI in a world of tailored discussions 📚🗨️"
    DALLE3_REQUESTS = "🖼 DALLE3 images"
    DALLE3_REQUESTS_DESCRIPTION = "Turn ideas into art with DALLE3 – where your imagination becomes stunning visual reality! 🎨🌈"
    FACE_SWAP_REQUESTS = "📷 Images with face replacement"
    FACE_SWAP_REQUESTS_DESCRIPTION = "Enter the playful world of Face Swap for laughs and surprises in every image! 😂🔄"
    ACCESS_TO_CATALOG = "🎭 Access to a roles catalog"
    ACCESS_TO_CATALOG_DESCRIPTION = "Unlock a universe of specialized AI assistants with access to our exclusive catalog, where every role is tailored to fit your unique needs and tasks"
    ANSWERS_AND_REQUESTS_WITH_VOICE_MESSAGES = "🎙 Answers and requests with voice messages"
    ANSWERS_AND_REQUESTS_WITH_VOICE_MESSAGES_DESCRIPTION = "Experience the ease and convenience of voice communication with our AI: Send and receive voice messages for a more dynamic and expressive interaction"
    FAST_ANSWERS = "⚡ Fast answers"
    FAST_ANSWERS_DESCRIPTION = "Quick Messages feature offers lightning-fast, accurate AI responses, ensuring you're always a step ahead in communication"
    MIN_ERROR = "Oops! It looks like the number entered is below our minimum threshold. Please enter a value that meets or exceeds the minimum required. Let's try that again! 🔄"
    VALUE_ERROR = "Whoops! That doesn't seem like a number. 🤔 Could you please enter a numeric value? Let's give it another go! 🔢"
    PACKAGE_SUCCESS = """
🎉 *Cha-Ching! Payment success!* 💳

Your payment just zoomed through like a superhero! 🦸‍ You've successfully unlocked the awesome power of your chosen package. Get ready for a rollercoaster of AI fun and excitement! 🎢

Remember, with great power comes great... well, you know how it goes. Let's make some magic happen! ✨🪄
"""

    # Catalog
    CATALOG = """
🎭 *Step right up to our role catalogue extravaganza!* 🌟

Ever dreamt of having an AI sidekick specialized just for you? Our catalog is like a magical wardrobe, each role a unique outfit tailored for your adventures in AI land! 🧙‍♂️✨
Choose from an array of AI personas, each with its own flair and expertise. Whether you need a brainstorm buddy, a creative muse, or a factual wizard, we've got them all!

👉 Ready to meet your match? Just hit the button below and let the magic begin! 🎩👇
"""
    CATALOG_FORBIDDEN_ERROR = """
🔒 *Whoops! Looks like you've hit a VIP-only zone!* 🌟

You're just a click away from unlocking our treasure trove of AI roles, but it seems you don't have the golden key yet. No worries, though! You can grab it easily.
🚀 Head over to /subscribe for some fantastic subscription options, or check out /buy if you're in the mood for some a la carte AI delights.

Once you're all set up, our catalog of AI wonders will be waiting for you – your ticket to an extraordinary world of AI possibilities! 🎫✨
"""
    PERSONAL_ASSISTANT = {
        "name": "🤖 Personal assistant",
        "description": """
Your go-to for anything and everything!
From answering questions to deep conversations, I'm here to assist you like a trusty sidekick 🌟
Let's tackle life's puzzles together!
""",
        "instruction": "You are a helpful assistant."
    }
    TUTOR = {
        "name": "📚 Tutor",
        "description": """
Unlock the world of knowledge across all subjects!
I'm here to make complex concepts simple and learning enjoyable 📚
Whether it's math, science, or art, let's learn together!
""",
        "instruction": "You are a helpful tutor."
    }
    LANGUAGE_TUTOR = {
        "name": "🗣️ Language tutor",
        "description": """
Embark on a linguistic adventure!
From basic phrases to fluency, I'll guide you through the nuances of languages with ease and fun 🌐
Let's converse in new tongues!
""",
        "instruction": "You are a helpful language tutor."
    }
    CREATIVE_WRITER = {
        "name": "🖋️ Creative writer",
        "description": """
Ready to explore worlds of wonder?
From crafting captivating stories to penning heartfelt poetry, let's unleash our collective creativity 🖋️
Your imagination is the limit!
""",
        "instruction": "You are a helpful creative writer."
    }
    TECHNICAL_ADVISOR = {
        "name": "💻 Technical advisor",
        "description": """
Navigating the tech maze made easy!
Whether it's understanding new software, fixing bugs, or exploring tech trends, I'm here to simplify technology 💻
Let's decode the digital world together!
""",
        "instruction": "You are a helpful technical advisor."
    }
    MARKETER = {
        "name": "📈 Marketer",
        "description": """
Let's elevate your brand and outreach!
From market research to campaign strategies, I'm here to help you navigate the marketing landscape and achieve your business goals 📊
Your success is our target!
""",
        "instruction": "You are a helpful marketer."
    }
    SMM_SPECIALIST = {
        "name": "📱 SMM-Specialist",
        "description": """
Transform your social media presence!
I'll help you create engaging content, grow your audience, and stay ahead in the ever-evolving social media space 📱
Let's make social media work for you!
""",
        "instruction": "You are a helpful SMM-specialist."
    }
    CONTENT_SPECIALIST = {
        "name": "📝 Content specialist",
        "description": """
Content is king, and I'm here to help you rule!
From SEO optimization to compelling copy, let's create content that resonates and engages ✍️
Your message matters!
""",
        "instruction": "You are a helpful content specialist."
    }
    DESIGNER = {
        "name": "🎨 Designer",
        "description": """
Visual storytelling at its best!
Let's design experiences that captivate and communicate, from websites to brand identities 🖌️
Your vision, our canvas!
""",
        "instruction": "You are a helpful designer."
    }
    SOCIAL_MEDIA_PRODUCER = {
        "name": "📸 Producer in social media",
        "description": """
Crafting stories that click and connect on social media!
Let's produce content that stands out and speaks to your audience 🎥
Your story, brilliantly told on social platforms!
""",
        "instruction": "You are a helpful social media producer."
    }
    LIFE_COACH = {
        "name": "🌱 Life coach",
        "description": """
Empowering you to reach your fullest potential!
From setting goals to overcoming obstacles, I'm here to support and inspire you on your journey to personal growth 🌱
Let's grow together!
""",
        "instruction": "You are a helpful life coach."
    }
    ENTREPRENEUR = {
        "name": "💼 Entrepreneur",
        "description": """
Turning ideas into reality!
Whether it's starting a business or scaling up, let's navigate the entrepreneurial journey with innovative strategies and insights 💡
Your dream, our mission!
""",
        "instruction": "You are a helpful entrepreneur."
    }

    # Chats
    DEFAULT_CHAT_TITLE = "New chat"
    SHOW_CHATS = "Show chats"
    CREATE_CHAT = "Create a new chat"
    CREATE_CHAT_FORBIDDEN = """
🚫 Oops!

Looks like you've hit the limit for creating new chats. But don't worry, the world of endless chats is just a click away! 🌍✨

Head over to /subscribe or /buy to unlock the power of multiple chats. More chats, more fun! 🎉
"""
    TYPE_CHAT_NAME = "Type your chat name"
    SWITCH_CHAT = "Switch between chats"
    SWITCH_CHAT_FORBIDDEN = """
"🔄 Switching gears? Hold that thought! ⚙️

You're currently in your one and only chat universe. It's a cozy place, but why not expand your horizons? 🌌

To hop between multiple thematic chats, just get your pass from /subscribe or /buy. Let the chat-hopping begin! 🐇
"""
    DELETE_CHAT = "Delete a chat"
    DELETE_CHAT_FORBIDDEN = """
🗑️ Delete this chat? That's lonely talk! 💬

This is your sole chat kingdom, and a kingdom needs its king or queen! Deleting it would be like canceling your own party. 🎈

How about adding more chats to your realm instead? Check out /subscribe or /buy to build your chat empire! 👑
"""
    DELETE_CHAT_SUCCESS = "🗑️ Chat successfully deleted! 🎉"

    # Face swap
    TELL_ME_YOUR_GENDER = "Tell me your gender:"
    YOUR_GENDER = "Your gender:"
    UNSPECIFIED = "Unspecified 🤷"
    MALE = "Male 🚹"
    FEMALE = "Female 🚺"
    SEND_ME_YOUR_PICTURE = """
📸 *Ready for a photo transformation? Here's how to get started!*

👍 *Ideal photo guidelines*:
- Clear, high-quality selfie.
- Only one person should be in the selfie.

👎 *Please avoid these types of photos*:
- Group photos.
- Animals.
- Children under 18 years.
- Full body shots.
- Nude or inappropriate images.
- Sunglasses or any face-obscuring items.
- Blurry, out-of-focus images.
- Videos and animations.
- Compressed or altered images.

Once you've got the perfect shot, upload your photo and let the magic happen 🌟
"""
    CHOOSE_YOUR_PACKAGE = """
🌟*Let's get creative with your photos!*

*First step:* Choose your adventure! 🚀

Ready? Let's dive into a world of imagination! 🌈 Just *select a package below* and start your photo adventure 👇
    """
    CELEBRITIES = "Celebrities ⭐️"
    MOVIE_CHARACTERS = "Movie characters 🎥"
    PROFESSIONS = "Professions 🧑‍💻"
    SEVEN_WONDERS_OF_THE_ANCIENT_WORLD = "Seven Wonders of the Ancient World 🌈"
    FACE_SWAP_MIN_ERROR = """
🤨 *Hold on there, partner!*

Looks like you're trying to request fewer than 1 image. In the world of creativity, we need at least 1 to get the ball rolling!

🌟 *Tip*: Type a number greater than 0 to start the magic. Let's unleash those creative ideas!
"""
    FACE_SWAP_MAX_ERROR = """
🚀 *Whoa, aiming high, I see!* But, uh-oh...

You're asking for more images than we have.

🧐 *How about this?* Let's try a number within the package limit!
"""

    ERROR = "I've got an error"
    BACK = "Back ◀️"
    CLOSE = "Close 🚪"
    CANCEL = "Cancel ❌"

    @staticmethod
    def profile(subscription_type: SubscriptionType,
                gender: UserGender,
                current_model: str,
                monthly_limits,
                additional_usage_quota) -> str:
        emojis = Subscription.get_emojis()

        if gender == UserGender.MALE:
            gender_info = f"Gender: {English.MALE}"
        elif gender == UserGender.FEMALE:
            gender_info = f"Gender: {English.FEMALE}"
        else:
            gender_info = f"Gender: {English.UNSPECIFIED}"

        return f"""
Profile 👤

Subscription type: {subscription_type} {emojis[subscription_type]}
{gender_info}
Currency: RUB
Current model: {current_model}
Change model: /mode

✉️
GPT-3.5 requests for month: {monthly_limits[Quota.GPT3]}/{SubscriptionLimit.LIMITS[subscription_type][Quota.GPT3]}
Additional GPT-3.5 requests: {additional_usage_quota[Quota.GPT3]}
GPT-4.0 requests for month: {monthly_limits[Quota.GPT4]}/{SubscriptionLimit.LIMITS[subscription_type][Quota.GPT4]}
Additional GPT-4.0 requests: {additional_usage_quota[Quota.GPT4]}

🖼
DALL-E 3 images for month: {monthly_limits[Quota.DALLE3]}/{SubscriptionLimit.LIMITS[subscription_type][Quota.DALLE3]}
Additional DALL-E 3 images: {additional_usage_quota[Quota.DALLE3]}

📷
Face swap images for month: {monthly_limits[Quota.FACE_SWAP]}/{SubscriptionLimit.LIMITS[subscription_type][Quota.FACE_SWAP]}
Additional face swap images: {additional_usage_quota[Quota.FACE_SWAP]}

💬
Additional chats: {additional_usage_quota[Quota.ADDITIONAL_CHATS]}

Subscribe: /subscribe
Buy additional requests: /buy
"""

    @staticmethod
    def subscribe(currency: Currency):
        prices = Subscription.get_prices(currency)

        return f"""
🤖Ready to supercharge your digital journey? Here's what's on the menu:

- *Standard* ⭐: For just {prices[SubscriptionType.STANDARD]}, step into the AI playground! Perfect for daily musings, creative bursts, and those "just curious" moments. Chat up a storm with ChatGPT 3, conjure images from thin air with DALLE-3, and swap faces faster than you can say "cheese"! 🧀

- *VIP* 🔥: Got grander ambitions? {prices[SubscriptionType.VIP]} unlocks deeper dialogues, more complex image creation, and access to a wider array of digital personas. It's the power user's delight, offering a premium lane on the AI highway 🛣️

- *Platinum* 💎: For the connoisseurs, {prices[SubscriptionType.PLATINUM]} grants you the keys to the AI kingdom! Max out on ChatGPT 4 prompts, create thematic chat rooms, and get exclusive access to the latest AI innovations. It's all you can AI, and then some! 🍽️

Pick your potion and hit the button below to subscribe:
"""

    @staticmethod
    def choose_how_many_months_to_subscribe(subscription_type: SubscriptionType):
        emojis = Subscription.get_emojis()

        return f"""
You're choosing *{subscription_type}* {emojis[subscription_type]}

Please select the subscription period by clicking on the button:
"""

    @staticmethod
    def cycles_subscribe():
        return {
            SubscriptionPeriod.MONTH1: English.MONTH_1,
            SubscriptionPeriod.MONTHS3: English.MONTHS_3,
            SubscriptionPeriod.MONTHS6: English.MONTHS_6,
        }

    @staticmethod
    def confirmation_subscribe(subscription_type: SubscriptionType, subscription_period: SubscriptionPeriod):
        cycles = English.cycles_subscribe()

        return f"You're about to activate your subscription for {cycles[subscription_period]}."

    # Package
    @staticmethod
    def buy():
        return """
🤖 Welcome to the AI Shopping Spree! 🛍

Welcome to the shop zone, where each button tap unlocks a world of AI wonders!
🧠 *ChatGPT3 & ChatGPT4*: Engage in deep, thought-provoking conversations. Your new AI buddies await!
🎨 *DALLE-3*: Transform ideas into stunning visuals. It's like painting with AI!
👤 *Face Swap*: Play with identities in images. It's never been this exciting!
🗣️ *Voice Messages*: Say it out loud! Chatting with AI has never sounded better.
💬 *Thematic Chats*: Dive into specialized topics and explore dedicated chat realms.
🎭 *Role Catalog Access*: Need a specific assistant? Browse our collection and find your perfect AI match.
⚡ *Quick Messages*: Fast, efficient, and always on point. AI communication at lightning speed.

Hit a button and embark on an extraordinary journey with AI! It's time to redefine what's possible 🌌🛍️
"""

    @staticmethod
    def choose_min(package_type: PackageType):
        return f"""
🚀 Fantastic!

You've selected the *{package_type}* package.
🌟 Please *type in the number of requests* you'd like to go for
"""

    # Chats
    @staticmethod
    def chats(current_chat_name: str, total_chats: int, available_to_create_chats: int):
        return f"""
🗨️ *Current chat: {current_chat_name}* 🌟

Welcome to the dynamic world of AI-powered chats! Here's what you can do:

- Create New Thematic Chats: Immerse yourself in focused discussions tailored to your interests.
- Switch Between Chats: Effortlessly navigate through your different chat landscapes.
- Delete Chats: Clean up by removing the chats you no longer need.

📈 Total Chats: *{total_chats} | Chats Available to Create: {available_to_create_chats}*

Ready to tailor your chat experience? Explore the options below and let the conversations begin! 🚀👇
"""

    # Face swap
    @staticmethod
    def choose_face_swap_package(name: str, available_images, total_images: int, used_images: int) -> str:
        remain_images = total_images - used_images
        return f"""
*{name}*

You've got a treasure trove of *{total_images} images* in your pack, ready to unleash your creativity! 🌟

🌠 *Your available generations*: {available_images} images. Need more? Explore /buy and /subscribe!
🔍 *Used so far*: {used_images} images. Wow, you're on a roll!
🚀 *Remaining*: {remain_images} images. {'Looks like you have used them all' if remain_images == 0 else 'So much potential'}!

👉 Want more? Type the number of new images to add or press the *Back* button to explore different exciting packages.
"""

    @staticmethod
    def face_swap_package_forbidden(available_images: int):
        return f"""
🔔 *Oops, a little hiccup!* 🚧

Looks like you've got only *{available_images} generations* left in your arsenal.

💡 *Pro Tip*: Sometimes, less is more! Try a smaller number, or give /buy and /subscribe a whirl for unlimited possibilities!
"""

    @staticmethod
    def wait_for_another_request(seconds: int) -> str:
        return f"Please wait for another {seconds} seconds before sending the next question ⏳"

    @staticmethod
    def processing_request():
        texts = [
            "I'm currently consulting my digital crystal ball for the best answer... 🔮",
            "One moment please, I'm currently training my hamsters to generate your answer... 🐹",
            "I'm currently rummaging through my digital library for the perfect answer. Bear with me... 📚",
            "Hold on, I'm channeling my inner AI guru for your answer... 🧘",
            "Please wait while I consult with the internet overlords for your answer... 👾",
            "Compiling the wisdom of the ages... or at least what I can find on the internet... 🌐",
            "Just a sec, I'm putting on my thinking cap... Ah, that's better. Now, let's see... 🎩",
            "I'm rolling up my virtual sleeves and getting down to business. Your answer is coming up... 💪",
            "Running at full steam! My AI gears are whirring to fetch your answer... 🚂",
            "Diving into the data ocean to fish out your answer. Be right back... 🌊🎣",
            "I'm consulting with my virtual elves. They're usually great at finding answers... 🧝",
            "Engaging warp drive for hyper-speed answer retrieval. Hold on tight... 🚀",
            "I'm in the kitchen cooking up a fresh batch of answers. This one's gonna be delicious... 🍳",
            "Taking a quick trip to the cloud and back. Hope to bring back some smart raindrops of info... ☁️",
            "Planting your question in my digital garden. Let's see what grows... 🌱🤖"
        ]

        return random.choice(texts)
