import os
import random
from datetime import datetime

import requests
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

from bot.replies import generate_reply
from bot.fonts import stylish_text

load_dotenv()

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN", "")
OWNER_ID = os.getenv("OWNER_ID", "")

GRAPH_API_VERSION = os.getenv(
    "GRAPH_API_VERSION",
    "v23.0"
)

GROUP_LINK = os.getenv(
    "GROUP_LINK",
    "https://t.me/Akatsuki_rulex"
)

RK_RAJA_IMAGE_URL = os.getenv(
    "RK_RAJA_IMAGE_URL",
    ""
)

# Server start = bot ON
BOT_ENABLED = True

# Locked users
LOCKED_USERS = set()

# User statistics
USER_STATS = {}

STATS = {
    "messages_received": 0,
    "replies_sent": 0,
    "errors": 0,
    "started_at": datetime.utcnow().isoformat() + "Z",
    "last_message": "",
    "last_reply": ""
}

RK_RAJA_MESSAGE = f"""🌙᯾🙂𝐁ɽ፝֟ɵ͜͡ƙ⃟ɛ͠ɳ💔ϯ•🕊️𝐇ɘ፝֟͜͡ʌ̴ʀ⃞ʈ🩷•ϯ

Joine my gc Rk raja Family
{GROUP_LINK}"""


# ==================================================
# GRAPH API
# ==================================================

def graph_url(path):
    return (
        f"https://graph.facebook.com/"
        f"{GRAPH_API_VERSION}/{path}"
    )


def send_text(recipient_id, text):

    if not PAGE_ACCESS_TOKEN:
        print("PAGE_ACCESS_TOKEN missing")
        STATS["errors"] += 1
        return False

    payload = {
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": text
        },
        "access_token": PAGE_ACCESS_TOKEN
    }

    try:

        r = requests.post(
            graph_url("me/messages"),
            json=payload,
            timeout=20
        )

        print(
            "SEND TEXT:",
            r.status_code,
            r.text
        )

        if r.ok:
            STATS["replies_sent"] += 1
            STATS["last_reply"] = text
            return True

        STATS["errors"] += 1
        return False

    except requests.RequestException as e:

        print("SEND TEXT ERROR:", e)
        STATS["errors"] += 1
        return False


def send_image(recipient_id, image_url):

    if not PAGE_ACCESS_TOKEN:
        return False

    if not image_url:
        return False

    payload = {
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type": "image",
                "payload": {
                    "url": image_url,
                    "is_reusable": True
                }
            }
        },
        "access_token": PAGE_ACCESS_TOKEN
    }

    try:

        r = requests.post(
            graph_url("me/messages"),
            json=payload,
            timeout=20
        )

        print(
            "SEND IMAGE:",
            r.status_code,
            r.text
        )

        if not r.ok:
            STATS["errors"] += 1

        return r.ok

    except requests.RequestException as e:

        print("SEND IMAGE ERROR:", e)
        STATS["errors"] += 1
        return False


# ==================================================
# USER SYSTEM
# ==================================================

def get_user_stats(user_id):

    if user_id not in USER_STATS:

        USER_STATS[user_id] = {
            "messages": 0,
            "xp": 0
        }

    return USER_STATS[user_id]


def add_user_message(user_id):

    stats = get_user_stats(user_id)

    stats["messages"] += 1
    stats["xp"] += 10

    return stats


def user_level(xp):
    return (xp // 100) + 1


SHAYARI = [

    "Muskurahat ka koi mol nahi,\npar jiski wajah tum ho, woh pal anmol hai. ❤️",

    "Dil ki baat lafzon mein kaha nahi karte,\njo apne hain unhe bhula nahi karte. 🥀",

    "Kuch log kahani nahi,\nkhubsurat ehsaas ban jaate hain. ✨",

    "Mohabbat naam hai us ehsaas ka,\njisme khud se zyada fikr kisi aur ki hoti hai. ❤️",

    "Raat kitni bhi khamosh ho,\nsubah ek nayi kahani zaroor laati hai. 🌙",

    "Waqt badalta zaroor hai,\npar achhe log dil se kabhi nahi jaate. ❤️",

    "Kuch yaadein tasveer nahi hoti,\nphir bhi dil mein hamesha zinda rehti hain. 🌸",

    "Khamoshi bhi bahut kuch keh jaati hai,\nbas samajhne wala chahiye. 🌙"

]


def make_user_info(user_id):

    stats = get_user_stats(user_id)

    level = user_level(
        stats["xp"]
    )

    next_xp = level * 100

    remaining = max(
        0,
        next_xp - stats["xp"]
    )

    shayari = random.choice(
        SHAYARI
    )

    locked = user_id in LOCKED_USERS

    lock_status = (
        "🔒 LOCKED"
        if locked
        else
        "🔓 UNLOCKED"
    )

    return f"""👤 𝐔𝐒𝐄𝐑 𝐈𝐍𝐅𝐎

🆔 User ID:
{user_id}

⭐ Level:
{level}

✨ XP:
{stats["xp"]}

💬 Messages:
{stats["messages"]}

📈 Next Level:
{next_xp} XP

🔐 Message Status:
{lock_status}

✍️ 𝐒𝐡𝐚𝐲𝐚𝐫𝐢:

{shayari}"""


# ==================================================
# RK RAJA
# ==================================================

def is_rk_raja(text):

    text = text.lower()
    text = text.replace("_", " ")

    return (
        "rk raja" in text
        or "rkraja" in text
    )


# ==================================================
# REPLY
# ==================================================

def make_reply(text):

    reply = generate_reply(text)

    if random.random() < 0.35:
        reply = stylish_text(reply)

    return reply


# ==================================================
# OWNER COMMANDS
# ==================================================

def owner_command(sender_id, text):

    global BOT_ENABLED

    if not OWNER_ID:
        return False

    if str(sender_id) != str(OWNER_ID):
        return False

    command = text.strip().lower()

    # START
    if command == "/bot on":

        BOT_ENABLED = True

        send_text(
            sender_id,
            "🟢 𝐑𝐊 𝐑𝐀𝐉𝐀 𝐁𝐎𝐓 𝐒𝐓𝐀𝐑𝐓𝐄𝐃\n\n"
            "Automatic replies ON ✅"
        )

        return True

    # STOP
    if command == "/bot off":

        BOT_ENABLED = False

        send_text(
            sender_id,
            "🔴 𝐑𝐊 𝐑𝐀𝐉𝐀 𝐁𝐎𝐓 𝐒𝐓𝐎𝐏𝐏𝐄𝐃\n\n"
            "Automatic replies OFF 🛑"
        )

        return True

    # USER LOCK
    if command.startswith("/lock "):

        user_id = text.strip()[6:].strip()

        if not user_id:
            return True

        LOCKED_USERS.add(
            user_id
        )

        send_text(
            sender_id,
            f"🔒 User locked:\n{user_id}"
        )

        return True

    # USER UNLOCK
    if command.startswith("/unlock "):

        user_id = text.strip()[8:].strip()

        if not user_id:
            return True

        LOCKED_USERS.discard(
            user_id
        )

        send_text(
            sender_id,
            f"🔓 User unlocked:\n{user_id}"
        )

        return True

    # LIST LOCKED USERS
    if command == "/locked":

        if not LOCKED_USERS:

            send_text(
                sender_id,
                "🔓 Koi user locked nahi hai."
            )

        else:

            users = "\n".join(
                LOCKED_USERS
            )

            send_text(
                sender_id,
                "🔒 LOCKED USERS\n\n" + users
            )

        return True

    return False


# ==================================================
# MESSAGE HANDLER
# ==================================================

def handle_message(
    sender_id,
    text
):

    if not sender_id or not text:
        return

    text = text.strip()

    STATS["messages_received"] += 1
    STATS["last_message"] = text

    stats = add_user_message(
        sender_id
    )

    print()
    print("==============================")
    print("MESSAGE:", text)
    print("USER:", sender_id)
    print("LEVEL:", user_level(stats["xp"]))

    # Owner controls
    if owner_command(
        sender_id,
        text
    ):
        return

    # Bot stopped
    if not BOT_ENABLED:
        print("BOT OFF")
        return

    # User locked
    if sender_id in LOCKED_USERS:

        print(
            "USER LOCKED:",
            sender_id
        )

        return

    # /info
    if text.lower() == "/info":

        send_text(
            sender_id,
            make_user_info(
                sender_id
            )
        )

        return

    # RK Raja
    if is_rk_raja(text):

        if RK_RAJA_IMAGE_URL:

            send_image(
                sender_id,
                RK_RAJA_IMAGE_URL
            )

        send_text(
            sender_id,
            RK_RAJA_MESSAGE
        )

        return

    # Normal reply
    reply = make_reply(text)

    print(
        "BOT REPLY:",
        reply
    )

    send_text(
        sender_id,
        reply
    )


# ==================================================
# DASHBOARD
# ==================================================

@app.route("/")
def index():

    return render_template(
        "index.html"
    )


@app.route("/health")
def health():

    return jsonify({
        "status": "online",
        "bot": "RK RAJA BOT",
        "bot_enabled": BOT_ENABLED
    })


@app.route("/api/status")
def api_status():

    return jsonify({

        "bot": "RK RAJA BOT",

        "status":
            "RUNNING"
            if BOT_ENABLED
            else "STOPPED",

        "server": "ONLINE",

        "webhook": "READY",

        "messages_received":
            STATS["messages_received"],

        "replies_sent":
            STATS["replies_sent"],

        "users":
            len(USER_STATS),

        "locked_users":
            len(LOCKED_USERS),

        "errors":
            STATS["errors"],

        "last_message":
            STATS["last_message"],

        "last_reply":
            STATS["last_reply"],

        "started_at":
            STATS["started_at"]
    })


# ==================================================
# OWNER WEB DASHBOARD CONTROLS
# ==================================================

@app.route(
    "/api/bot/<action>",
    methods=["POST"]
)
def bot_control(action):

    global BOT_ENABLED

    # Browser dashboard se owner token verify
    owner_key = request.headers.get(
        "X-Owner-Key",
        ""
    )

    if not OWNER_ID:
        return jsonify({
            "ok": False,
            "error": "OWNER_ID not configured"
        }), 500

    if owner_key != OWNER_ID:
        return jsonify({
            "ok": False,
            "error": "Unauthorized"
        }), 403

    if action == "start":

        BOT_ENABLED = True

        return jsonify({
            "ok": True,
            "status": "RUNNING"
        })

    if action == "stop":

        BOT_ENABLED = False

        return jsonify({
            "ok": True,
            "status": "STOPPED"
        })

    return jsonify({
        "ok": False,
        "error": "Unknown action"
    }), 400


# ==================================================
# OWNER USER LOCK CONTROL
# ==================================================

@app.route(
    "/api/user/<action>",
    methods=["POST"]
)
def user_control(action):

    owner_key = request.headers.get(
        "X-Owner-Key",
        ""
    )

    if owner_key != OWNER_ID:

        return jsonify({
            "ok": False,
            "error": "Unauthorized"
        }), 403

    data = request.get_json(
        silent=True
    ) or {}

    user_id = str(
        data.get(
            "user_id",
            ""
        )
    ).strip()

    if not user_id:

        return jsonify({
            "ok": False,
            "error": "user_id required"
        }), 400

    if action == "lock":

        LOCKED_USERS.add(
            user_id
        )

    elif action == "unlock":

        LOCKED_USERS.discard(
            user_id
        )

    else:

        return jsonify({
            "ok": False,
            "error": "Unknown action"
        }), 400

    return jsonify({
        "ok": True,
        "user_id": user_id,
        "locked":
            user_id in LOCKED_USERS
    })


# ==================================================
# META WEBHOOK VERIFY
# ==================================================

@app.route(
    "/webhook",
    methods=["GET"]
)
def webhook_verify():

    mode = request.args.get(
        "hub.mode"
    )

    token = request.args.get(
        "hub.verify_token"
    )

    challenge = request.args.get(
        "hub.challenge"
    )

    if (
        mode == "subscribe"
        and token == VERIFY_TOKEN
    ):

        return challenge or "", 200

    return "Verification failed", 403


# ==================================================
# META WEBHOOK RECEIVE
# ==================================================

@app.route(
    "/webhook",
    methods=["POST"]
)
def webhook_receive():

    data = request.get_json(
        silent=True
    ) or {}

    print()
    print("WEBHOOK:")
    print(data)

    if data.get("object") != "page":

        return "EVENT_RECEIVED", 200

    for entry in data.get(
        "entry",
        []
    ):

        for messaging in entry.get(
            "messaging",
            []
        ):

            message = messaging.get(
                "message",
                {}
            )

            # Ignore Page echo
            if message.get(
                "is_echo"
            ):
                continue

            sender = messaging.get(
                "sender",
                {}
            )

            sender_id = sender.get(
                "id"
            )

            text = message.get(
                "text"
            )

            if sender_id and text:

                handle_message(
                    sender_id,
                    text
                )

    return "EVENT_RECEIVED", 200


# ==================================================
# LOCAL REPLY TEST API
# ==================================================

@app.route(
    "/api/reply",
    methods=["POST"]
)
def api_reply():

    data = request.get_json(
        silent=True
    ) or {}

    text = str(
        data.get(
            "text",
            ""
        )
    ).strip()

    if not text:

        return jsonify({
            "ok": False,
            "error": "Text required"
        }), 400

    return jsonify({
        "ok": True,
        "reply": make_reply(text)
    })


# ==================================================
# START SERVER
# ==================================================

if __name__ == "__main__":

    port = int(
        os.getenv(
            "PORT",
            "25042"
        )
    )

    print()
    print("==============================")
    print("      RK RAJA BOT")
    print("==============================")
    print("BOT: RUNNING")
    print("SERVER: ONLINE")
    print("PORT:", port)
    print("==============================")

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
