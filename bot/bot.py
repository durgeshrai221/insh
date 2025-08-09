import os
import telebot
from flask import Flask, request, abort, jsonify
from dotenv import load_dotenv
from utils import encode_uid

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = os.getenv("BASE_URL")  # e.g., https://your-render-project.onrender.com

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not set in environment.")

if not BASE_URL:
    raise RuntimeError("BASE_URL not set in environment.")

bot = telebot.TeleBot(BOT_TOKEN)

# Create Flask app
app = Flask(__name__)


# Handle /start command
@bot.message_handler(commands=["start"])
def start_command(message):
    uid = encode_uid(message.chat.id)
    capture_url = f"{BASE_URL}/capture?uid={uid}"
    bot.send_message(message.chat.id, f"Click here to open camera: {capture_url}")

# Flask webhook route for Telegram
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return jsonify({"status": "ok"})

# Health check route
@app.route("/", methods=["GET"])
def index():
    return "Bot is running."

if __name__ == "__main__":

    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)