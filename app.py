import os
import asyncio
from flask import Flask, render_template, request, send_file, abort
from telethon import TelegramClient
from dotenv import load_dotenv

# ---------------- LOAD ENV ----------------
load_dotenv()
API_ID = os.getenv("TG_API_ID")
API_HASH = os.getenv("TG_API_HASH")

if not API_ID or not API_HASH:
    raise RuntimeError("Telegram API credentials missing")

# ---------------- APP CONFIG ----------------
app = Flask(__name__)
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# ---------------- TELEGRAM CLIENT ----------------
client = TelegramClient("tg_session", int(API_ID), API_HASH)

# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/fetch", methods=["POST"])
def fetch_info():
    link = request.form.get("link")
    if not link:
        abort(400, "No link provided")

    try:
        qualities = asyncio.run(get_video_qualities(link))
        return render_template("index.html", qualities=qualities, link=link)

    except Exception as e:
        abort(400, str(e))


@app.route("/download", methods=["POST"])
def download():
    link = request.form.get("link")
    quality = request.form.get("quality")

    if not link or not quality:
        abort(400, "Invalid request")

    try:
        path = asyncio.run(download_video(link, quality))
        return send_file(path, as_attachment=True)

    except Exception as e:
        abort(500, str(e))


# ---------------- CORE LOGIC ----------------
async def get_video_qualities(link):
    async with client:
        msg = (await client.get_messages(link, limit=1))[0]

        if not msg.video:
            raise ValueError("No video found in link")

        qualities = []
        for attr in msg.video.attributes:
            if hasattr(attr, "w"):
                qualities.append(f"{attr.h}p")

        return list(set(qualities))


async def download_video(link, quality):
    async with client:
        msg = (await client.get_messages(link, limit=1))[0]

        for video in msg.video.alternative_videos:
            if f"{video.height}p" == quality:
                return await client.download_media(video, DOWNLOAD_DIR)

        return await client.download_media(msg.video, DOWNLOAD_DIR)


# ---------------- MAIN ----------------
if __name__ == "__main__":
    app.run(debug=True)
