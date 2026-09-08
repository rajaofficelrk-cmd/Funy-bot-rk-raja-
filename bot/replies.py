import random

OPENERS = [
    "😂 Arey suno",
    "😏 Oho",
    "🤣 Hahaha",
    "👀 Achha ji",
    "😜 Arey wah",
    "🥰 Awww",
    "🙄 Haan ji",
    "😎 Bilkul",
    "😂 Kya baat hai",
    "😏 Itna pyaar",
    "🤭 Ohooo",
    "🤣 Bhai sahab",
    "👀 Main sun raha hoon",
    "😜 Batao batao",
    "❤️ Achhaaa",
]

MIDDLES = [
    "aaj bade mood mein ho",
    "itne pyaar se kyun bula rahe ho",
    "kya scene chal raha hai",
    "masti karne ka mood lag raha hai",
    "baat interesting ho gayi",
    "tumhari baat sun raha hoon",
    "ab batao kya hukam hai",
    "lagta hai kuch gadbad hai",
    "aaj full masti chalegi",
    "kuch toh secret hai",
    "tumhari timing kamaal hai",
    "ab curiosity badh gayi",
    "ye baat toh alag level ki hai",
    "mujhe sab samajh aa raha hai",
    "ab chup nahi rehna",
]

ENDINGS = [
    "😂 bolo kya hua?",
    "😜 batao na!",
    "😏 ab sach-sach batao.",
    "🤣 hasi aa gayi yaar.",
    "❤️ bolo, sun raha hoon.",
    "👀 kya chal raha hai?",
    "🥰 aise hi baat karte raho.",
    "🙄 itna suspense kyun?",
    "😎 RK RAJA present hai.",
    "😂 ek baar aur bolo.",
    "🤭 ye toh interesting hai.",
    "😜 masti karte hain.",
    "❤️ tension mat lo.",
    "🤣 aaj toh maza aayega.",
    "👀 main yahin hoon.",
]

HELLO = [
    "👋 Hello ji ❤️",
    "😂 Hiii, RK RAJA present hai!",
    "😜 Hiiiii, kya haal hai?",
    "🥰 Hello jaan, bolo kya scene hai!",
    "👀 Haan ji, sun raha hoon.",
]

GOOD_MORNING = [
    "🌅 Good Morning ❤️",
    "☀️ Good Morning ji 😍",
    "🌸 Subah-subah yaad kar liya 😜",
    "🥰 Good Morning, aaj ka din mast ho!",
]

GOOD_AFTERNOON = [
    "☀️ Good Afternoon ❤️",
    "😎 Good Afternoon ji!",
    "😂 Dopahar mein bhi masti on hai!",
]

GOOD_EVENING = [
    "🌆 Good Evening ❤️",
    "😏 Good Evening ji, kya haal?",
    "🥰 Shaam suhani aur baatein mast!",
]

GOOD_NIGHT = [
    "🌙 Good Night ❤️",
    "🥰 Sweet dreams ji!",
    "😴 Ab so jao, kal phir masti karenge 😂",
    "🌙 Good Night, take care ❤️",
]

BYE = [
    "Bye ❤️",
    "👋 Bye ji, phir milte hain!",
    "😂 Byeee, jaldi wapas aana!",
    "🥰 Take care ❤️",
]

BOT_CALL = [
    "😒 Sun raha hoon, behra nahi hoon main 😂",
    "😂 Itni baar BOT BOT kyu laga rakha hai?",
    "👀 RK RAJA aapki baatein sun raha hai 😌",
    "🤣 Bot nahi hoon main, itna BOT BOT mat karo!",
    "🙄 Haan bolo, sun raha hoon... attendance laga rahe ho kya? 😂",
    "😏 RK RAJA yahin hai, baar-baar BOT bolne ki zarurat nahi.",
    "😂 Ek baar BOT bola tha, teen baar kyun bula rahe ho?",
    "👂 Sun raha hoon bhai, behra nahi hoon 😜",
]

FUNNY = [
    "🤣 Bhai ye kya comedy chal rahi hai?",
    "😂 Aaj toh tum full masti mood mein ho!",
    "😜 Pehle hasi control karo, phir baat karte hain!",
    "🤣 Is baat pe toh award milna chahiye!",
    "😂 Kya mast scene bana diya!",
]

FLIRT = [
    "😏 Itna cute kyun ban rahe ho?",
    "😉 Aise baat karoge toh reply toh dena padega.",
    "🥰 Tumhari baaton mein alag hi vibe hai.",
    "😜 Itna pyaar se bologe toh maan jaunga.",
    "❤️ Aaj mood kuch zyada hi romantic lag raha hai.",
]

SHAYARI = [
    "❤️ Dil ki baat lafzon mein kaha nahi karte, kuch raaz aankhon se bhi bayan hote hain.",
    "🌙 Raat khamosh hai, baatein hazaar hain, tum online ho toh dil bekaraar hai.",
    "🥰 Muskurahat tumhari kamaal karti hai, bina bole bhi dil se sawaal karti hai.",
]

LOVE = [
    "❤️ Love you too ji!",
    "🥰 Awww, kitna pyaara!",
    "😍 Dil garden garden ho gaya!",
    "❤️ Itna pyaar milega toh reply toh banta hai.",
]

def random_masti():
    return (
        random.choice(OPENERS) + " " +
        random.choice(MIDDLES) + ", " +
        random.choice(ENDINGS)
    )

def generate_reply(text):
    t = " ".join(text.lower().strip().split())

    # Help
    if t in {"help", "/help", "#help", ".help"}:
        return (
            "🤖 RK RAJA COMMANDS\n\n"
            "😂 joke | funny | masti | roast\n"
            "😏 flirt | love | cute\n"
            "✍️ shayari | attitude | sad\n"
            "❤️ baby | babu | sona | shona | jaan | janu\n"
            "🌅 good morning\n"
            "☀️ good afternoon\n"
            "🌆 good evening\n"
            "🌙 good night\n"
            "👋 bye\n"
            "🤖 bot bot bot\n"
            "👑 rk raja"
        )

    if "good morning" in t:
        return random.choice(GOOD_MORNING)

    if "good afternoon" in t:
        return random.choice(GOOD_AFTERNOON)

    if "good evening" in t:
        return random.choice(GOOD_EVENING)

    if "good night" in t:
        return random.choice(GOOD_NIGHT)

    if t == "bye" or "bye" in t:
        return random.choice(BYE)

    if t.count("bot") >= 3:
        return random.choice(BOT_CALL)

    if "bot" in t:
        return random.choice([
            "👀 Haan bolo, RK RAJA sun raha hai.",
            "😂 Haan bhai, sun raha hoon.",
            "😏 Kya hua? Itne pyaar se BOT kyun bula rahe ho?",
        ])

    if any(x in t for x in ["hello", "hii", "hi", "hey"]):
        return random.choice(HELLO)

    if any(x in t for x in ["joke", "funny", "masti"]):
        return random.choice(FUNNY)

    if any(x in t for x in ["flirt", "hot", "cute"]):
        return random.choice(FLIRT)

    if "shayari" in t:
        return random.choice(SHAYARI)

    if any(x in t for x in ["love", "i love you"]):
        return random.choice(LOVE)

    if any(x in t for x in ["baby", "babu", "sona", "shona", "jaan", "janu"]):
        return random.choice([
            "🥰 Haan ji, bolo ❤️",
            "😏 Itne pyaar se bulaoge toh jawab dena padega.",
            "❤️ Haan jaan, sun raha hoon.",
            "😂 Bolo babu, kya hua?",
        ])

    return random_masti()
