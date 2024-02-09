import random
from typing import List

from bot.locales.texts import Texts
from bot.database.models.common import Currency, Quota, Model
from bot.database.models.package import PackageType
from bot.database.models.subscription import Subscription, SubscriptionType, SubscriptionPeriod, SubscriptionLimit
from bot.database.models.user import UserGender


class English(Texts):
    START = """
🤖 <b>Welcome to the future of artificial intelligence with GPTsTurboBot!</b> 🎉

I'm your personal gateway to the world of artificial intelligence and neural networks. Discover the capabilities of AI:
✉️ Communicate with <b>ChatGPT3.5</b>: ask questions, get answers
🧠 Explore advanced intelligence with <b>ChatGPT4.0</b>
🎨 Create unique images with <b>DALL-E 3</b>
😜 Try <b>Face Swap</b> to exchange faces with someone in a photo
🎵 Compose original melodies with <b>MusicGen</b>

Here's a quick guide to get started:
✉️ To receive a text response from <b>ChatGPT3.5</b>, simply enter your query in the chat
🧠 To get a text response from <b>ChatGPT4.0</b>, enter the command /chatgpt4 and then just write your query in the chat
🎨 To create an image with <b>DALL-E 3</b>, enter the command /dalle3, and then let your imagination run wild with your request
😜 To swap faces with someone in a photo with <b>Face Swap</b>, enter the command /face_swap, then choose images from our unique packages or send your own
🎵 To create a melody with <b>MusicGen</b>, enter the command /music_gen, and then write a description of the melody
🔄 To switch between different neural networks, enter the command /mode, and then select the neural network depending on your creative needs
🔍 To learn more about the capabilities of each AI model, enter the command /info
🎭️ To choose a specialized digital assistant in <b>ChatGPT3.5</b> and <b>ChatGPT4.0</b> models, enter the command /catalog, and then select a specific digital assistant to help with your tasks
💬 To manage thematic chats, enter the command /chats
📊 To check usage information and subscription/purchase details, enter the command /profile
🔧 To customize me to improve your experience, enter the command /settings

And that's not all! Just press /help to see all my magical AI commands available to you.
I'm here to be your co-pilot on this adventure! 🚀
"""
    COMMANDS = """
🤖 Here's what you can explore:

👋 /start - <b>About me</b>: Discover what I can do for you.
🌍 /language - <b>Switch Languages</b>: Set your preferred language for system messages.
🧠 /mode - <b>Swap neural network models</b> on the fly with — <b>ChatGPT3.5</b>, <b>ChatGPT4.0</b>, <b>DALLE-3</b>, or <b>Face Swap</b>!
✉️ /chatgpt3 - <b>Engage with ChatGPT3.5</b>: Start chatting in a text-based conversation.
🧠 /chatgpt4 - <b>Explore ChatGPT4.0</b>: Experience advanced AI responses.
🎨 /dalle3 - <b>Create with DALL-E 3</b>: Bring your imaginations to life with images.
😜 /face_swap - <b>Have fun with Face Swap</b>: Change faces in photos.
🎵 /music_gen - <b>Melodies with MusicGen</b>: Create music without copyrights.
👤 /profile - <b>View your profile</b>: Check your subscription details or usage quota and more.
🔧 /settings - <b>Customize your experience</b>: Tailor me to fit your needs.
🎭 /catalog - <b>Select a specialized assistant</b>: Pick a digital helper designed for your tasks.
💬 /chats - <b>Manage context-specific chats</b>: Create, switch, reset, or delete thematic chats.
💳 /subscribe or /buy - <b>Learn about our subscriptions and benefits</b> or <b>choose individual packages</b>.
🎁 /bonus - Learn about your bonus balance, invite friends, and <b>exchange bonuses for unique generation packages</b>.
🔑 /promo_code - <b>Unleash exclusive AI features</b> and special offers with your <b>promo code</b>.
📡 /feedback - <b>Leave feedback</b>: Help me improve.

Just type away or use a command to begin your AI journey! 🌟
"""
    INFO = """
🤖 <b>Let's check out what each model can do for you:</b>

✉️ <b>ChatGPT3.5: The Versatile Communicator</b>
- <i>Small Talk to Deep Conversations</i>: Ideal for chatting about anything from daily life to sharing jokes.
- <i>Educational Assistant</i>: Get help with homework, language learning, or complex topics like coding.
- <i>Personal Coach</i>: Get motivation, fitness tips, or even meditation guidance.
- <i>Creative Writer</i>: Need a post, story, or even a song? ChatGPT3.5 can whip it up in seconds.
- <i>Travel Buddy</i>: Ask for travel tips, local cuisines, or historical facts about your next destination.
- <i>Business Helper</i>: Draft emails, create business plans, or brainstorm marketing ideas.
- <i>Role Play</i>: Engage in creative role-playing scenarios for entertainment or storytelling.
- <i>Quick Summaries</i>: Summarize long articles or reports into concise text.

🧠 <b>ChatGPT4.0: The Advanced Intellect</b>
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

🎶 <b>MusicGen: Your Personal Composer</b>
<i>Creating Unique Melodies</i>: Turn your ideas into musical pieces of any genre - from classical to pop.
<i>Music for Every Moment</i>: Specially created compositions for relaxation, study, workouts, or meditation.
<i>Personalized Soundtracks</i>: Create a soundtrack for your next video project, game, or presentation.
<i>Exploring Musical Styles</i>: Experiment with different musical genres and sounds to find your unique style.
<i>Learning and Inspiration</i>: Gain new insights into music theory and the history of genres through music creation.
<i>Instant Melody Creation</i>: Just enter a text description or mood, and MusicGen will instantly turn it into music.
"""

    # Feedback
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

    # Bonus
    BONUS_ACTIVATED_SUCCESSFUL = """
🌟 <b>Bonus activated!</b> 🌟

Congratulations! You've successfully used your bonus balance. Now, you can dive deeper into the world of artificial intelligence.

Start using your generations right now and discover new horizons with our neural networks! 🚀
"""

    # Promo code
    PROMO_CODE_INFO = """
🔓 <b>Unlock the world of AI wonders with your secret code!</b> 🌟

If you've got a <b>promo code</b>, just type it in to reveal hidden features and special surprises 🔑

<b>No code?</b> No problem! Simply click 'Cancel' to continue exploring the AI universe without it 🚀
"""
    PROMO_CODE_SUCCESS = """
🎉 <b>Your promo code has been successfully activated!</b> 🌟

To see what the activated promo code has brought you, type the command /profile ✨

Get ready to dive into a world of AI wonders with your shiny new perks. Happy exploring! 🚀
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
To change a model choose a button below 👇
"""
    SWITCHED_TO_CHATGPT3 = """
🤖 <b>Welcome to the world of ChatGPT3!</b>

You've successfully switched to the ChatGPT3 model. Consider this your personal virtual brain, ready to handle all your questions and ideas. Feel free to write anything - from simple queries to complex tasks. And don't worry, your previous conversations are stored in memory, so the context of your dialogue won't be lost

Go ahead, explore the capabilities of ChatGPT3! 🎉
"""
    SWITCHED_TO_CHATGPT4 = """
🚀 <b>Welcome to the world of ChatGPT4!</b>

Congratulations, you've switched to the ChatGPT4 model. This is a real breakthrough in the world of neural networks! ChatGPT4 offers deeper understanding and expanded capabilities compared to its predecessors. Discover new horizons of communication with AI. Your previous conversations are remembered, and the context history is preserved

Start your journey into the future with ChatGPT4! 🎉
"""
    SWITCHED_TO_DALLE3 = """
🎨 <b>Welcome to the world of DALLE-3!</b>

You've switched to the DALLE-3 model — your personal AI artist. Now, you can request to have any image drawn, whatever comes to your mind. Just describe your idea in a single message, and DALLE-3 will transform it into a visual masterpiece. Note: each new message is processed individually, previous request contexts are not considered

Time to create! 🎉
"""
    SWITCHED_TO_FACE_SWAP = """
🎭 <b>Welcome to the world of Face Swap!</b>

You've switched to the Face Swap model — where faces switch places as if by magic. Here, you can choose images from our unique packages or send your own photo. Want to see yourself in the guise of a celebrity or a movie character? Just select or send the desired image, and let Face Swap work its magic

Your new face awaits! 🎉
"""
    SWITCHED_TO_MUSIC_GEN = """
🎵 <b>Welcome to the world of MusicGen!</b>

You've switched to the MusicGen model — a marvelous world where music is born before your eyes. Create a unique melody by sharing your mood or idea for a composition. From a classical symphony to a modern beat, MusicGen will help you turn your musical dreams into reality.

Let every note tell your story! 🎶
"""
    ALREADY_SWITCHED_TO_THIS_MODEL = """
🔄 <b>Oops, looks like everything stayed the same!</b>

You've selected the same model that's already active. Don't worry, your digital universe remains unchanged. You can continue chatting or creating as usual. If you want to switch things up, simply choose a different model using /mode

Either way, we're here to help! 🛟
"""
    REQUEST_FORBIDDEN_ERROR = """
<b>Oops! Your request just bumped into our safety guardian!</b> 🚨

It seems there's something in your request that our vigilant content defender decided to block 🛑
Please check your text for any forbidden content and try again!

Our goal is safety and respect for every user! 🌟
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

    # MusicGen
    MUSIC_GEN_INFO = """
Your musical workshop 🎹

Open the door to a world where every idea of yours turns into music! With <b>MusicGen</b>, your imagination is the only limit. We're ready to transform your words and descriptions into unique melodies 🎼

Tell us what kind of music you want to create. Use words to describe its style, mood, and instruments. You don't need to be a professional - just share your idea, and let's bring it to life together! 🎤
"""
    MUSIC_GEN_TYPE_SECONDS = """
<b>How many seconds in your symphony?</b> ⏳

Fantastic! Your melody idea is ready to come to life. Now, the exciting part: how much time do we give this musical magic to unfold in all its glory? <b>MusicGen</b> awaits your decision 🎼

Write or choose the duration of your composition in seconds. Whether it's a flash of inspiration or an epic odyssey, we're ready to create! ✨
"""
    MUSIC_GEN_MIN_ERROR = """
🤨 <b>Hold on there, partner!</b>

Looks like you're trying to request fewer than 1 second. In the world of creativity, we need at least 1 to get the ball rolling!

🌟 <b>Tip</b>: Type a number greater than 0 to start the magic. Let's unleash those creative ideas!
"""
    SECONDS_30 = "🔹 30 seconds"
    SECONDS_60 = "🔹 60 seconds"
    SECONDS_180 = "🔹 180 seconds"

    # Settings
    SHOW_THE_NAME_OF_THE_CHATS = "Show the name of the chats"
    SHOW_THE_NAME_OF_THE_ROLES = "Show the name of the roles"
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
You can renew your magic pass with /subscribe to keep exploring the AI universe. Or, if you prefer, take a peek at /buy for some tailor-made individual packages 🎁

The AI adventure awaits! Recharge, regroup, and let's continue this exciting journey together. 🤖✨
"""
    PACKAGES_END = """
🕒 <b>Your package or packages time is up!</b> ⌛

Oops, it looks like your fast messages (or voice messages, catalog access) package has run its course. But don't worry, new opportunities always await beyond the horizon!

🎁 Want to continue? Check out our offers in /buy or consider a subscription via /subscribe. More exciting moments are ahead!

🚀 Ready for a fresh start? Rejoin and dive back into the world of amazing AI possibilities!
"""
    CHATS_RESET = """
🔄 <b>Chats updated!</b> 💬

Your chats have switched their unique roles to "Personal Assistant" as your access to the role catalog has ended. But don't worry, your AI helpers are still here to keep the conversation going!

🎁 Want your previous roles back? Visit /buy to purchase a new package or subscribe via /subscribe for unlimited access to the catalog.

🌟 Keep exploring! Your chats are always ready for new amazing conversations with AI.
"""

    # Package
    GPT3_REQUESTS = "✉️ GPT3.5 requests"
    GPT3_REQUESTS_DESCRIPTION = "Unleash the power of GPT 3.5 for witty chats, smart advice, and endless fun! 🤖✨"
    GPT4_REQUESTS = "🧠 GPT4.0 requests"
    GPT4_REQUESTS_DESCRIPTION = "Experience GPT4's advanced intelligence for deeper insights and groundbreaking conversations 🧠🌟"
    THEMATIC_CHATS = "💬 Thematic chats"
    THEMATIC_CHATS_DESCRIPTION = "Dive into topics you love with Thematic Chats, guided by AI in a world of tailored discussions 📚🗨️"
    DALLE3_REQUESTS = "🖼 DALLE3 images"
    DALLE3_REQUESTS_DESCRIPTION = "Turn ideas into art with DALLE3 – where your imagination becomes stunning visual reality! 🎨🌈"
    FACE_SWAP_REQUESTS = "📷 Images with face replacement"
    FACE_SWAP_REQUESTS_DESCRIPTION = "Enter the playful world of Face Swap for laughs and surprises in every image! 😂🔄"
    MUSIC_GEN_REQUESTS = "🎵 Seconds of generation of melodies"
    MUSIC_GEN_REQUESTS_DESCRIPTION = "Discover a world where every prompt turns into a unique melody! 🎶✨"
    ACCESS_TO_CATALOG = "🎭 Access to a roles catalog"
    ACCESS_TO_CATALOG_DESCRIPTION = "Unlock a universe of specialized AI assistants with access to our exclusive catalog, where every role is tailored to fit your unique needs and tasks"
    ANSWERS_AND_REQUESTS_WITH_VOICE_MESSAGES = "🎙 Answers and requests with voice messages"
    ANSWERS_AND_REQUESTS_WITH_VOICE_MESSAGES_DESCRIPTION = "Experience the ease and convenience of voice communication with our AI: Send and receive voice messages for a more dynamic and expressive interaction"
    FAST_ANSWERS = "⚡ Fast answers"
    FAST_ANSWERS_DESCRIPTION = "Quick Messages feature offers lightning-fast, accurate AI responses, ensuring you're always a step ahead in communication"
    MIN_ERROR = "Oops! It looks like the number entered is below our minimum threshold. Please enter a value that meets or exceeds the minimum required. Let's try that again! 🔄"
    MAX_ERROR = "Oops! It looks like the number entered is higher than you can purchase. Please enter a smaller value or one corresponding to your balance. Let's try that again! 🔄"
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
    SHOW_CHATS = "Show chats 👁️"
    CREATE_CHAT = "Create a new chat 💬"
    CREATE_CHAT_FORBIDDEN = """
🚫 Oops!

Looks like you've hit the limit for creating new chats. But don't worry, the world of endless chats is just a click away! 🌍✨

Head over to /subscribe or /buy to unlock the power of multiple chats. More chats, more fun! 🎉
"""
    CREATE_CHAT_SUCCESS = "💬 Chat created! 🎉\n👌 Don't forget to switch to a new one using /chats"
    TYPE_CHAT_NAME = "Type your chat name"
    SWITCH_CHAT = "Switch between chats 🔄"
    SWITCH_CHAT_FORBIDDEN = """
"🔄 <b>Switching gears? Hold that thought!</b> ⚙️

You're currently in your one and only chat universe. It's a cozy place, but why not expand your horizons? 🌌

To hop between multiple thematic chats, just get your pass from /subscribe or /buy. Let the chat-hopping begin! 🐇
"""
    SWITCH_CHAT_SUCCESS = "Chat successfully switched! 🎉"
    RESET_CHAT = "Reset chat ♻️"
    RESET_CHAT_WARNING = """
🧹 <b>Chat cleanup incoming!</b> 🚨

You're about to erase all messages and clear the context of this chat. This action is irreversible, and all your conversations will vanish into virtual dust. Are you sure you want to proceed?

✅ <b>Approve</b> - Yes, let's start with a clean slate.
❌ <b>Cancel</b> - No, I still have more to say!
"""
    RESET_CHAT_SUCCESS = """
🧹<b>Chat successfully cleared!</b> ✨

Now, like a goldfish, I don't remember what was said before 🐠
"""
    DELETE_CHAT = "Delete a chat 🗑"
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

    ERROR = """
I've got an unknown error 🤒

Please try again or contact @roman_danilov 🔧
"""
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

🧠
GPT-4.0 requests for month: {monthly_limits[Quota.GPT4]}/{SubscriptionLimit.LIMITS[subscription_type][Quota.GPT4]}
Additional GPT-4.0 requests: {additional_usage_quota[Quota.GPT4]}

🖼
DALL-E 3 images for month: {monthly_limits[Quota.DALLE3]}/{SubscriptionLimit.LIMITS[subscription_type][Quota.DALLE3]}
Additional DALL-E 3 images: {additional_usage_quota[Quota.DALLE3]}

📷
Face swap images for month: {monthly_limits[Quota.FACE_SWAP]}/{SubscriptionLimit.LIMITS[subscription_type][Quota.FACE_SWAP]}
Additional face swap images: {additional_usage_quota[Quota.FACE_SWAP]}

🎵
Seconds for creating melodies for month: {monthly_limits[Quota.MUSIC_GEN]}/{SubscriptionLimit.LIMITS[subscription_type][Quota.MUSIC_GEN]}
Additional seconds for creating melodies: {additional_usage_quota[Quota.MUSIC_GEN]}

💬
Additional chats: {additional_usage_quota[Quota.ADDITIONAL_CHATS]}

🎭
Access to a catalog: {'Yes' if additional_usage_quota[Quota.ACCESS_TO_CATALOG] else 'No'}

🎙
Send and get voice messages: {'Yes' if additional_usage_quota[Quota.VOICE_MESSAGES] else 'No'}

⚡
Fast answers: {'Yes' if additional_usage_quota[Quota.FAST_MESSAGES] else 'No'}

Invite friends and get bonus: /bonus
Subscribe: /subscribe
Buy additional requests or possibilities: /buy
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
🧠 <b>ChatGPT3.5 & ChatGPT4.0</b>: Engage in deep, thought-provoking conversations. Your new AI buddies await!
🎨 <b>DALLE-3</b>: Transform ideas into stunning visuals. It's like painting with AI!
👤 <b>Face Swap</b>: Play with identities in images. It's never been this exciting!
🎵 <b>Harmony with MusicGen</b>: Create unique melodies that will belong only to you!
🗣️ <b>Voice Messages</b>: Say it out loud! Chatting with AI has never sounded better.
💬 <b>Thematic Chats</b>: Dive into specialized topics and explore dedicated chat realms.
🎭 <b>Role Catalog Access</b>: Need a specific assistant? Browse our collection and find your perfect AI match.
⚡ <b>Quick Messages</b>: Fast, efficient, and always on point. AI communication at lightning speed.

Hit a button and embark on an extraordinary journey with AI! It's time to redefine what's possible 🌌🛍️
"""

    @staticmethod
    def choose_min(package_type: PackageType):
        name = ""
        quantity = ""
        if package_type == PackageType.GPT3:
            name = English.GPT3_REQUESTS
            quantity = "requests"
        elif package_type == PackageType.GPT4:
            name = English.GPT4_REQUESTS
            quantity = "requests"
        elif package_type == PackageType.CHAT:
            name = English.THEMATIC_CHATS
            quantity = "chats"
        elif package_type == PackageType.DALLE3:
            name = English.DALLE3_REQUESTS
            quantity = "images"
        elif package_type == PackageType.FACE_SWAP:
            name = English.FACE_SWAP_REQUESTS
            quantity = "generations"
        elif package_type == PackageType.MUSIC_GEN:
            name = English.MUSIC_GEN_REQUESTS
            quantity = "seconds"
        elif package_type == PackageType.ACCESS_TO_CATALOG:
            name = English.ACCESS_TO_CATALOG
            quantity = "months"
        elif package_type == PackageType.VOICE_MESSAGES:
            name = English.ANSWERS_AND_REQUESTS_WITH_VOICE_MESSAGES
            quantity = "months"
        elif package_type == PackageType.FAST_MESSAGES:
            name = English.FAST_ANSWERS
            quantity = "months"
        return f"""
🚀 Fantastic!

You've selected the <b>{name}</b> package

🌟 Please <b>type in the number of {quantity}</b> you'd like to go for
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

Ready to tailor your chat experience? Explore the options below and let the conversations begin! 👇
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

    # MusicGen
    @staticmethod
    def music_gen_forbidden(available_seconds: int):
        return f"""
🔔 <b>Oops, a little hiccup!</b> 🚧

Looks like you've got only <b>{available_seconds} seconds</b> left in your arsenal.

💡 <b>Pro Tip</b>: Sometimes, less is more! Try a smaller number, or give /buy and /subscribe a whirl for unlimited possibilities!
"""

    # AI
    @staticmethod
    def switched(model: Model):
        if model == Model.GPT3:
            return English.SWITCHED_TO_CHATGPT3
        elif model == Model.GPT4:
            return English.SWITCHED_TO_CHATGPT4
        elif model == Model.DALLE3:
            return English.SWITCHED_TO_DALLE3
        elif model == Model.FACE_SWAP:
            return English.SWITCHED_TO_FACE_SWAP
        elif model == Model.MUSIC_GEN:
            return English.SWITCHED_TO_MUSIC_GEN

    @staticmethod
    def chatgpt_recommendations() -> List[str]:
        texts = [
            "Tell me an interesting fact about space 👩‍🚀",
            "What could be the consequences of global warming? 🌍",
            "Write a short story titled 'Time Travel' 🕔",
            "What are the best strategies for learning a new language? 🦜",
            "Explain to me how photosynthesis works 🌿",
            "Suggest some interesting science fiction books to read 📚",
            "What are some methods for stress management? 🧘",
            "Write a poem about nature 🌳",
            "What are the basic principles of healthy eating? 🥦",
            "Tell a story about a traveler who can move between parallel worlds 🌌",
            "Describe what an ideal city of the future would look like 🏙️",
            "Invent a recipe for a unique dish inspired by the sea 🐟",
            "Create a script for a movie about adventures in the dinosaur era 🦖",
            "Develop a game where players build their own civilizations from scratch 🌍",
            "Write a poem dedicated to the first flight to Mars 🚀",
            "Propose ideas for an eco-friendly home of the future 🌱",
            "Describe a world where music can change reality 🎶",
            "Invent a story about a wizard who secretly lives in the modern world 🧙",
            "What would life be like if humans could communicate with animals? 🐾",
            "What would be the consequences if people could read each other's minds? 🧠",
            "Describe a world where all technology is powered by magic ✨",
            "Tell about a city where all inhabitants are robots 🤖",
            "Invent a fairy tale about a dragon that is afraid of fire 🔥",
            "Describe a utopian society with no conflicts and poverty 🕊️",
            "How would history change if dinosaurs had never gone extinct? 🦕",
            "Describe a world where every person is born with a unique talent 🌟",
            "Tell about an underwater city and its inhabitants 🌊",
            "Propose a concept for an experimental music genre 🎵",
            "Write a story about an encounter with aliens on Earth 👽",
            "Describe a future sports competition 🚀",
        ]

        return texts

    @staticmethod
    def dalle_recommendations() -> List[str]:
        texts = [
            "Martian cityscape under a pink sky 🪐",
            "Steampunk version of the Taj Mahal 🕌",
            "Surreal landscape with floating islands 🌌",
            "Futuristic cyberpunk cityscape 🏙️",
            "Portrait of a cat as a king 👑🐱",
            "Garden with crystal flowers and neon trees 🌸",
            "Castle in the clouds ☁️🏰",
            "Ice sculptures in the Antarctic desert ❄️🌵",
            "Medieval knight battling robots 🤖🗡️",
            "Enchanted forest with talking trees 🌲",
            "Underwater city with mermaids and dolphins 🧜‍♀️🐬",
            "Apocalyptic landscape with abandoned buildings 🌪️",
            "Human-alien encounter on the Moon 🌕👽",
            "Animated chess pieces on a board ♟️",
            "Dragon flying around a waterfall 🐉🌊",
            "Abstract Picasso-style composition 🎨",
            "Modern city built on giant trees 🌳🏢",
            "Magical portal to another world 🌀",
            "Victorian-style festive fairground city 🎪",
            "Lost temple in the jungle with mysterious ruins 🌿🛕",
            "Heavenly city with floating islands and rainbow bridges 🌈",
            "Dystopian city with robotic plants 🌿🤖",
            "Pirate ship atop a cloud ☁️🏴‍☠️",
            "Portrait of a dog dressed as King Louis XIV 🐶👑",
            "Future city with flying cars and glass roads 🚗🌉",
            "Space diner with galactic meals and starry light 🌌🍽️",
            "Magical mirror reflecting a parallel universe 🪞🌌",
            "Magical waterfall with floating crystals and light beings 💎🌊",
            "Space station orbiting an earthy forest 🌍🛰️",
            "Labyrinth of green hedges on another planet with two suns 🌿🪐",
        ]

        return texts

    @staticmethod
    def music_gen_recommendations() -> List[str]:
        texts = [
            "A pop track with infectious melodies, tropical percussion, and cheerful rhythms, perfect for the beach 🏖",
            "A magnificent orchestral arrangement with powerful beats, epic brass fanfares, creating a cinematic atmosphere worthy of a heroic battle 🎻",
            "A classic reggae track with an electric guitar solo 🎸",
            "A dynamic combination of hip-hop and orchestral elements, with sweeping strings and brass, evoking a sense of the city's live energy 🌆",
            "Violins and synthesizers, inspiring reflections on life and the universe 🌌",
            "An 80s electronic track with melodic synthesizers, memorable beat, and groovy bass 💾",
            "An energetic reggaeton track with loud 808 bass, synthesizer melodies layered with Latin percussion elements, uplifting the mood 🎉",
            "A duet of piano and cello, playing sad chamber music 🎹🎻",
            "Smooth jazz with a saxophone solo, piano chords 🎷",
            "An acoustic folk song for road trips: guitar, flute, choirs 🚗",
            "A rock track with guitars, a heavy bass line, and crazy drum breaks 🎶",
            "A horror movie soundtrack with dark melodies and unexpected sound effects, creating an atmosphere of tension 🎬👻",
            "An energetic techno track with hard basses and a fast rhythm, ideal for the dance floor 🕺",
            "Jazz-fusion with elements of funk, saxophone solo, and complex rhythmic patterns 🎷🎶",
            "Calm meditative music with Eastern motifs for relaxation and peace 🧘‍✨",
            "Rhythmic beats for gym workouts 🏋️‍♂️",
            "A video game soundtrack with epic orchestral melodies and digital effects, giving a sense of adventure 🎮🔊",
            "Melancholic cello for deep reflections 🎻",
            "Cheerful music for a children's party 🎈",
            "Classical music in a modern arrangement with electronic elements, a bridge between the past and future 🎻💫",
            "Dubstep with powerful basses and jerky rhythms, raises adrenaline 🎛️🔊",
            "Classical music for a candlelit dinner 🕯️",
            "Light and airy music for yoga 🧘",
            "An invigorating track for a morning jog 🏃‍",
            "A romantic guitar melody for a date 👩‍❤️‍👨",
            "Relaxing music for sleep with the sound of rain 🌧️",
            "An inspiring soundtrack for traveling 🚗",
            "A live jazz composition for evening relaxation 🎷",
            "A dance hit for a party 🎉",
            "Calm piano melodies for studying 📚",
        ]

        return texts

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

        text = random.choice(texts)
        text += "\n\n⚠️ Generation can take up to 5 minutes"

        return text

    @staticmethod
    def processing_request_music_gen():
        texts = [
            "Launching the music generator, hold onto your ears... 🎶👂",
            "Mixing notes like a DJ at a party... 🎧🕺",
            "The melody wizard is in action, get ready for magic... 🧙‍✨",
            "Creating music that will make even robots dance... 🤖💃",
            "The music laboratory is in action, things are heating up... 🔬🔥",
            "Catching a wave of inspiration and turning it into sounds... 🌊🎹",
            "Climbing to musical peaks, anticipate... 🏔️🎶",
            "Creating something that ears have never heard before... 🌟👂",
            "Time to dive into an ocean of harmony and rhythm... 🌊🎶",
            "Opening the door to a world where music creates reality... 🚪🌍",
            "Cracking the codes of composition to create something unique... 🧬🎶",
            "Crafting melodies like a chef crafts culinary masterpieces... 🍽️🎹",
            "Throwing a party on the keys, each note is a guest... 🎉🎹",
            "Carving a path through the melodic labyrinth... 🌀🎵",
            "Turning air vibrations into magical sounds... 🌬️🎼",
        ]

        text = random.choice(texts)
        text += "\n\n⚠️ Generation can take up to 10 minutes"

        return text

    # Settings
    @staticmethod
    def settings(model: Model) -> str:
        return f"""
⚙️ <b>Settings for model:</b> <i>{model}</i> 🤖
"""

    # Bonus
    @staticmethod
    def bonus(user_id: str, referred_count: int, balance: float, currency: Currency) -> str:
        if currency == Currency.USD:
            balance = f"{Currency.SYMBOLS[currency]}{balance}"
        else:
            balance = f"{balance}{Currency.SYMBOLS[currency]}"

        return f"""
🎁 <b>Your bonus balance</b>

👤 You've invited: {referred_count}
💰 Current balance: {balance}

🌟 Your personal referral link for invitations:
https://t.me/GPTsTurboBot?start={user_id}

Choose how to spend your earnings:
"""

    @staticmethod
    def referral_successful(added_to_balance: float, currency: Currency) -> str:
        if currency == Currency.USD:
            added_to_balance = f"{Currency.SYMBOLS[currency]}{added_to_balance}"
        else:
            added_to_balance = f"{added_to_balance}{Currency.SYMBOLS[currency]}"

        return f"""
🌟 <b>Congratulations! Your referral magic worked!</b> 🌟

Thanks to you, a new user has joined us, and as a token of our appreciation, your balance has been increased by {added_to_balance}! Use them to access exclusive features or to add more generations in the neural networks. 💸

To use the bonus, enter the /bonus command and follow the instructions. Let every invitation bring you not only the joy of communication but also pleasant bonuses!
"""
