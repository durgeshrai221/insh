import os
from dotenv import load_dotenv
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils import encode_uid

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = os.getenv("BASE_URL")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not found in environment.")

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Generate Capture Link", callback_data="gen_link"))
    bot.send_message(message.chat.id,
                     f"Hello {message.from_user.first_name}!\nPress the button to get a personal capture link (camera + mic).",
                     reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "gen_link")
def send_link(call):
    uid_enc = encode_uid(call.message.chat.id)
    link = f"{BASE_URL}/capture?uid={uid_enc}"
    bot.send_message(call.message.chat.id, f"Your capture link:\n{link}")

if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()
