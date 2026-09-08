import os
import time
import requests

from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

from replies import generate_reply

load_dotenv()

app = Flask(__name__)

STARTED_AT = time.time()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "change-this")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN", "")
GRAPH_API_VERSION = os.getenv("GRAPH_API_VERSION", "v23.0")

BOT_ENABLED = os.getenv("BOT_ENABLED", "true").lower() == "true"
ADMIN_ID = os.getenv("OWNER_ID", "")
GROUP_LINK = os.getenv(
    "GROUP_LINK",
    "https://t.me/Akatsuki_rulex"
)

LIVE_USERS = {}
LOGS = []

CONFIG = {
    "admin_id": ADMIN_ID,
    "fight_file": "",
    "appstate_configured": False,
}


# -------------------------
# LOGGING
# -------------------------

def add_log(message):
    LOGS.insert(0, {
        "time": time.strftime("%H:%M:%S"),
        "message": str(message)
    })

    del LOGS[100:]


# -------------------------
# USER TRACKING
# -------------------------

def track_user(sender_id, text):
    now = time.strftime("%Y-%m-%d %H:%M:%S")

    user = LIVE_USERS.setdefault(
        sender_id,
        {
            "messages": 0,
            "last_message": "",
            "last_seen": ""
        }
    )

    user["messages"] += 1
    user["last_message"] = text[:200]
    user["last_seen"] = now


# -------------------------
# SEND MESSAGE
# -------------------------

def send_text(recipient_id, text):

    if not PAGE_ACCESS_TOKEN:
        add_log(
            "Reply skipped: Page Access Token is not configured."
        )
        return False

    url = (
        f"https://graph.facebook.com/"
        f"{GRAPH_API_VERSION}/me/messages"
    )

    payload = {
        "recipient": {
            "id": recipient_id
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
            timeout=15
        )

        success = (
            200 <= response.status_code < 300
        )

        if success:
            add_log(
                f"✅ Message sent -> {recipient_id}"
            )
        else:
            add_log(
                f"❌ Send failed -> "
                f"{response.status_code}"
            )

        return success

    except requests.RequestException as exc:

        add_log(
            f"❌ Send error: {exc}"
        )

        return False


# -------------------------
# DASHBOARD
# -------------------------

@app.get("/")
def dashboard():
    return render_template("index.html")


# -------------------------
# HEALTH CHECK
# -------------------------

@app.get("/health")
def health():

    return jsonify({
        "status": "online",
        "bot_enabled": BOT_ENABLED,
        "uptime_seconds": int(
            time.time() - STARTED_AT
        )
    })


# -------------------------
# STATUS API
# -------------------------

@app.get("/api/status")
def status():

    users = [
        {
            "uid": uid,
            **data
        }
        for uid, data
        in list(LIVE_USERS.items())[:100]
    ]

    total_messages = sum(
        user["messages"]
        for user in LIVE_USERS.values()
    )

    return jsonify({

        "online": True,

        "enabled": BOT_ENABLED,

        "uptime_seconds": int(
            time.time() - STARTED_AT
        ),

        "users": len(LIVE_USERS),

        "messages": total_messages,

        "admin_id": CONFIG["admin_id"],

        "fight_file": CONFIG["fight_file"],

        "appstate_configured":
            CONFIG["appstate_configured"],

        "users_data": users,

        "logs": LOGS[:50]
    })


# -------------------------
# START / STOP
# -------------------------

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
            "enabled": True
        })

    if action == "stop":

        BOT_ENABLED = False

        add_log(
            "🔴 BOT STOPPED"
        )

        return jsonify({
            "ok": True,
            "enabled": False
        })

    return jsonify({
        "ok": False,
        "error": "Unknown action"
    }), 400


# -------------------------
# ADMIN UID
# -------------------------

@app.post("/api/admin")
def save_admin():

    global ADMIN_ID

    data = (
        request.get_json(
            silent=True
        )
        or {}
    )

    ADMIN_ID = str(
        data.get(
            "admin_id",
            ""
        )
    ).strip()

    CONFIG["admin_id"] = ADMIN_ID

    add_log(
        "👑 Admin UID updated"
    )

    return jsonify({
        "ok": True,
        "admin_id": ADMIN_ID
    })


# -------------------------
# DASHBOARD CONFIG
# -------------------------

@app.post("/api/config")
def save_config():

    data = (
        request.get_json(
            silent=True
        )
        or {}
    )

    CONFIG["fight_file"] = str(
        data.get(
            "fight_file",
            ""
        )
    ).strip()

    # AppState is only kept as a
    # dashboard configuration value.
    CONFIG["appstate_configured"] = bool(
        str(
            data.get(
                "appstate",
                ""
            )
        ).strip()
    )

    add_log(
        "⚙️ Dashboard configuration saved"
    )

    return jsonify({
        "ok": True,
        "config": CONFIG
    })


# -------------------------
# META WEBHOOK VERIFY
# -------------------------

@app.get("/webhook")
@app.get("/webhook/")
def verify_webhook():

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
        return challenge or ""

    return "Forbidden", 403


# -------------------------
# META WEBHOOK EVENTS
# -------------------------

@app.post("/webhook")
@app.post("/webhook/")
def webhook():

    data = (
        request.get_json(
            silent=True
        )
        or {}
    )

    for entry in data.get(
        "entry",
        []
    ):

        for event in entry.get(
            "messaging",
            []
        ):

            sender_id = (
                event
                .get("sender", {})
                .get("id")
            )

            message = event.get(
                "message",
                {}
            )

            text = message.get(
                "text",
                ""
            )

            if not sender_id:
                continue

            if not text:
                continue

            track_user(
                sender_id,
                text
            )

            add_log(
                f"📩 {sender_id}: {text}"
            )

            if not BOT_ENABLED:
                continue

            reply = generate_reply(
                text
            )

            if reply:
                send_text(
                    sender_id,
                    reply
                )

    return "EVENT_RECEIVED", 200


# -------------------------
# LOCAL START
# -------------------------

if __name__ == "__main__":

    port = int(
        os.getenv(
            "PORT",
            "25042"
        )
    )

    print(
        "🤖 RK RAJA BOT STARTING..."
    )

    print(
        "✅ BOT ONLINE"
    )

    print(
        "♻️ BOT WILL KEEP RUNNING "
        "WHILE HOST PROCESS IS ALIVE"
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False,
        threaded=True
    )
