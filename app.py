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

BOT_ID = os.getenv("BOT_ID", "YOUR_BOT_ID")
ADMIN_ID = os.getenv("OWNER_ID", "YOUR_ADMIN_ID")
GROUP_LINK = os.getenv(
    "GROUP_LINK",
    "https://t.me/Akatsuki_rulex"
)

BOT_ENABLED = os.getenv(
    "BOT_ENABLED", "true"
).lower() == "true"

START_TIME = time.time()
LOCK = Lock()

LIVE_USERS = {}
LOGS = []
CONFIG = {
    "fight_file": "",
    "appstate_configured": False
}


def add_log(text):
    with LOCK:
        LOGS.insert(0, {
            "time": time.strftime("%H:%M:%S"),
            "text": text
        })
        del LOGS[100:]


def send_text(uid, text):
    if not PAGE_ACCESS_TOKEN:
        add_log("❌ PAGE_ACCESS_TOKEN missing")
        return False

    url = (
        f"https://graph.facebook.com/"
        f"{GRAPH_API_VERSION}/me/messages"
    )

    payload = {
        "recipient": {"id": uid},
        "message": {"text": text},
        "messaging_type": "RESPONSE"
    }

    try:
        r = requests.post(
            url,
            params={"access_token": PAGE_ACCESS_TOKEN},
            json=payload,
            timeout=20
        )

        add_log(f"📤 {uid}: {r.status_code}")
        return r.ok

    except Exception as e:
        add_log(f"❌ Send error: {e}")
        return False


def track_user(uid, text):
    with LOCK:
        old = LIVE_USERS.get(uid, {})

        LIVE_USERS[uid] = {
            "uid": uid,
            "messages": old.get("messages", 0) + 1,
            "last_message": text[:120],
            "last_seen": time.strftime("%Y-%m-%d %H:%M:%S"),
            "status": "LIVE"
        }


def make_reply(text):
    t = text.strip().lower()

    if t in {"hi", "hii", "hello", "hey"}:
        return "👀 Haan bolo 😌 RK Raja Bot sun raha hai."

    if "good morning" in t:
        return "🌅 Good Morning ❤️ Aaj ka din mast rahe!"

    if "good afternoon" in t:
        return "☀️ Good Afternoon 😌 Kya haal hai?"

    if "good evening" in t:
        return "🌆 Good Evening ❤️ Batao kya chal raha hai?"

    if "good night" in t:
        return "🌙 Good Night 😴 Sweet dreams ❤️"

    if t == "bye" or t.startswith("bye "):
        return "Bye ❤️ Phir milte hain 😌"

    if t.count("bot") >= 3:
        return "😒 Sun raha hoon, behra nahi hoon main 😂"

    if "bot" in t:
        return "👀 Haan bolo, RK RAJA yahin hai 😌"

    if "rk raja" in t:
        return (
            "🌙᯾🙂𝐁ɽ፝֟ɵ͜͡ƙ⃟ɛ͠ɳ💔ϯ•🕊️𝐇ɘ፝֟͜͡ʌ̴ʀ⃞ʈ🩷•ϯ\n\n"
            "Joine my gc Rk raja Family\n"
            f"{GROUP_LINK}"
        )

    if t in {"joke", "jokes"}:
        return (
            "😂 Teacher: Homework kahan hai?\n"
            "Student: Sir, network problem thi 📶🤣"
        )

    if t in {"love", "pyaar"}:
        return "❤️ Pyaar wali baat hai toh araam se bolo 😌"

    if t in {"baby", "babu", "sona", "shona", "jaan", "janu"}:
        return "😏 Haan bolo, itne pyaar se bula rahe ho toh sunna padega ❤️"

    if t in {"sad", "dukhi"}:
        return "🥺 Kya hua? Bolo, main sun raha hoon."

    if t in {"help", "commands"}:
        return (
            "🤖 RK RAJA BOT\n\n"
            "help • joke • love • baby • jaan\n"
            "good morning • good afternoon\n"
            "good evening • good night • bye\n\n"
            "Normal message bhi bhejo 😌"
        )

    if "thank" in t:
        return "😊 Welcome ❤️"

    if "sorry" in t:
        return "😌 Koi baat nahi."

    return (
        "👀 Achhaaa... batao aur kya chal raha hai? 😌\n"
        "RK Raja Bot sun raha hai ❤️"
    )


@app.get("/")
def dashboard():
    return render_template("index.html")


@app.get("/health")
def health():
    return jsonify({
        "online": True,
        "bot_enabled": BOT_ENABLED,
        "bot_id": BOT_ID
    })


@app.get("/api/status")
def status():
    return jsonify({
        "online": True,
        "bot_enabled": BOT_ENABLED,
        "bot_id": BOT_ID,
        "admin_id": ADMIN_ID,
        "messages": sum(
            u["messages"] for u in LIVE_USERS.values()
        ),
        "live_users": list(LIVE_USERS.values()),
        "logs": LOGS[:50],
        "fight_file": CONFIG["fight_file"],
        "appstate_configured": CONFIG["appstate_configured"],
        "uptime": int(time.time() - START_TIME)
    })


@app.post("/api/bot/<action>")
def bot_action(action):
    global BOT_ENABLED

    if action == "start":
        BOT_ENABLED = True
        add_log("🟢 Bot STARTED")
        return jsonify(ok=True, bot_enabled=True)

    if action == "stop":
        BOT_ENABLED = False
        add_log("🔴 Bot STOPPED")
        return jsonify(ok=True, bot_enabled=False)

    return jsonify(ok=False), 400


@app.post("/api/config")
def save_config():
    data = request.get_json(silent=True) or {}

    # AppState value is deliberately NOT stored or executed.
    if "appstate" in data:
        CONFIG["appstate_configured"] = bool(
            str(data["appstate"]).strip()
        )

    if "fight_file" in data:
        CONFIG["fight_file"] = str(
            data["fight_file"]
        )[:200]

    add_log("⚙️ Dashboard configuration updated")

    return jsonify({
        "ok": True,
        "appstate_configured":
            CONFIG["appstate_configured"],
        "fight_file":
            CONFIG["fight_file"]
    })


@app.get("/webhook")
def webhook_verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if (
        mode == "subscribe"
        and token == VERIFY_TOKEN
        and challenge
    ):
        return challenge, 200

    return "Verification failed", 403


@app.post("/webhook")
def webhook_receive():
    data = request.get_json(silent=True) or {}

    if data.get("object") != "page":
        return "EVENT_RECEIVED", 200

    if not BOT_ENABLED:
        return "EVENT_RECEIVED", 200

    for entry in data.get("entry", []):
        for event in entry.get("messaging", []):

            uid = event.get("sender", {}).get("id")
            message = event.get("message", {})
            text = message.get("text", "")

            if not uid or not text:
                continue

            text = text.strip()

            track_user(uid, text)
            add_log(f"📩 {uid}: {text}")

            reply = make_reply(text)
            send_text(uid, reply)

    return "EVENT_RECEIVED", 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", "25042"))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
