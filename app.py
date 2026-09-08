import os
import time
from collections import defaultdict
from threading import Lock

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, request, render_template

from bot.replies import generate_reply

load_dotenv()

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "change-this")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN", "")
GRAPH_API_VERSION = os.getenv("GRAPH_API_VERSION", "v23.0")

OWNER_ID = os.getenv("OWNER_ID", "")
BOT_ID = os.getenv("BOT_ID", "")

GROUP_LINK = os.getenv(
    "GROUP_LINK",
    "https://t.me/Akatsuki_rulex"
)

RK_RAJA_IMAGE_URL = os.getenv(
    "RK_RAJA_IMAGE_URL",
    ""
)

BOT_ENABLED = os.getenv(
    "BOT_ENABLED",
    "true"
).lower() == "true"

START_TIME = time.time()

LOCKED_USERS = set()

STATS = defaultdict(int)

LIVE_USERS = {}

STATE_LOCK = Lock()


def log(message):
    app.logger.info(message)


def graph_url(path):
    return (
        f"https://graph.facebook.com/"
        f"{GRAPH_API_VERSION}/"
        f"{path.lstrip('/')}"
    )


def send_text(recipient_id, text):
    if not PAGE_ACCESS_TOKEN:
        log("PAGE_ACCESS_TOKEN missing.")
        return False

    try:
        r = requests.post(
            graph_url("me/messages"),
            params={
                "access_token": PAGE_ACCESS_TOKEN
            },
            json={
                "recipient": {
                    "id": recipient_id
                },
                "messaging_type": "RESPONSE",
                "message": {
                    "text": text
                }
            },
            timeout=15
        )

        if not r.ok:
            log(
                f"Graph error {r.status_code}: "
                f"{r.text[:300]}"
            )

        return r.ok

    except requests.RequestException as exc:
        log(f"Graph request error: {exc}")
        return False


def send_image(recipient_id, image_url):
    if not PAGE_ACCESS_TOKEN or not image_url:
        return False

    try:
        r = requests.post(
            graph_url("me/messages"),
            params={
                "access_token": PAGE_ACCESS_TOKEN
            },
            json={
                "recipient": {
                    "id": recipient_id
                },
                "messaging_type": "RESPONSE",
                "message": {
                    "attachment": {
                        "type": "image",
                        "payload": {
                            "url": image_url,
                            "is_reusable": True
                        }
                    }
                }
            },
            timeout=15
        )

        return r.ok

    except requests.RequestException:
        return False


# =========================================================
# LIVE USER TRACKING
# =========================================================

def track_user(sender_id, text):
    uid = str(sender_id)
    now = time.strftime("%H:%M:%S")

    with STATE_LOCK:
        old = LIVE_USERS.get(uid, {})

        LIVE_USERS[uid] = {
            "uid": uid,
            "messages": old.get("messages", 0) + 1,
            "last_message": str(text)[:120],
            "last_seen": now,
            "status": "LIVE"
        }


# =========================================================
# ADMIN COMMANDS
# =========================================================

def owner_command(sender_id, text):

    if not OWNER_ID:
        return False, None

    if str(sender_id) != str(OWNER_ID):
        return False, None

    t = " ".join(
        str(text).lower().split()
    )

    global BOT_ENABLED

    if t == "bot on":
        BOT_ENABLED = True
        return True, "🤖 BOT ONLINE 👍"

    if t == "bot off":
        BOT_ENABLED = False
        return True, "🛑 BOT OFF"

    if t.startswith("lock "):
        uid = t.split(maxsplit=1)[1].strip()

        if uid:
            LOCKED_USERS.add(uid)
            return True, "🔒 User locked."

    if t.startswith("unlock "):
        uid = t.split(maxsplit=1)[1].strip()

        if uid:
            LOCKED_USERS.discard(uid)
            return True, "🔓 User unlocked."

    if t == "locked":
        return True, (
            f"🔒 Locked users: "
            f"{len(LOCKED_USERS)}"
        )

    return False, None


# =========================================================
# MESSAGE HANDLER
# =========================================================

def handle_message(sender_id, text):

    global BOT_ENABLED

    if not BOT_ENABLED:
        return

    if str(sender_id) in LOCKED_USERS:
        return

    # Track every API-supported sender
    track_user(
        sender_id,
        text
    )

    handled, admin_reply = owner_command(
        sender_id,
        text
    )

    if handled:
        if admin_reply:
            send_text(
                sender_id,
                admin_reply
            )
        return

    t = " ".join(
        str(text).lower().strip().split()
    )

    # User-requested controlled sticker action
    if t in {
        "spam sticker",
        "sticker spam"
    }:
        send_text(
            sender_id,
            "🎨 Sticker mode requested 😜\n"
            "Controlled media action only; "
            "no unlimited flooding."
        )
        return

    # RK RAJA
    if (
        "rk raja" in t
        or t == "rkraja"
    ):

        if RK_RAJA_IMAGE_URL:
            send_image(
                sender_id,
                RK_RAJA_IMAGE_URL
            )

        send_text(
            sender_id,
            "🌙᯾🙂𝐁ɽ፝֟ɵ͜͡ƙ⃟ɛ͠ɳ💔ϯ•🕊️𝐇ɘ፝֟͜͡ʌ̴ʀ⃞ʈ🩷•ϯ\n\n"
            "Joine my gc Rk raja Family\n"
            f"{GROUP_LINK}"
        )

        return

    reply = generate_reply(text)

    if reply:
        send_text(
            sender_id,
            reply
        )

    with STATE_LOCK:
        STATS["messages"] += 1


# =========================================================
# DASHBOARD
# =========================================================

@app.get("/")
def index():
    return render_template(
        "index.html",
        bot_id=BOT_ID,
        admin_id=OWNER_ID
    )


# =========================================================
# HEALTH
# =========================================================

@app.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "bot_enabled": BOT_ENABLED,
        "uptime_seconds": int(
            time.time() - START_TIME
        )
    })


# =========================================================
# STATUS
# =========================================================

@app.get("/api/status")
def status():

    with STATE_LOCK:
        users = list(
            LIVE_USERS.values()
        )

        messages = STATS["messages"]

    return jsonify({
        "online": True,
        "bot_enabled": BOT_ENABLED,
        "messages": messages,
        "locked_users": len(LOCKED_USERS),
        "live_users": users,
        "bot_id": BOT_ID,
        "admin_id": OWNER_ID
    })


# =========================================================
# START / STOP
# =========================================================

@app.post("/api/bot/<action>")
def bot_action(action):

    global BOT_ENABLED

    if action == "start":
        BOT_ENABLED = True
        return jsonify({
            "ok": True,
            "bot_enabled": True
        })

    if action == "stop":
        BOT_ENABLED = False
        return jsonify({
            "ok": True,
            "bot_enabled": False
        })

    return jsonify({
        "ok": False,
        "error": "unknown action"
    }), 400


# =========================================================
# USER LOCK / UNLOCK
# =========================================================

@app.post("/api/user/<action>")
def user_action(action):

    data = (
        request.get_json(
            silent=True
        ) or {}
    )

    uid = str(
        data.get(
            "user_id",
            ""
        )
    ).strip()

    if not uid:
        return jsonify({
            "ok": False,
            "error": "user_id required"
        }), 400

    if action == "lock":
        LOCKED_USERS.add(uid)

        return jsonify({
            "ok": True
        })

    if action == "unlock":
        LOCKED_USERS.discard(uid)

        return jsonify({
            "ok": True
        })

    return jsonify({
        "ok": False,
        "error": "unknown action"
    }), 400


# =========================================================
# WEBHOOK VERIFY
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
    ):
        return (
            challenge or "",
            200
        )

    return "Forbidden", 403


# =========================================================
# WEBHOOK RECEIVE
# =========================================================

@app.post("/webhook")
def webhook_receive():

    payload = (
        request.get_json(
            silent=True
        ) or {}
    )

    if payload.get(
        "object"
    ) != "page":
        return (
            "EVENT_RECEIVED",
            200
        )

    for entry in payload.get(
        "entry",
        []
    ):

        for event in entry.get(
            "messaging",
            []
        ):

            sender = event.get(
                "sender",
                {}
            )

            sender_id = sender.get(
                "id"
            )

            message = event.get(
                "message",
                {}
            )

            text = message.get(
                "text"
            )

            if (
                sender_id
                and text
            ):
                log(
                    f"{sender_id}: {text}"
                )

                handle_message(
                    sender_id,
                    text
                )

    return (
        "EVENT_RECEIVED",
        200
    )


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(
            os.getenv(
                "PORT",
                "25042"
            )
        ),
        debug=False
    )
