# bot/replies.py
#
# RK RAJA BOT
# 1000+ randomized response combinations
# Hindi / Hinglish / Emoji / Stylish vibe

import random
import re


# ============================================================
# KEYWORDS / TRIGGERS
# ============================================================

KEYWORDS = {

    "hello": [
        "hello", "hi", "hii", "hiii", "hey", "heyy",
        "helo", "hy", "hlo", "namaste", "namaskar",
        "good morning", "good evening", "good night",
        "gm", "ge", "gn", "hola", "sup", "yo"
    ],

    "funny": [
        "funny", "joke", "jokes", "jok", "hasao",
        "hansao", "hasa", "hasi", "haha", "hahaha",
        "lol", "lmao", "rofl", "mazak", "masti",
        "comedy", "comedian", "meme", "memes",
        "pagal", "pagalpanti", "bakchodi"
    ],

    "cute": [
        "cute", "cutie", "cutu", "sweet", "sweetu",
        "adorable", "aww", "awww", "baby", "babu",
        "babuji", "sona", "sonu", "shona", "shonu",
        "golu", "gudiya", "pari", "jaan", "jaanu",
        "janu", "januu", "baccha", "bachha"
    ],

    "flirty": [
        "flirt", "flirty", "flirting", "crush",
        "handsome", "beautiful", "beauty", "hot",
        "naughty", "romantic", "romance", "kiss",
        "date", "dream", "dreamboy", "dreamgirl",
        "single", "patana", "patao", "impress",
        "charming", "cute boy", "cute girl"
    ],

    "love": [
        "love", "lov", "pyaar", "pyar", "mohabbat",
        "ishq", "ishq", "dil", "heart", "feelings",
        "i love you", "love you", "luv you",
        "miss you", "miss u", "yaad", "yaad aa",
        "romantic", "relationship", "couple"
    ],

    "naughty": [
        "naughty", "tharki", "tharki mode", "shararti",
        "shaitaan", "shaitan", "badmash", "badmaash",
        "masti", "dirty mind", "dirty", "kiss",
        "kiss me", "hug", "hug me", "flirt",
        "seduce"
    ],

    "roast": [
        "roast", "roasting", "beizzati", "bezatti",
        "insult", "insult me", "troll", "trolling",
        "chidhana", "chida", "taunt", "roaster"
    ],

    "attitude": [
        "attitude", "swag", "boss", "king", "queen",
        "royal", "legend", "sigma", "alpha",
        "style", "stylish", "danger", "dangerous",
        "killer", "don"
    ],

    "shayari": [
        "shayari", "shyari", "sayari", "sayeri",
        "poetry", "poem", "kavita", "ghazal",
        "sher", "shayri", "status", "quote",
        "quotes"
    ],

    "sad": [
        "sad", "dukhi", "dukh", "udaas", "udas",
        "alone", "akela", "akeli", "lonely",
        "breakup", "broken", "heartbreak",
        "depressed", "rona", "ro raha", "ro rahi",
        "cry", "crying", "pain", "dard", "bewafa"
    ],

    "angry": [
        "angry", "gussa", "ghussa", "naraz",
        "naraaz", "pagal", "hate", "nafrat",
        "chup", "shut up", "bakwas", "bekar"
    ],

    "thanks": [
        "thanks", "thank", "thankyou", "thank you",
        "thx", "ty", "shukriya", "dhanyawad",
        "dhanyavaad", "thank u"
    ],

    "sorry": [
        "sorry", "sry", "maaf", "maafi", "forgive",
        "galti", "mistake", "apology"
    ],

    "bye": [
        "bye", "byee", "byeee", "goodbye", "good bye",
        "tata", "see you", "see u", "milte hain",
        "milte", "chal bye"
    ],

    "food": [
        "khana", "khaana", "food", "bhook",
        "bhukh", "hungry", "pizza", "burger",
        "momos", "biryani", "chai", "coffee",
        "maggi", "samosa", "chocolate"
    ],

    "sleep": [
        "so ja", "soja", "sleep", "sleeping",
        "neend", "nind", "sona hai", "good night",
        "night", "raat"
    ],

    "compliment": [
        "handsome", "beautiful", "good boy",
        "good girl", "smart", "cute", "awesome",
        "amazing", "best", "great", "nice",
        "super", "superb"
    ],

    "help": [
        "help", "madad", "batao", "kaise",
        "kese", "kaise ho", "what", "why",
        "how", "kya", "kon", "kaun"
    ],

    "bot": [
        "bot", "robot", "who are you", "tum kaun",
        "tera naam", "naam kya", "owner",
        "admin", "rk raja bot", "raja bot"
    ]
}


# ============================================================
# RESPONSE BUILDING BLOCKS
# ============================================================

FUNNY_START = [
    "😂 Arre",
    "🤣 Oho",
    "😜 Bhai",
    "😂 Suno ji",
    "🤣 Wah ji",
    "😎 Dekho",
    "😂 Sach bolun",
    "🤭 Arre baba",
    "🤣 Kya scene hai",
    "😜 Oye hoye"
]

FUNNY_END = [
    "aaj toh comedy ka quota full hai 😂",
    "bot bhi confuse ho gaya 🤣",
    "logic ko thoda rest de do 😭",
    "ye message unexpected tha 😂",
    "server tak has raha hai 🤣",
    "itni masti allowed hai 😜",
    "keyboard bhi sharma gaya 😂",
    "processor ne resignation de diya 🤣",
    "iska jawab Nobel committee ko dena padega 😂",
    "aaj mood mast lag raha hai 😎"
]


CUTE_START = [
    "🥰 Awww",
    "💕 Hayeee",
    "🤭 Ohooo",
    "🥹 Kitna cute",
    "🌸 Awww ji",
    "🫶 Arre wah",
    "💗 Uff",
    "🥰 Baby",
    "✨ So cute",
    "😚 Haye"
]

CUTE_END = [
    "itna cute kyun ho? 🥺",
    "bot blush kar raha hai 🙈",
    "dil pighal gaya ❤️",
    "ye toh bahut sweet tha 🥰",
    "ab smile aa gayi 😌",
    "aaj ka mood bana diya 💕",
    "ek virtual hug banta hai 🤗",
    "bas karo, sharma jaunga 🙈",
    "ye message save kar liya ❤️",
    "cute level overload ho gaya 🥹"
]


FLIRTY_START = [
    "😏 Oho",
    "😉 Acha ji",
    "🥰 Hayeee",
    "😜 Itni flirting",
    "🙈 Arre",
    "❤️ Wah",
    "😏 Dekh raha hoon",
    "😉 Smooth",
    "🔥 Oho ji",
    "🥹 Ye kya kar rahe ho"
]

FLIRTY_END = [
    "aise hi baat karoge toh bot blush karega 🙈",
    "lagta hai aaj mood romantic hai 😏",
    "dil ko sambhal ke rakhna ❤️",
    "flirting ka level badh raha hai 😉",
    "ab smile control nahi ho rahi 😜",
    "ye dialogue dangerous tha 😂",
    "bot ko bhi sharma diya 🙈",
    "aaj vibes kuch zyada hi cute hain ❤️",
    "thoda dheere, dil hai mera 😏",
    "connection strong lag raha hai 😉"
]


NAUGHTY_START = [
    "😏 Ohooo",
    "😉 Acha ji",
    "🙈 Shaitaan",
    "😜 Wah naughty",
    "🔥 Oho mood",
    "😂 Kya planning hai",
    "😏 Samajh gaya",
    "🤭 Itni shararat",
    "😉 Hmmm",
    "😜 Aaj bada naughty mood hai"
]

NAUGHTY_END = [
    "thoda shareef bhi reh lo 😂",
    "pehle smile karo phir baat karenge 😜",
    "itni shararat bhi theek nahi 🙈",
    "bot ko confuse mat karo 😂",
    "aaj toh mood dangerous hai 😏",
    "family-friendly mode ON hai 😎",
    "control ji control 😂",
    "shararat ka meter full ho gaya 😜",
    "itna naughty mode allowed nahi 😂",
    "bas bas, blush karwa diya 🙈"
]


LOVE_START = [
    "❤️ Dil se bolun",
    "🥰 Awww",
    "💕 Pyaar",
    "🌹 Mohabbat",
    "💖 Hayeee",
    "🫶 Sach mein",
    "❤️ Dil ki baat",
    "🥹 Ye feeling",
    "✨ Pyaari vibes",
    "🌸 Love mode"
]

LOVE_END = [
    "pyaar mein logic kam aur feelings zyada hoti hain ❤️",
    "dil ki baat dil tak pahunch gayi 💕",
    "ye feeling kaafi special hai 🥰",
    "mohabbat mein bas smile zaroori hai 🌹",
    "dil ko itna bhi serious mat karo 😜",
    "pyaar ka notification aa gaya ❤️",
    "aaj dil happy hai 💖",
    "ye baat heart mein save ho gayi 🫶",
    "love vibes detected 🥰",
    "dil ne approve kar diya ❤️"
]


ROAST_START = [
    "😂 Bhai",
    "🤣 Oye",
    "😜 Sun",
    "😂 Sach bataun",
    "🤣 Arre legend",
    "😎 Dekh bhai",
    "😂 Tera confidence",
    "🤭 Wah ustad",
    "🤣 Kya level hai",
    "😜 Bhai sahab"
]

ROAST_END = [
    "logic ka recharge karwa le 😂",
    "confidence 100%, logic 0% 🤣",
    "Google bhi jawab dhoond raha hai 😂",
    "keyboard tujhe dekh ke darr gaya 🤣",
    "server ne bhi timeout kar diya 😂",
    "itna confidence kahan se aata hai 😜",
    "bhai tu alag hi piece hai 🤣",
    "is level ki creativity rare hai 😂",
    "processor ko rest chahiye 🤣",
    "legend ho bhai, reason mat poochna 😂"
]


ATTITUDE_LINES = [
    "😎 Apna rule simple hai: respect do, respect lo.",
    "👑 King wali vibe, tension wali nahi.",
    "🔥 Style copy ho sakta hai, attitude nahi.",
    "😎 Silent mode, royal mode.",
    "👑 Naam yaad rakhna, vibe khud yaad rahegi.",
    "🔥 Level apna alag hai.",
    "😎 Competition se zyada peace pasand hai.",
    "👑 Royal entry, simple personality.",
    "🔥 Attitude nahi, self-respect hai.",
    "😎 Apni vibe mein mast."
]


SAD_LINES = [
    "🥺 Thoda waqt do, sab better lagega.",
    "❤️ Khud ko blame mat karo.",
    "🌙 Har raat ke baad subah hoti hai.",
    "🤗 Dil halka karna ho toh baat karo.",
    "🥀 Kuch dard waqt ke saath kam ho jaate hain.",
    "❤️ Tumhari value kisi ek person se decide nahi hoti.",
    "🌸 Mushkil waqt permanent nahi hota.",
    "🫶 Apna khayal rakho.",
    "✨ Ek bad day poori life nahi hoti.",
    "🤝 Himmat rakho, scene badlega."
]


FOOD_LINES = [
    "🍕 Pizza ka naam sunte hi bot hungry ho gaya 😂",
    "🍔 Burger chalega, diet kal se 😂",
    "🍜 Momos ho toh mujhe bhi bula lena 😜",
    "🍛 Biryani ke liye koi permission nahi chahiye 😂",
    "☕ Chai + gossip = perfect combination.",
    "🍫 Chocolate bhejo, phir reply premium milega 😎",
    "🍟 Fries share karoge ya sab khud khaoge? 😂",
    "🥤 Cold drink ke saath thodi masti bhi honi chahiye.",
    "🍜 Maggi emergency food hai 😎",
    "🍕 Khana pehle, tension baad mein."
]


SLEEP_LINES = [
    "😴 So jao ji, kal phir duniya handle karni hai.",
    "🌙 Good night, sweet dreams.",
    "🥱 Neend aa rahi hai toh phone side mein rakho.",
    "😴 Bot bhi sleep mode mein jaane wala hai.",
    "🌙 Raat ko overthinking se bachna.",
    "🛌 Blanket pakdo aur so jao 😂",
    "✨ Sweet dreams ji.",
    "😴 Kal fresh mood ke saath aana.",
    "🌙 Good night, take care ❤️",
    "🥱 Ab bas, sleep mode ON."
]


# ============================================================
# SHAYARI
# ============================================================

SHAYARI = [
    "🌙 Raat khamosh hai, chand bhi pareshaan hai, kisi ke message ka intezaar hai.",
    "❤️ Dil ki baat lafzon mein kaha nahi jaati, kuch feelings bas mehsoos ki jaati.",
    "🌹 Mohabbat ek ehsaas hai, jo lafzon ka mohtaaj nahi.",
    "✨ Muskurahat chhoti si hai, par kisi ka din bana sakti hai.",
    "🥀 Kuch log yaad ban jaate hain, kuch log wajah ban jaate hain.",
    "🌙 Chand bhi sharma jaaye, jab koi itna pyara muskuraye.",
    "💫 Zindagi chhoti si kahani hai, har pal apni nishani hai.",
    "❤️ Dil saaf ho toh chehra khud khoobsurat lagta hai.",
    "🌸 Alfaaz kam pad jaate hain jab feelings zyada ho jaati hain.",
    "🌹 Ishq naam nahi, ek khoobsurat ehsaas hai.",
    "🥀 Dard chupana bhi ek hunar hai, har koi samajh nahi pata.",
    "🌙 Raat lambi ho sakti hai, par subah zaroor aati hai.",
    "💖 Kisi ki smile ka reason banna bhi mohabbat hai.",
    "✨ Khamoshi bhi kabhi kabhi sab kuch keh deti hai.",
    "🌸 Yaadein wahi hoti hain jo waqt ke baad bhi saath rahein.",
    "❤️ Dil se nikli baat seedha dil tak jaati hai.",
    "🌹 Waqt badalta hai, par kuch yaadein nahi badalti.",
    "💫 Aankhon mein sapne aur dil mein umeed rakho.",
    "🥰 Pyaar wahi jo izzat ke saath nibhaya jaaye.",
    "🌙 Kuch rishte naam ke mohtaaj nahi hote."
]


# ============================================================
# GREETING
# ============================================================

HELLO_LINES = [
    "👋 Hello ji! RK Raja Bot present hai 😎",
    "😂 Hello hello! Kya scene hai?",
    "😎 Haan bolo boss, bot sun raha hai.",
    "👋 Hii ji! Aaj kya hukam hai?",
    "🔥 Welcome boss!",
    "🥰 Hiiiii! Kya haal hai?",
    "😂 Arre hello! Itni der se kahan the?",
    "😜 Hello ji, masti karein?",
    "👑 Welcome to RK Raja Bot.",
    "🤖 Bot online hai, bolo kya baat hai?"
]


# ============================================================
# BOT INFO
# ============================================================

BOT_LINES = [
    "🤖 Main RK Raja Bot hoon 😎",
    "👑 Naam RK Raja Bot, kaam reply dena.",
    "😂 Main bot hoon, lekin vibes human wali hain.",
    "🔥 RK Raja Bot — always ready.",
    "😎 Bot online, mood bhi online.",
    "🤖 Question bhejo, reply milega.",
    "👑 RK Raja Bot ki attendance full hai.",
    "😂 Main coffee nahi peeta, phir bhi active hoon.",
    "⚡ Bot mode activated.",
    "😎 Simple bot, complicated replies."
]


# ============================================================
# THANKS
# ============================================================

THANKS_LINES = [
    "😎 Anytime boss!",
    "❤️ Welcome ji!",
    "🥰 Koi baat nahi.",
    "😂 Thank you ki zarurat nahi.",
    "🤝 Always welcome!",
    "🔥 Anytime!",
    "😜 Bas chocolate bhej dena.",
    "😂 Welcome welcome!",
    "❤️ Khushi hui help karke.",
    "😎 Bot service available hai."
]


# ============================================================
# SORRY
# ============================================================

SORRY_LINES = [
    "🥰 Koi baat nahi, maaf kiya.",
    "❤️ Chill karo, sab okay hai.",
    "🤝 Mistakes hoti rehti hain.",
    "😌 It's okay ji.",
    "😂 Chalo maaf kiya, ab smile karo.",
    "🥹 Koi tension nahi.",
    "❤️ Dil pe mat lo.",
    "😎 All good boss.",
    "🤗 No worries.",
    "✨ Sab set hai."
]


# ============================================================
# BYE
# ============================================================

BYE_LINES = [
    "👋 Bye ji, jaldi wapas aana.",
    "🥺 Itni jaldi bye?",
    "😎 Okay boss, milte hain.",
    "❤️ Take care!",
    "😂 Bye bye!",
    "🌙 Good night agar raat hai.",
    "✨ Phir milenge.",
    "🤝 Stay happy!",
    "😜 Permission granted, jao.",
    "👋 See you soon!"
]


# ============================================================
# CUTE GENERATED RESPONSES
# ============================================================

CUTE_MIDDLE = [
    "itna cute message",
    "ye pyaari si baat",
    "tumhari sweet vibe",
    "ye adorable style",
    "itni pyari calling",
    "ye cute sa attitude",
    "tumhari innocent baat",
    "ye sweet message",
    "tumhari lovely vibe",
    "ye chhoti si smile"
]


# ============================================================
# FLIRTY GENERATED RESPONSES
# ============================================================

FLIRTY_MIDDLE = [
    "aise smile karoge",
    "aise pyaar se bologe",
    "itni cute flirting karoge",
    "aise naam se bulaoge",
    "itni sweet baat karoge",
    "aise aankhon wali vibe doge",
    "itna charming banoge",
    "itna romantic mood banaoge",
    "aise compliment doge",
    "itni lovely baat karoge"
]


# ============================================================
# FUNNY GENERATED RESPONSES
# ============================================================

FUNNY_MIDDLE = [
    "tera message",
    "ye dialogue",
    "tera confidence",
    "ye question",
    "ye scene",
    "ye idea",
    "teri entry",
    "ye bakchodi",
    "tera logic",
    "ye conversation"
]


# ============================================================
# EXTRA RANDOM LINES
# ============================================================

EXTRA_LINES = [
    "😂 Matlab kuch bhi!",
    "🤣 Bhai kya imagination hai!",
    "😜 Aaj mood mast hai.",
    "👀 Main sab dekh raha hoon.",
    "🤖 Processing feelings...",
    "😂 Ye toh unexpected tha.",
    "😎 Interesting message.",
    "🔥 Vibe detected.",
    "🥰 Cute energy detected.",
    "😏 Flirty energy detected.",
    "🤣 Comedy level high.",
    "🌹 Romantic mode detected.",
    "👑 Royal vibe detected.",
    "🥺 Emotional mode detected.",
    "😴 Sleep mode detected.",
    "🍕 Food mode detected.",
    "😂 Bot ko bhi hasi aa gayi.",
    "😜 Thoda chill karo.",
    "😎 Sab control mein hai.",
    "✨ Good vibes only."
]


# ============================================================
# INTENT DETECTION
# ============================================================

def normalize(text):
    text = str(text).lower().strip()

    # Multiple spaces remove
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text


def detect_intent(text):

    text = normalize(text)

    # Priority:
    # love / flirty / naughty before generic words

    priority = [
        "naughty",
        "flirty",
        "love",
        "cute",
        "roast",
        "shayari",
        "funny",
        "sad",
        "angry",
        "attitude",
        "food",
        "sleep",
        "thanks",
        "sorry",
        "bye",
        "hello",
        "bot",
        "help"
    ]

    for category in priority:

        words = KEYWORDS.get(
            category,
            []
        )

        for word in words:

            word = normalize(word)

            if word in text:
                return category

    return "default"


# ============================================================
# UNIQUE RESPONSE GENERATOR
# ============================================================

def generated_funny():

    start = random.choice(
        FUNNY_START
    )

    middle = random.choice(
        FUNNY_MIDDLE
    )

    end = random.choice(
        FUNNY_END
    )

    return (
        f"{start} {middle} dekh ke "
        f"{end}"
    )


def generated_cute():

    start = random.choice(
        CUTE_START
    )

    middle = random.choice(
        CUTE_MIDDLE
    )

    end = random.choice(
        CUTE_END
    )

    return (
        f"{start} {middle} dekhkar "
        f"{end}"
    )


def generated_flirty():

    start = random.choice(
        FLIRTY_START
    )

    middle = random.choice(
        FLIRTY_MIDDLE
    )

    end = random.choice(
        FLIRTY_END
    )

    return (
        f"{start} {middle} toh "
        f"{end}"
    )


def generated_naughty():

    start = random.choice(
        NAUGHTY_START
    )

    end = random.choice(
        NAUGHTY_END
    )

    return f"{start}, {end}"


def generated_love():

    start = random.choice(
        LOVE_START
    )

    end = random.choice(
        LOVE_END
    )

    return f"{start} {end}"


def generated_roast():

    start = random.choice(
        ROAST_START
    )

    end = random.choice(
        ROAST_END
    )

    return f"{start}, {end}"


# ============================================================
# MAIN REPLY
# ============================================================

def generate_reply(text):

    intent = detect_intent(text)

    if intent == "hello":
        return random.choice(
            HELLO_LINES
        )

    if intent == "funny":
        return generated_funny()

    if intent == "cute":
        return generated_cute()

    if intent == "flirty":
        return generated_flirty()

    if intent == "naughty":
        return generated_naughty()

    if intent == "love":
        return generated_love()

    if intent == "roast":
        return generated_roast()

    if intent == "attitude":
        return random.choice(
            ATTITUDE_LINES
        )

    if intent == "shayari":
        return random.choice(
            SHAYARI
        )

    if intent == "sad":
        return random.choice(
            SAD_LINES
        )

    if intent == "angry":
        return random.choice([
            "😌 Gussa thoda side mein rakho.",
            "😂 Itna gussa health ke liye achha nahi.",
            "🤝 Chill karo, baat se solve karte hain.",
            "🥺 Pehle smile, phir gussa.",
            "😎 Calm down boss.",
            "❤️ Gusse mein decision mat lena.",
            "😂 Bot ko mat darao.",
            "🤗 Thoda relax karo.",
            "🌸 Deep breath lo.",
            "😌 Sab theek ho jayega."
        ])

    if intent == "thanks":
        return random.choice(
            THANKS_LINES
        )

    if intent == "sorry":
        return random.choice(
            SORRY_LINES
        )

    if intent == "bye":
        return random.choice(
            BYE_LINES
        )

    if intent == "food":
        return random.choice(
            FOOD_LINES
        )

    if intent == "sleep":
        return random.choice(
            SLEEP_LINES
        )

    if intent == "bot":
        return random.choice(
            BOT_LINES
        )

    if intent == "help":
        return random.choice([
            "😎 Bolo kya help chahiye?",
            "🤖 Question bhejo, try karta hoon.",
            "😂 Help desk open hai.",
            "👀 Batao problem kya hai?",
            "🤝 Haan ji, bolo.",
            "🔥 Bot ready hai.",
            "😎 Explain karo, dekhte hain.",
            "🤖 Jo poochna hai pooch lo.",
            "✨ Bolo boss.",
            "😂 Problem batao, solution dhoondte hain."
        ])

    # Default
    return random.choice(
        EXTRA_LINES
    )


# ============================================================
# CHECK RESPONSE COUNT
# ============================================================

def estimated_response_count():

    static_count = sum(
        len(v)
        for v in [
            HELLO_LINES,
            SHAYARI,
            ATTITUDE_LINES,
            SAD_LINES,
            FOOD_LINES,
            SLEEP_LINES,
            THANKS_LINES,
            SORRY_LINES,
            BYE_LINES,
            BOT_LINES,
            EXTRA_LINES
        ]
    )

    generated_count = (
        len(FUNNY_START)
        * len(FUNNY_MIDDLE)
        * len(FUNNY_END)
        +
        len(CUTE_START)
        * len(CUTE_MIDDLE)
        * len(CUTE_END)
        +
        len(FLIRTY_START)
        * len(FLIRTY_MIDDLE)
        * len(FLIRTY_END)
        +
        len(NAUGHTY_START)
        * len(NAUGHTY_END)
        +
        len(LOVE_START)
        * len(LOVE_END)
        +
        len(ROAST_START)
        * len(ROAST_END)
    )

    return static_count + generated_count


if __name__ == "__main__":

    print(
        "RK Raja Bot estimated response combinations:",
        estimated_response_count()
    )

    tests = [
        "hello",
        "mujhe joke sunao",
        "tum bahut cute ho",
        "i love you",
        "thoda flirt karo",
        "naughty mood",
        "mujhe roast karo",
        "shayari sunao",
        "main sad hoon",
        "khana khaya",
        "good night"
    ]

    print("\nTEST RESPONSES:\n")

    for message in tests:

        print(
            f"USER : {message}"
        )

        print(
            f"BOT  : {generate_reply(message)}"
        )

        print()
