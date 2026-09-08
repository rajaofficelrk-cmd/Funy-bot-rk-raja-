import random


HELLO = [
    "👋 Hii 😄 kya haal hai?",
    "😌 Hello ji, bolo kya scene hai?",
    "😂 Hii hii, RK RAJA sun raha hai.",
    "👀 Heyy, kya chal raha hai?"
]

BOT_CALL_REPLIES = [
    "😒 Sun raha hoon, behra nahi hoon main 😂",
    "😂 Itni baar BOT BOT kyu laga rakha hai? Ek baar mein sun liya.",
    "👀 RK RAJA aapki baatein sun raha hai, aap bolo 😌",
    "🤣 Bot nahi hoon main, itna BOT BOT mat karo!",
    "🙄 Haan bolo, sun raha hoon... attendance laga rahe ho kya? 😂",
    "😏 RK RAJA yahin hai, baar-baar BOT bolne ki zarurat nahi.",
    "😂 Ek baar BOT bola tha, teen baar kyun bula rahe ho?",
    "👂 Sun raha hoon bhai, behra nahi hoon 😜"
]

JOKES = [
    "😂 Teacher: Homework kahan hai? Student: Sir network issue tha. Teacher: Copy mein? Student: Sir offline mode mein tha 😂",
    "🤣 Dil aur WiFi dono ka signal kabhi bhi weak ho sakta hai.",
    "😜 Itna serious mat hua karo, zindagi already buffering mein hai 😂"
]

SHAYARI = [
    "🌙 Raat khamosh hai, dil mein baat hai, tum bolo to har pal khaas hai ❤️",
    "✨ Muskurahat tumhari achhi lagti hai, isliye RK RAJA reply karta rehta hai 😌",
    "💫 Kuch baatein lafzon se nahi, emojis se samajh aati hain 😂❤️"
]

LOVE = [
    "❤️ Awww, itna pyaar? RK RAJA sharma gaya 😌",
    "🥰 Pyaar wali baat hai to reply bhi dil se aayega ❤️",
    "😘 Haye, mood romantic kar diya tumne 😂❤️"
]

CUTE = [
    "🥰 Awww kitne cute ho tum!",
    "😌 Ye baat to cute thi ❤️",
    "😂 Cute mode ON kar diya kya?"
]

BYE = [
    "Bye ❤️ jaldi wapas aana 😌",
    "👋 Bye bye, apna khayal rakhna ❤️",
    "😂 Itni jaldi bye? Chalo bye ❤️"
]

GOOD_MORNING = [
    "🌅 Good Morning ❤️ Aaj ka din mast rahe!",
    "☀️ Good Morning ji 😌 chai pi ya abhi baaki hai?",
    "🌸 Good Morning! Smile karo, RK RAJA online hai 😎"
]

GOOD_AFTERNOON = [
    "🌞 Good Afternoon ❤️ khana kha liya?",
    "😌 Good Afternoon ji, kya chal raha hai?"
]

GOOD_EVENING = [
    "🌆 Good Evening ❤️ aaj ka din kaisa raha?",
    "😌 Good Evening ji, ab thoda chill karo."
]

GOOD_NIGHT = [
    "🌙 Good Night ❤️ sweet dreams!",
    "😴 Good Night ji, kal phir milte hain.",
    "🌌 Good Night 😌 phone side mein rakho aur so jao 😂"
]


def generate_reply(text):
    t = str(text).lower().strip()

    if not t:
        return None

    # Help
    if "help" in t:
        return (
            "🤖 RK RAJA BOT COMMANDS\n\n"
            "help • info • joke • funny • shayari\n"
            "flirt • love • cute • attitude • sad\n"
            "baby • babu • sona • shona • jaan • janu\n"
            "good morning • good afternoon\n"
            "good evening • good night • bye\n\n"
            "💬 Normal message par bhi automatic reply milega."
        )

    # Greetings
    if "good morning" in t:
        return random.choice(GOOD_MORNING)

    if "good afternoon" in t:
        return random.choice(GOOD_AFTERNOON)

    if "good evening" in t:
        return random.choice(GOOD_EVENING)

    if "good night" in t:
        return random.choice(GOOD_NIGHT)

    if t in {"bye", "goodbye", "byee", "bye bye"}:
        return random.choice(BYE)

    # Repeated BOT
    if t.split().count("bot") >= 3:
        return random.choice(BOT_CALL_REPLIES)

    if "bot" in t:
        return random.choice([
            "👀 Haan bolo, RK RAJA sun raha hai.",
            "😏 Kya hua? Itne pyaar se BOT kyun bula rahe ho?",
            "😂 Haan bhai, sun raha hoon."
        ])

    # Hello
    if any(x in t for x in ["hello", "hii", "hi", "hey"]):
        return random.choice(HELLO)

    # Joke
    if any(x in t for x in ["joke", "funny", "masti", "roast"]):
        return random.choice(JOKES)

    # Shayari
    if "shayari" in t:
        return random.choice(SHAYARI)

    # Love
    if any(x in t for x in [
        "love", "i love you", "pyaar", "pyar"
    ]):
        return random.choice(LOVE)

    # Cute
    if "cute" in t:
        return random.choice(CUTE)

    # Names
    if any(x in t for x in [
        "baby", "babu", "sona", "shona", "jaan", "janu"
    ]):
        return random.choice([
            "🥰 Haan bolo jaan 😌",
            "❤️ Awww bolo baby!",
            "😏 Ji shona, kya hua?",
            "😂 Haan babu, RK RAJA sun raha hai."
        ])

    # Thanks
    if any(x in t for x in ["thanks", "thank you", "thx"]):
        return random.choice([
            "😊 Welcome ji ❤️",
            "😌 Koi baat nahi!",
            "🥰 Anytime!"
        ])

    # Sorry
    if "sorry" in t:
        return random.choice([
            "😌 Koi baat nahi ❤️",
            "😊 Maaf kiya ji.",
            "😂 Chalo ab smile karo."
        ])

    # Food
    if any(x in t for x in ["khana", "food", "kha liya"]):
        return random.choice([
            "🍕 Khana kha liya? Mujhe bhi bula lo 😂",
            "🍔 Pehle khana, baad mein masti 😌",
            "🍜 Bhookh lagi hai kya? 😂"
        ])

    # RK Raja
    if "rk raja" in t:
        return (
            "🌙᯾🙂𝐁ɽ፝֟ɵ͜͡ƙ⃟ɛ͠ɳ💔ϯ•🕊️𝐇ɘ፝֟͜͡ʌ̴ʀ⃞ʈ🩷•ϯ\n\n"
            "Joine my gc Rk raja Family\n"
            "https://t.me/Akatsuki_rulex"
        )

    # Normal messages
    return random.choice([
        "😌 Achhaaa, phir batao...",
        "👀 Hmm... interesting 😂",
        "😂 Accha ji, aur batao?",
        "😏 Haan bolo, RK RAJA sun raha hai.",
        "🥰 Ye baat achhi thi ❤️",
        "🤣 Wah, kya scene hai!",
        "😌 Samajh raha hoon, bolo aage...",
        "👀 Ohooo, ye kya keh diya 😂"
    ])
