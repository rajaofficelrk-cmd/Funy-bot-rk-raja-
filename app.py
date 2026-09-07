from flask import Flask, request, render_template, jsonify
from bot.replies import generate_reply, detect_intent
from bot.fonts import stylish_text
import os
import requests

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "change-this")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN", "")
GRAPH_API_VERSION = os.getenv("GRAPH_API_VERSION", "v23.0")

GROUP_LINK = "https://t.me/Akatsuki_rulex"

RK_RAJAA_TEXT = f"""🌙᯾🙂💔ϯ•🕊️🩷•ϯ

RK Raja

💀 Joine my GC
RK Raja Family

👇 Join Here 👇
{GROUP_LINK}
"""


def send_text(recipient_id, text):
    url = (
        f"https://graph.facebook.com/"
        f"{GRAPH_API_VERSION}/me/messages"
    )

    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": text}
    }

    r = requests.post(
        url,
        params={"access_token": PAGE_ACCESS_TOKEN},
        json=payload,
        timeout=15
    )

    print("TEXT:", r.status_code, r.text)
    return r.ok


def send_image(recipient_id):
    image_url = os.getenv("RK_RAJA_IMAGE_URL")

    if not image_url:
        return False

    url = (
        f"https://graph.facebook.com/"
        f"{GRAPH_API_VERSION}/me/messages"
    )

    payload = {
        "recipient": {"id": recipient_id},
        "message": {
            "attachment": {
                "type": "image",
                "payload": {
                    "url": image_url,
                    "is_reusable": True
                }
            }
        }
    }

    r = requests.post(
        url,
        params={"access_token": PAGE_ACCESS_TOKEN},
        json=payload,
        timeout=15
    )

    print("IMAGE:", r.status_code, r.text)
    return r.ok


def handle_message(sender_id, message):

    text = message.lower().strip()

    # RK Raja trigger
    if "rk raja" in text or "rkraja" in text:
        send_image(sender_id)
        send_text(sender_id, RK_RAJAA_TEXT)
        return

    # Commands
    if text == "/joke":
        reply = generate_reply("joke")
    elif text == "/shayari":
        reply = generate_reply("shayari")
    elif text == "/love":
        reply = generate_reply("love")
    elif text == "/help":
        reply = (
            "🤖 RK Raja Bot\n\n"
            "/joke 😂\n"
            "/shayari ✨\n"
            "/love ❤️\n"
            "/gif 🎬\n"
            "/help ℹ️"
        )
    else:
        reply = generate_reply(message)

    # Random English Unicode font
    reply = stylish_text(reply)

    send_text(sender_id, reply)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/health")
def health():
    return jsonify({
        "status": "online",
        "bot": "RK Raja Bot"
    })


@app.route("/api/reply", methods=["POST"])
def api_reply():

    data = request.get_json(silent=True) or {}
    message = data.get("message", "")

    if not message:
        return jsonify({"error": "message required"}), 400

    reply = stylish_text(generate_reply(message))

    return jsonify({
        "bot": "RK Raja",
        "reply": reply
    })


@app.route("/webhook", methods=["GET", "POST"])
def webhook():

    if request.method == "GET":

        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200

        return "Verification failed", 403

    data = request.get_json(silent=True) or {}

    try:
        for entry in data.get("entry", []):
            for event in entry.get("messaging", []):

                sender_id = event.get("sender", {}).get("id")
                message = event.get("message", {})
                text = message.get("text")

                if sender_id and text:
                    handle_message(sender_id, text)

    except Exception as e:
        print("Webhook error:", e)

    return "EVENT_RECEIVED", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
