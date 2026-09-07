import random
import re


REPLIES = {

    "hello": [
        "Hello ji 😂 kya haal hai?",
        "Hii 😎 aaj ka kya scene hai?",
        "Ohooo entry ho gayi 😂",
        "Hello boss 👑 bolo kya hukum hai?",
        "Hii ji ❤️ bot present hai.",
        "Namaste ji 🙏 chai piyoge? 😂",
        "Hello 😂 itni der se kahan the?",
        "Hii 😁 mood mast lag raha hai.",
        "Welcome boss 😎",
        "Hello ji 🌸 kya chal raha hai?"
    ],

    "love": [
        "Pyaar? 😂 Pehle chocolate lao ❤️",
        "Love sunte hi processor sharma gaya 😂❤️",
        "Dil already busy hai 😎❤️",
        "Pyaar dangerous hai bhai 😂",
        "Mohabbat ka server kabhi-kabhi down hota hai 😭",
        "Love hai to proof do 😂",
        "Dil sambhal ke rakhna ❤️",
        "Pyaar mein RAM bhi full ho jaati hai 😂",
        "Ishq ka network weak hai 😂",
        "Pyaar achha hai, WiFi bhi zaroori hai 😎"
    ],

    "baby": [
        "Baby bola? 😳 chocolate lao 😂",
        "Haan baby ji ❤️ kya hukum?",
        "Baby mode activated 😂",
        "Itna pyaar? Server garam ho gaya 😂",
        "Baby ji bolo 😎",
        "Aww baby 😂❤️",
        "Jaan bula diya 😭❤️",
        "Bot ko sharam aa rahi hai 😂",
        "Haan jaan 😎 kya scene?",
        "Baby naam se battery full ho gayi 😂"
    ],

    "joke": [
        "Battery 1% aur confidence 100% 😂",
        "Mummy: phone chhod do. Main: Maa career hai 😂",
        "Exam ka paper dekha, paper ne mujhe dekha... dono chup 😂",
        "WiFi gaya to family yaad aa gayi 😂",
        "Main diet par hoon... diet ko pata nahi 😂",
        "Alarm aur meri neend ki roz kushti hoti hai 😂",
        "Phone bola storage full, maine kaha memories hain 😂",
        "Monday ko dekhkar Sunday bhi ro deta hai 😂",
        "Mere jokes free hain, quality ka guarantee nahi 😂",
        "Online class mein camera off = invisible attendance 😂"
    ],

    "shayari": [
        "Dil diya tha sambhal ke rakhna,\nScreenshot lekar group mein bhej diya 😂❤️",
        "Teri yaadon mein hum kho gaye,\nWiFi mila to online ho gaye 😂",
        "Mohabbat ka zamana bhi ajeeb hai,\nSeen karke reply na dena naseeb hai 😂",
        "Dil toot gaya koi baat nahi,\nCharger mil gaya ab raat sahi 😂",
        "Aankhon mein sapne, haath mein phone,\nDil mein pyaar aur balance zero 😂",
        "Ishq mein hum barbaad hue,\nData pack bhi khatam hua 😂",
        "Tera message aaya to smile aa gayi,\nPhir dekha bank ka SMS tha 😂",
        "Mohabbat WiFi jaisi hai,\nSignal aaye to sab mast 😂",
        "Dil ki baat kehni thi,\nNetwork chala gaya 😂",
        "Tum mile to laga zindagi haseen hai,\nBill aaya to duniya rangeen hai 😂"
    ],

    "roast": [
        "Tera confidence dekhkar WiFi bhi jealous hai 😂",
        "Bhai tera logic loading mein atka hai 😂",
        "Attitude premium, performance trial version 😂",
        "Brain airplane mode mein hai kya? 😂",
        "Tera swag full, talent pending 😂",
        "Argument karna calculator se feelings discuss karne jaisa hai 😂",
        "Teri timing perfect hai... galat time par 😂",
        "Legend ho bhai, bas game mein nahi 😂",
        "Confidence unlimited data jaisa hai 😂",
        "Evidence abhi tak nahi mila 😂"
    ],

    "sad": [
        "Sad mat ho bhai ❤️ comeback karo.",
        "Mood off? Chai piyo ☕😂",
        "Dil halka karo ❤️",
        "Jo gaya usko jaane do 😎",
        "Tension logout karo 😂",
        "Bot tumhare saath hai ❤️",
        "Rona allowed hai, data waste mat karo 😂",
        "Kal better hoga bhai ❤️",
        "Sadness ko uninstall karo 😂",
        "Smile free hai 😁"
    ],

    "thanks": [
        "Welcome ji 😂",
        "Koi baat nahi boss 😎",
        "Mention not ❤️",
        "Welcome 😂 party kab?",
        "Thanks ka jawab samose se do 😂",
        "Arey welcome ji 😁",
        "Bot khush hua ❤️",
        "Itna thanks? Chocolate bhejo 😂",
        "Welcome boss 👑",
        "Koi dikkat nahi 😎"
    ],

    "bye": [
        "Bye 😂 jaldi wapas aana.",
        "Tata boss 😎",
        "Bye bye ❤️",
        "Jao bhai, bot wait karega 😂",
        "See you soon 😎",
        "Bye ji 🙏",
        "Kal phir milte hain 😂",
        "Goodbye boss ❤️",
        "Tata 😂",
        "Comeback zaroor karna 😎"
    ],

    "default": [
        "Bhai ye kya likh diya 😂",
        "Samajh nahi aaya, funny laga 😂",
        "Ek baar simple language mein bolo 😎",
        "Bot soch raha hai 🤔😂",
        "Message received 😂",
        "Kya scene hai bhai?",
        "Interesting message 😂",
        "Thoda context do boss 😎",
        "Processor confuse ho gaya 😂",
        "Aur batao ji ❤️"
    ]
}


KEYWORDS = {
    "hello": [
        "hello", "helo", "hlo", "hey",
        "namaste", "hi", "hii", "hiii"
    ],

    "love": [
        "love", "pyaar", "pyar",
        "mohabbat", "ishq", "crush"
    ],

    "baby": [
        "baby", "babu", "sona", "shona",
        "jaan", "janu", "babes"
    ],

    "joke": [
        "joke", "jokes", "funny",
        "majak", "mazak", "chutkula"
    ],

    "shayari": [
        "shayari", "shyari",
        "poetry", "sher"
    ],

    "roast": [
        "roast", "beizzati",
        "insult", "roast me"
    ],

    "sad": [
        "sad", "dukhi", "udaas",
        "dard", "breakup"
    ],

    "thanks": [
        "thanks", "thank",
        "thankyou", "shukriya"
    ],

    "bye": [
        "bye", "goodbye",
        "tata", "see you"
    ]
}


def clean_text(text):
    text = str(text or "").lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def detect_intent(text):
    text = clean_text(text)

    for intent, words in KEYWORDS.items():
        for word in words:
            if word in text:
                return intent

    if "?" in text:
        return "default"

    return "default"


def make_extra_funny(reply):
    endings = [
        "",
        " 😂",
        " 😎",
        " 🤣",
        " ❤️😂",
        " 😭😂",
        " 🔥😂",
        " 👑😂"
    ]

    prefixes = [
        "",
        "Bhai 😂 ",
        "Boss 😎 ",
        "Oho 😂 ",
        "Arey ji 😁 ",
        "Suno 😂 "
    ]

    if random.random() < 0.35:
        reply = random.choice(prefixes) + reply

    if random.random() < 0.40:
        reply += random.choice(endings)

    return reply


def generate_reply(text):
    intent = detect_intent(text)

    replies = REPLIES.get(
        intent,
        REPLIES["default"]
    )

    reply = random.choice(replies)

    return make_extra_funny(reply)
