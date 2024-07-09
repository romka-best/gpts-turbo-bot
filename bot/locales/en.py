import random
from typing import List, Dict

from bot.locales.texts import Texts
from bot.database.models.common import Currency, Quota, Model, ChatGPTVersion, ClaudeGPTVersion
from bot.database.models.package import PackageType, Package
from bot.database.models.subscription import (
    Subscription,
    SubscriptionType,
    SubscriptionPeriod,
    SubscriptionLimit,
    SubscriptionStatus,
)
from bot.database.models.user import UserGender


class English(Texts):
    START = """
🤖 <b>Welcome to the future of artificial intelligence with ChatGPTs Turbo AI Bot!</b> 🎉

I'm your personal gateway to the world of artificial intelligence and neural networks. Discover the capabilities of AI:
✉️ Communicate with <b>ChatGPT-3.5 Turbo</b>: ask questions, get answers
🧠 Explore advanced intelligence with <b>ChatGPT-4.0 Turbo</b>
💥 Unleash the full potential of AI with <b>ChatGPT-4.0 Omni</b>
💫 The perfect blend of speed and intelligence for business tasks with <b>Claude 3 Sonnet</b>
🚀 Ultimate power for tackling the most complex challenges with <b>Claude 3 Opus</b>
🖼 Draw beautiful pictures with <b>DALL-E</b>
🎨 Create unique images with <b>Midjourney</b>
😜 Try <b>FaceSwap</b> to exchange faces with someone in a photo
🎵 Compose original melodies with <b>MusicGen</b>
🎸 Record your own songs with <b>Suno</b>

Here's a quick guide to get started:
🧠 To get a text response from <b>ChatGPT</b>, enter the command /chatgpt, select the version, and then just type your requests in the chat
🚀 To get a text response from <b>Claude</b>, enter the command /claude, select the version, and then just type your requests in the chat
🖼 To create an image with <b>DALL-E</b>, enter the command /dalle, and then let your imagination run wild with your request
🎨 To create an image with <b>Midjourney</b>, enter the command /midjourney, and then start creating using your imagination with your request
😜 To swap faces with someone in a photo with <b>FaceSwap</b>, enter the command /face_swap, then choose images from our unique packages or send your own
🎵 To create a melody with <b>MusicGen</b>, enter the command /music_gen, and then write a description of the melody
🎸 To create a song with <b>Suno</b>, enter the command /suno, and then write a description of the song or send your own lyrics
🔄 To switch between different neural networks, enter the command /mode, and then select the neural network depending on your creative needs
📊 To check usage information and subscription/purchase details, enter the command /profile
🔍 To learn more about the capabilities of each AI model, enter the command /info
🎭️ To choose a specialized digital assistant in <b>ChatGPT</b> models, enter the command /settings
💬 To manage thematic chats in <b>ChatGPT</b> models, enter the command /settings
🔧 To customize AI models to improve your experience, enter the command /settings

And that's not all! Just type /help to see all my magical AI commands available to you.
I'm here to be your co-pilot on this adventure! 🚀
"""
    COMMANDS = """
🤖 <b>Here's what you can explore:</b>

👋 /start - <b>About me</b>: Discover what I can do for you.
🤖 /mode - <b>Swap neural network models</b> on the fly with — <b>ChatGPT</b>, <b>Claude</b>, <b>DALL-E</b>, <b>Midjourney</b>, <b>FaceSwap</b>, <b>MusicGen</b>, or <b>Suno</b>!
💳 /buy - <b>Subscribe or buy individual packages</b>: Get a new level
👤 /profile - <b>View your profile</b>: Check your subscription details or usage quota and more
🔧 /settings - <b>Customize your experience</b>: Tailor model to fit your needs. There you can also <b>select a digital employee</b> with <b>context-specific chats management</b>
🌍 /language - <b>Switch languages</b>: Set your preferred language for system interface
ℹ️ /info - <b>Get information about AI</b>: Learn for what and why do you need them
🧠 /chatgpt - <b>Chat with ChatGPT</b>: Start a text conversation and receive advanced AI responses
🚀 /claude - <b>Chat with Claude</b>: Begin a discussion and explore the depth of responses from Claude
🖼 /dalle - <b>Draw with DALL-E</b>: Turn your ideas into drawings
🎨 /midjourney - <b>Create with DALL-E 3</b>: Bring your imaginations to life with images
😜 /face_swap - <b>Have fun with FaceSwap</b>: Change faces in photos
🎵 /music_gen - <b>Melodies with MusicGen</b>: Create music without copyrights
🎸 /suno - <b>Songs with Suno</b>: Create your own song with your lyrics and different genres
🎁 /bonus - Learn about your bonus balance and <b>exchange bonuses for unique generation packages</b>
🔑 /promo_code - <b>Unleash exclusive AI features</b> and special offers with your <b>promo code</b>
📡 /feedback - <b>Leave feedback</b>: Help me improve

Just type away a command to begin your AI journey! 🌟
"""
    INFO = """
🤖 <b>Select the models type you want to get information about:</b>
"""
    INFO_TEXT_MODELS = """
🤖 <b>Select the model you want to get information about:</b>
"""
    INFO_IMAGE_MODELS = """
🤖 <b>Select the model you want to get information about:</b>
"""
    INFO_MUSIC_MODELS = """
🤖 <b>Select the model you want to get information about:</b>
"""
    INFO_CHATGPT = """
🤖 <b>There is what each model can do for you:</b>

✉️ <b>ChatGPT-3.5 Turbo: The Versatile Communicator</b>
- <i>Small Talk to Deep Conversations</i>: Ideal for chatting about anything from daily life to sharing jokes.
- <i>Educational Assistant</i>: Get help with homework, language learning, or complex topics like coding.
- <i>Personal Coach</i>: Get motivation, fitness tips, or even meditation guidance.
- <i>Creative Writer</i>: Need a post, story, or even a song? ChatGPT-3.5 Turbo can whip it up in seconds.
- <i>Travel Buddy</i>: Ask for travel tips, local cuisines, or historical facts about your next destination.
- <i>Business Helper</i>: Draft emails, create business plans, or brainstorm marketing ideas.

🧠 <b>ChatGPT-4.0 Turbo: The Advanced Intellect</b>
- <i>In-Depth Analysis</i>: Perfect for detailed research, technical explanations, or exploring hypothetical scenarios.
- <i>Problem Solver</i>: Get help with advanced math problems, programming bugs, or scientific queries.
- <i>Language Expert</i>: Translate complex texts or practice conversational skills in various languages.
- <i>Creative Consultant</i>: Develop plot ideas for your posts, script dialogues, or explore artistic concepts.
- <i>Personalized Recommendations</i>: Get book, movie, or travel recommendations based on your interests.

💥 <b>ChatGPT-4.0 Omni: Next-Generation Intelligence</b>
<i>Detailed Analysis</i>: Perfect for in-depth research, complex technical explanations, or virtual scenario analysis.
<i>Complex Problem Solving</i>: From mathematical calculations to diagnosing software issues and answering scientific queries.
<i>Language Mastery</i>: High-level translation and enhancement of conversational skills in various languages.
<i>Creative Mentor</i>: Inspiring ideas for blogs, scripts, or artistic research.
<i>Personalized Recommendations</i>: Tailored picks for books, movies, or travel routes based on your preferences.
"""
    INFO_CLAUDE = """
🤖 <b>There is what each model can do for you:</b>

💫 <b>Claude 3 Sonnet: A Balance of Speed and Wisdom</b>
<i>Multifunctional Analysis</i>: Effective for comprehensive research and technical explanations.
<i>Problem Solving</i>: Assistance with solving mathematical issues, software bugs, or scientific puzzles.
<i>Linguistic Expert</i>: A reliable assistant for translating texts and enhancing conversational skills in various languages.
<i>Creative Advisor</i>: Development of creative ideas for content and artistic projects.
<i>Personal Guide</i>: Recommendations for cultural content and travel planning tailored to your interests.

🚀 <b>Claude 3 Opus: The Pinnacle of Power and Depth</b>
<i>Advanced Analysis</i>: Ideal for tackling the most complex research and hypothetical scenarios.
<i>Problem Solving Expert</i>: Addresses challenging scientific inquiries, technical issues, and mathematical problems.
<i>Language Mastery</i>: Translations and language practice at a professional level.
<i>Creative Consultant</i>: Support in developing unique ideas for scripts and art projects.
<i>Recommendations Concierge</i>: Expert advice on selecting books, movies, and travel plans that match your tastes.
"""
    INFO_DALL_E = """
🤖 <b>There is what the model can do for you:</b>

🖼 <b>DALL-E: The Creative Genius</b>
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
    INFO_FACE_SWAP = """
🤖 <b>There is what the model can do for you:</b>

🤡 <b>FaceSwap: The Entertainment Master</b>
- <i>Fun Reimaginations</i>: See how you'd look in different historical eras or as various movie characters.
- <i>Personalized Greetings</i>: Create unique birthday cards or invitations with personalized images.
- <i>Memes and Content Creation</i>: Spice up your social media with funny or imaginative face-swapped pictures.
- <i>Digital Makeovers</i>: Experiment with new haircuts or makeup styles.
- <i>Celebrity Mashups</i>: Combine your face with celebrities for fun comparisons.
"""
    INFO_MUSIC_GEN = """
🤖 <b>There is what the model can do for you:</b>

🎶 <b>MusicGen: Your Personal Composer</b>
<i>Creating Unique Melodies</i>: Turn your ideas into musical pieces of any genre - from classical to pop.
<i>Personalized Soundtracks</i>: Create a soundtrack for your next video project, game, or presentation.
<i>Exploring Musical Styles</i>: Experiment with different musical genres and sounds to find your unique style.
<i>Learning and Inspiration</i>: Gain new insights into music theory and the history of genres through music creation.
<i>Instant Melody Creation</i>: Just enter a text description or mood, and MusicGen will instantly turn it into music.
"""
    INFO_SUNO = """
🤖 <b>There is what the model can do for you:</b>

🎸 <b>Suno: A Pro in Creating Songs</b>
<i>Text-to-song transformation</i>: Suno turns your text into songs, matching melody and rhythm to your style.
<i>Personalized songs</i>: Create unique songs for special moments, whether it's a personal gift or a soundtrack for your event.
<i>Explore musical genres</i>: Discover new musical horizons by experimenting with different styles and sounds.
<i>Music education and inspiration</i>: Learn about music theory and the history of genres through the practice of composition.
<i>Instant music creation</i>: Describe your emotions or scenario, and Suno will immediately bring your description to life as a song.
"""

    TEXT_MODELS = "🔤 Text models"
    IMAGE_MODELS = "🧑‍🎨 Image models"
    MUSIC_MODELS = "🎺 Music models"

    # Feedback
    FEEDBACK = """
🌟 <b>Your opinion matters!</b> 🌟

Hey there! We're always looking to improve and your feedback is like gold dust to us 💬✨

- Love something about our bot? Let us know!
- Got a feature request? We're all ears!
- Something bugging you? We're here to squash those bugs 🐞

Just type your thoughts and hit send. Your insights help us grow and get better every day.
And remember, every piece of feedback is a step towards making our bot even more awesome. Can't wait to hear from you! 💌
"""
    FEEDBACK_SUCCESS = """
🌟 <b>Feedback received!</b> 🌟

Thank you for sharing your thoughts! 💌
Your input is the secret sauce to our success. We're cooking up some improvements and your feedback is the key ingredient 🍳🔑

Keep an eye out for updates and new features, all inspired by you. We will add 25 credits to your balance after the administrators check the content of the feedback, but in the meantime, happy chatting! 🚀

Your opinion matters a lot to us! 💖
"""
    FEEDBACK_APPROVED = """
🌟 <b>Feedback received!</b> 🌟

As a token of appreciation, your balance has increased by 25 credits 🪙! Use them to access exclusive functions or replenish the number of generations in neural networks 💸

To use the bonus, enter the command /bonus and follow the instructions!
"""
    FEEDBACK_APPROVED_WITH_LIMIT_ERROR = """
🌟 <b>Feedback received!</b> 🌟

Thanks to your efforts, we will improve the boat! But, unfortunately, we cannot award you a reward, as the limit of rewards for feedback has been exceeded

Enter the /bonus command to learn about other ways to earn bonus credits. Keep sharing and enjoy every moment here! 🎉
"""
    FEEDBACK_DENIED = """
🌟 <b>Feedback received!</b> 🌟

Unfortunately, your feedback was not constructive enough and we cannot increase your bonus balance 😢

But don't worry! You can enter the command /bonus to see the other ways to top up the bonus balance!
"""

    # Profile
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
    UPLOAD_PHOTO = "Upload photo 📷"
    UPLOADING_PHOTO = "Uploading photo..."
    NO_FACE_IN_PHOTO = "I can't see a face in the photo. Please try another 📷"

    CHANGE_PHOTO = "Change photo 📷"
    CHANGE_PHOTO_SUCCESS = "📸 Photo successfully uploaded! 🌟"

    CHOOSE_GENDER = "Choose gender 🚹🚺"
    CHANGE_GENDER = "Change gender 🚹🚺"

    OPEN_BONUS_INFO = "🎁 Open bonus balance"
    OPEN_BUY_SUBSCRIPTIONS_INFO = "💎 Subscribe"
    OPEN_BUY_PACKAGES_INFO = "🛍 Purchase individual packages"
    CANCEL_SUBSCRIPTION = "❌ Cancel subscription"
    CANCEL_SUBSCRIPTION_CONFIRMATION = "❗Are you sure you want to cancel the subscription?"
    CANCEL_SUBSCRIPTION_SUCCESS = "💸 Subscription cancellation was successful!"
    NO_ACTIVE_SUBSCRIPTION = "💸 You don't have an active subscription"

    # Language
    LANGUAGE = "Language:"
    CHOOSE_LANGUAGE = "Selected language: English 🇺🇸"

    # Bonus
    BONUS_ACTIVATED_SUCCESSFUL = """
🌟 <b>Bonus activated!</b> 🌟

Congratulations! You've successfully used your bonus balance. Now, you can dive deeper into the world of artificial intelligence.

Start using your generations right now and discover new horizons with our neural networks! 🚀
"""
    BONUS_CHOOSE_PACKAGE = "Choose how to spend your earnings:"
    INVITE_FRIEND = "👥 Invite a friend"
    LEAVE_FEEDBACK = "📡 Leave a feedback"
    CASH_OUT = "🛍 Cash out credits"
    REFERRAL_SUCCESS = """
🌟 <b>Congratulations! Your referral magic worked!</b> 🌟

Thanks to you, a new user has joined us, and as a token of our appreciation, your and your friend's balance has been increased by 25 credits 🪙! Use them to access exclusive features or to add more generations in the neural networks 💸

To use the bonus, enter the /bonus command and follow the instructions. Let every invitation bring you not only the joy of communication but also pleasant bonuses!
"""
    REFERRAL_LIMIT_ERROR = """
🌟 <b>Congratulations! Your referral magic worked!</b> 🌟

Thanks to your efforts, a new user has joined us! Unfortunately, we cannot award you a reward, as the limit of rewards for inviting friends has been exceeded

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
But hey, don't lose heart! You can still explore our other magical offers with /buy or /bonus. There's always something exciting waiting for you in our AI wonderland! 🎩✨

Stay curious and let the AI adventure continue! 🌟🚀
"""
    PROMO_CODE_NOT_FOUND_ERROR = """
🔍 <b>Oops, promo code not found!</b>

It seems like the promo code you entered is playing hide and seek with us 🕵️‍♂️. We couldn't find it in our system 🤔
Double-check for any typos and give it another go. If it's still a no-show, maybe it's time to hunt for another code or check out our /buy options for some neat deals 🛍️

Keep your spirits high, and let's keep the AI fun rolling! 🚀🎈
"""
    PROMO_CODE_ALREADY_USED_ERROR = """
🚫 <b>Oops, déjà vu!</b>

Looks like you've already used this promo code. It's a one-time magic spell, and it seems you've already cast it! ✨🧙
No worries, though! You can check out our latest offers with /buy or /bonus. There's always a new trick up our AI sleeve! 🎉🔮

Keep exploring and let the AI surprises continue! 🤖
"""

    # AI
    MODE = """
To change a model click a button below 👇
"""
    CHOOSE_CHATGPT_MODEL = """
To choose a ChatGPT model click a button below 👇
"""
    CHOOSE_CLAUDE_MODEL = """
To choose a Claude model click a button below 👇
"""
    SWITCHED_TO_CHATGPT3_TURBO = """
🤖 <b>Welcome to the world of ChatGPT-3.5 Turbo!</b>

You've successfully switched to the <b>ChatGPT-3.5 Turbo</b> model. Consider this your personal virtual brain, ready to handle all your questions and ideas. Feel free to write anything - from simple queries to complex tasks. And don't worry, your previous conversations are stored in memory, so the context of your dialogue won't be lost

Go ahead, explore the capabilities of <b>ChatGPT-3.5 Turbo</b>! 🎉
"""
    SWITCHED_TO_CHATGPT4_TURBO = """
🚀 <b>Welcome to the world of ChatGPT-4.0 Turbo!</b>

Congratulations, you've switched to the <b>ChatGPT-4.0 Turbo</b> model. This is a real breakthrough in the world of neural networks! <b>ChatGPT-4.0 Turbo</b> offers deeper understanding and expanded capabilities compared to its predecessors. Discover new horizons of communication with AI. Your previous conversations are remembered, and the context history is preserved

Start your journey into the future with <b>ChatGPT-4.0 Turbo</b>! 🎉
"""
    SWITCHED_TO_CHATGPT4_OMNI = """
💥 <b>Welcome to a new era with ChatGPT-4.0 Omni!</b>

You have successfully switched to the <b>ChatGPT-4.0 Omni</b> model. This is the pinnacle of artificial intelligence innovation! <b>ChatGPT-4.0 Omni</b> surpasses previous models in depth of understanding and breadth of capabilities. Dive into an enhanced AI interaction experience. Your previous conversation history has been preserved, so we can pick up right where we left off.

Embark on an exciting journey with <b>ChatGPT-4.0 Omni</b>! 🎉
"""
    SWITCHED_TO_CLAUDE_3_SONNET = """
💫 <b>Welcome to the world of Claude 3 Sonnet!</b>

You have successfully switched to the <b>Claude 3 Sonnet</b> model. A master of balanced intelligence and speed! This model is perfectly suited for corporate tasks, combining quick responsiveness with deep analysis. Your experience will be enhanced by the preserved conversation history, allowing you to continue the dialogue without losing context.

Experience a new level of interaction with <b>Claude 3 Sonnet</b>! 🎉
"""
    SWITCHED_TO_CLAUDE_3_OPUS = """
🚀 <b>Welcome to the world of Claude 3 Opus!</b>

You have successfully switched to the <b>Claude 3 Opus</b> model. This is the peak of technological power for the most complex tasks! This model offers unprecedented depth of understanding and the ability to solve the most challenging problems. Your previous conversation history has been preserved, ensuring a seamless continuation of communication.

Prepare for an advanced experience with <b>Claude 3 Opus</b>! 🎉
"""
    SWITCHED_TO_DALL_E = """
🖼 <b>Welcome to the world of DALL-E!</b>

You've switched to the <b>DALL-E</b> model — your personal AI artist. Now, you can request to have any image drawn, whatever comes to your mind. Just describe your idea in a single message, and <b>DALL-E</b> will transform it into a visual masterpiece. Note: each new message is processed individually, previous request contexts are not considered

Time to create! 🎉
"""
    SWITCHED_TO_MIDJOURNEY = """
🎨 <b>Welcome to the world of Midjourney!</b>

You have successfully switched to the <b>Midjourney</b> model — this is your personal guide to the world of creative visualizations. Now you can instruct her to create any image that you can think of. Just describe your idea in one message, and <b>Midjourney</b> will bring it to life in a unique visual style. Please note that each of your requests is processed individually and is not related to the previous ones.

Time to create! 🎉
"""
    SWITCHED_TO_FACE_SWAP = """
🎭 <b>Welcome to the world of FaceSwap!</b>

You've switched to the <b>FaceSwap</b> model — where faces switch places as if by magic. Here, you can choose images from our unique packages or send your own photo. Want to see yourself in the guise of a celebrity or a movie character? Just select or send the desired image, and let <b>FaceSwap</b> work its magic

Your new face awaits! 🎉
"""
    SWITCHED_TO_MUSIC_GEN = """
🎵 <b>Welcome to the world of MusicGen!</b>

You've switched to the <b>MusicGen</b> model — a marvelous world where music is born before your eyes. Create a unique melody by sharing your mood or idea for a composition. From a classical symphony to a modern beat, <b>MusicGen</b> will help you turn your musical dreams into reality.

Let every note tell your story! 🎶
"""
    SWITCHED_TO_SUNO = """
🎸 <b>Welcome to the world of Suno!</b>

You've switched to the <b>Suno</b> model — your personal music producer. Here, you can turn your textual descriptions into full-fledged songs. Write a lyrics, specify your desired style, and <b>Suno</b> will craft a unique song for you. From soft ballads to dynamic hits, Suno has the ability to bring your musical vision to life.

It's time to express your emotions through music! 🎶
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

Your quota for the current model has just done a Houdini and disappeared! 🎩
But don't worry, you've got options:
- Check out /buy for more magical moments, or
- Invite your friends using /bonus command to get some bonuses, or
- Switch up the fun with a different AI model using /mode

The adventure continues! 🚀✨
"""
    IMAGE_SUCCESS = "✨ Here's your image creation! 🎨"

    # Examples
    CHATGPT4_OMNI_EXAMPLE = "👇 This is how *ChatGPT-4.0 Omni* would respond to your request 💥"
    CLAUDE_3_OPUS_EXAMPLE = "👇 This is how *Claude 3 Opus* would respond to your request 🚀"
    MIDJOURNEY_EXAMPLE = """
☝️ These are the images that <b>Midjourney</b> would draw for your request

To start drawing using <b>Midjourney</b>, just type the command /midjourney 🎨
"""
    SUNO_EXAMPLE = """
☝️ This is the song that <b>Suno</b> would create for your request

To start creating songs using <b>Suno</b>, just type the command /suno 🎸
"""

    PHOTO_FEATURE_FORBIDDEN = """
⚠️ Sending photos is only available in models: <b>ChatGPT-4.0</b> and <b>Claude 3</b>

Use /mode to switch to a model that supports image vision 👀
"""

    # Midjourney
    MIDJOURNEY_ALREADY_CHOSE_UPSCALE = "You've already chosen this image, try a new one 🙂"

    # Suno
    SUNO_INFO = """
🤖 <b>Choose the style for creating your song:</b>

🎹 In <b>simple mode</b>, you only need to describe the theme of the song and the genre
🎸 In <b>custom mode</b>, you have the opportunity to use your own lyrics and experiment with genres

<b>Suno</b> will create 2 tracks, up to 2 minutes each 🎧
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

To unlock the magic of voice-to-text, simply wave your wand with /buy or /bonus

Let's turn those voice messages into text and keep the conversation flowing! 🌟🔮
"""

    # Payment
    BUY = """
🚀 <b>Welcome to the wonder store!</b> 🛍

The gates to a world of exclusive opportunities are now open before you! What will it be today?

🌟 <b>Subscription: Your VIP pass to a world of opportunities!</b>
Gain full access to the entire spectrum of innovative services: from conversations with ChatGPT to creating unique songs with Suno. Use thematic chats to delve into topics of interest and expand your horizons every day. Discover the comfort of quick responses and the uniqueness of personalized images with FaceSwap. All this and much more are waiting for you in our subscriptions: <b>STANDARD</b> ✨, <b>VIP</b> 🔥, or <b>PREMIUM</b> 💎

🛍 <b>Packages: The perfect solution for specific needs!</b>
Looking for a targeted solution for a one-time project? Our Package provides the necessary number of requests and services to help you achieve your goals. Choose only what you need for your next creative breakthrough or business task, and pay only for the resources you use

Choose by clicking a button below 👇
"""
    CHANGE_CURRENCY = "💱 Change currency"
    YOOKASSA_PAYMENT_METHOD = "🪆💳 YooKassa"
    PAY_SELECTION_PAYMENT_METHOD = "🌍💳 PaySelection"
    TELEGRAM_STARS_PAYMENT_METHOD = "✈️⭐️ Telegram Stars"
    CHOOSE_PAYMENT_METHOD = """
<b>Choose a payment method:</b>

🪆💳 <b>YooKassa (Russian's Cards)</b>

🌍💳 <b>PaySelection (International Cards)</b>

✈️⭐️ <b>Telegram Stars (Currency in Telegram)</b>
"""
    PROCEED_TO_PAY = "🌐 Proceed to payment"

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

Hey there, AI enthusiast! 🌟
Your subscription has come to an end. But don't worry, the AI journey isn't over yet! 🚀
You can renew your magic pass with /buy or /bonus to keep exploring the AI universe or, if you prefer, take a peek for some tailor-made individual packages 🎁

The AI adventure awaits! Recharge, regroup, and let's continue this exciting journey together. 🤖✨
"""
    PACKAGES_END = """
🕒 <b>Your package or packages time is up!</b> ⌛

Oops, it looks like your fast messages (or voice messages, catalog access) package has run its course. But don't worry, new opportunities always await beyond the horizon!

🎁 Want to continue? Check out our offers or consider a subscription via /buy or /bonus. More exciting moments are ahead!

🚀 Ready for a fresh start? Rejoin and dive back into the world of amazing AI possibilities!
"""
    CHATS_RESET = """
🔄 <b>Chats updated!</b> 💬

Your chats have switched their unique roles to "Personal Assistant" as your access to the role catalog has ended. But don't worry, your AI helpers are still here to keep the conversation going!

🎁 Want your previous roles back? Visit /buy to purchase a new package or subscribe for unlimited access to the catalog.

🌟 Keep exploring! Your chats are always ready for new amazing conversations with AI.
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
    GPT3_REQUESTS = "✉️ ChatGPT-3.5 Turbo requests"
    GPT3_REQUESTS_DESCRIPTION = "Unleash the power of ChatGPT-3.5 Turbo for witty chats, smart advice, and endless fun! ✉️"
    GPT4_REQUESTS = "🧠 ChatGPT-4.0 Turbo requests"
    GPT4_REQUESTS_DESCRIPTION = "Experience ChatGPT-4.0 Turbo advanced intelligence for deeper insights and groundbreaking conversations 🧠"
    GPT4_OMNI_REQUESTS = "💥 ChatGPT-4.0 Omni requests"
    GPT4_OMNI_REQUESTS_DESCRIPTION = "Discover new horizons with the intelligence of ChatGPT-4.0 Omni for deeper analyses and innovative dialogues! 💥"
    CLAUDE_3_SONNET_REQUESTS = "💫 Claude 3 Sonnet requests"
    CLAUDE_3_SONNET_REQUESTS_DESCRIPTION = "Explore the balance of speed and intelligence with Claude 3 Sonnet for accurate and timely solutions! 💫"
    CLAUDE_3_OPUS_REQUESTS = "🚀 Claude 3 Opus requests"
    CLAUDE_3_OPUS_REQUESTS_DESCRIPTION = "Experience the power of Claude 3 Opus to solve the most complex challenges and create profound insights! 🚀"
    DALL_E_REQUESTS = "🖼 DALL-E images"
    DALL_E_REQUESTS_DESCRIPTION = "Turn ideas into art with DALL-E – where your imagination becomes stunning visual reality! 🖼"
    MIDJOURNEY_REQUESTS = "🎨 Midjourney images"
    MIDJOURNEY_REQUESTS_DESCRIPTION = "Unleash your creativity with Midjourney – transform your thoughts into magnificent visual works of art! 🎨"
    FACE_SWAP_REQUESTS = "📷 Images with face replacement"
    FACE_SWAP_REQUESTS_DESCRIPTION = "Enter the playful world of FaceSwap for laughs and surprises in every image! 😂🔄"
    MUSIC_GEN_REQUESTS = "🎵 Seconds of generation of melodies"
    MUSIC_GEN_REQUESTS_DESCRIPTION = "Discover a world where every prompt turns into a unique melody! 🎶"
    SUNO_REQUESTS = "🎸 Suno songs"
    SUNO_REQUESTS_DESCRIPTION = "Discover a world where every text you write is transformed into a unique song! 🎸"
    THEMATIC_CHATS = "💬 Thematic chats"
    THEMATIC_CHATS_DESCRIPTION = "Dive into topics you love with Thematic Chats, guided by AI in a world of tailored discussions 🗨️"
    ACCESS_TO_CATALOG = "🎭 Access to a roles catalog"
    ACCESS_TO_CATALOG_DESCRIPTION = "Unlock a universe of specialized AI assistants with access to our exclusive catalog, where every role is tailored to fit your unique needs and tasks"
    ANSWERS_AND_REQUESTS_WITH_VOICE_MESSAGES = "🎙 Answers and requests with voice messages"
    ANSWERS_AND_REQUESTS_WITH_VOICE_MESSAGES_DESCRIPTION = "Experience the ease and convenience of voice communication with our AI: Send and receive voice messages for a more dynamic and expressive interaction"
    FAST_ANSWERS = "⚡ Fast answers"
    FAST_ANSWERS_DESCRIPTION = "Quick Messages feature offers lightning-fast, accurate AI responses, ensuring you're always a step ahead in communication"
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
🎭 <b>Step right up to our role catalogue extravaganza!</b> 🌟

Ever dreamt of having an AI sidekick specialized just for you? Our catalog is like a magical wardrobe, each role a unique outfit tailored for your adventures in AI land! 🧙‍♂️✨
Choose from an array of AI personas, each with its own flair and expertise. Whether you need a brainstorm buddy, a creative muse, or a factual wizard, we've got them all!

👉 Ready to meet your match? Just hit the button below and let the magic begin! 🎩👇
"""
    CATALOG_FORBIDDEN_ERROR = """
🔒 <b>Whoops! Looks like you've hit a VIP-only zone!</b> 🌟

You're just a click away from unlocking our treasure trove of AI roles, but it seems you don't have the golden key yet. No worries, though! You can grab it easily.
🚀 Head over to /buy for some fantastic subscription options, or check out individual packages if you're in the mood for some a la carte AI delights.

Once you're all set up, our catalog of AI wonders will be waiting for you – your ticket to an extraordinary world of AI possibilities! 🎫✨
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

Head over to /buy or /bonus to unlock the power of multiple chats. More chats, more fun! 🎉
"""
    CREATE_CHAT_SUCCESS = "💬 Chat created! 🎉\n👌 Don't forget to switch to a new one using /chats"
    TYPE_CHAT_NAME = "Type your chat name"
    SWITCH_CHAT = "Switch between chats 🔄"
    SWITCH_CHAT_FORBIDDEN = """
"🔄 <b>Switching gears? Hold that thought!</b> ⚙️

You're currently in your one and only chat universe. It's a cozy place, but why not expand your horizons? 🌌

To hop between multiple thematic chats, just get your pass from /buy or /bonus. Let the chat-hopping begin! 🐇
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

This is your sole chat kingdom, and a kingdom needs its king or queen! Deleting it would be like canceling your own party. 🎈

How about adding more chats to your realm instead? Check out /buy or /bonus to build your chat empire! 👑
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
- 📷 Send us photos with faces for face swapping in FaceSwap!
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
    FACE_SWAP_NO_FACE_FOUND_ERROR = """
🚫 <b>Problem with Photo Processing</b>

Unfortunately, we were unable to clearly identify a face in the photo from your /profile
Please upload a new photo where your face is clearly visible and in good quality via the /profile command.

🔄 After uploading a new photo, please try again. Thank you for your patience!
"""

    ERROR = """
I've got an unknown error 🤒

Please try again or contact our tech support:
"""
    NETWORK_ERROR = """
I lost my connection with Telegram 🤒

Please try again 🥺
"""
    CONNECTION_ERROR = """
I lost my connection with my database 🤒

Please try again 🥺
"""
    TECH_SUPPORT = "👨‍💻 Tech Support"
    BACK = "Back ◀️"
    CLOSE = "Close 🚪"
    CANCEL = "Cancel ❌"
    APPROVE = "Approve ✅"
    AUDIO = "Audio 🔈"
    VIDEO = "Video 📹"
    SKIP = "Skip ⏩️"

    EXCEED_NOTIFY_PURCHASE = "😕 Sorry, but to make a purchase, its total amount must exceed 100 rubles/1 dollar/100 Telegram Stars"
    EXCEED_NOTIFY_BASKET = "😕 Sorry, but to make a purchase, the total amount of the basket must exceed 100 rubles/1 dollar/100 Telegram Stars"

    TERMS_LINK = "https://telegra.ph/Terms-of-Service-in-GPTsTurboBot-05-07"

    @staticmethod
    def profile(
        subscription_type,
        subscription_status,
        gender,
        current_model,
        current_model_version,
        monthly_limits,
        additional_usage_quota,
        renewal_date,
        credits,
    ) -> str:
        emojis = Subscription.get_emojis()

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

        if current_model == Model.CHAT_GPT and current_model_version == ChatGPTVersion.V3_Turbo:
            current_model = English.CHATGPT3_TURBO
        elif current_model == Model.CHAT_GPT and current_model_version == ChatGPTVersion.V4_Turbo:
            current_model = English.CHATGPT4_TURBO
        elif current_model == Model.CHAT_GPT and current_model_version == ChatGPTVersion.V4_Omni:
            current_model = English.CHATGPT4_OMNI
        elif current_model == Model.CLAUDE and current_model_version == ClaudeGPTVersion.V3_Sonnet:
            current_model = English.CLAUDE_3_SONNET
        elif current_model == Model.CLAUDE and current_model_version == ClaudeGPTVersion.V3_Opus:
            current_model = English.CLAUDE_3_OPUS
        elif current_model == Model.DALL_E:
            current_model = English.DALL_E
        elif current_model == Model.MIDJOURNEY:
            current_model = English.MIDJOURNEY
        elif current_model == Model.FACE_SWAP:
            current_model = English.FACE_SWAP
        elif current_model == Model.MUSIC_GEN:
            current_model = English.MUSIC_GEN
        elif current_model == Model.SUNO:
            current_model = English.SUNO

        return f"""
<b>Profile</b> 👤

---------------------------

🤖 <b>Current model: {current_model}</b>
{gender_info}

---------------------------

{emojis[subscription_type]} <b>Subscription type:</b> {subscription_type}
🗓 <b>Subscription renewal date:</b> {renewal_date}
{subscription_info}

---------------------------

Quota:
━ ✉️ <b>ChatGPT-3.5 Turbo</b>:
    ┣ {monthly_limits[Quota.CHAT_GPT3_TURBO]}/{SubscriptionLimit.LIMITS[subscription_type][Quota.CHAT_GPT3_TURBO]}
    ┗ Additional: {additional_usage_quota[Quota.CHAT_GPT3_TURBO]}
━ 🧠 <b>ChatGPT-4.0 Turbo</b>:
    ┣ {monthly_limits[Quota.CHAT_GPT4_TURBO]}/{SubscriptionLimit.LIMITS[subscription_type][Quota.CHAT_GPT4_TURBO]}
    ┗ Additional: {additional_usage_quota[Quota.CHAT_GPT4_TURBO]}
━ 💥 <b>ChatGPT-4.0 Omni</b>:
    ┣ {monthly_limits[Quota.CHAT_GPT4_OMNI]}/{SubscriptionLimit.LIMITS[subscription_type][Quota.CHAT_GPT4_OMNI]}
    ┗ Additional: {additional_usage_quota[Quota.CHAT_GPT4_OMNI]}
━ 💫 <b>Claude 3 Sonnet</b>:
    ┣ {monthly_limits[Quota.CLAUDE_3_SONNET]}/{SubscriptionLimit.LIMITS[subscription_type][Quota.CLAUDE_3_SONNET]}
    ┗ Additional: {additional_usage_quota[Quota.CLAUDE_3_SONNET]}
━ 🚀 <b>Claude 3 Opus</b>:
    ┣ {monthly_limits[Quota.CLAUDE_3_OPUS]}/{SubscriptionLimit.LIMITS[subscription_type][Quota.CLAUDE_3_OPUS]}
    ┗ Additional: {additional_usage_quota[Quota.CLAUDE_3_OPUS]}
━ 🖼 <b>DALL-E</b>:
    ┣ {monthly_limits[Quota.DALL_E]}/{SubscriptionLimit.LIMITS[subscription_type][Quota.DALL_E]}
    ┗ Additional: {additional_usage_quota[Quota.DALL_E]}
━ 🎨 <b>Midjourney</b>:
    ┣ {monthly_limits[Quota.MIDJOURNEY]}/{SubscriptionLimit.LIMITS[subscription_type][Quota.MIDJOURNEY]}
    ┗ Additional: {additional_usage_quota[Quota.MIDJOURNEY]}
━ 📷 <b>FaceSwap</b>:
    ┣ {monthly_limits[Quota.FACE_SWAP]}/{SubscriptionLimit.LIMITS[subscription_type][Quota.FACE_SWAP]}
    ┗ Additional: {additional_usage_quota[Quota.FACE_SWAP]}
━ 🎵 <b>MusicGen</b>:
    ┣ {monthly_limits[Quota.MUSIC_GEN]}/{SubscriptionLimit.LIMITS[subscription_type][Quota.MUSIC_GEN]}
    ┗ Additional: {additional_usage_quota[Quota.MUSIC_GEN]}
━ 🎸 <b>Suno</b>:
    ┣ {monthly_limits[Quota.SUNO]}/{SubscriptionLimit.LIMITS[subscription_type][Quota.SUNO]}
    ┗ Additional: {additional_usage_quota[Quota.SUNO]}
━ 💬 <b>Thematic chats</b>: {additional_usage_quota[Quota.ADDITIONAL_CHATS]}
━ 🎭 <b>Access to a catalog with digital employees</b>: {'Yes' if additional_usage_quota[Quota.ACCESS_TO_CATALOG] else 'No'}
━ 🎙 <b>Voice messages</b>: {'Yes' if additional_usage_quota[Quota.VOICE_MESSAGES] else 'No'}
━ ⚡ <b>Fast answers</b>: {'Yes' if additional_usage_quota[Quota.FAST_MESSAGES] else 'No'}

---------------------------

🪙 <b>Quantity of bonus credits:</b> {credits}
"""

    # Payment
    @staticmethod
    def payment_description_subscription(user_id: str, subscription_type: SubscriptionType):
        return f"Paying a subscription {subscription_type} for user: {user_id}"

    @staticmethod
    def payment_description_renew_subscription(user_id: str, subscription_type: SubscriptionType):
        return f"Renewing a subscription {subscription_type} for user: {user_id}"

    @staticmethod
    def subscribe(currency: Currency, min_prices: Dict):
        return f"""
🤖 Ready to supercharge your digital journey? Here's what's on the menu:

- <b>STANDARD</b> ⭐: {min_prices[SubscriptionType.STANDARD]}{Currency.SYMBOLS[currency]}/month
- <b>VIP</b> 🔥: {min_prices[SubscriptionType.VIP]}{Currency.SYMBOLS[currency]}/month
- <b>PREMIUM</b> 💎: {min_prices[SubscriptionType.PREMIUM]}{Currency.SYMBOLS[currency]}/month

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
            SubscriptionPeriod.MONTHS12: English.MONTHS_12,
        }

    @staticmethod
    def confirmation_subscribe(subscription_type: SubscriptionType, currency: Currency, price: float):
        if currency == Currency.XTR:
            return f"You're about to activate subscription {subscription_type} {Subscription.get_emojis()[subscription_type]} for {price}{Currency.SYMBOLS[currency]}"
        return f"""
You're about to activate subscription {subscription_type} {Subscription.get_emojis()[subscription_type]} for {price}{Currency.SYMBOLS[currency]}/month

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
    def package(currency: Currency, page: int):
        if currency == Currency.USD:
            balance = f"{Currency.SYMBOLS[currency]}0.01"
        else:
            balance = f"1{Currency.SYMBOLS[currency]}"

        if page == 0:
            description = (
                "🧠 <b>ChatGPT</b>: Engage in deep, thought-provoking conversations!\n\n"
                "🚀 <b>Claude</b>: Engage in dialogues that expand the horizons of thinking!\n\n"
                "💬 <b>Thematic Chats</b>: Dive into specialized topics and explore dedicated chat realms\n\n"
                "🎭 <b>Role Catalog Access</b>: Need a specific assistant? Browse our collection and find your perfect AI match"
            )
        elif page == 1:
            description = (
                "🖼 <b>DALL-E</b>: Transform ideas into stunning visuals!\n\n"
                "🎨 <b>Midjourney</b>: Turn ideas into incredible realistic images!\n\n"
                "👤 <b>FaceSwap</b>: Play with identities in images!"
            )
        elif page == 2:
            description = (
                "🎵 <b>Harmony with MusicGen</b>: Create unique melodies that will belong only to you!\n\n"
                "🎸 <b>Creative with Suno</b>: Create original songs with your own lyrics in different genres!"
            )
        elif page == 3:
            description = (
                "🗣️ <b>Voice Messages</b>: Say it out loud! Chatting with AI has never sounded better\n\n"
                "⚡ <b>Quick Messages</b>: Fast, efficient, and always on point. AI communication at lightning speed"
            )
        else:
            description = ""

        return f"""
🤖 <b>Welcome to the AI shopping spree!</b> 📦

🪙 <b>1 credit = {balance}</b>

Each button tap unlocks a world of AI wonders:
{description}

Hit a button and choose a package:
"""

    @staticmethod
    def get_package_name_and_quantity_by_package_type(package_type: PackageType):
        name = ""
        quantity = ""
        if package_type == PackageType.CHAT_GPT3_TURBO:
            name = English.GPT3_REQUESTS
            quantity = "requests"
        elif package_type == PackageType.CHAT_GPT4_TURBO:
            name = English.GPT4_REQUESTS
            quantity = "requests"
        elif package_type == PackageType.CHAT_GPT4_OMNI:
            name = English.GPT4_OMNI_REQUESTS
            quantity = "requests"
        elif package_type == PackageType.CLAUDE_3_SONNET:
            name = English.CLAUDE_3_SONNET_REQUESTS
            quantity = "requests"
        elif package_type == PackageType.CLAUDE_3_OPUS:
            name = English.CLAUDE_3_OPUS_REQUESTS
            quantity = "requests"
        elif package_type == PackageType.DALL_E:
            name = English.DALL_E_REQUESTS
            quantity = "images"
        elif package_type == PackageType.MIDJOURNEY:
            name = English.MIDJOURNEY_REQUESTS
            quantity = "images"
        elif package_type == PackageType.FACE_SWAP:
            name = English.FACE_SWAP_REQUESTS
            quantity = "generations"
        elif package_type == PackageType.MUSIC_GEN:
            name = English.MUSIC_GEN_REQUESTS
            quantity = "seconds"
        elif package_type == PackageType.SUNO:
            name = English.SUNO_REQUESTS
            quantity = "songs"
        elif package_type == PackageType.CHAT:
            name = English.THEMATIC_CHATS
            quantity = "chats"
        elif package_type == PackageType.ACCESS_TO_CATALOG:
            name = English.ACCESS_TO_CATALOG
            quantity = "months"
        elif package_type == PackageType.VOICE_MESSAGES:
            name = English.ANSWERS_AND_REQUESTS_WITH_VOICE_MESSAGES
            quantity = "months"
        elif package_type == PackageType.FAST_MESSAGES:
            name = English.FAST_ANSWERS
            quantity = "months"
        return name, quantity

    @staticmethod
    def choose_min(package_type: PackageType):
        name, quantity = English.get_package_name_and_quantity_by_package_type(package_type)

        return f"""
🚀 Fantastic!

You've selected the <b>{name}</b> package

🌟 Please <b>type in the number of {quantity}</b> you'd like to go for
"""

    @staticmethod
    def shopping_cart(currency: Currency, cart_items: List[Dict], discount: int):
        text = ""
        total_sum = 0.0
        for index, cart_item in enumerate(cart_items):
            package_type, package_quantity = cart_item.get("package_type", None), cart_item.get("quantity", 0)

            name, quantity = English.get_package_name_and_quantity_by_package_type(package_type)

            text += f"{index + 1}. {name} ({package_quantity} {quantity})\n"
            total_sum += Package.get_price(currency, package_type, package_quantity, discount)

        if currency == Currency.USD:
            total_sum = f"{Currency.SYMBOLS[currency]}{total_sum}"
        else:
            total_sum = f"{total_sum}{Currency.SYMBOLS[currency]}"

        if not text:
            text = "Your cart is empty"

        return f"""
🛒 <b>Cart</b>

{text}

💳 Total: {total_sum}
"""

    @staticmethod
    def confirmation_package(package_name: str, package_quantity: int, currency: Currency, price: float) -> str:
        return f"You're about to buy {package_quantity} package(-s) <b>{package_name}</b> for {price}{Currency.SYMBOLS[currency]}"

    @staticmethod
    def confirmation_cart(cart_items: List[Dict], currency: Currency, price: float) -> str:
        text = ""
        for index, cart_item in enumerate(cart_items):
            package_type, package_quantity = cart_item.get("package_type", None), cart_item.get("quantity", 0)

            name, quantity = English.get_package_name_and_quantity_by_package_type(package_type)

            text += f"{index + 1}. {name} ({package_quantity} {quantity})\n"

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
    def switched(model: Model, model_version: str):
        if model == Model.CHAT_GPT and model_version == ChatGPTVersion.V3_Turbo:
            return English.SWITCHED_TO_CHATGPT3_TURBO
        elif model == Model.CHAT_GPT and model_version == ChatGPTVersion.V4_Turbo:
            return English.SWITCHED_TO_CHATGPT4_TURBO
        elif model == Model.CHAT_GPT and model_version == ChatGPTVersion.V4_Omni:
            return English.SWITCHED_TO_CHATGPT4_OMNI
        elif model == Model.CLAUDE and model_version == ClaudeGPTVersion.V3_Sonnet:
            return English.SWITCHED_TO_CLAUDE_3_SONNET
        elif model == Model.CLAUDE and model_version == ClaudeGPTVersion.V3_Opus:
            return English.SWITCHED_TO_CLAUDE_3_OPUS
        elif model == Model.DALL_E:
            return English.SWITCHED_TO_DALL_E
        elif model == Model.MIDJOURNEY:
            return English.SWITCHED_TO_MIDJOURNEY
        elif model == Model.FACE_SWAP:
            return English.SWITCHED_TO_FACE_SWAP
        elif model == Model.MUSIC_GEN:
            return English.SWITCHED_TO_MUSIC_GEN
        elif model == Model.SUNO:
            return English.SWITCHED_TO_SUNO

    @staticmethod
    def requests_recommendations() -> List[str]:
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
    def image_recommendations() -> List[str]:
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
    def music_recommendations() -> List[str]:
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
            "Embarking on a galactic journey of face swapping... 🌌👽"
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

    # Settings
    @staticmethod
    def settings(human_model: str, current_model: Model, dall_e_cost=1) -> str:
        if current_model == Model.CHAT_GPT:
            additional_text = f"\n<b>Version ChatGPT-3.5</b>: {ChatGPTVersion.V3_Turbo}\n<b>Version ChatGPT-4.0</b>: {ChatGPTVersion.V4_Turbo}\n<b>Version ChatGPT-4.0 Omni</b>: {ChatGPTVersion.V4_Omni}"
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
    def bonus(user_id: str, balance: float, referred_count: int, feedback_count: int) -> str:
        return f"""
🎁 <b>Your bonus balance</b>

💰 Current balance: {float(balance)}

To top up your bonus balance, you can:
1️⃣ Invite friends:
    - 💸 For each invited user, you and the invited user will get 25 credits each 🪙
    - 🌟 Your personal referral link for invitations: {Texts.referral_link(user_id, False)}
    - 👤 You've invited: {referred_count}
2️⃣ Leave feedback:
    - 💸 For each constructive feedback, you get 25 credits 🪙
    - 📡 To leave feedback, enter the command /feedback
    - 💭 You've left: {feedback_count}

Choose how to spend your earnings:
"""
