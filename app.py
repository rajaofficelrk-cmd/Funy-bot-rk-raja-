import os
import time
import requests

from threading import Lock
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN", "")
GRAPH_API_VERSION = os.getenv("GRAPH_API_VERSION", "v23.0")

ADMIN_ID = os.getenv("OWNER_ID", "")

GROUP_LINK = os.getenv(
    "GROUP_LINK",
    "https://t.me/Akatsuki_rulex"
)

BOT_ENABLED = (
    os.getenv("BOT_ENABLED", "true").lower() == "true"
)

START_TIME = time.time()

LOCK = Lock()

LIVE_USERS = {}
LOGS = []

CONFIG = {
    "fight_file": "",
    "appstate_configured": False
}


# =========================================================
# LOG
# =========================================================

def add_log(text):
    with LOCK:
        LOGS.insert(0, {
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "text": text
        })

        del LOGS[100:]


# =========================================================
# MESSENGER SEND
# =========================================================

def send_text(uid, text):

    if not PAGE_ACCESS_TOKEN:
        add_log("❌ PAGE_ACCESS_TOKEN missing")
        return False

    url = (
        f"https://graph.facebook.com/"
        f"{GRAPH_API_VERSION}/me/messages"
    )

    payload = {
        "recipient": {
            "id": uid
        },
        "message": {
            "text": text
        },
        "messaging_type": "RESPONSE"
    }

    try:

        response = requests.post(
            url,
            params={
                "access_token": PAGE_ACCESS_TOKEN
            },
            json=payload,
            timeout=20
        )

        add_log(
            f"📤 SEND {uid} | HTTP {response.status_code}"
        )

        if not response.ok:
            add_log(
                f"❌ Meta: {response.text[:300]}"
            )

        return response.ok

    except Exception as e:

        add_log(
            f"❌ Send error: {str(e)}"
        )

        return False


# =========================================================
# LIVE USER TRACKING
# =========================================================

def track_user(uid, text):

    with LOCK:

        old = LIVE_USERS.get(uid, {})

        LIVE_USERS[uid] = {
            "uid": uid,
            "messages": old.get("messages", 0) + 1,
            "last_message": text[:150],
            "last_seen": time.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "status": "LIVE"
        }


# =========================================================
# REPLY ENGINE
# =========================================================

def make_reply(text):

    t = text.strip().lower()

    # HELP
    if t in {
        "help",
        "commands",
        "/help"
    }:
        return (
            "🤖 RK RAJA BOT\n\n"
            "💬 Normal message → automatic reply\n\n"
            "📚 Commands:\n"
            "help\n"
            "joke\n"
            "love\n"
            "baby\n"
            "babu\n"
            "sona\n"
            "shona\n"
            "jaan\n"
            "janu\n"
            "sad\n"
            "bye\n"
            "good morning\n"
            "good afternoon\n"
            "good evening\n"
            "good night"
        )

    # GREETINGS
    if t in {
        "hi",
        "hii",
        "hiii",
        "hello",
        "hey",
        "helo"
    }:
        return (
            "👀 Haan bolo 😌\n"
            "RK Raja Bot sun raha hai ❤️"
        )

    # MORNING
    if "good morning" in t:
        return (
            "🌅 Good Morning ❤️\n"
            "Aaj ka din mast rahe 😌"
        )

    # AFTERNOON
    if "good afternoon" in t:
        return (
            "☀️ Good Afternoon 😌\n"
            "Kya haal hai?"
        )

    # EVENING
    if "good evening" in t:
        return (
            "🌆 Good Evening ❤️\n"
            "Batao kya chal raha hai 😌"
        )

    # NIGHT
    if "good night" in t:
        return (
            "🌙 Good Night 😴❤️\n"
            "Sweet dreams!"
        )

    # BYE
    if t == "bye" or t.startswith("bye "):
        return "Bye ❤️ Phir milte hain 😌"

    # BOT BOT BOT
    if t.split().count("bot") >= 3:
        return (
            "😒 Sun raha hoon, "
            "behra nahi hoon main 😂"
        )

    # BOT
    if "bot" in t:
        return random_bot_reply()

    # RK RAJA
    if "rk raja" in t:
        return (
            "🌙᯾🙂𝐁ɽ፝֟ɵ͜͡ƙ⃟ɛ͠ɳ💔ϯ•"
            "🕊️𝐇ɘ፝֟͜͡ʌ̴ʀ⃞ʈ🩷•ϯ\n\n"
            "Joine my gc Rk raja Family\n"
            f"{GROUP_LINK}"
        )

    # LOVE NAMES
    if t in {
        "baby",
        "babu",
        "sona",
        "shona",
        "jaan",
        "janu"
    }:
        return (
            "😏 Haan bolo ❤️\n"
            "Itne pyaar se bula rahe ho "
            "toh sunna padega 😌"
        )

    # LOVE
    if t in {
        "love",
        "pyaar",
        "pyar"
    }:
        return (
            "❤️ Pyaar wali baat hai toh "
            "araam se bolo 😌"
        )

    # JOKE
    if t in {
        "joke",
        "jokes"
    }:
        return (
            "😂 Teacher: Homework kahan hai?\n"
            "Student: Sir, network problem thi 📶🤣"
        )

    # SAD
    if t in {
        "sad",
        "dukhi",
        "udaas"
    }:
        return (
            "🥺 Kya hua?\n"
            "Bolo, main sun raha hoon ❤️"
        )

    # THANKS
    if (
        "thank" in t
        or "thanks" in t
    ):
        return "😊 Welcome ❤️"

    # SORRY
    if "sorry" in t:
        return "😌 Koi baat nahi ❤️"

    # SLEEP
    if "sleep" in t or "so ja" in t:
        return (
            "😴 Haan jao ab,\n"
            "kal phir baat karenge ❤️"
        )

    # FOOD
    if any(x in t for x in [
        "khana",
        "food",
        "bhookh",
        "kha liya"
    ]):
        return (
            "🍕 Khana kha liya ya "
            "sirf bot ko message kar rahe ho? 😂"
        )

    # DEFAULT
    return (
        "👀 Achhaaa...\n"
        "Batao aur kya chal raha hai? 😌\n"
        "RK Raja Bot sun raha hai ❤️"
    )


def random_bot_reply():

    import random

    replies = [
        "👀 Haan bolo, RK RAJA sun raha hai 😌",
        "😂 Haan bhai, sun raha hoon.",
        "😏 Kya hua? Itne pyaar se BOT kyun bula rahe ho?",
        "🤣 Bot yahin hai, bolo kya kaam hai?",
        "👂 Sun raha hoon bhai, behra nahi hoon 😜",
        "🙄 Haan bolo, attendance laga rahe ho kya? 😂",
        "😏 RK RAJA yahin hai, baar-baar BOT bolne ki zarurat nahi."
    ]

    return random.choice(replies)


# =========================================================
# DASHBOARD
# =========================================================

@app.get("/")
def dashboard():

    return render_template(
        "index.html"
    )


# =========================================================
# HEALTH
# =========================================================

@app.get("/health")
def health():

    return jsonify({
        "online": True,
        "bot_enabled": BOT_ENABLED,
        "admin_id": ADMIN_ID
    })


# =========================================================
# STATUS API
# =========================================================

@app.get("/api/status")
def status():

    with LOCK:

        users = list(
            LIVE_USERS.values()
        )

        logs = list(
            LOGS[:50]
        )

    return jsonify({

        "online": True,

        "bot_enabled":
            BOT_ENABLED,

        "admin_id":
            ADMIN_ID,

        "messages":
            sum(
                u["messages"]
                for u in users
            ),

        "live_users":
            users,

        "logs":
            logs,

        "fight_file":
            CONFIG["fight_file"],

        "appstate_configured":
            CONFIG["appstate_configured"],

        "uptime":
            int(
                time.time() -
                START_TIME
            )
    })


# =========================================================
# START / STOP
# =========================================================

@app.post("/api/bot/<action>")
def bot_action(action):

    global BOT_ENABLED

    if action == "start":

        BOT_ENABLED = True

        add_log(
            "🟢 BOT STARTED"
        )

        return jsonify({
            "ok": True,
            "bot_enabled": True
        })

    if action == "stop":

        BOT_ENABLED = False

        add_log(
            "🔴 BOT STOPPED"
        )

        return jsonify({
            "ok": True,
            "bot_enabled": False
        })

    return jsonify({
        "ok": False,
        "error": "Invalid action"
    }), 400


# =========================================================
# ADMIN UID
# =========================================================

@app.post("/api/admin")
def save_admin():

    global ADMIN_ID

    data = (
        request.get_json(
            silent=True
        )
        or {}
    )

    admin_id = str(
        data.get(
            "admin_id",
            ""
        )
    ).strip()

    if not admin_id:

        return jsonify({
            "ok": False,
            "error": "Admin UID required"
        }), 400

    ADMIN_ID = admin_id

    add_log(
        "👤 Admin UID updated"
    )

    return jsonify({
        "ok": True,
        "admin_id": ADMIN_ID
    })


# =========================================================
# DASHBOARD CONFIG
# =========================================================

@app.post("/api/config")
def save_config():

    data = (
        request.get_json(
            silent=True
        )
        or {}
    )

    # AppState is NOT stored.
    # Only whether the UI field is non-empty
    # is recorded.

    if "appstate" in data:

        CONFIG[
            "appstate_configured"
        ] = bool(
            str(
                data["appstate"]
            ).strip()
        )

    if "fight_file" in data:

        CONFIG[
            "fight_file"
        ] = str(
            data["fight_file"]
        )[:200]

    add_log(
        "⚙️ Dashboard configuration updated"
    )

    return jsonify({
        "ok": True,
        "appstate_configured":
            CONFIG[
                "appstate_configured"
            ],
        "fight_file":
            CONFIG["fight_file"]
    })


# =========================================================
# META WEBHOOK VERIFY
# =========================================================

@app.get("/webhook")
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
        and challenge
    ):
        return challenge, 200

    return (
        "Verification failed",
        403
    )


# =========================================================
# META MESSENGER WEBHOOK
# =========================================================

@app.post("/webhook")
def webhook_receive():

    data = (
        request.get_json(
            silent=True
        )
        or {}
    )

    if data.get("object") != "page":

        return (
            "EVENT_RECEIVED",
            200
        )

    if not BOT_ENABLED:

        return (
            "EVENT_RECEIVED",
            200
        )

    for entry in data.get(
        "entry",
        []
    ):

        for event in entry.get(
            "messaging",
            []
        ):

            uid = (
                event
                .get("sender", {})
                .get("id")
            )

            message = (
                event
                .get("message", {})
            )

            text = message.get(
                "text",
                ""
            )

            if not uid or not text:
                continue

            text = text.strip()

            track_user(
                uid,
                text
            )

            add_log(
                f"📩 {uid}: {text}"
            )

            reply = make_reply(
                text
            )

            send_text(
                uid,
                reply
            )

    return (
        "EVENT_RECEIVED",
        200
    )


# =========================================================
# LOCAL START
# =========================================================

if __name__ == "__main__":

    port = int(
        os.getenv(
            "PORT",
            "25042"
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
)
