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


# =========================================================
# CONFIG
# =========================================================

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "change-this")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN", "")
GRAPH_API_VERSION = os.getenv("GRAPH_API_VERSION", "v23.0")

OWNER_ID = os.getenv("OWNER_ID", "")

GROUP_LINK = os.getenv(
    "GROUP_LINK",
    "https://t.me/Akatsuki_rulex"
)

RK_RAJA_IMAGE_URL = os.getenv(
    "RK_RAJA_IMAGE_URL",
    ""
)

BOT_ENABLED = (
    os.getenv("BOT_ENABLED", "true").lower() == "true"
)


# =========================================================
# STATE
# =========================================================

LOCKED_USERS = set()

STATS = defaultdict(int)

STATE_LOCK = Lock()

START_TIME = time.time()


# =========================================================
# LOG
# =========================================================

def log(message):
    app.logger.info(message)


# =========================================================
# GRAPH API
# =========================================================

def graph_url(path):
    return (
        f"https://graph.facebook.com/"
        f"{GRAPH_API_VERSION}/"
        f"{path.lstrip('/')}"
    )


# =========================================================
# SEND TEXT
# =========================================================

def send_text(recipient_id, text):

    if not PAGE_ACCESS_TOKEN:
        log("PAGE_ACCESS_TOKEN missing.")
        return False

    try:

        response = requests.post(
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

        if not response.ok:

            log(
                f"Graph send error "
                f"{response.status_code}: "
                f"{response.text[:300]}"
            )

        return response.ok

    except requests.RequestException as exc:

        log(
            f"Graph request error: {exc}"
        )

        return False


# =========================================================
# SEND IMAGE
# =========================================================

def send_image(recipient_id, image_url):

    if not PAGE_ACCESS_TOKEN:
        return False

    if not image_url:
        return False

    try:

        response = requests.post(

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

        if not response.ok:

            log(
                f"Image send error "
                f"{response.status_code}: "
                f"{response.text[:300]}"
            )

        return response.ok

    except requests.RequestException as exc:

        log(
            f"Image request error: {exc}"
        )

        return False


# =========================================================
# OWNER COMMANDS
#
# Admin UID panel mein nahi hai.
# OWNER_ID .env se aayega.
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


    # BOT ON
    if t == "bot on":

        BOT_ENABLED = True

        return True, (
            "🤖 BOT ONLINE 👍"
        )


    # BOT OFF
    if t == "bot off":

        BOT_ENABLED = False

        return True, (
            "🛑 BOT OFF"
        )


    # LOCK USER
    if t.startswith("lock "):

        uid = t.split(
            maxsplit=1
        )[1].strip()

        if not uid:
            return True, "⚠️ User ID missing."

        LOCKED_USERS.add(uid)

        return True, (
            "🔒 User locked successfully."
        )


    # UNLOCK USER
    if t.startswith("unlock "):

        uid = t.split(
            maxsplit=1
        )[1].strip()

        if not uid:
            return True, "⚠️ User ID missing."

        LOCKED_USERS.discard(uid)

        return True, (
            "🔓 User unlocked successfully."
        )


    # LOCKED LIST
    if t == "locked":

        return True, (
            f"🔒 Locked users: "
            f"{len(LOCKED_USERS)}"
        )


    return False, None


# =========================================================
# HANDLE MESSAGE
# =========================================================

def handle_message(sender_id, text):

    global BOT_ENABLED

    if not BOT_ENABLED:
        return


    # -----------------------------------------------------
    # LOCKED USER
    # -----------------------------------------------------

    if str(sender_id) in LOCKED_USERS:
        log(
            f"Ignored locked user: "
            f"{sender_id}"
        )
        return


    # -----------------------------------------------------
    # ADMIN COMMANDS
    # -----------------------------------------------------

    handled, owner_reply = owner_command(
        sender_id,
        text
    )

    if handled:

        if owner_reply:
            send_text(
                sender_id,
                owner_reply
            )

        return


    # -----------------------------------------------------
    # NORMALIZE TEXT
    # -----------------------------------------------------

    t = " ".join(
        str(text).lower().strip().split()
    )


    # -----------------------------------------------------
    # USER REQUESTED STICKER MODE
    #
    # No automatic flooding.
    # Actual sticker capability depends
    # on Meta API support.
    # -----------------------------------------------------

    if t in {
        "spam sticker",
        "sticker spam"
    }:

        send_text(
            sender_id,

            "🎨 Sticker mode requested 😜\n"
            "Controlled sticker/media action "
            "can be added when your Meta app "
            "supports the required media feature."
        )

        return


    # -----------------------------------------------------
    # RK RAJA TRIGGER
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # GENERATE NORMAL REPLY
    # -----------------------------------------------------

    reply = generate_reply(text)


    if reply:

        send_text(
            sender_id,
            reply
        )


    # -----------------------------------------------------
    # STATS
    # -----------------------------------------------------

    with STATE_LOCK:

        STATS["messages"] += 1

        STATS[
            str(sender_id)
        ] += 1


# =========================================================
# DASHBOARD
# =========================================================

@app.get("/")
def index():

    return render_template(
        "index.html"
    )


# =========================================================
# HEALTH
# =========================================================

@app.get("/health")
def health():

    return jsonify({

        "status": "ok",

        "bot_enabled":
            BOT_ENABLED,

        "uptime_seconds":
            int(
                time.time()
                - START_TIME
            )

    })


# =========================================================
# STATUS API
# =========================================================

@app.get("/api/status")
def status():

    with STATE_LOCK:

        message_count = (
            STATS["messages"]
        )

    return jsonify({

        "online": True,

        "bot_enabled":
            BOT_ENABLED,

        "messages":
            message_count,

        "locked_users":
            len(LOCKED_USERS)

    })


# =========================================================
# START / STOP
# =========================================================

@app.post("/api/bot/<action>")
def bot_action(action):

    global BOT_ENABLED


    if action == "start":

        BOT_ENABLED = True

        log(
            "Bot started from dashboard."
        )

        return jsonify({

            "ok": True,

            "bot_enabled": True

        })


    if action == "stop":

        BOT_ENABLED = False

        log(
            "Bot stopped from dashboard."
        )

        return jsonify({

            "ok": True,

            "bot_enabled": False

        })


    return jsonify({

        "ok": False,

        "error":
            "unknown action"

    }), 400


# =========================================================
# USER LOCK / UNLOCK
# =========================================================

@app.post("/api/user/<action>")
def user_action(action):

    data = (
        request.get_json(
            silent=True
        )
        or {}
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

            "error":
                "user_id required"

        }), 400


    if action == "lock":

        LOCKED_USERS.add(uid)

        return jsonify({

            "ok": True,

            "locked": True

        })


    if action == "unlock":

        LOCKED_USERS.discard(uid)

        return jsonify({

            "ok": True,

            "locked": False

        })


    return jsonify({

        "ok": False,

        "error":
            "unknown action"

    }), 400


# =========================================================
# META WEBHOOK VERIFY
# =========================================================

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

        return (
            challenge or "",
            200
        )


    return (
        "Forbidden",
        403
    )


# =========================================================
# META WEBHOOK RECEIVE
# =========================================================

@app.route(
    "/webhook",
    methods=["POST"]
)
def webhook_receive():

    payload = (
        request.get_json(
            silent=True
        )
        or {}
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
                    f"Message from "
                    f"{sender_id}: "
                    f"{text}"
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
