# bot/replies.py

import random


# =========================================================
# /help — ONLY slash command
# =========================================================

HELP_TEXT = """
╔══════════════════════════════╗
      👑 RK RAJA BOT 👑
        💖 HELP MENU 💖
╚══════════════════════════════╝

⚠️ NOTE:
Sirf HELP ke liye / use karo.
Baaki options bina / ke chalenge.

━━━━━━━━━━━━━━━━━━━━━━
😂 FUN
━━━━━━━━━━━━━━━━━━━━━━
joke
funny
masti
pagal
roast
attitude
hasao

━━━━━━━━━━━━━━━━━━━━━━
❤️ LOVE
━━━━━━━━━━━━━━━━━━━━━━
love
pyaar
flirt
romantic
cute
babu
baby
sona
shona
jaan
janu
sweet
miss you

━━━━━━━━━━━━━━━━━━━━━━
🌹 SHAYARI
━━━━━━━━━━━━━━━━━━━━━━
shayari
love shayari
flirt shayari
romantic shayari
sad shayari

━━━━━━━━━━━━━━━━━━━━━━
🥰 CUTE ACTION
━━━━━━━━━━━━━━━━━━━━━━
hug
kiss
umma
ummi
pyaar
miss

━━━━━━━━━━━━━━━━━━━━━━
🌅 TIME
━━━━━━━━━━━━━━━━━━━━━━
good morning
good afternoon
good evening
good night
bye

━━━━━━━━━━━━━━━━━━━━━━
🤖 BOT
━━━━━━━━━━━━━━━━━━━━━━
bot
bot bot bot
rk
raja
rk raja

━━━━━━━━━━━━━━━━━━━━━━
💬 NORMAL CHAT
━━━━━━━━━━━━━━━━━━━━━━
Koi bhi normal message bhejo.
Bot automatically fun/cute reply karega.

━━━━━━━━━━━━━━━━━━━━━━
👑 RK RAJA
━━━━━━━━━━━━━━━━━━━━━━
Telegram:
https://t.me/Akatsuki_rulex
"""


# =========================================================
# BOT CALL REPLIES
# =========================================================

BOT_CALL_REPLIES = [
    "😒 Sun raha hoon, behra nahi hoon main 😂",
    "😂 Itni baar BOT BOT kyu laga rakha hai?",
    "👀 RK RAJA aapki baatein sun raha hai.",
    "🤣 Bot nahi hoon main, itna BOT BOT mat karo!",
    "🙄 Haan bolo, sun raha hoon... attendance laga rahe ho kya? 😂",
    "😏 RK RAJA yahin hai, baar-baar BOT bolne ki zarurat nahi.",
    "😂 Ek baar BOT bola tha, teen baar kyun bula rahe ho?",
    "👂 Sun raha hoon bhai, behra nahi hoon 😜",
]


BOT_REPLY = [
    "👀 Haan bolo, RK RAJA sun raha hai.",
    "😏 Kya hua? Itne pyaar se BOT kyun bula rahe ho?",
    "😂 Haan bhai, sun raha hoon.",
    "🙄 Bolo na, main yahin hoon.",
    "🤖 Present sir! 😂",
]


# =========================================================
# GENERAL HUMAN-LIKE REPLIES
# =========================================================

OPENERS = [
    "Acha ji 😏",
    "Ohooo 👀",
    "Haye 🙈",
    "Arey wah 😍",
    "Hmm ji 😌",
    "Awww 🥰",
    "Oho baby 😜",
    "Haye re ❤️",
    "Wah ji wah 😍",
    "Arey cutie 🙈",
    "Hmmmm 👀",
    "Oho sona ❤️",
    "Acha babu 😜",
    "Haye janu 🥰",
    "Accha ji 👀",
]

MIDDLES = [
    "itne pyaar se baat karoge",
    "aise message bhejoge",
    "itni sweet baat karoge",
    "mujhe aise bulaoge",
    "itna attention doge",
    "baar-baar yaad karoge",
    "itna cute banoge",
    "aise smile karoge",
    "itni achhi baat karoge",
    "itna pyaara message karoge",
    "mujhse aise baatein karoge",
    "itni der tak chat karoge",
    "aise care dikhaoge",
    "mood itna romantic karoge",
    "itna sweet behave karoge",
]

ENDINGS = [
    "toh main kaise chup rahun 😜❤️",
    "toh reply toh banta hai na 🙈",
    "phir toh dil khush ho gaya 🥰",
    "toh thoda sa flirt toh banta hai 😏",
    "phir main bhi smile karunga ❤️",
    "toh meri bhi sharam aa jayegi 🙈",
    "phir toh conversation interesting ho gayi 👀",
    "toh tumhari baat maan hi leta hoon 😌❤️",
    "phir toh tum special ho gaye 😍",
    "toh ab batao aur kya kehna hai? 😜",
    "phir toh tumse baat karne ka mann karega ❤️",
    "toh mood hi bana diya tumne 🥰",
    "phir toh aaj chat lambi chalegi 😏",
    "toh smile automatically aa gayi 🙈",
    "phir toh tum dangerous ho 😜❤️",
]


# =========================================================
# GREETING
# =========================================================

HELLO = [
    "Hii 😍 kaise ho?",
    "Hello ji ❤️ kya haal hai?",
    "Hii hii 🙈 kya chal raha hai?",
    "Heyyy 😏 finally aa gaye.",
    "Hello baby 🥰 kya chal raha hai?",
    "Hii cutie 👀 mujhe yaad kiya kya?",
    "Oho hello 😜 aaj mood kaisa hai?",
    "Heyy ❤️ bolo kya scene hai?",
]


# =========================================================
# MORNING / AFTERNOON / EVENING / NIGHT
# =========================================================

GOOD_MORNING = [
    "Good Morning 🌅❤️ Aaj ka din tumhare liye bahut pyaara ho.",
    "Good Morning jaan 😍 subah-subah yaad aa gaye.",
    "Good Morning ☀️🥰 smile ke saath din start karo.",
    "Good Morning babu 🙈 aaj khush rehna.",
    "Good Morning ❤️ chai pi ya abhi tak sleepy ho? 😴",
]

GOOD_AFTERNOON = [
    "Good Afternoon ☀️❤️ Lunch hua?",
    "Good Afternoon 😍 aaj ka din kaisa ja raha hai?",
    "Good Afternoon babu 🥰 thoda rest bhi kar lena.",
    "Good Afternoon 😏 itni dhoop mein bhi tumhari vibe cool hai.",
]

GOOD_EVENING = [
    "Good Evening 🌆❤️ Aaj ka din kaisa raha?",
    "Good Evening jaan 🥰 ab thoda relax karo.",
    "Good Evening 😍 shaam aur tumhari baatein, nice combination.",
    "Good Evening babu 🙈 ab toh chat ka time hai.",
]

GOOD_NIGHT = [
    "Good Night 🌙❤️ Sweet dreams.",
    "Good Night jaan 🥰 kal phir baatein karenge.",
    "Good Night babu 🙈 achhe se sona.",
    "Good Night 😴❤️ apna khayal rakhna.",
    "Good Night 🌙✨ phone side mein rakho aur so jao 😜",
]


# =========================================================
# BYE
# =========================================================

BYE = [
    "Bye ❤️ jaldi wapas aana.",
    "Bye bye 🙈 itni jaldi ja rahe ho?",
    "Okay bye 😍 take care.",
    "Bye jaan ❤️ phir milte hain.",
    "Acha bye 😜 but jaldi return karna.",
]


# =========================================================
# LOVE
# =========================================================

LOVE = [
    "Awww ❤️ ye sunke smile aa gayi.",
    "Hmm 😏 love wali vibe aa rahi hai.",
    "🥰 Dil ko achha laga tumhari baat sunkar.",
    "❤️ Itna pyaar doge toh main bhi sweet reply dunga.",
    "🙈 Aise bolke mujhe shy mat karo.",
    "😍 Ye toh dil wali baat kar di.",
    "❤️ Tumhari baat mein alag hi sweetness hai.",
]


# =========================================================
# CUTE
# =========================================================

CUTE = [
    "Awww 🥺❤️ kitne cute ho tum.",
    "🙈 Itna sweet message!",
    "🥰 Tumhari baat mein alag hi cuteness hai.",
    "❤️ Ye message toh dil le gaya.",
    "😏 Cute toh tum khud ho.",
    "🫶 Awww, kya cute vibe hai.",
]


# =========================================================
# FUNNY
# =========================================================

FUNNY = [
    "😂 Ye sunke bot bhi has pada.",
    "🤣 Tumhari timing kamaal ki hai.",
    "😂 Bhai kya imagination hai!",
    "😜 Aaj full masti mode ON lag raha hai.",
    "🤣 Ye message unexpected tha.",
    "😂 Bhai tu comedy material hai.",
    "😆 Hasi control karna mushkil ho gaya.",
]


# =========================================================
# MASTI
# =========================================================

MASTI = [
    "😂 Aaj full masti mode ON!",
    "🤣 Chal phir, aaj serious hona mana hai.",
    "😜 Masti karni hai toh bot ready hai!",
    "😂 Mood ko boring mat hone do!",
    "😎 Aaj sirf chill aur masti.",
]


# =========================================================
# ROAST
# =========================================================

ROAST = [
    "😂 Bhai pehle apna WiFi check kar, phir attitude dikha.",
    "🤣 Itna confidence? Source batao zara.",
    "😜 Roast chahiye tha ya halka sa reality check?",
    "😂 Tumhari entry hi comedy hai bhai!",
    "🤣 Bhai tu khud hi meme hai.",
]


# =========================================================
# ATTITUDE
# =========================================================

ATTITUDE = [
    "😎 Vibe apni alag hai.",
    "👑 Royal rehna aadat hai.",
    "😏 Attitude nahi, bas standard thoda high hai.",
    "🔥 Apni vibe, apne rules.",
    "😎 Silent mode, royal attitude.",
]


# =========================================================
# SAD
# =========================================================

SAD = [
    "🥺 Kya hua? Thoda smile karo.",
    "❤️ Bura waqt hamesha nahi rehta.",
    "🌙 Dil halka kar lo, baat karna ho toh karo.",
    "🥀 Sab theek ho jayega, tension mat lo.",
    "🫂 Don't worry, thoda relax karo.",
]


# =========================================================
# SHAYARI
# =========================================================

SHAYARI = [
    "🌙 Raat khamosh hai, par dil mein hazaar baatein hain. ❤️",
    "✨ Kuch log baaton se nahi, ehsaason se yaad rehte hain.",
    "🥀 Yaadein purani ho sakti hain, ehsaas nahi.",
    "❤️ Muskurahat chhoti si hoti hai, par asar bahut bada karti hai.",
    "🌹 Dil ki baat lafzon mein kaha nahi karte,\nKuch ehsaas bas mehsoos kiya karte hain.",
]


# =========================================================
# LOVE SHAYARI
# =========================================================

LOVE_SHAYARI = [
    "❤️ Mohabbat lafzon ki mohtaaj nahi,\nBas ek ehsaas hi kaafi hai.",
    "🌹 Kuch log dil mein aise bas jaate hain,\nKi door hokar bhi paas lagte hain.",
    "✨ Muskurahat ki wajah poochhi,\nToh dil ne tumhara naam le diya. ❤️",
    "🥰 Tera zikr ho toh chehre pe smile aa jaati hai.",
]


# =========================================================
# FLIRT SHAYARI
# =========================================================

FLIRT_SHAYARI = [
    "🌹 Nazar mili toh baat ban gayi,\nTum muskura diye toh raat ban gayi. ❤️",
    "✨ Tumhari smile ka kya kehna,\nDil bole bas tumse baat karte rehna. 😏❤️",
    "🌙 Chand bhi thoda sharma gaya,\nJab tumhara zikr aa gaya. 🥰",
    "😏 Tum saamne ho toh baat kuch aur hai,\nTumhari smile mein hi ek raaz hai. ❤️",
]


# =========================================================
# SAD SHAYARI
# =========================================================

SAD_SHAYARI = [
    "🥀 Kuch yaadein muskurane nahi deti,\nAur kuch log bhulaye nahi jaate.",
    "🌙 Khamoshi bhi kabhi-kabhi bahut kuch keh jaati hai.",
    "💔 Waqt badal jaata hai,\nPar kuch yaadein wahi reh jaati hain.",
    "🥀 Dil chup hai,\nPar yaadein abhi bhi bolti hain.",
]


# =========================================================
# ROMANTIC
# =========================================================

ROMANTIC = [
    "❤️ Tumhari baaton mein alag hi vibe hai.",
    "🥰 Aaj mood thoda romantic lag raha hai.",
    "🙈 Itni sweet baatein karoge toh smile aa jayegi.",
    "😏 Tumhari timing bhi kamaal ki hai.",
    "❤️ Chat ka mood hi cute ho gaya.",
]


# =========================================================
# HUG / KISS / UMMA / UMMI
# =========================================================

HUG = [
    "🤗 Awww, ek cute sa virtual hug 🤗❤️",
    "🫂 Lo ji, warm hug tumhare liye 🥰",
    "🫂❤️ Hug accepted... ab smile karo 😜",
    "🤗 Ek tight virtual hug, bas cute wala ❤️",
    "🫂 Aao ek friendly hug ho jaye 😄",
]


KISS = [
    "😘 Ek cute si virtual kiss ❤️",
    "💋 Lo ji, ek sweet sa kiss 😘",
    "😘❤️ Cute kiss received!",
    "🙈 Ek chhoti si virtual kiss, bas cute wali 😜",
]


UMMA = [
    "😘 Ummaaa ❤️🙈",
    "💋 Ummmmaa 😘❤️",
    "🥰 Ek cute si ummaaa!",
    "😘 Umma received 😜❤️",
]


UMMI = [
    "😘 Ummiii ❤️",
    "🙈 Ummiii... kitne cute ho!",
    "🥰 Ek sweet si ummi 😘",
    "❤️ Ummiii 😜",
]


# =========================================================
# GENERIC
# =========================================================

GENERIC = [
    "Hmm 👀 tumhari baat interesting hai 😏",
    "Oho 😜 ye toh unexpected tha.",
    "Acha ji ❤️ continue karo, sun raha hoon.",
    "Haye 🙈 tum bhi na...",
    "Interesting 👀 tumse baat karke vibe achhi ho rahi hai.",
    "Awww 🥰 ye message cute tha.",
    "😏 Tumhari baaton mein kuch toh magic hai.",
    "😂 Tumse baat karna dangerous hai, smile rukti hi nahi.",
    "❤️ Acchi vibe aa rahi hai tumhari.",
    "🙈 Itna sweet message expect nahi kiya tha.",
]


# =========================================================
# FLIRT ENGINE
# =========================================================

def flirty_reply(text=""):
    opener = random.choice(OPENERS)
    middle = random.choice(MIDDLES)
    ending = random.choice(ENDINGS)

    if random.random() < 0.30:
        question = random.choice([
            "Waise aaj itne cute kyun ho? 👀",
            "Tum hamesha aise hi baat karte ho kya? 😏",
            "Waise mujhe yaad kar rahe the kya? 🙈",
            "Aaj ka mood itna romantic hai kya? ❤️",
            "Sach batao, smile kar rahe ho na? 😜",
            "Itni attention mujhe hi kyun? 👀",
            "Aaj mujhse kitni der baat karoge? 😏",
            "Tum itne sweet kab se ho gaye? ❤️",
        ])

        return f"{opener} {middle}, {ending}\n\n{question}"

    return f"{opener} {middle}, {ending}"


# =========================================================
# MAIN REPLY ENGINE
#
# IMPORTANT:
# /help is the ONLY slash command.
# Everything else works without slash.
# =========================================================

def generate_reply(text):
    t = " ".join(str(text).lower().strip().split())

    if not t:
        return "👀 Kuch bolo na, RK RAJA sun raha hai."

    # -----------------------------------------------------
    # ONLY /help
    # -----------------------------------------------------

    if t == "/help":
        return HELP_TEXT

    # -----------------------------------------------------
    # If someone writes other slash commands, tell them
    # only /help uses slash.
    # -----------------------------------------------------

    if t.startswith("/"):
        return "⚠️ Sirf /help slash ke saath use hota hai.\nBaaki commands bina / ke likho 😜"

    # -----------------------------------------------------
    # BOT BOT BOT
    # -----------------------------------------------------

    bot_count = t.split().count("bot")

    if bot_count >= 3:
        return random.choice(BOT_CALL_REPLIES)

    if t == "bot":
        return random.choice(BOT_REPLY)

    # -----------------------------------------------------
    # RK RAJA
    # -----------------------------------------------------

    if "rk raja" in t or "rkraja" in t:
        return (
            "👑 𝐑𝐊 𝐑𝐀𝐉𝐀 ❤️\n\n"
            "🌸 RK RAJA XWD TELEGRAM GC\n"
            "JOIN PLEASE 🙏\n\n"
            "https://t.me/Akatsuki_rulex"
        )

    if t in {"rk", "raja"}:
        return (
            "👑 𝐑𝐊 𝐑𝐀𝐉𝐀 ❤️\n\n"
            "🌸 RK RAJA XWD TELEGRAM GC\n"
            "JOIN PLEASE 🙏\n\n"
            "https://t.me/Akatsuki_rulex"
        )

    # -----------------------------------------------------
    # GREETINGS
    # -----------------------------------------------------

    if any(x in t for x in [
        "hello",
        "hii",
        "hiii",
        "hiiii",
        "hey",
        "heyy"
    ]):
        return random.choice(HELLO)

    # -----------------------------------------------------
    # TIME
    # -----------------------------------------------------

    if "good morning" in t:
        return random.choice(GOOD_MORNING)

    if "good afternoon" in t:
        return random.choice(GOOD_AFTERNOON)

    if "good evening" in t:
        return random.choice(GOOD_EVENING)

    if "good night" in t or "goodnight" in t:
        return random.choice(GOOD_NIGHT)

    # -----------------------------------------------------
    # BYE
    # -----------------------------------------------------

    if t in {
        "bye",
        "byee",
        "byeee",
        "bye bye",
        "goodbye",
        "good bye"
    }:
        return random.choice(BYE)

    # -----------------------------------------------------
    # CUTE ACTIONS
    # -----------------------------------------------------

    if t in {
        "hug",
        "hugg",
        "hug me"
    }:
        return random.choice(HUG)

    if t in {
        "kiss",
        "kiss me",
        "kisses"
    }:
        return random.choice(KISS)

    if t in {
        "umma",
        "ummma",
        "ummmaa"
    }:
        return random.choice(UMMA)

    if t in {
        "ummi",
        "ummii",
        "ummiii"
    }:
        return random.choice(UMMI)

    # -----------------------------------------------------
    # SHAYARI
    # -----------------------------------------------------

    if t in {
        "shayari",
        "shyari",
        "poetry",
        "sher"
    }:
        return random.choice(SHAYARI)

    if t in {
        "love shayari",
        "romantic shayari"
    }:
        return random.choice(LOVE_SHAYARI)

    if t in {
        "flirt shayari",
        "flirty shayari"
    }:
        return random.choice(FLIRT_SHAYARI)

    if t == "sad shayari":
        return random.choice(SAD_SHAYARI)

    # -----------------------------------------------------
    # FUN
    # -----------------------------------------------------

    if t in {
        "joke",
        "funny",
        "hasao",
        "hasi"
    }:
        return random.choice(FUNNY)

    if t in {
        "masti",
        "mastii"
    }:
        return random.choice(MASTI)

    if t == "roast":
        return random.choice(ROAST)

    if t in {
        "attitude",
        "swag"
    }:
        return random.choice(ATTITUDE)

    # -----------------------------------------------------
    # LOVE
    # -----------------------------------------------------

    if t in {
        "love",
        "pyaar",
        "i love you",
        "love you",
        "miss you",
        "miss u"
    }:
        return random.choice(LOVE)

    if t in {
        "babu",
        "baby",
        "sona",
        "shona",
        "jaan",
        "janu",
        "sweet",
        "sweetu"
    }:
        return random.choice(LOVE)

    # -----------------------------------------------------
    # FLIRT
    # -----------------------------------------------------

    if t in {
        "flirt",
        "flirting"
    }:
        return flirty_reply(t)

    if t in {
        "romantic",
        "romance"
    }:
        return random.choice(ROMANTIC)

    # -----------------------------------------------------
    # CUTE
    # -----------------------------------------------------

    if t in {
        "cute",
        "cutie"
    }:
        return random.choice(CUTE)

    # -----------------------------------------------------
    # SAD
    # -----------------------------------------------------

    if t in {
        "sad",
        "dukhi",
        "udaas",
        "alone"
    }:
        return random.choice(SAD)

    # -----------------------------------------------------
    # DEFAULT
    # Any normal message gets automatic reply.
    # -----------------------------------------------------

    return flirty_reply(t)
