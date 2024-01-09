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
🔍 Use /mode to learn more about what each AI model can do
👁️‍🗨️ Dive into /catalog to pick a specialized assistant tailored to your tasks
📊 Check your usage and subscription details with /profile
🔧 Personalize your experience further in /settings

And there's more! Just tap /help to see all the magical AI commands at your disposal.
Let AI be your co-pilot in this adventure! 🚀
"""
    COMMANDS = """
🤖 Here's what you can explore:

👋 /start - <b>About me</b>
🌍 /language - Engage with any language, <b>set system messages</b>.
🧠 /mode - <b>Swap neural network models</b> on the fly with — <b>ChatGPT3</b>, <b>ChatGPT4</b>, <b>DALLE-3</b>, or <b>Face Swap</b>!
👤 /profile - <b>Check your profile</b> to see your usage quota and more.
🔧 /settings - <b>Customize your experience</b> for a seamless user experience.
🎭 /catalog - <b>Pick a specialized assistant</b> for tasks tailored just for you.
💬 /chats - <b>Create, switch, or delete context-specific chats</b>.
💳 /subscribe or /buy - <b>Learn about our plans and perks</b> or opt for individual packages.
🎁 /promo_code - <b>Unleash exclusive AI features</b> and special offers with your <b>promo code</b>.
📡 /feedback - Give me a feedback and <b>improve me</b>.

Just type away or use a command to begin your AI journey! 🌟
"""
    FEEDBACK = """
🌟 <b>Your opinion matters!</b> 🌟

Hey there! We're always looking to improve and your feedback is like gold dust to us. 💬✨
- Love something about our bot? Let us know!
- Got a feature request? We're all ears!
- Something bugging you? We're here to squash those bugs 🐞
Just type your thoughts and hit send. It's that simple! Your insights help us grow and get better every day.

And remember, every piece of feedback is a step towards making our bot even more awesome. Can't wait to hear from you! 💌
"""
    FEEDBACK_SUCCESS = """
🌟 <b>Feedback received!</b> 🌟

Thank you for sharing your thoughts! 💌
Your input is the secret sauce to our success. We're cooking up some improvements and your feedback is the key ingredient 🍳🔑
Keep an eye out for updates and new features, all inspired by you. Until then, happy chatting! 🚀

Your opinion matters a lot to us! 💖
"""

    # Profile
    TELL_ME_YOUR_GENDER = "Tell me your gender:"
    YOUR_GENDER = "Your gender:"
    UNSPECIFIED = "Unspecified 🤷"
    MALE = "Male 🚹"
    FEMALE = "Female 🚺"
    SEND_ME_YOUR_PICTURE = """
📸 <b>Ready for a photo transformation? Here's how to get started!</b>

👍 <b>Ideal photo guidelines</b>:
- Clear, high-quality selfie.
- Only one person should be in the selfie.

👎 <b>Please avoid these types of photos</b>:
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
    CHANGE_PHOTO = "Change photo 📷"
    CHANGE_PHOTO_SUCCESS = "📸 Photo successfully uploaded! 🌟"
    CHANGE_GENDER = "Change gender 🚹🚺"

    # Language
    LANGUAGE = "Language:"
    CHOOSE_LANGUAGE = "Selected language: English 🇺🇸"

    # Promo code
    PROMO_CODE_INFO = """
🔓 <b>Unlock the world of AI wonders with your secret code!</b> 🌟

If you've got a <b>promo code</b>, just type it in to reveal hidden features and special surprises 🎁

<b>No code?</b> No problem! Simply click 'Cancel' to continue exploring the AI universe without it 🚀
"""
    PROMO_CODE_SUCCESS = """
🎉 <b>Woohoo! You've Struck Gold!</b> 🌟

Your promo code has been successfully activated! Get ready to dive into a world of AI wonders with your shiny new perks 🚀
Thanks for joining us on this AI-powered adventure. Enjoy the extra goodies and let's make some magic together! ✨

Happy exploring! 🤖🌐
"""
    PROMO_CODE_ALREADY_HAVE_SUBSCRIPTION = """
🚫 <b>Whoopsie-daisy!</b> 🙈

Looks like you're already part of our exclusive subscriber's club! 🌟
"""
    PROMO_CODE_EXPIRED_ERROR = """
🕒 <b>Whoops, time's up on this promo code!</b>

Looks like this promo code has hit its expiration date 📆. It's like a Cinderella story, but without the glass slipper 🥿
But hey, don't lose heart! You can still explore our other magical offers with /subscribe or /buy. There's always something exciting waiting for you in our AI wonderland! 🎩✨

Stay curious and let the AI adventure continue! 🌟🚀
"""
    PROMO_CODE_NOT_FOUND_ERROR = """
🔍 <b>Oops, promo code not found!</b>

It seems like the promo code you entered is playing hide and seek with us 🕵️‍♂️. We couldn't find it in our system 🤔
Double-check for any typos and give it another go. If it's still a no-show, maybe it's time to hunt for another code or check out our /subscribe and /buy options for some neat deals 🛍️

Keep your spirits high, and let's keep the AI fun rolling! 🚀🎈
"""
    PROMO_CODE_ALREADY_USED_ERROR = """
🚫 <b>Oops, déjà vu!</b>

Looks like you've already used this promo code. It's a one-time magic spell, and it seems you've already cast it! ✨🧙
No worries, though! You can check out our latest offers with /subscribe or /buy. There's always a new trick up our AI sleeve! 🎉🔮

Keep exploring and let the AI surprises continue! 🤖
"""

    # AI
    MODE = """
🤖 Let's check out what each model can do for you:

✉️ <b>ChatGPT3: The Versatile Communicator</b>
- <i>Small Talk to Deep Conversations</i>: Ideal for chatting about anything from daily life to sharing jokes.
- <i>Educational Assistant</i>: Get help with homework, language learning, or complex topics like coding.
- <i>Personal Coach</i>: Get motivation, fitness tips, or even meditation guidance.
- <i>Creative Writer</i>: Need a post, story, or even a song? ChatGPT3 can whip it up in seconds.
- <i>Travel Buddy</i>: Ask for travel tips, local cuisines, or historical facts about your next destination.
- <i>Business Helper</i>: Draft emails, create business plans, or brainstorm marketing ideas.
- <i>Role Play</i>: Engage in creative role-playing scenarios for entertainment or storytelling.
- <i>Quick Summaries</i>: Summarize long articles or reports into concise text.

🧠 <b>ChatGPT4: The Advanced Intellect</b>
- <i>In-Depth Analysis</i>: Perfect for detailed research, technical explanations, or exploring hypothetical scenarios.
- <i>Problem Solver</i>: Get help with advanced math problems, programming bugs, or scientific queries.
- <i>Language Expert</i>: Translate complex texts or practice conversational skills in various languages.
- <i>Creative Consultant</i>: Develop plot ideas for your posts, script dialogues, or explore artistic concepts.
- <i>Health and Wellness</i>: Discuss wellness and mental health topics in-depth.
- <i>Personalized Recommendations</i>: Get book, movie, or travel recommendations based on your interests.

🎨 <b>DALLE-3: The Creative Genius</b>
- <i>Art on Demand</i>: Generate unique art from descriptions – perfect for illustrators or those seeking inspiration.
- <i>Ad Creator</i>: Produce eye-catching images for advertising or social media content.
- <i>Educational Tool</i>: Visualize complex concepts for better understanding in education.
- <i>Interior Design</i>: Get ideas for room layouts or decoration themes.
- <i>Fashion Design</i>: Create clothing designs or fashion illustrations.
- <i>Personalized Comics</i>: Create comic strips or cartoon characters from your stories.
- <i>Product Mockups</i>: Create mockups for product ideas or inventions.

🤡 <b>Face Swap: The Entertainment Master</b>
- <i>Fun Reimaginations</i>: See how you'd look in different historical eras or as various movie characters.
- <i>Personalized Greetings</i>: Create unique birthday cards or invitations with personalized images.
- <i>Role Play</i>: Experiment with different looks for role-playing games or virtual meetings.
- <i>Memes and Content Creation</i>: Spice up your social media with funny or imaginative face-swapped pictures.
- <i>Digital Makeovers</i>: Experiment with new haircuts or makeup styles.
- <i>Celebrity Mashups</i>: Combine your face with celebrities for fun comparisons.

To change a model choose a button below 👇
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
🎙 <b>Oops! Seems like your voice went into the AI void!</b>

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
🎉 <b>Hooray! You're all set!</b> 🚀

Your subscription is now as active as a caffeinated squirrel! 🐿️☕ Welcome to the club of awesomeness. Here's what's going to happen next:
- A world of possibilities just opened up 🌍✨
- Your AI pals are gearing up to assist you 🤖👍
- Get ready to dive into a sea of features and fun 🌊🎉

Thank you for embarking on this fantastic journey with us! Let's make some magic happen! 🪄🌟
"""
    SUBSCRIPTION_RESET = """
🚀 <b>Subscription quota refreshed!</b>

Hello there, fellow AI adventurer! 🌟
Guess what? Your subscription quota has just been topped up! It's like a magic refill, but better because it's real. 🧙‍♂️
You've got a whole new month of AI-powered fun ahead of you. Chat, create, explore – the sky's the limit! ✨

Keep unleashing the power of AI and remember, we're here to make your digital dreams come true. Let's rock this month! 🤖💥
"""
    SUBSCRIPTION_END = """
🛑 <b>Subscription expired!</b>

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
🎉 <b>Cha-Ching! Payment success!</b> 💳

Your payment just zoomed through like a superhero! 🦸‍ You've successfully unlocked the awesome power of your chosen package. Get ready for a rollercoaster of AI fun and excitement! 🎢

Remember, with great power comes great... well, you know how it goes. Let's make some magic happen! ✨🪄
"""

    # Catalog
    CATALOG = """
🎭 <b>Step right up to our role catalogue extravaganza!</b> 🌟

Ever dreamt of having an AI sidekick specialized just for you? Our catalog is like a magical wardrobe, each role a unique outfit tailored for your adventures in AI land! 🧙‍♂️✨
Choose from an array of AI personas, each with its own flair and expertise. Whether you need a brainstorm buddy, a creative muse, or a factual wizard, we've got them all!

👉 Ready to meet your match? Just hit the button below and let the magic begin! 🎩👇
"""
    CATALOG_FORBIDDEN_ERROR = """
🔒 <b>Whoops! Looks like you've hit a VIP-only zone!</b> 🌟

You're just a click away from unlocking our treasure trove of AI roles, but it seems you don't have the golden key yet. No worries, though! You can grab it easily.
🚀 Head over to /subscribe for some fantastic subscription options, or check out /buy if you're in the mood for some a la carte AI delights.

Once you're all set up, our catalog of AI wonders will be waiting for you – your ticket to an extraordinary world of AI possibilities! 🎫✨
"""
    CREATE_ROLE = "Create a new role"

    # Chats
    DEFAULT_CHAT_TITLE = "New chat"
    SHOW_CHATS = "Show chats"
    CREATE_CHAT = "Create a new chat"
    CREATE_CHAT_FORBIDDEN = """
🚫 Oops!

Looks like you've hit the limit for creating new chats. But don't worry, the world of endless chats is just a click away! 🌍✨

Head over to /subscribe or /buy to unlock the power of multiple chats. More chats, more fun! 🎉
"""
    CREATE_CHAT_SUCCESS = "💬 Chat created! 🎉"
    TYPE_CHAT_NAME = "Type your chat name"
    SWITCH_CHAT = "Switch between chats"
    SWITCH_CHAT_FORBIDDEN = """
"🔄 <b>Switching gears? Hold that thought!</b> ⚙️

You're currently in your one and only chat universe. It's a cozy place, but why not expand your horizons? 🌌

To hop between multiple thematic chats, just get your pass from /subscribe or /buy. Let the chat-hopping begin! 🐇
"""
    SWITCH_CHAT_SUCCESS = "🔀 Chat successfully switched! 🎉"
    DELETE_CHAT = "Delete a chat"
    DELETE_CHAT_FORBIDDEN = """
🗑️ <b>Delete this chat? That's lonely talk!</b> 💬

This is your sole chat kingdom, and a kingdom needs its king or queen! Deleting it would be like canceling your own party. 🎈

How about adding more chats to your realm instead? Check out /subscribe or /buy to build your chat empire! 👑
"""
    DELETE_CHAT_SUCCESS = "🗑️ Chat successfully deleted! 🎉"

    # Face swap
    CHOOSE_YOUR_PACKAGE = """
🌟<b>Let's get creative with your photos!</b>

<b>First step:</b> Choose your adventure! 🚀

Ready? Let's dive into a world of imagination! 🌈 Just <b>select a package below</b> and start your photo adventure 👇
    """
    GENERATIONS_IN_PACKAGES_ENDED = """
🎨 <b>Wow, you've used up all your generations in our packages! Your creativity is astounding!</b> 🌟

What's next?
- 📷 Send us photos with faces for face swapping in Face Swap!
- 🔄 Or switch models via /mode to continue creating with other AI tools!

Time for new AI discoveries! 🚀
"""
    FACE_SWAP_MIN_ERROR = """
🤨 <b>Hold on there, partner!</b>

Looks like you're trying to request fewer than 1 image. In the world of creativity, we need at least 1 to get the ball rolling!

🌟 <b>Tip</b>: Type a number greater than 0 to start the magic. Let's unleash those creative ideas!
"""
    FACE_SWAP_MAX_ERROR = """
🚀 <b>Whoa, aiming high, I see!</b> But, uh-oh...

You're asking for more images than we have.

🧐 <b>How about this?</b> Let's try a number within the package limit!
"""

    ERROR = "I've got an error"
    BACK = "Back ◀️"
    CLOSE = "Close 🚪"
    CANCEL = "Cancel ❌"
    APPROVE = "Approve ✅"

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
<b>Profile</b> 👤

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

- <b>Standard</b> ⭐: For just {prices[SubscriptionType.STANDARD]}, step into the AI playground! Perfect for daily musings, creative bursts, and those "just curious" moments. Chat up a storm with ChatGPT 3, conjure images from thin air with DALLE-3, and swap faces faster than you can say "cheese"! 🧀

- <b>VIP</b> 🔥: Got grander ambitions? {prices[SubscriptionType.VIP]} unlocks deeper dialogues, more complex image creation, and access to a wider array of digital personas. It's the power user's delight, offering a premium lane on the AI highway 🛣️

- <b>Platinum</b> 💎: For the connoisseurs, {prices[SubscriptionType.PLATINUM]} grants you the keys to the AI kingdom! Max out on ChatGPT 4 prompts, create thematic chat rooms, and get exclusive access to the latest AI innovations. It's all you can AI, and then some! 🍽️

Pick your potion and hit the button below to subscribe:
"""

    @staticmethod
    def choose_how_many_months_to_subscribe(subscription_type: SubscriptionType):
        emojis = Subscription.get_emojis()

        return f"""
You're choosing <b>{subscription_type}</b> {emojis[subscription_type]}

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
🤖 <b>Welcome to the AI Shopping Spree!</b> 🛍

Welcome to the shop zone, where each button tap unlocks a world of AI wonders!
🧠 <b>ChatGPT3 & ChatGPT4</b>: Engage in deep, thought-provoking conversations. Your new AI buddies await!
🎨 <b>DALLE-3</b>: Transform ideas into stunning visuals. It's like painting with AI!
👤 <b>Face Swap</b>: Play with identities in images. It's never been this exciting!
🗣️ <b>Voice Messages</b>: Say it out loud! Chatting with AI has never sounded better.
💬 <b>Thematic Chats</b>: Dive into specialized topics and explore dedicated chat realms.
🎭 <b>Role Catalog Access</b>: Need a specific assistant? Browse our collection and find your perfect AI match.
⚡ <b>Quick Messages</b>: Fast, efficient, and always on point. AI communication at lightning speed.

Hit a button and embark on an extraordinary journey with AI! It's time to redefine what's possible 🌌🛍️
"""

    @staticmethod
    def choose_min(package_type: PackageType):
        return f"""
🚀 Fantastic!

You've selected the <b>{package_type}</b> package.
🌟 Please <b>type in the number of requests</b> you'd like to go for
"""

    # Chats
    @staticmethod
    def chats(current_chat_name: str, total_chats: int, available_to_create_chats: int):
        return f"""
🗨️ <b>Current chat: {current_chat_name}</b> 🌟

Welcome to the dynamic world of AI-powered chats! Here's what you can do:

- Create New Thematic Chats: Immerse yourself in focused discussions tailored to your interests.
- Switch Between Chats: Effortlessly navigate through your different chat landscapes.
- Delete Chats: Clean up by removing the chats you no longer need.

📈 Total Chats: <b>{total_chats} | Chats Available to Create: {available_to_create_chats}</b>

Ready to tailor your chat experience? Explore the options below and let the conversations begin! 🚀👇
"""

    # Face swap
    @staticmethod
    def choose_face_swap_package(name: str, available_images, total_images: int, used_images: int) -> str:
        remain_images = total_images - used_images
        return f"""
<b>{name}</b>

You've got a treasure trove of <b>{total_images} images</b> in your pack, ready to unleash your creativity! 🌟

🌠 <b>Your available generations</b>: {available_images} images. Need more? Explore /buy and /subscribe!
🔍 <b>Used so far</b>: {used_images} images. {'Wow, you are on a roll!' if used_images > 0 else ''}
🚀 <b>Remaining</b>: {remain_images} images. {'Looks like you have used them all' if remain_images == 0 else 'So much potential'}!

📝 <b>Type how many face swaps you want to do, or choose from the quick selection buttons below</b>. The world of face transformations awaits! 🎭🔄
"""

    @staticmethod
    def face_swap_package_forbidden(available_images: int):
        return f"""
🔔 <b>Oops, a little hiccup!</b> 🚧

Looks like you've got only <b>{available_images} generations</b> left in your arsenal.

💡 <b>Pro Tip</b>: Sometimes, less is more! Try a smaller number, or give /buy and /subscribe a whirl for unlimited possibilities!
"""

    @staticmethod
    def wait_for_another_request(seconds: int) -> str:
        return f"Please wait for another {seconds} seconds before sending the next question ⏳"

    @staticmethod
    def processing_request_text():
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

    @staticmethod
    def processing_request_image():
        texts = [
            "Gathering stardust to create your cosmic artwork... 🌌",
            "Mixing a palette of digital colors for your masterpiece... 🎨",
            "Dipping into the virtual inkwell to sketch your vision... 🖌️",
            "Summoning the AI muses for a stroke of genius... 🌠",
            "Crafting pixels into perfection, just a moment... 👁️🎭",
            "Whipping up a visual feast for your eyes... 🍽️👀",
            "Consulting with digital Da Vinci for your artistic request... 🎭",
            "Dusting off the digital easel for your creative request... 🖼️🖌️",
            "Conjuring a visual spell in the AI cauldron... 🧙‍🔮",
            "Activating the virtual canvas. Get ready for artistry... 🖼️️",
            "Assembling your ideas in a gallery of pixels... 🖼️👨‍🎨",
            "Embarking on a digital safari to capture your artistic vision... 🦁🎨",
            "Revving up the AI art engines, stand by... 🏎️💨",
            "Plunging into a pool of digital imagination... 🏊‍💭",
            "Cooking up a visual symphony in the AI kitchen... 🍳🎼"
        ]

        return random.choice(texts)

    @staticmethod
    def processing_request_face_swap():
        texts = [
            "Warping into the face-swapping dimension... 🌌👤",
            "Mixing and matching faces like a digital Picasso... 🧑‍🎨🖼️",
            "Swapping faces faster than a chameleon changes colors... 🦎🌈",
            "Unleashing the magic of face fusion... ✨👥",
            "Engaging in facial alchemy, transforming identities... 🧙‍🧬",
            "Cranking up the face-swapping machine... 🤖🔀",
            "Concocting a potion of facial transformation... 🧪👩‍🔬🔬",
            "Casting a spell in the realm of face enchantments... 🧚‍🎭️",
            "Orchestrating a symphony of facial features... 🎼👩‍🎤👨‍🎤",
            "Sculpting new faces in my digital art studio... 🎨👩‍🎨",
            "Brewing a cauldron of face-swap magic... 🧙‍🔮",
            "Building faces like a master architect... 🏗️👷‍",
            "Embarking on a mystical quest for the perfect face blend... 🗺️🔍",
            "Launching a rocket of face morphing adventures... 🚀👨‍🚀👩‍🚀",
            "Embarking on a galactic journey of face swapping... 🌌👽"
        ]

        return random.choice(texts)
