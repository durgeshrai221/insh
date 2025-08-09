# bot/bot.py
import os
import logging
from dotenv import load_dotenv
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils import encode_uid

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
RENDER_BASE_URL = os.getenv("RENDER_BASE_URL")  # e.g. https://your-app.onrender.com

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not set in environment")

if not RENDER_BASE_URL:
    logging.warning("RENDER_BASE_URL not set. Links will be examples until you set it.")

bot = telebot.TeleBot(BOT_TOKEN, threaded=True)
logging.basicConfig(level=logging.INFO)

@bot.message_handler(commands=['start'])
def handle_start(message):
    name = message.from_user.first_name or "User"
    markup = InlineKeyboardMarkup()
    btn = InlineKeyboardButton("Generate Capture Link", callback_data="generate_link")
    markup.add(btn)

    bot.send_message(
        message.chat.id,
        f"Hello {name}!\nPress the button to get a personal capture link (camera + mic).",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda c: c.data == "generate_link")
def handle_generate_link(call):
    chat_id = call.from_user.id
    encoded = encode_uid(str(chat_id))
    base = RENDER_BASE_URL or "https://example.com"
    link = f"{base}/capture?uid={encoded}"
    bot.send_message(call.message.chat.id, f"Your capture link:\n{link}")
    bot.answer_callback_query(call.id)

if __name__ == "__main__":
    logging.info("Bot polling started")
    bot.infinity_polling()
