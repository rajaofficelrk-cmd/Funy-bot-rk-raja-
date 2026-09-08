import os
from app import app

if __name__ == "__main__":
    port = int(os.getenv("PORT", "25042"))

    print("🤖 RK RAJA BOT STARTING...")
    print("✅ BOT ONLINE")
    print(f"🌐 PORT: {port}")
    print("♻️ BOT RUNNING CONTINUOUSLY...")

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False,
        threaded=True
    )
