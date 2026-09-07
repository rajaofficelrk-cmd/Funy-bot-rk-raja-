import os
import random

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
GRAPH_API_VERSION = os.getenv("GRAPH_API_VERSION", "v23.0")

GROUP_LINK = os.getenv(
    "GROUP_LINK",
    "https://t.me/Akatsuki_rulex"
)

RK_RAJA_IMAGE_URL = os.getenv("RK_RAJA_IMAGE_URL", "")

# AppState is accepted only as configuration text.
# It is NOT used for Facebook login/session automation.
FBSTATE = ""

BOT_ENABLED = True


RK_RAJA_MESSAGE = f"""🌙᯾🙂𝐁ɽ፝֟ɵ͜͡ƙ⃟ɛ͠ɳ💔ϯ•🕊️𝐇ɘ፝֟͜͡ʌ̴ʀ⃞ʈ🩷•ϯ

Joine my gc Rk raja Family
{GROUP_LINK}"""


def graph_url(path):
    return f"https://graph.facebook.com/{GRAPH_API_VERSION}/{path}"


def send_text(recipient_id, text):
    if not PAGE_ACCESS_TOKEN:
        print("PAGE_ACCESS_TOKEN missing")
        return False

    url = graph_url("me/messages")

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
            url,
            json=payload,
            timeout=20
        )

        print(
            "SEND TEXT:",
            r.status_code,
            r.text
        )

        return r.ok

    except requests.RequestException as e:
        print("SEND TEXT ERROR:", e)
        return False


def send_image(recipient_id, image_url):
    if not PAGE_ACCESS_TOKEN:
        return False

    if not image_url:
        return False

    url = graph_url("me/messages")

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
            url,
            json=payload,
            timeout=20
        )

        print(
            "SEND IMAGE:",
            r.status_code,
            r.text
        )

        return r.ok

    except requests.RequestException as e:
        print("SEND IMAGE ERROR:", e)
        return False


def is_rk_raja(text):
    normalized = (
        text
        .lower()
        .strip()
        .replace("_", " ")
    )

    normalized = " ".join(normalized.split())

    return (
        "rk raja" in normalized
        or "rkraja" in normalized
    )


def owner_command(sender_id, text):
    global BOT_ENABLED

    if not OWNER_ID:
        return False

    if str(sender_id) != str(OWNER_ID):
        return False

    command = text.strip().lower()

    if command == "/bot off":
        BOT_ENABLED = False

        send_text(
            sender_id,
            "🛑 𝐑𝐊 𝐑𝐚𝐣𝐚 𝐁𝐨𝐭 𝐎𝐅𝐅 kar diya gaya hai, Owner."
        )

        return True

    if command == "/bot on":
        BOT_ENABLED = True

        send_text(
            sender_id,
            "✅ 𝐑𝐊 𝐑𝐚𝐣𝐚 𝐁𝐨𝐭 𝐎𝐍 kar diya gaya hai, Owner."
        )

        return True

    return False


def handle_message(sender_id, text):

    if not text:
        return

    # Owner ON/OFF
    if owner_command(sender_id, text):
        return

    # Bot disabled
    if not BOT_ENABLED:
        return

    # RK Raja trigger
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

    # Normal funny response
    reply = generate_reply(text)

    if random.random() < 0.35:
        reply = stylish_text(reply)

    send_text(
        sender_id,
        reply
    )


@app.route("/")
def index():
    return render_template(
        "index.html",
        bot_enabled=BOT_ENABLED
    )


@app.route("/health")
def health():
    return jsonify({
        "status": "online",
        "bot_enabled": BOT_ENABLED
    })


@app.route("/webhook", methods=["GET"])
def webhook_verify():

    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if (
        mode == "subscribe"
        and token == VERIFY_TOKEN
    ):
        return challenge or "", 200

    return "Verification failed", 403


@app.route("/webhook", methods=["POST"])
def webhook_receive():

    data = request.get_json(
        silent=True
    ) or {}

    print("WEBHOOK:", data)

    if data.get("object") != "page":
        return "Ignored", 200

    for entry in data.get("entry", []):

        for messaging in entry.get(
            "messaging",
            []
        ):

            sender = messaging.get(
                "sender",
                {}
            )

            sender_id = sender.get("id")

            message = messaging.get(
                "message",
                {}
            )

            text = message.get("text")

            if sender_id and text:

                handle_message(
                    sender_id,
                    text
                )

    return "EVENT_RECEIVED", 200


@app.route("/api/status")
def api_status():

    return jsonify({
        "bot": "RK Raja Bot",
        "enabled": BOT_ENABLED,
        "owner_configured": bool(OWNER_ID),
        "page_token_configured": bool(
            PAGE_ACCESS_TOKEN
        ),
        "fbstate_field": True
    })


@app.route("/api/fbstate", methods=["POST"])
def save_fbstate():

    global FBSTATE

    data = request.get_json(
        silent=True
    ) or {}

    value = data.get(
        "fbstate",
        ""
    )

    if not isinstance(value, str):
        return jsonify({
            "ok": False,
            "error": "Invalid AppState"
        }), 400

    # Keep it in server memory only.
    # Never print it or expose it through /api/status.
    FBSTATE = value.strip()

    return jsonify({
        "ok": True,
        "message": "AppState field received safely."
    })


@app.route("/api/reply", methods=["POST"])
def api_reply():

    data = request.get_json(
        silent=True
    ) or {}

    text = str(
        data.get("text", "")
    ).strip()

    if not text:
        return jsonify({
            "ok": False,
            "error": "Text required"
        }), 400

    reply = generate_reply(text)

    return jsonify({
        "ok": True,
        "reply": reply
    })


if __name__ == "__main__":

    port = int(
        os.getenv(
            "PORT",
            "5000"
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
