from app import app
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "25042"))

    print("🤖 RK RAJA BOT STARTING...")
    print("✅ BOT IS ONLINE")
    print("♻️ BOT WILL KEEP RUNNING")

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False,
        threaded=True
    )
