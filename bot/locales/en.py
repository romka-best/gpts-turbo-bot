import random
from typing import Union

from bot.database.models.product import Product, ProductCategory, ProductType
from bot.database.models.prompt import Prompt
from bot.database.operations.product.getters import get_product
from bot.helpers.formatters.format_number import format_number
from bot.helpers.getters.get_user_discount import get_user_discount
from bot.locales.texts import Texts
from bot.database.models.common import (
    Currency,
    Quota,
    Model,
    ModelType,
    ChatGPTVersion,
    ClaudeGPTVersion,
    GeminiGPTVersion,
    AspectRatio,
    SendType,
)
from bot.database.models.subscription import (
    SubscriptionPeriod,
    SubscriptionStatus,
)
from bot.database.models.user import UserGender, UserSettings
from bot.locales.types import LanguageCode


class English(Texts):
    START = """
🤖 <b>Welcome to the future of AI with me, MindFusion AI Bot!</b> 🎉

I'm your personal gateway to the world of neural networks. Discover the capabilities of AI:
━ 💭 <b>Text Responses</b>:
    ┣ Communicate free with:
        ┣ <b>ChatGPT 4.0 Omni Mini ✉️</b> /chatgpt
        ┣ <b>Claude 3.5 Haiku 📜</b> /claude
        ┗ <b>Gemini 1.5 Flash 🏎</b> /gemini
    ┣ Unleash the full potential of AI with:
        ┣ <b>ChatGPT 4.0 Omni 💥</b> and <b>ChatGPT o1-mini 🧩</b> /chatgpt
        ┣ <b>Claude 3.5 Sonnet 💫</b> /claude
        ┗ <b>Gemini 1.5 Pro 💼</b> /gemini
    ┗ Explore the most advanced level of intelligence with:
        ┣ <b>ChatGPT o1-preview 🧪</b> /chatgpt
        ┣ <b>Claude 3.0 Opus 🚀</b> /claude
        ┗ <b>Gemini 1.0 Ultra 🛡️</b> /gemini

━ 🖼 <b>Create Images</b>:
    ┣ Draw beautiful, unforgettable pictures with:
        ┣ <b>DALL-E 3 👨‍🎨</b> /dalle
        ┣ <b>Midjourney 6.1 🎨</b> /midjourney
        ┣ <b>Stable Diffusion 3.5 🎆</b> /stable_diffusion
        ┗ <b>Flux 1.1 Pro 🫐</b> /flux
    ┣ Exchange faces with someone in a photo with <b>FaceSwap 📷️</b> /face_swap
    ┗ Edit your images using <b>Photoshop AI 🪄</b> /photoshop

━ 🎵 <b>Compose Music</b>:
    ┣ Compose original melodies with <b>MusicGen 🎺</b> /music_gen
    ┗ Record your own songs with <b>Suno 4.0 🎸</b> /suno

I am constantly updating myself, implementing the most advanced technologies so that you can fully leverage the possibilities of artificial intelligence. <b>I am the only bot with emotional intelligence</b>, ready to help you with any questions and creative endeavors 🚀
"""
    START_QUICK_GUIDE = "📖 Quick Guide"
    START_ADDITIONAL_FEATURES = "🔮 Additional Features"
    QUICK_GUIDE = """
📖 Here's a quick guide to get started:

━ 💭 <b>Text Responses</b>:
    ┣ 1️⃣ Enter one of the commands:
        ┣ /chatgpt 💥
        ┣ /claude 🚀
        ┗ /gemini 💼
    ┣ 2️⃣ Select the version
    ┗ 3️⃣ Write your requests into the chat

━ 🖼 <b>Create Images</b>:
    ┣ 1️⃣ Enter one of the commands:
        ┣ /dalle 👨‍🎨
        ┣ /midjourney 🎨
        ┣ /stable_diffusion 🎆
        ┗ /flux 🫐
    ┗ 2️⃣ Start creating using your imagination with your requests

━ 😜 <b>Exchange Faces in Photos</b>:
    ┣ 1️⃣ Enter the command /face_swap
    ┣ 2️⃣ Follow the instructions to help me creating better photos
    ┗ 3️⃣ Choose images from my unique packages or send your own photos

━ 🪄 <b>Edit Images</b>:
    ┣ 1️⃣ Enter the command /photoshop
    ┣ 2️⃣ Choose what you want to do with the image
    ┗ 3️⃣ Send the image for editing

━ 🎵 <b>Compose Music</b>:
    ┣ 1️⃣ Enter one of the command
        ┣ /music_gen 🎺
        ┗ /suno 🎸
    ┗ 2️⃣ Write a description of the music or send your own lyrics
"""
    ADDITIONAL_FEATURES = """
🔮 <b>Additional Features</b>:

━ 🔄 /mode - One command for switching between all AI models
━ 📊 /profile - I'll show your profile and quotes
━ 🔍 /info - Useful information about each AI model
━ 🎁 /bonus - Learn how to get free access to all AI models for free
━ 🎭️ /settings - Personalization and settings. Digital employees and thematic chats for text models
"""
    MAINTENANCE_MODE = "🤖 I'm in maintenance mode. Please wait a little bit 🛠"

    COMMANDS = """
🤖 <b>Here's what you can explore:</b>

━ Common commands:
    ┣ 👋 /start - <b>About me</b>: Discover what I can do for you
    ┣ 👤 /profile - <b>View your profile</b>: Check your usage quota or subscription details and more
    ┣ 🌍 /language - <b>Switch languages</b>: Set your preferred language for the interface
    ┣ 💳 /buy - <b>Subscribe or buy packages</b>: Get a new level
    ┣ 🎁 /bonus - Learn about your bonus balance and <b>exchange bonuses for generation packages</b>
    ┣ 🔑 /promo_code - <b>Activate promo code</b> if you have it
    ┣ 📡 /feedback - <b>Leave feedback</b>: Help me improve
    ┗ 📄 /terms - <b>TOS</b>: Terms of Service

━ AI commands:
    ┣ 🤖 /mode - <b>Swap neural network models</b> on the fly with — <b>ChatGPT</b>, <b>Claude</b>, <b>Gemini</b>, <b>DALL-E</b>, <b>Midjourney</b>, <b>Stable Diffusion</b>, <b>FaceSwap</b>, <b>Photoshop AI</b>, <b>MusicGen</b>, or <b>Suno</b>!
    ┣ ℹ️ /info - <b>Get information about AI</b>: Learn for what and why do you need them
    ┣ 📁 /catalog - <b>Catalog of roles and prompts</b>: Boost your communication efficiency with me
    ┣ 💥 /chatgpt - <b>Chat with ChatGPT</b>: Start a text conversation and receive advanced AI responses
    ┣ 🚀 /claude - <b>Chat with Claude</b>: Begin a discussion and explore the depth of responses from Claude
    ┣ ✨ /gemini - <b>Chat with Gemini</b>: Start chatting and immerse yourself in advanced answers from the new AI
    ┣ 👨‍🎨 /dalle - <b>Draw with DALL-E</b>: Turn your ideas into drawings
    ┣ 🎨 /midjourney - <b>Create with DALL-E 3</b>: Bring your imaginations to life with images
    ┣ 🎆 /stable_diffusion - <b>Uniqueness with Stable Diffusion</b>: Create unique images
    ┣ 🫐 /flux - <b>Experiments with Flux</b>: Explore endless image variations without limitations
    ┣ 😜 /face_swap - <b>Have fun with FaceSwap</b>: Change faces in photos
    ┣ 🪄 /photoshop - <b>Magic with Photoshop AI</b>: Retouch and edit your photos with one touch
    ┣ 🎺 /music_gen - <b>Melodies with MusicGen</b>: Create music without copyrights
    ┣ 🎸 /suno - <b>Songs with Suno</b>: Create your own song with your lyrics and different genres
    ┗ 🔧 /settings - <b>Customize your experience</b>: Tailor model to fit your needs. There you can also <b>select a digital employee</b> with <b>context-specific chats management</b>

Just type away a command to begin your AI journey! 🌟
"""
    INFO = """
🤖 <b>Select the models type you want to get information about:</b>
"""
    INFO_TEXT_MODELS = """
🤖 <b>Select the text model you want to get information about:</b>
"""
    INFO_IMAGE_MODELS = """
🤖 <b>Select the graphic model you want to get information about:</b>
"""
    INFO_MUSIC_MODELS = """
🤖 <b>Select the music model you want to get information about:</b>
"""
    INFO_VIDEO_MODELS = """
🤖 <b>Select the video model you want to get information about:</b>
"""
    INFO_CHATGPT = """
🤖 <b>There is what each model can do for you:</b>

✉️ <b>ChatGPT 4.0 Omni Mini: The Versatile Communicator</b>
- <i>Small Talk to Deep Conversations</i>: Ideal for chatting about anything from daily life to sharing jokes.
- <i>Educational Assistant</i>: Get help with homework, language learning, or complex topics like coding.
- <i>Personal Coach</i>: Get motivation, fitness tips, or even meditation guidance.
- <i>Creative Writer</i>: Need a post, story, or even a song? ChatGPT 4.0 Omni Mini can whip it up in seconds.
- <i>Travel Buddy</i>: Ask for travel tips, local cuisines, or historical facts about your next destination.
- <i>Business Helper</i>: Draft emails, create business plans, or brainstorm marketing ideas.

💥 <b>ChatGPT 4.0 Omni: Next-Generation Intelligence</b>
- <i>Detailed Analysis</i>: Perfect for in-depth research, complex technical explanations, or virtual scenario analysis.
- <i>Complex Problem Solving</i>: From mathematical calculations to diagnosing software issues and answering scientific queries.
- <i>Language Mastery</i>: High-level translation and enhancement of conversational skills in various languages.
- <i>Creative Mentor</i>: Inspiring ideas for blogs, scripts, or artistic research.
- <i>Personalized Recommendations</i>: Tailored picks for books, movies, or travel routes based on your preferences.

🧩 <b>ChatGPT o1-mini: A Mini Expert for Problem Solving</b>
- <i>Deep Analysis</i>: Assists with logical reasoning and solving complex problems.
- <i>Critical Thinking</i>: Excels at tasks that require attention to detail and well-reasoned conclusions.
- <i>Educational Assistant</i>: Helps with solutions in programming, mathematics, or scientific research.
- <i>Efficiency</i>: Provides quick and accurate answers to both practical and theoretical questions.

🧪 <b>ChatGPT o1-preview: A Revolution in Reasoning</b>
- <i>Advanced Data Analysis</i>: Suitable for processing and analyzing large volumes of information.
- <i>Argumentative Problem Solving</i>: Ideal for tasks that require well-justified conclusions and complex logical structures.
- <i>Hypothesis Generation</i>: Perfect for scientific research and experimentation.
- <i>Strategy Development</i>: Can assist with developing complex strategies in business or personal projects.
"""
    INFO_CLAUDE = """
🤖 <b>There is what each model can do for you:</b>

📜 <b>Claude 3.5 Haiku: The Art of Brevity and Wisdom</b>
- <i>Deep and Concise Responses</i>: Perfect for brief yet meaningful insights and advice.
- <i>Quick Problem Solving</i>: Instantly delivers solutions for everyday and technical questions.
- <i>Linguistic Precision</i>: Mastery in expressing the essence in a few words, whether it's translation or explanation.
- <i>Creativity in Minimalism</i>: Supports creating short-form content, from poems to succinct ideas.

💫 <b>Claude 3.5 Sonnet: A Balance of Speed and Wisdom</b>
- <i>Multifunctional Analysis</i>: Effective for comprehensive research and technical explanations.
- <i>Problem Solving</i>: Assistance with solving mathematical issues, software bugs, or scientific puzzles.
- <i>Linguistic Expert</i>: A reliable assistant for translating texts and enhancing conversational skills in various languages.
- <i>Creative Advisor</i>: Development of creative ideas for content and artistic projects.
- <i>Personal Guide</i>: Recommendations for cultural content and travel planning tailored to your interests.

🚀 <b>Claude 3.0 Opus: The Pinnacle of Power and Depth</b>
- <i>Advanced Analysis</i>: Ideal for tackling the most complex research and hypothetical scenarios.
- <i>Problem Solving Expert</i>: Addresses challenging scientific inquiries, technical issues, and mathematical problems.
- <i>Language Mastery</i>: Translations and language practice at a professional level.
- <i>Creative Consultant</i>: Support in developing unique ideas for scripts and art projects.
- <i>Recommendations Concierge</i>: Expert advice on selecting books, movies, and travel plans that match your tastes.
"""
    INFO_GEMINI = """
🤖 <b>There is what each model can do for you:</b>

🏎 <b>Gemini 1.5 Flash: Speed and Efficiency</b>
- <i>Quick Data Analysis</i>: Ideal for tasks that require instant data processing and response generation.
- <i>Immediate Results</i>: Perfect for fast information retrieval and instant problem-solving.
- <i>Simplified Problem Solving</i>: Capable of assisting with basic calculations, daily tasks, and fast queries.
- <i>Seamless Interaction</i>: Provides users with accurate information in minimal time, ensuring a high level of precision.

💼 <b>Gemini 1.5 Pro: Professional Power</b>
- <i>In-Depth Analysis</i>: Excels in complex research, deep data analysis, and detailed technical explanations.
- <i>Comprehensive Problem Solving</i>: Suited for high-level tasks, scientific challenges, and complex mathematical questions.
- <i>Linguistic Flexibility</i>: Assists with translations, text editing, and supports multiple languages at a professional level.
- <i>Creative Thinking</i>: Aids in developing ideas for creative projects, writing, and other artistic tasks.
- <i>Personalized Recommendations</i>: Offers expert advice on content selection and event planning based on individual preferences.

🛡 <b>Gemini 1.0 Ultra: Power and Precision</b>
- <i>Unlimited Analytics</i>: Excels in handling complex tasks, deep analysis, and large-scale data processing.
- <i>Accurate Solutions</i>: Ideal for complex calculations and scientific research.
- <i>Linguistic Mastery</i>: Expertise in translations and support for language tasks at the highest level.
- <i>Creative Inspiration</i>: A valuable assistant in the creation and development of complex creative projects and ideas.
- <i>Personalized Interaction</i>: Tailors its responses to your specific needs and preferences.
"""
    INFO_DALL_E = """
🤖 <b>There is what the model can do for you:</b>

👨‍🎨 <b>DALL-E: The Creative Genius</b>
- <i>Art on Demand</i>: Generate unique art from descriptions – perfect for illustrators or those seeking inspiration.
- <i>Ad Creator</i>: Produce eye-catching images for advertising or social media content.
- <i>Educational Tool</i>: Visualize complex concepts for better understanding in education.
- <i>Interior Design</i>: Get ideas for room layouts or decoration themes.
- <i>Fashion Design</i>: Create clothing designs or fashion illustrations.
"""
    INFO_MIDJOURNEY = """
🤖 <b>There is what the model can do for you:</b>

🎨 <b>Midjourney: Navigator of Creativity</b>
- <i>Art Design</i>: Creating visual masterpieces and abstractions, ideal for artists and designers in search of a unique style.
- <i>Architectural modeling</i>: Generation of conceptual designs of buildings and space layouts.
- <i>Educational assistant</i>: Illustrations for educational materials that improve the perception and understanding of complex topics.
- <i>Interior design</i>: Visualization of interior solutions, from classics to modern trends.
- <i>Fashion and style</i>: The development of fashionable bows and accessories, experiments with colors and shapes.
"""
    INFO_STABLE_DIFFUSION = """
🤖 <b>There is what the model can do for you:</b>

🎆 <b>Stable Diffusion: Image Generation Tool</b>
- <i>Creative Illustration</i>: Generate unique images based on text prompts, perfect for artists, designers, and writers.
- <i>Concept Art and Sketches</i>: Create conceptual images for games, films, and other projects, helping visualize ideas.
- <i>Image Stylization</i>: Transform existing images into different artistic styles, from comic book designs to classic painting styles.
- <i>Design Prototyping</i>: Quickly generate visual concepts for logos, posters, or web design projects.
- <i>Art Style Experimentation</i>: Experiment with colors, shapes, and textures to develop new visual solutions.
"""
    INFO_FLUX = """
🤖 <b>There is what the model can do for you:</b>

🫐 <b>Flux: Experiments with Flux</b>

- <i>Endless Variations</i>: Generate diverse images from a single prompt, each result being unique.
- <i>Fine-Tuning Parameters</i>: Control the image creation process to achieve results tailored to your specific needs.
- <i>Randomized Generation</i>: Introduce elements of randomness to create unexpectedly creative outcomes.
- <i>Diverse Visual Concepts</i>: Explore a wide range of artistic styles and approaches, adjusting the process to fit your project.
- <i>Fast Visual Experiments</i>: Experiment with various concepts and styles without limitations, unlocking new creative possibilities.
"""
    INFO_FACE_SWAP = """
🤖 <b>There is what the model can do for you:</b>

🤡 <b>FaceSwap: The Entertainment Master</b>
- <i>Fun Reimaginations</i>: See how you'd look in different historical eras or as various movie characters.
- <i>Personalized Greetings</i>: Create unique birthday cards or invitations with personalized images.
- <i>Memes and Content Creation</i>: Spice up your social media with funny or imaginative face-swapped pictures.
- <i>Digital Makeovers</i>: Experiment with new haircuts or makeup styles.
- <i>Celebrity Mashups</i>: Combine your face with celebrities for fun comparisons.
"""
    INFO_PHOTOSHOP_AI = """
🤖 <b>There is what the model can do for you:</b>

🪄 <b>Photoshop AI: Magic with Photos</b>
- <i>Photo Restoration</i>: Revives old or damaged photos, returning them to their original state.
- <i>Black-and-White to Color</i>: Breathes life into black-and-white photos by adding vibrant and natural colors.
- <i>Background Removal</i>: Easily removes the background from images, leaving only the main subject.
"""
    INFO_MUSIC_GEN = """
🤖 <b>There is what the model can do for you:</b>

🎺 <b>MusicGen: Your Personal Composer</b>
- <i>Creating Unique Melodies</i>: Turn your ideas into musical pieces of any genre - from classical to pop.
- <i>Personalized Soundtracks</i>: Create a soundtrack for your next video project, game, or presentation.
- <i>Exploring Musical Styles</i>: Experiment with different musical genres and sounds to find your unique style.
- <i>Learning and Inspiration</i>: Gain new insights into music theory and the history of genres through music creation.
- <i>Instant Melody Creation</i>: Just enter a text description or mood, and MusicGen will instantly turn it into music.
"""
    INFO_SUNO = """
🤖 <b>There is what the model can do for you:</b>

🎸 <b>Suno: A Pro in Creating Songs</b>
- <i>Text-to-song transformation</i>: Suno turns your text into songs, matching melody and rhythm to your style.
- <i>Personalized songs</i>: Create unique songs for special moments, whether it's a personal gift or a soundtrack for your event.
- <i>Explore musical genres</i>: Discover new musical horizons by experimenting with different styles and sounds.
- <i>Music education and inspiration</i>: Learn about music theory and the history of genres through the practice of composition.
- <i>Instant music creation</i>: Describe your emotions or scenario, and Suno will immediately bring your description to life as a song.
"""

    SERVER = "💻 Server"
    DATABASE = "🗄 Database"

    TEXT_MODELS = "🔤 Text models"
    IMAGE_MODELS = "🖼 Image models"
    MUSIC_MODELS = "🎵 Music models"
    VIDEO_MODELS = "📹 Video models"

    # Feedback
    FEEDBACK = """
🌟 <b>Your opinion matters!</b> 🌟

Hey there! I'm always looking to improve and your feedback is like gold dust to me ✨

- Love something about me? Let me know 😊
- Got a feature request? I'm all ears 🦻
- Something bugging you? I'm here to squash those bugs 🐞

And remember, every piece of feedback is a step towards making me even more awesome. Can't wait to hear from you! 💌
"""
    FEEDBACK_SUCCESS = """
🌟 <b>Feedback received!</b> 🌟

Your input is the secret sauce to my success. I'm cooking up some improvements and your feedback is the key ingredient 🍳🔑
I will add 25 credits to your balance after my creators check the content of the feedback, but in the meantime, happy chatting!

Your opinion matters a lot to me! 💖
"""
    FEEDBACK_APPROVED = """
🌟 <b>Feedback approved!</b> 🌟

As a token of appreciation, your balance has increased by 25 credits 🪙! Use them to access exclusive functions or replenish the number of generations in neural networks 💸

To use the bonus, enter the command /bonus and follow the instructions!
"""
    FEEDBACK_APPROVED_WITH_LIMIT_ERROR = """
🌟 <b>Feedback approved!</b> 🌟

Thanks to your efforts, we will improve the boat! But, unfortunately, we cannot award you a reward, as the limit of rewards for feedback has been exceeded

Enter the /bonus command to learn about other ways to earn bonus credits. Keep sharing and enjoy every moment here! 🎉
"""
    FEEDBACK_DENIED = """
🌟 <b>Feedback denied!</b> 🌟

Unfortunately, your feedback was not constructive enough and I cannot increase your bonus balance 😢

But don't worry! You can enter the command /bonus to see the other ways to top up the bonus balance!
"""

    # Profile
    SHOW_QUOTA = "🔄 Show Quota"
    TELL_ME_YOUR_GENDER = "Tell me your gender:"
    YOUR_GENDER = "Your gender:"
    UNSPECIFIED = "Unspecified 🤷"
    MALE = "Male 👕"
    FEMALE = "Female 👚"
    SEND_ME_YOUR_PICTURE = """
📸 <b>Ready for a photo transformation? Send a photo of yours!</b>

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

Once you've got the perfect shot, <b>upload your photo</b> and let the magic happen 🌟
    """
    UPLOAD_PHOTO = "📷 Upload Photo"
    UPLOADING_PHOTO = "Uploading photo..."
    NO_FACE_IN_PHOTO = "I can't see a face in the photo. Please try another 📷"

    CHANGE_PHOTO = "📷 Change Photo"
    CHANGE_PHOTO_SUCCESS = "📸 Photo successfully uploaded! 🌟"

    CHOOSE_GENDER = "🚹🚺 Choose Gender"
    CHANGE_GENDER = "🚹🚺 Change Gender"

    OPEN_SETTINGS = "⚙️ Open Settings"
    OPEN_BONUS_INFO = "🎁 Open Bonus Balance"
    OPEN_BUY_SUBSCRIPTIONS_INFO = "💎 Subscribe"
    OPEN_BUY_PACKAGES_INFO = "🛍 Purchase Packages"
    CANCEL_SUBSCRIPTION = "❌ Cancel Subscription"
    CANCEL_SUBSCRIPTION_CONFIRMATION = "❗Are you sure you want to cancel the subscription?"
    CANCEL_SUBSCRIPTION_SUCCESS = "💸 Subscription cancellation was successful"
    NO_ACTIVE_SUBSCRIPTION = "💸 You don't have an active subscription"

    # Language
    LANGUAGE = "Language:"
    CHOOSE_LANGUAGE = "Selected language: English 🇺🇸"

    # Bonus
    BONUS_ACTIVATED_SUCCESSFUL = """
🌟 <b>Bonus activated!</b> 🌟

Congrats! You've successfully used your bonus balance. Now, you can dive deeper into the world of artificial intelligence.

Start using your generations right now and discover new horizons with my neural networks! 🚀
"""
    BONUS_CHOOSE_PACKAGE = "Choose how to spend your earnings:"
    INVITE_FRIEND = "👥 Invite a friend"
    LEAVE_FEEDBACK = "📡 Leave a feedback"
    PLAY = "🎮 Play"
    PLAY_GAME = "🎮 Try my luck"
    PLAY_GAME_CHOOSE = """
🎮 <b>Choose your game:</b>

━ 🎳 <b>Bowling</b>:
Knock down the pins! Your result: from 1 to 6 — that's the number of credits you'll earn!

━ ⚽️ <b>Football</b>:
The football challenge! Score a goal and receive a guaranteed 5 credits!

━ 🏀 <b>Basketball</b>:
The shot of fate! A precise hand will earn you 10 credits!

━ 🎯 <b>Darts</b>:
Hit the bullseye! A sharp eye could win you 15 credits!

━ 🎲 <b>Dice</b>:
The dice of luck! If fortune favors you, you'll win 20 credits!

━ 🎰 <b>Casino</b>:
🍋 Lucky number! If three matching numbers appear, you'll hit 50 credits!
🎰 Jackpot! Roll three 7️⃣s and score 100 credits!

✨ Remember: You only have one attempt each day, so choose wisely and good luck! 😊
"""
    PLAY_BOWLING_GAME = "🎳 Play bowling"
    PLAY_BOWLING_GAME_DESCRIPTION = """
🎳 <b>Bowling: Ready to take your shot?</b>

When you hit the "Play" button, I’ll instantly roll the ball into the pins! Your chance of winning is 100%, because you’re guaranteed to earn credits. It all depends on how many pins I knock down — from 1 to 6. The number of pins knocked down equals your credits!

Every throw is a win, but how big will your victory be?
"""
    PLAY_SOCCER_GAME = "⚽️ Play soccer"
    PLAY_SOCCER_GAME_DESCRIPTION = """
⚽️ <b>Football Challenge: Ready to score a goal?</b>

Hit "Play", and I’ll take control of the ball! I’ll launch it straight toward the goal, but luck will decide — there’s a 60% chance to score and win credits!

If I hit the target, you’ll earn 5 credits. Ready to see if this will be the winning goal?
"""
    PLAY_BASKETBALL_GAME = "🏀 Play basketball"
    PLAY_BASKETBALL_GAME_DESCRIPTION = """
🏀 <b>Shot of Fate: Time to take the shot!</b>

Hit "Play", and I’ll make the crucial shot at the basketball hoop! There’s a 40% chance the ball will land perfectly, and if it does — you’ll earn 10 credits!

Will I nail this shot like a pro? Let’s find out after the throw!
"""
    PLAY_DARTS_GAME = "🎯 Play darts"
    PLAY_DARTS_GAME_DESCRIPTION = """
🎯 <b>Bullseye Challenge: Can you hit the mark?</b>

Hit "Play", and I’ll throw the dart straight at the target! There’s a ~16.67% chance of hitting the bullseye and winning — it’s not easy, but a victory will earn you 15 credits!

Ready to take the risk and see how accurate I am?
"""
    PLAY_DICE_GAME = "🎲 Roll the dice"
    PLAY_DICE_GAME_CHOOSE = """
🎲 <b>Lucky Dice: Take a guess!</b>

Pick a number from 1 to 6, and I’ll roll the dice! If you guess the number that comes up, you’ll win a solid 20 credits. But the odds of winning are 1 in 6.

Can you sense your luck and guess which number will land?
"""
    PLAY_CASINO_GAME = "🎰 Play at casino"
    PLAY_CASINO_GAME_DESCRIPTION = """
🎰 <b>Casino: Take your luck to the max!</b>

Hit "Play", and I’ll spin the casino reels. If three matching numbers appear — congratulations, you win! There’s a nearly 5% chance to land three of a kind, which will earn you 50 credits. But here’s the twist: if you get three 7s, you hit the Jackpot and score 100 credits! The chance of this super prize is just over 1%, but maybe today is your lucky day?

Go ahead, spin the reels and see what fortune has in store for you!
"""
    PLAY_GAME_WON = """
🎉 <b>Congratulations!</b>

Luck is on your side! You’ve won! Your prize is waiting for you in /bonus.

Come back tomorrow for more victories. Luck loves players like you! 🎊
"""
    PLAY_GAME_LOST = """
😔 <b>No luck today...</b>

Luck is all about timing! Don’t worry, or I’ll start worrying too!

Try again tomorrow, and maybe fortune will smile on you even brighter! 🍀
"""
    PLAY_GAME_REACHED_LIMIT = """
⏳ <b>Oops, looks like you've already played today!</b>

But don’t worry — tomorrow brings a new chance to test your luck!

Come back and show us what you’ve got! 👏
"""
    CASH_OUT = "🛍 Cash out credits"
    REFERRAL_SUCCESS = """
🌟 <b>Congrats! Your referral magic worked!</b> 🌟

Thanks to you, a new user has joined, and as a token of my appreciation, your and your friend's balance has been increased by 25 credits 🪙! Use them to access exclusive features or to add more generations in the neural networks 💸

To use the bonus, enter the /bonus command and follow the instructions. Let every invitation bring you not only the joy of communication but also pleasant bonuses!
"""
    REFERRAL_LIMIT_ERROR = """
🌟 <b>Congrats! Your referral magic worked!</b> 🌟

Thanks to your efforts, a new user has joined! Unfortunately, we cannot award you a reward, as the limit of rewards for inviting friends has been exceeded

Enter the /bonus command to learn about other ways to earn bonus credits. Keep sharing and enjoy every moment here! 🎉
"""

    # Promo code
    PROMO_CODE_ACTIVATE = "🔑 Activate promo code"
    PROMO_CODE_INFO = """
🔓 <b>Unlock the world of AI wonders with your secret code!</b> 🌟

If you've got a <b>promo code</b>, just type it in to reveal hidden features and special surprises 🔑

<b>No code?</b> No problem! Simply click 'Cancel' to continue exploring the AI universe without it 🚀
"""
    PROMO_CODE_SUCCESS = """
🎉 <b>Your promo code has been successfully activated!</b> 🌟

Get ready to dive into a world of AI wonders with your shiny new perks

Happy exploring! 🚀
"""
    PROMO_CODE_ALREADY_HAVE_SUBSCRIPTION = """
🚫 <b>Whoopsie-daisy!</b> 🙈

Looks like you're already part of our exclusive subscriber's club! 🌟
"""
    PROMO_CODE_EXPIRED_ERROR = """
🕒 <b>Whoops, time's up on this promo code!</b>

Looks like this promo code has hit its expiration date. It's like a Cinderella story, but without the glass slipper 🥿

But hey, don't lose heart! You can still explore our other magical offers just hit the button below:
"""
    PROMO_CODE_NOT_FOUND_ERROR = """
🔍 <b>Oops, promo code not found!</b>

It seems like the promo code you entered is playing hide and seek with me cuz I couldn't find it in my system 🕵️‍♂️

🤔 Double-check for any typos and give it another go. If it's still a no-show, maybe it's time to hunt for another code or check out our /buy options for some neat deals 🛍️
"""
    PROMO_CODE_ALREADY_USED_ERROR = """
🚫 <b>Oops, déjà vu!</b>

Looks like you've already used this promo code. It's a one-time magic spell, and it seems you've already cast it! ✨🧙

No worries, though! You can check out our latest offers with clicking one of the buttons below:
"""

    # AI
    MODE = """
To change a model click a button below 👇
"""
    CHOOSE_CHATGPT_MODEL = """
To choose a <b>ChatGPT 💭</b> model click a button below 👇
"""
    CHOOSE_CLAUDE_MODEL = """
To choose a <b>Claude 📄</b> model click a button below 👇
"""
    CHOOSE_GEMINI_MODEL = """
To choose a <b>Gemini ✨</b> model click a button below 👇
"""
    SWITCHED_TO_AI_SETTINGS = "⚙️ Go to Model's Settings"
    SWITCHED_TO_AI_INFO = "ℹ️ Learn More About This Model"
    SWITCHED_TO_AI_EXAMPLES = "💡 Show Examples"
    ALREADY_SWITCHED_TO_THIS_MODEL = """
🔄 <b>Oops, looks like everything stayed the same!</b>

You've selected the same model that's already active. Don't worry, your digital universe remains unchanged. You can continue chatting or creating as usual. If you want to switch things up, simply choose a different model using /mode

Either way, I'm here to help! 🛟
"""
    REQUEST_FORBIDDEN_ERROR = """
<b>Oops! Your request just bumped into our safety guardian!</b> 🚨

It seems there's something in your request that my coworker vigilant content defender decided to block 🛑
Please check your text for any forbidden content and try again!

My goal is safety and respect for every user! 🌟
"""
    PHOTO_FORBIDDEN_ERROR = "I don't know how to work with photos in this AI model yet 👀"
    ALBUM_FORBIDDEN_ERROR = "In the current AI model, I can't process multiple photos at once, please send one 🙂"
    VIDEO_FORBIDDEN_ERROR = "I don't know how to work with videos yet 👀"
    DOCUMENT_FORBIDDEN_ERROR = "I don't know how to work with such documents yet 👀"
    STICKER_FORBIDDEN_ERROR = "I don't know how to work with stickers yet 👀"
    SERVER_OVERLOADED_ERROR = "I have a heavy load on the server right now 🫨\n\nPlease, try later!"
    ALREADY_MAKE_REQUEST = "You've already made a request. Please wait ⚠️"
    READY_FOR_NEW_REQUEST = "You can ask the next request 😌"
    CONTINUE_GENERATING = "Continue generating"
    REACHED_USAGE_LIMIT = """
<b>Oops! 🚨</b>

Your today's quota for the current model has just done a Houdini and disappeared! 🎩

❗️But don't worry, you've got options:
"""
    CHANGE_AI_MODEL = "🤖 Change AI Model"
    REMOVE_RESTRICTION = "⛔️ Remove the Restriction"
    REMOVE_RESTRICTION_INFO = "To remove the restriction, choose one of the actions 👇"
    IMAGE_SUCCESS = "✨ Here's your image creation! 🎨"
    FILE_TOO_BIG_ERROR = """
🚧 <b>Oops!</b>

The file you sent is too large. I can only process files smaller than 20MB.

Please try again with a smaller file 😊
"""

    # Examples
    CHATGPT4_OMNI_EXAMPLE = "👇 This is how *ChatGPT 4.0 Omni* would respond to your request 💥"
    CLAUDE_3_SONNET_EXAMPLE = "👇 This is how *Claude 3.5 Sonnet* would respond to your request 🚀"
    GEMINI_1_PRO_EXAMPLE = "👇 This is how *Gemini 1.5 Pro* would respond to your request 💼"
    MIDJOURNEY_EXAMPLE = """
☝️ These are the images that <b>Midjourney</b> would draw for your request

To start drawing using <b>Midjourney</b>, just type the command /midjourney 🎨
"""
    SUNO_EXAMPLE = """
☝️ This is the song that <b>Suno</b> would create for your request

To start creating songs using <b>Suno</b>, just type the command /suno 🎸
"""

    PHOTO_FEATURE_FORBIDDEN = """
⚠️ Sending photos is only available in models:
━ <b>ChatGPT</b>:
    ┣ ChatGPT 4.0 Omni Mini ✉️
    ┗ ChatGPT 4.0 Omni 💥
━ <b>Claude</b>:
    ┣ Claude 3.5 Sonnet 💫
    ┗ Claude 3.0 Opus 🚀
━ <b>Gemini</b>:
    ┣ Gemini 1.5 Flash 🏎
    ┣ Gemini 1.5 Pro 💼
    ┗ Gemini 1.0 Ultra 🛡️

Use /mode to switch to a model that supports image vision 👀
"""

    # Midjourney
    MIDJOURNEY_ALREADY_CHOSE_UPSCALE = "You've already chosen this image, try a new one 🙂"

    # Flux
    STRICT_SAFETY_TOLERANCE = "🔒 Strict Prompt Security"
    MIDDLE_SAFETY_TOLERANCE = "🔏 Average Prompt Security"
    PERMISSIVE_SAFETY_TOLERANCE = "🔓 Weak Prompt Security"

    # Suno
    SUNO_INFO = """
🤖 <b>Choose the style for creating your song:</b>

🎹 In <b>simple mode</b>, you only need to describe the theme of the song and the genre
🎸 In <b>custom mode</b>, you have the opportunity to use your own lyrics and experiment with genres

<b>Suno</b> will create 2 tracks, up to 4 minutes each 🎧
"""
    SUNO_SIMPLE_MODE = "🎹 Simple"
    SUNO_CUSTOM_MODE = "🎸 Custom"
    SUNO_SIMPLE_MODE_PROMPT = """
🎶 <b>Song Description</b>

To create your song in simple mode, please describe the theme of the song and the musical genre you desire. This will help the system better understand your expectations and create something truly unique for you.

📝 Write your prompt below and let's start the creative process!
"""
    SUNO_CUSTOM_MODE_LYRICS = """
🎤 <b>Song Lyrics</b>

To create your song in custom mode, you need to provide the lyrics that will be used in the music. This is a crucial element that will give your composition a unique character and a special mood.

✍️ Send the lyrics of your future song right now, and let's create a musical masterpiece together!
"""
    SUNO_CUSTOM_MODE_GENRES = """
🎵 <b>Genre Selection</b>

To ensure your song in custom mode matches your preferences, please specify the genres you'd like to incorporate. The choice of genre significantly influences the style and mood of the composition, so choose carefully.

🔍 List the desired genres separated by commas in your next message, and let's start creating your unique song!
"""
    SUNO_START_AGAIN = "Start again 🔄"
    SUNO_TOO_MANY_WORDS = "<b>Oh, oh!</b>🚧\n\nAt some steps, you sent too much text 📝\n\nTry again, but with a smaller text, please!"
    SUNO_VALUE_ERROR = "It doesn't look like a prompt 🧐\n\nPlease enter a different value"

    # MusicGen
    MUSIC_GEN_INFO = """
Your musical workshop 🎹

Open the door to a world where every idea of yours turns into music! With <b>MusicGen</b>, your imagination is the only limit. I'm ready to transform your words and descriptions into unique melodies 🎼

Tell me what kind of music you want to create. Use words to describe its style, mood, and instruments. You don't need to be a professional - just share your idea, and let's bring it to life together! 🎤
"""
    MUSIC_GEN_TYPE_SECONDS = """
<b>How many seconds in your symphony?</b> ⏳

Fantastic! Your melody idea is ready to come to life. Now, the exciting part: how much time do we give this musical magic to unfold in all its glory? <b>MusicGen</b> awaits your decision 🎼

Write or choose the duration of your composition in seconds. Whether it's a flash of inspiration or an epic odyssey, I'm ready to create! ✨
"""
    MUSIC_GEN_MIN_ERROR = """
🤨 <b>Hold on there, partner!</b>

Looks like you're trying to request fewer than 1 second. In the world of creativity, I need at least 1 to get the ball rolling!

🌟 <b>Tip</b>: Type a number greater than 0 to start the magic!
"""
    MUSIC_GEN_MAX_ERROR = """
🤨 <b>Hold on there, partner!</b>

Looks like you're trying to request more than 3 minutes, I can't generate more yet!

🌟 <b>Tip</b>: Type a number less than 180 to start the magic!
"""
    SECONDS_30 = "🔹 30 seconds"
    SECONDS_60 = "🔹 60 seconds (1 minute)"
    SECONDS_180 = "🔹 180 seconds (3 minutes)"

    # Settings
    SETTINGS_CHOOSE_MODEL_TYPE = """
⚙️ <b>Welcome to settings!</b> ⚙️

🌍 To change the interface language, enter the command /language
🤖 To change the model, enter the command /mode

Here you are the artist, and settings are your palette. Choose the model type you want to personalize for yourself below 👇
"""
    SETTINGS_CHOOSE_MODEL = """
Choose the model you want to personalize for yourself below 👇
"""
    SHOW_THE_NAME_OF_THE_CHATS = "Show the name of the chats"
    SHOW_THE_NAME_OF_THE_ROLES = "Show the name of the roles"
    SHOW_USAGE_QUOTA_IN_MESSAGES = "Show usage quota in messages"
    VOICE_MESSAGES = "Voice messages 🎙"
    TURN_ON_VOICE_MESSAGES_FROM_RESPONDS = "Turn on voice messages"
    LISTEN_VOICES = "Listen voices"

    # Voice
    VOICE_MESSAGES_FORBIDDEN = """
🎙 <b>Oops! Seems like your voice went into the AI void!</b>

To unlock the magic of voice-to-text, simply wave your wand with buttons below:
"""

    # Payment
    BUY = """
🚀 <b>Welcome to the Wonder Store!</b> 🪄

You’re stepping into a world of exclusive possibilities! What will it be today?

🌟 <b>Subscriptions: Everything All at Once — Your VIP pass to all AI tools and beyond!</b>
Chat with ChatGPT, Claude, and Gemini; Create with DALL-E, Midjourney, Stable Diffusion, Flux, FaceSwap, and Photoshop AI; Make music with MusicGen and Suno; Enjoy voice messages, quick replies, themed chats, and much more. Everything is included in the subscription for your convenience and daily discoveries!

🛍 <b>Packages: Pay only for the generations you need!</b>
Need specific generations for particular tasks? Packages let you choose a set number of requests and AI tools — pay only for what you truly need.

Choose by clicking a button below 👇
"""
    CHANGE_CURRENCY = "💱 Change currency"
    YOOKASSA_PAYMENT_METHOD = "🪆💳 YooKassa"
    PAY_SELECTION_PAYMENT_METHOD = "🌍💳 PaySelection"
    STRIPE_PAYMENT_METHOD = "🌍💳 Stripe"
    TELEGRAM_STARS_PAYMENT_METHOD = "✈️⭐️ Telegram Stars"
    CHOOSE_PAYMENT_METHOD = """
<b>Choose a payment method:</b>

🪆💳 <b>YooKassa (Russian's Cards)</b>

🌍💳 <b>Stripe (International Cards)</b>

✈️⭐️ <b>Telegram Stars (Currency in Telegram)</b>
"""
    PROCEED_TO_PAY = "🌐 Proceed to payment"
    MONTHLY = "Monthly"
    YEARLY = "Yearly"

    # Subscription
    MONTH_1 = "1 month"
    MONTHS_3 = "3 months"
    MONTHS_6 = "6 months"
    MONTHS_12 = "12 months"
    DISCOUNT = "💸 Discount"
    NO_DISCOUNT = "No discount"
    SUBSCRIPTION = "💳 Subscription"
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

Your subscription has come to an end. But don't worry, the AI journey isn't over yet! 🚀

You can renew your magic pass with clicking one of the buttons below to keep exploring the AI universe:
"""
    PACKAGES_END = """
🕒 <b>Your package or packages time is up!</b> ⌛

Oops, it looks like your fast messages (or voice messages, catalog access) package has run its course. But don't worry, new opportunities always await beyond the horizon!

🎁 Want to continue? Check out my offers by hitting one of the buttons below:
"""
    CHATS_RESET = """
🔄 <b>Chats updated!</b> 💬

Your chats have switched their unique roles to "Personal Assistant" as your access to the role catalog has ended. But don't worry, your AI helpers are still here to keep the conversation going!

🎁 Want your previous roles back? Click one of the button below to purchase a new package or subscribe for unlimited access
"""

    # Package
    PACKAGE = "🛍 Package"
    PACKAGES = "🛍 Packages"
    SHOPPING_CART = "🛒 Cart"
    ADD_TO_CART = "➕ Add to cart"
    BUY_NOW = "🛍 Buy now"
    REMOVE_FROM_CART = "➖ Remove from cart"
    GO_TO_CART = "🛒 Go to cart"
    CONTINUE_SHOPPING = "🛍 Continue shopping"
    PROCEED_TO_CHECKOUT = "💳 Proceed to checkout"
    CLEAR_CART = "🗑 Clear cart"
    ADD_TO_CART_OR_BUY_NOW = "Buy now or add to cart?"
    ADDED_TO_CART = "Added to cart ✅"
    GO_TO_CART_OR_CONTINUE_SHOPPING = "Go to cart or continue shopping?"
    MIN_ERROR = "Oops! It looks like the total sum is below our minimum threshold. Please choose count of packages that meets or exceeds the minimum required. Let's try that again! 🔄"
    MAX_ERROR = "Oops! It looks like the number entered is higher than you can purchase. Please enter a smaller value or one corresponding to your balance. Let's try that again! 🔄"
    VALUE_ERROR = """
Whoops! That doesn't seem like a number 🤔

Could you please enter a numeric value?

Let's give it another go! 🔢
"""
    PACKAGE_SUCCESS = """
🎉 <b>Cha-Ching! Payment success!</b> 💳

Your payment just zoomed through like a superhero! 🦸‍ You've successfully unlocked the awesome power of your chosen package. Get ready for a rollercoaster of AI fun and excitement! 🎢

Remember, with great power comes great... well, you know how it goes. Let's make some magic happen! ✨🪄
"""
    PACKAGES_SUCCESS = """
🎉 <b>Cha-Ching! Payment success!</b> 💳

Your payment just zoomed through like a superhero! 🦸‍ You've successfully unlocked the awesome power of your chosen packages. Get ready for a rollercoaster of AI fun and excitement! 🎢

Remember, with great power comes great... well, you know how it goes. Let's make some magic happen! ✨🪄
"""

    # Catalog
    MANAGE_CATALOG = "Manage catalog 🎭"
    CATALOG = """
📁 <b>Welcome to the Catalog of Possibilities!</b>

Here you’ll find a collection of digital assistant roles and a prompt library for inspiration.

It’s all in your hands – just press the button 👇
"""
    CATALOG_DIGITAL_EMPLOYEES = "Roles Catalog 🎭"
    CATALOG_DIGITAL_EMPLOYEES_INFO = """
🎭 <b>Step right up to our role catalogue extravaganza!</b> 🌟

Choose from an array of AI personas, each with its own flair and expertise 🎩

Just hit the button below 👇
"""
    CATALOG_PROMPTS = "Prompts Catalog 🗯"
    CATALOG_PROMPTS_CHOOSE_MODEL_TYPE = """
🗯 <b>Welcome to the Prompts Catalog!</b>

Text, graphic, and musical models are ready to inspire you

Simply choose the type you need by clicking the button below 👇
"""
    CATALOG_PROMPTS_CHOOSE_CATEGORY = """
🗯 <b>Prompts Catalog</b>

Select the <b>category</b> you need by clicking the button below 👇
"""
    CATALOG_PROMPTS_CHOOSE_SUBCATEGORY = """
🗯 <b>Prompts Catalog</b>

Select the <b>subcategory</b> you need by clicking the button below 👇
"""

    @staticmethod
    def catalog_prompts_choose_prompt(prompts: list[Prompt]):
        prompt_info = ''
        for index, prompt in enumerate(prompts):
            is_last = index == len(prompts) - 1
            left_part = '┣' if not is_last else '┗'
            right_part = '\n' if not is_last else ''
            prompt_info += f'    {left_part} <b>{index + 1}</b>: {prompt.names.get(LanguageCode.EN)}{right_part}'

        return f"""
🗯 <b>Prompts Catalog</b>

Prompts:
{prompt_info}

Select the <b>prompt number</b> to get the full prompt by clicking the button below 👇
"""

    @staticmethod
    def catalog_prompts_info_prompt(prompt: Prompt):
        return f"""
🗯 <b>Prompt Catalog</b>

You have selected the prompt: <b>{prompt.names.get(LanguageCode.EN)}</b>

Choose what you want to do by clicking the button below 👇
"""

    CATALOG_PROMPTS_GET_SHORT_PROMPT = "Get Short Prompt ⚡️"
    CATALOG_PROMPTS_GET_LONG_PROMPT = "Get Long Prompt 📜"
    CATALOG_PROMPTS_GET_EXAMPLES = "Get Prompt Results 👀"
    CATALOG_PROMPTS_COPY = "Copy This Prompt 📋"

    @staticmethod
    def catalog_prompts_examples(products: list[Product]):
        prompt_examples_info = ''
        for index, product in enumerate(products):
            is_last = index == len(products) - 1
            is_first = index == 0
            left_part = '┣' if not is_last else '┗'
            right_part = '\n' if not is_last else ''
            prompt_examples_info += f'{left_part if not is_first else "┏"} <b>{index + 1}</b>: {product.names.get(LanguageCode.EN)}{right_part}'

        return f"""
{prompt_examples_info}
"""

    CATALOG_FORBIDDEN_ERROR = """
🔒 <b>Whoops! Looks like you've hit a VIP-only zone!</b> 🌟

You're just a click away from unlocking my treasure trove of AI roles, but it seems you don't have the golden key yet

No worries, though! You can grab it easily just hitting one of the buttons below:
"""
    CREATE_ROLE = "Create a new role"

    # Chats
    DEFAULT_CHAT_TITLE = "New chat"
    MANAGE_CHATS = "Manage chats 💬"
    SHOW_CHATS = "Show chats 👁️"
    CREATE_CHAT = "Create a new chat 💬"
    CREATE_CHAT_FORBIDDEN = """
🚫 Oops!

Looks like you've hit the limit for creating new chats. But don't worry, the world of endless chats is just a click away! 🌍✨

To unlock the power of multiple chats just choose one of the buttons below:
"""
    CREATE_CHAT_SUCCESS = "💬 Chat created! 🎉\n👌 Don't forget to switch to a new one using /chats"
    TYPE_CHAT_NAME = "Type your chat name"
    SWITCH_CHAT = "Switch between chats 🔄"
    SWITCH_CHAT_FORBIDDEN = """
"🔄 <b>Switching gears? Hold that thought!</b> ⚙️

You're currently in your one and only chat universe. It's a cozy place, but why not expand your horizons? 🌌

To hop between multiple thematic chats, just get your pass by clicking one of the buttons below:
"""
    SWITCH_CHAT_SUCCESS = "Chat successfully switched! 🎉"
    RESET_CHAT = "Reset chat ♻️"
    RESET_CHAT_WARNING = """
🧹 <b>Chat cleanup incoming!</b> 🚨

You're about to erase all messages and clear the context of this chat. This action is irreversible, and all your messages will vanish into virtual dust. Are you sure you want to proceed?

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

This is your sole chat kingdom, and a kingdom needs its king or queen! Deleting it would be like canceling your own party 🎈

How about adding more chats to your realm instead? Check out buttons below to build your chat empire:
"""
    DELETE_CHAT_SUCCESS = "🗑️ Chat successfully deleted! 🎉"

    # FaceSwap
    CHOOSE_YOUR_PACKAGE = """
🌟<b>Let's get creative with your photos!</b>

Ready? Let's dive into a world of imagination! 🚀

🌈 Send me a photo in which I will replace the face with yours from /profile or just <b>select a package below</b> and start your photo adventure 👇
    """
    GENERATIONS_IN_PACKAGES_ENDED = """
🎨 <b>Wow, you've used up all your generations in our packages! Your creativity is astounding!</b> 🌟

What's next?
- 📷 Send me photos with faces for face swapping in FaceSwap!
- 🔄 Or switch models via /mode to continue creating with other AI tools!

Time for new AI discoveries! 🚀
"""
    FACE_SWAP_MIN_ERROR = """
🤨 <b>Hold on there, partner!</b>

Looks like you're trying to request fewer than 1 image. In the world of creativity, I need at least 1 to get the ball rolling!

🌟 <b>Tip</b>: Type a number greater than 0 to start the magic. Let's unleash those creative ideas!
"""
    FACE_SWAP_MAX_ERROR = """
🚀 <b>Whoa, aiming high, I see!</b> But, uh-oh...

You're asking for more images than we have.

🧐 <b>How about this?</b> Let's try a number within the package limit!
"""
    FACE_SWAP_NO_FACE_FOUND_ERROR = """
🚫 <b>Problem with Photo Processing</b>

Unfortunately, we were unable to clearly identify a face in the photo from your /profile
Please upload a new photo where your face is clearly visible and in good quality via the /profile command.

🔄 After uploading a new photo, please try again. Thank you for your patience!
"""
    # Photoshop AI
    PHOTOSHOP_AI_INFO = """
This section brings together AI tools for editing and styling images.

Click the button below to choose an action and start your creative journey! 👇
"""
    PHOTOSHOP_AI_RESTORATION = "Restoration 🖌"
    PHOTOSHOP_AI_RESTORATION_INFO = """
The tool detects scratches and cuts on the original image and removes them.

📸 Upload your image to the chat and let the magic begin! ✨
"""
    PHOTOSHOP_AI_COLORIZATION = "Colorization 🌈"
    PHOTOSHOP_AI_COLORIZATION_INFO = """
The tool allows you to add color to black-and-white images.

📸 Upload your image to the chat and let the magic begin! ✨
"""
    PHOTOSHOP_AI_REMOVE_BACKGROUND = "Background Removal 🗑"
    PHOTOSHOP_AI_REMOVE_BACKGROUND_INFO = """
The tool allows you to remove the background from an image.

📸 Upload your image to the chat and let the magic begin! ✨
"""

    ERROR = """
I've got an unknown error 🤒

Please try again or contact our tech support:
"""
    NETWORK_ERROR = """
I lost my connection with Telegram 🤒

Please try again 🥺
"""
    TECH_SUPPORT = "👨‍💻 Tech Support"
    BACK = "Back ◀️"
    CLOSE = "Close 🚪"
    CANCEL = "Cancel ❌"
    APPROVE = "Approve ✅"
    IMAGE = "Image 🖼"
    DOCUMENT = "Document 📄"
    AUDIO = "Audio 🔈"
    VIDEO = "Video 📹"
    SKIP = "Skip ⏩️"

    TERMS_LINK = "https://telegra.ph/Terms-of-Service-in-GPTsTurboBot-05-07"

    @staticmethod
    def purchase_minimal_price(currency: Currency, current_price: str) -> str:
        left_part_price = Currency.SYMBOLS[currency] if currency == Currency.USD else ''
        right_part_price = '' if currency == Currency.USD else Currency.SYMBOLS[currency]
        return f"""
😕 Oh no...

To complete the purchase, the total amount must be equal to or greater than <b>{left_part_price}1{right_part_price}</b>
Currently, the total purchase amount is: <b>{left_part_price}{current_price}{right_part_price}</b>
"""

    @staticmethod
    def profile(
        subscription_name,
        subscription_status,
        gender,
        current_model,
        current_model_version,
        current_currency,
        renewal_date,
    ) -> str:
        if subscription_status == SubscriptionStatus.CANCELED:
            subscription_info = f"📫 <b>Subscription Status:</b> Canceled. Active until {renewal_date}"
        else:
            subscription_info = "📫 <b>Subscription Status:</b> Active"

        if gender == UserGender.MALE:
            gender_info = f"<b>Gender:</b> {English.MALE}"
        elif gender == UserGender.FEMALE:
            gender_info = f"<b>Gender:</b> {English.FEMALE}"
        else:
            gender_info = f"<b>Gender:</b> {English.UNSPECIFIED}"

        if current_model == Model.CHAT_GPT and current_model_version == ChatGPTVersion.V4_Omni_Mini:
            current_model = English.CHATGPT4_OMNI_MINI
        elif current_model == Model.CHAT_GPT and current_model_version == ChatGPTVersion.V4_Omni:
            current_model = English.CHATGPT4_OMNI
        elif current_model == Model.CHAT_GPT and current_model_version == ChatGPTVersion.V1_O_Mini:
            current_model = English.CHAT_GPT_O_1_MINI
        elif current_model == Model.CHAT_GPT and current_model_version == ChatGPTVersion.V1_O_Preview:
            current_model = English.CHAT_GPT_O_1_PREVIEW
        elif current_model == Model.CLAUDE and current_model_version == ClaudeGPTVersion.V3_Haiku:
            current_model = English.CLAUDE_3_HAIKU
        elif current_model == Model.CLAUDE and current_model_version == ClaudeGPTVersion.V3_Sonnet:
            current_model = English.CLAUDE_3_SONNET
        elif current_model == Model.CLAUDE and current_model_version == ClaudeGPTVersion.V3_Opus:
            current_model = English.CLAUDE_3_OPUS
        elif current_model == Model.GEMINI and current_model_version == GeminiGPTVersion.V1_Flash:
            current_model = English.GEMINI_1_FLASH
        elif current_model == Model.GEMINI and current_model_version == GeminiGPTVersion.V1_Pro:
            current_model = English.GEMINI_1_PRO
        elif current_model == Model.GEMINI and current_model_version == GeminiGPTVersion.V1_Ultra:
            current_model = English.GEMINI_1_ULTRA
        elif current_model == Model.DALL_E:
            current_model = English.DALL_E
        elif current_model == Model.MIDJOURNEY:
            current_model = English.MIDJOURNEY
        elif current_model == Model.STABLE_DIFFUSION:
            current_model = English.STABLE_DIFFUSION
        elif current_model == Model.FLUX:
            current_model = English.FLUX
        elif current_model == Model.FACE_SWAP:
            current_model = English.FACE_SWAP
        elif current_model == Model.PHOTOSHOP_AI:
            current_model = English.PHOTOSHOP_AI
        elif current_model == Model.MUSIC_GEN:
            current_model = English.MUSIC_GEN
        elif current_model == Model.SUNO:
            current_model = English.SUNO

        if current_currency == Currency.XTR:
            current_currency = f'Telegram Stars {Currency.SYMBOLS[current_currency]}'
        else:
            current_currency = f'{Currency.SYMBOLS[current_currency]}'

        return f"""
<b>Profile</b> 👤

---------------------------

🤖 <b>Current model: {current_model}</b>
{gender_info}

---------------------------

💱 <b>Current currency: {current_currency}</b>
💳 <b>Subscription type:</b> {subscription_name}
🗓 <b>Subscription renewal date:</b> {f'{renewal_date}' if subscription_name != '🆓' else 'N/A'}
{subscription_info}

---------------------------

Choose action 👇
"""

    @staticmethod
    def profile_quota(
        subscription_limits: dict,
        daily_limits: dict,
        additional_usage_quota: dict,
        hours_before_limit_update: int,
        minutes_before_limit_update: int,
    ) -> str:
        return f"""
<b>Quota:</b>

🔤 <b>Text Models</b>:
━ <b>Basic</b>:
    ┣ Daily Limits: {format_number(daily_limits[Quota.CHAT_GPT4_OMNI_MINI])}/{format_number(subscription_limits[Quota.CHAT_GPT4_OMNI_MINI])}
    ┣ ✉️ ChatGPT 4.0 Omni Mini{f': extra {additional_usage_quota[Quota.CHAT_GPT4_OMNI_MINI]}' if additional_usage_quota[Quota.CHAT_GPT4_OMNI_MINI] > 0 else ''}
    ┣ 📜 Claude 3.5 Haiku{f': extra {additional_usage_quota[Quota.CLAUDE_3_HAIKU]}' if additional_usage_quota[Quota.CLAUDE_3_HAIKU] > 0 else ''}
    ┗ 🏎 Gemini 1.5 Flash{f': extra {additional_usage_quota[Quota.GEMINI_1_FLASH]}' if additional_usage_quota[Quota.GEMINI_1_FLASH] > 0 else ''}

━ <b>Advanced</b>:
    ┣ Daily Limits: {format_number(daily_limits[Quota.CHAT_GPT4_OMNI])}/{format_number(subscription_limits[Quota.CHAT_GPT4_OMNI])}
    ┣ 💥 ChatGPT 4.0 Omni{f': extra {additional_usage_quota[Quota.CHAT_GPT4_OMNI]}' if additional_usage_quota[Quota.CHAT_GPT4_OMNI] > 0 else ''}
    ┣ 🧩 ChatGPT o1-mini{f': extra {additional_usage_quota[Quota.CHAT_GPT_O_1_PREVIEW]}' if additional_usage_quota[Quota.CHAT_GPT_O_1_PREVIEW] > 0 else ''}
    ┣ 💫 Claude 3.5 Sonnet{f': extra {additional_usage_quota[Quota.CLAUDE_3_SONNET]}' if additional_usage_quota[Quota.CLAUDE_3_SONNET] > 0 else ''}
    ┗ 💼 Gemini 1.5 Pro{f': extra {additional_usage_quota[Quota.GEMINI_1_PRO]}' if additional_usage_quota[Quota.GEMINI_1_PRO] > 0 else ''}

━ <b>Flagship</b>:
    ┣ Daily Limits: {format_number(daily_limits[Quota.CHAT_GPT_O_1_PREVIEW])}/{format_number(subscription_limits[Quota.CHAT_GPT_O_1_PREVIEW])}
    ┣ 🧪 ChatGPT o1-preview{f': extra {additional_usage_quota[Quota.CHAT_GPT_O_1_PREVIEW]}' if additional_usage_quota[Quota.CHAT_GPT_O_1_PREVIEW] > 0 else ''}
    ┣ 🚀 Claude 3.0 Opus{f': extra {additional_usage_quota[Quota.CLAUDE_3_OPUS]}' if additional_usage_quota[Quota.CLAUDE_3_OPUS] > 0 else ''}
    ┗ 🛡️ Gemini 1.0 Ultra{f': extra {additional_usage_quota[Quota.GEMINI_1_ULTRA]}' if additional_usage_quota[Quota.GEMINI_1_ULTRA] > 0 else ''}

---------------------------

🖼 <b>Image Models</b>:
    ┣ Daily Limits: {format_number(daily_limits[Quota.DALL_E])}/{format_number(subscription_limits[Quota.DALL_E])}
    ┣ 👨‍🎨 DALL-E{f': extra {additional_usage_quota[Quota.DALL_E]}' if additional_usage_quota[Quota.DALL_E] > 0 else ''}
    ┣ 🎨 Midjourney{f': extra {additional_usage_quota[Quota.MIDJOURNEY]}' if additional_usage_quota[Quota.MIDJOURNEY] > 0 else ''}
    ┣ 🎆 Stable Diffusion{f': extra {additional_usage_quota[Quota.STABLE_DIFFUSION]}' if additional_usage_quota[Quota.STABLE_DIFFUSION] > 0 else ''}
    ┣ 🫐 Flux{f': extra {additional_usage_quota[Quota.FLUX]}' if additional_usage_quota[Quota.FLUX] > 0 else ''}
    ┣ 📷 FaceSwap{f': extra {additional_usage_quota[Quota.FACE_SWAP]}' if additional_usage_quota[Quota.FACE_SWAP] > 0 else ''}
    ┗ 🪄 Photoshop AI{f': extra {additional_usage_quota[Quota.PHOTOSHOP_AI]}' if additional_usage_quota[Quota.PHOTOSHOP_AI] > 0 else ''}

---------------------------

🎵 <b>Music Models</b>:
    ┣ Daily Limits: {format_number(daily_limits[Quota.SUNO])}/{format_number(subscription_limits[Quota.SUNO])}
    ┣ 🎺 MusicGen{f': extra {additional_usage_quota[Quota.MUSIC_GEN]}' if additional_usage_quota[Quota.MUSIC_GEN] > 0 else ''}
    ┗ 🎸 Suno{f': extra {additional_usage_quota[Quota.SUNO]}' if additional_usage_quota[Quota.SUNO] > 0 else ''}

---------------------------

━ 💬 <b>Thematic chats</b>: {daily_limits[Quota.ADDITIONAL_CHATS] + additional_usage_quota[Quota.ADDITIONAL_CHATS]}
━ 🎭 <b>Access to a catalog with digital employees</b>: {'✅' if daily_limits[Quota.ACCESS_TO_CATALOG] or additional_usage_quota[Quota.ACCESS_TO_CATALOG] else '❌'}
━ 🎙 <b>Voice messages</b>: {'✅' if daily_limits[Quota.VOICE_MESSAGES] or additional_usage_quota[Quota.VOICE_MESSAGES] else '❌'}
━ ⚡ <b>Fast answers</b>: {'✅' if daily_limits[Quota.FAST_MESSAGES] or additional_usage_quota[Quota.FAST_MESSAGES] else '❌'}

---------------------------

🔄 <i>Limit will be updated in: {hours_before_limit_update} h. {minutes_before_limit_update} min.</i>
"""

    @staticmethod
    def notify_about_quota(
        subscription_limits: dict,
    ) -> str:
        texts = [
            f"""
🤖 Hey, it's me! Remember me?

🤓 I'm here to remind you about your daily quotas:
- {format_number(subscription_limits[Quota.CHAT_GPT4_OMNI_MINI])} text requests waiting to be turned into your masterpieces
- {format_number(subscription_limits[Quota.DALL_E])} graphic opportunity ready to bring your ideas to life

🔥 Don’t let them go to waste — start now!
""",
            f"""
🤖 Hi, it's Fusi, your personal assistant. Yep, I'm back!

😢 I noticed you haven’t used your quotas for a while. Just a friendly reminder that every day you have:
- {format_number(subscription_limits[Quota.CHAT_GPT4_OMNI_MINI])} text requests to fuel your ideas
- {format_number(subscription_limits[Quota.DALL_E])} graphic slot to bring your thoughts to life

✨ Shall we get started? I'm ready right now!
""",
            f"""
🤖 It's me, Fusi, your personal robot, with an important reminder!

🤨 Did you know you have:
- {format_number(subscription_limits[Quota.CHAT_GPT4_OMNI_MINI])} text requests for your bright ideas
- {format_number(subscription_limits[Quota.DALL_E])} image slot to visualize your concepts

🔋 I'm fully charged and ready to help you create something amazing!
""",
            f"""
🤖 It’s me again! I missed you...

😢 I was just thinking... Your quotas might miss you too:
- {format_number(subscription_limits[Quota.CHAT_GPT4_OMNI_MINI])} inspiring text requests are waiting for their moment
- {format_number(subscription_limits[Quota.DALL_E])} visual idea ready to come to life

💡 Give me the chance to help you create something incredible!
""",
            f"""
🤖 Hi, it’s Fusi! Your quotas won’t use themselves, you know that, right?

🫤 Need a reminder? Here you go:
- {format_number(subscription_limits[Quota.CHAT_GPT4_OMNI_MINI])} text requests that could be the start of something big
- {format_number(subscription_limits[Quota.DALL_E])} image slot to sketch out your imagination

✨ Time to create, and I’m here to help. Let’s get started!
""",
        ]

        return random.choice(texts)

    # Payment
    @staticmethod
    def payment_description_subscription(user_id: str, name: str):
        return f"Paying a subscription {name} for user: {user_id}"

    @staticmethod
    def payment_description_renew_subscription(user_id: str, name: str):
        return f"Renewing a subscription {name} for user: {user_id}"

    @staticmethod
    def subscribe(subscriptions: list[Product], currency: Currency, user_discount: int):
        text_subscriptions = ''
        for subscription in subscriptions:
            subscription_name = subscription.names.get(LanguageCode.EN)
            subscription_price = subscription.prices.get(currency)
            left_part_price = Currency.SYMBOLS[currency] if currency == Currency.USD else ''
            right_part_price = Currency.SYMBOLS[currency] if currency != Currency.USD else ''
            if subscription_name and subscription_price:
                text_subscriptions += f'- <b>{subscription_name}</b>: '
                per_period = 'per month' if subscription.category == ProductCategory.MONTHLY else 'per year'

                discount = get_user_discount(user_discount, 0, subscription.discount)
                if discount:
                    discount_price = Product.get_discount_price(
                        ProductType.SUBSCRIPTION,
                        1,
                        subscription_price,
                        currency,
                        discount,
                        SubscriptionPeriod.MONTH1 if subscription.category == ProductCategory.MONTHLY else SubscriptionPeriod.MONTHS12,
                    )
                    text_subscriptions += f'<s>{left_part_price}{subscription_price}{right_part_price}</s> {left_part_price}{discount_price}{right_part_price} {per_period}\n'
                else:
                    text_subscriptions += f'{left_part_price}{subscription_price}{right_part_price} {per_period}\n'
        return f"""
🤖 Ready to supercharge your digital journey? Here's what's on the menu:

{text_subscriptions}

Pick your potion and hit the button below to subscribe:
"""

    @staticmethod
    def confirmation_subscribe(
        name: str,
        category: ProductCategory,
        currency: Currency,
        price: Union[str, int, float],
    ):
        left_price_part = Currency.SYMBOLS[currency] if currency == Currency.USD else ''
        right_price_part = '' if currency == Currency.USD else Currency.SYMBOLS[currency]
        period = 'month' if category == ProductCategory.MONTHLY else 'year'
        return f"""
You're about to activate subscription {name} for {left_price_part}{price}{right_price_part}/{period}

❗️You can cancel your subscription at any time in <b>Profile 👤</b>
"""

    # Package
    @staticmethod
    def payment_description_package(user_id: str, package_name: str, package_quantity: int):
        return f"Paying {package_quantity} package(-s) {package_name} for user: {user_id}"

    @staticmethod
    def payment_description_cart(user_id: str):
        return f"Paying packages from the cart for user: {user_id}"

    @staticmethod
    def package(currency: Currency, cost: str):
        if currency == Currency.USD:
            cost = f"{Currency.SYMBOLS[currency]}{cost}"
        else:
            cost = f"{cost}{Currency.SYMBOLS[currency]}"

        return f"""
🤖 <b>Welcome to the AI shopping spree!</b> 📦

🪙 <b>1 credit = {cost}</b>

Hit a button and choose a package:
"""

    @staticmethod
    def choose_min(name: str):
        return f"""
🚀 Fantastic!

You've selected the <b>{name}</b> package

🌟 Please <b>type in the number of quantity</b> you'd like to go for
"""

    @staticmethod
    async def shopping_cart(currency: Currency, cart_items: list[dict], discount: int):
        text = ""
        total_sum = 0
        left_price_part = Currency.SYMBOLS[currency] if currency == Currency.USD else ''
        right_price_part = '' if currency == Currency.USD else Currency.SYMBOLS[currency]

        for index, cart_item in enumerate(cart_items):
            product_id, product_quantity = cart_item.get("product_id", ''), cart_item.get("quantity", 0)

            product = await get_product(product_id)

            is_last = index == len(cart_items) - 1
            right_part = '\n' if not is_last else ''
            price = Product.get_discount_price(
                ProductType.PACKAGE,
                product_quantity,
                product.prices.get(currency),
                currency,
                discount,
            )
            total_sum += float(price)
            text += f"{index + 1}. {product.names.get(LanguageCode.EN)}: {product_quantity} ({left_price_part}{price}{right_price_part}){right_part}"

        if not text:
            text = "Your cart is empty"

        return f"""
🛒 <b>Cart</b>

{text}

💳 Total: {left_price_part}{round(total_sum, 2)}{right_price_part}
"""

    @staticmethod
    def confirmation_package(package_name: str, package_quantity: int, currency: Currency, price: str) -> str:
        left_price_part = Currency.SYMBOLS[currency] if currency == Currency.USD else ''
        right_price_part = '' if currency == Currency.USD else Currency.SYMBOLS[currency]
        return f"You're about to buy {package_quantity} package(-s) <b>{package_name}</b> for {left_price_part}{price}{right_price_part}"

    @staticmethod
    async def confirmation_cart(cart_items: list[dict], currency: Currency, price: float) -> str:
        text = ""
        for index, cart_item in enumerate(cart_items):
            product_id, product_quantity = cart_item.get("product_id", ''), cart_item.get("quantity", 0)

            product = await get_product(product_id)

            text += f"{index + 1}. {product.names.get(LanguageCode.EN)}: {product_quantity}\n"

        if currency == Currency.USD:
            total_sum = f"{Currency.SYMBOLS[currency]}{price}"
        else:
            total_sum = f"{price}{Currency.SYMBOLS[currency]}"

        return f"""
You're about to buy next packages from your cart:
{text}

To pay {total_sum}
"""

    # Chats
    @staticmethod
    def chats(current_chat_name: str, total_chats: int, available_to_create_chats: int):
        return f"""
🗨️ <b>Current chat: {current_chat_name}</b>

Welcome to the dynamic world of AI-powered chats! Here's what you can do:

- Create new thematic chats: Immerse yourself in focused discussions tailored to your interests.
- Switch between chats: Effortlessly navigate through your different chat landscapes.
- Reset chats: I'll forget what we talked about, so to speak, I'll lose the context.
- Delete chats: Clean up by removing the chats you no longer need.

📈 Total chats: <b>{total_chats} | Chats available to create: {available_to_create_chats}</b>

Ready to tailor your chat experience? Explore the options below and let the conversations begin! 👇
"""

    # FaceSwap
    @staticmethod
    def choose_face_swap_package(name: str, available_images, total_images: int, used_images: int) -> str:
        remain_images = total_images - used_images
        return f"""
<b>{name}</b>

You've got a treasure trove of <b>{total_images} images</b> in your pack, ready to unleash your creativity! 🌟

🌠 <b>Your available generations</b>: {available_images} images. Need more? Explore /buy or /bonus!
🔍 <b>Used so far</b>: {used_images} images. {'Wow, you are on a roll!' if used_images > 0 else ''}
🚀 <b>Remaining</b>: {remain_images} images. {'Looks like you have used them all' if remain_images == 0 else 'So much potential'}!

📝 <b>Type how many face swaps you want to do, or choose from the quick selection buttons below</b>. The world of face transformations awaits! 🎭🔄
"""

    @staticmethod
    def face_swap_package_forbidden(available_images: int):
        return f"""
🔔 <b>Oops, a little hiccup!</b> 🚧

Looks like you've got only <b>{available_images} generations</b> left in your arsenal.

💡 <b>Pro Tip</b>: Sometimes, less is more! Try a smaller number, or give /buy a whirl for unlimited possibilities!
"""

    # MusicGen
    @staticmethod
    def music_gen_forbidden(available_seconds: int):
        return f"""
🔔 <b>Oops, a little hiccup!</b> 🚧

Looks like you've got only <b>{available_seconds} seconds</b> left in your arsenal.

💡 <b>Pro Tip</b>: Sometimes, less is more! Try a smaller number, or give /buy a whirl for unlimited possibilities!
"""

    # AI
    @staticmethod
    def switched(model_name: str, model_type: ModelType, model_info: dict):
        if model_type == ModelType.TEXT:
            facts = f"""ℹ️ Facts and Settings:
    ┣ 📅 Knowledge up to: {model_info.get('training_data')}
    ┣ 📷 Image support: {'Yes ✅' if model_info.get('support_photos', False) else 'No ❌'}
    ┣ 📄 Document support: {'Coming Soon 🔜' if model_info.get('support_documents', False) else 'No ❌'}
    ┣ 🎙 Voice answers: {'Enabled ✅' if model_info.get(UserSettings.TURN_ON_VOICE_MESSAGES, False) else 'Disabled ❌'}
    ┗ 🎭 Current role: {model_info.get('role')}"""
        elif model_type == ModelType.IMAGE:
            facts = f"""ℹ️ Settings:
    ┣ 📐 Aspect ratio: {'Custom' if model_info.get(UserSettings.ASPECT_RATIO, AspectRatio.CUSTOM) == AspectRatio.CUSTOM else model_info.get(UserSettings.ASPECT_RATIO)}
    ┗ 🗯 Sending type: {English.DOCUMENT if model_info.get(UserSettings.SEND_TYPE, SendType.IMAGE) == SendType.DOCUMENT else English.IMAGE}"""
        elif model_type == ModelType.MUSIC:
            facts = f"""ℹ️ Settings:
    ┗ 🗯 Sending type: {English.VIDEO if model_info.get(UserSettings.SEND_TYPE, SendType.AUDIO) == SendType.VIDEO else English.AUDIO}"""
        else:
            facts = f"ℹ️ Facts and Settings: Coming Soon 🔜"

        return f"""
🔄 <b>You have successfully switched to the {model_name} model</b>

{facts}

⬇️ Use the buttons below to explore more:
"""

    @staticmethod
    def requests_recommendations() -> list[str]:
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
    def image_recommendations() -> list[str]:
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
    def music_recommendations() -> list[str]:
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
            "Planting your question in my digital garden. Let's see what grows... 🌱🤖",
            "Flexing my virtual muscles for a powerful answer... 💪",
            "Whoosh — calculations in progress! The answer will be ready soon... 🪄",
            "My digital owls are flying out in search of a wise answer. They'll be back with the goods soon... 🦉",
            "There's a brainstorm happening in cyberspace, and I'm catching lightning for your answer... ⚡",
            "My team of digital raccoons is on the hunt for the perfect answer. They're great at this... 🦝",
            "Sifting through information like a squirrel gathering nuts, looking for the juiciest one... 🐿️",
            "Throwing on my virtual detective coat, heading out to find your answer... 🕵️‍♂️️",
            "Downloading a fresh batch of ideas from space. Your answer will land in a few seconds... 🚀",
            "Hold on, laying out the data cards on the virtual table. Getting ready for a precise answer... 🃏",
            "My virtual ships are sailing the sea of information. The answer is on the horizon... 🚢",
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
            "Cooking up a visual symphony in the AI kitchen... 🍳🎼",
            "Pushing the clouds of creativity to craft your visual masterpiece... ☁️🎨",
            "Gathering digital brushes and paints to bring your vision to life... 🎨🖌️",
            "Summoning pixel dragons to create an epic image... 🐉",
            "Bringing in digital bees to collect the nectar for your visual bloom... 🐝",
            "Putting on my digital artist hat and getting to work on your masterpiece... 👒",
            "Dipping pixels into a magical solution so they can shine into a masterpiece... 🧪✨",
            "Sculpting your image from the clay of imagination, a masterpiece is on the way... 🏺",
            "My virtual elves are already painting your image... 🧝‍♂️",
            "Virtual turtles are carrying your image across the sea of data... 🐢",
            "Virtual kitties are paw-painting your masterpiece right now... 🐱",
        ]

        text = random.choice(texts)
        text += "\n\n⚠️ Generation can take up to 3 minutes"

        return text

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
            "Embarking on a galactic journey of face swapping... 🌌👽",
        ]

        text = random.choice(texts)
        text += "\n\n⚠️ Generation can take up to 5 minutes"

        return text

    @staticmethod
    def processing_request_music():
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

    @staticmethod
    def photoshop_ai_actions() -> list[str]:
        return [
            English.PHOTOSHOP_AI_RESTORATION,
            English.PHOTOSHOP_AI_COLORIZATION,
            English.PHOTOSHOP_AI_REMOVE_BACKGROUND,
        ]

    # Settings
    @staticmethod
    def settings(human_model: str, current_model: Model, dall_e_cost=1) -> str:
        if current_model == Model.CHAT_GPT:
            additional_text = f"\n<b>Version ChatGPT 4.0 Omni Mini</b>: {ChatGPTVersion.V4_Omni_Mini}\n<b>Version ChatGPT 4.0 Omni</b>: {ChatGPTVersion.V4_Omni}\n<b>Version ChatGPT o1-mini</b>: {ChatGPTVersion.V1_O_Mini}\n<b>Version ChatGPT o1-preview</b>: {ChatGPTVersion.V1_O_Preview}"
        elif current_model == Model.CLAUDE:
            additional_text = f"\n<b>Version Claude 3.5 Haiku</b>: {ClaudeGPTVersion.V3_Haiku}\n<b>Version Claude 3.5 Sonnet</b>: {ClaudeGPTVersion.V3_Sonnet}\n<b>Version Claude 3.0 Opus</b>: {ClaudeGPTVersion.V3_Opus}"
        elif current_model == Model.GEMINI:
            additional_text = f"\n<b>Version Gemini 1.5 Flash</b>: {GeminiGPTVersion.V1_Flash}\n<b>Version Gemini 1.5 Pro</b>: {GeminiGPTVersion.V1_Pro}\n<b>Version Gemini 1.0 Ultra</b>: {GeminiGPTVersion.V1_Ultra}"
        elif current_model == Model.DALL_E:
            additional_text = f"\nAt the current settings, 1 request costs: {dall_e_cost} 🖼"
        else:
            additional_text = ""

        return f"""
⚙️ <b>Settings for model:</b> {human_model}
{additional_text}
"""

    # Bonus
    @staticmethod
    def bonus(user_id: str, balance: float, referred_count: int, feedback_count: int, play_count: int) -> str:
        return f"""
🎁 <b>Your bonus balance</b>

💰 Current balance: {float(balance)}

To top up your bonus balance, you can:
━ 1️⃣ <b>Invite friends:</b>
    ┣ 💸 For each invited user, you and the invited user will get 25 credits each 🪙
    ┣ 🌟 Your personal referral link for invitations: {Texts.referral_link(user_id, False)}
    ┗ 👤 You've invited: {referred_count}

━ 2️⃣ <b>Leave feedback:</b>
    ┣ 💸 For each constructive feedback, you get 25 credits 🪙
    ┣ 📡 To leave feedback, enter the command /feedback
    ┗ 💭 You've left: {feedback_count}

━ 3️⃣ <b>Try your luck in one of the games:</b>
    ┣ 🎳 Play bowling and receive as many credits as the number of pins you knock down 1-6 🪙
    ┣ ⚽️ Score a goal and get 5 credits 🪙
    ┣ 🏀 Make a basket and receive 10 credits 🪙
    ┣ 🎯 Hit the bullseye and earn 15 credits 🪙
    ┣ 🎲 Guess the number that will come up on the dice and get 20 credits 🪙
    ┣ 🎰 Hit the Jackpot and receive 50-100 credits 🪙
    ┗ 🎮 You've plaid times: {play_count}

Choose the action:
"""
