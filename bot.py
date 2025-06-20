
import os
import time
import requests
from pyrogram import Client, filters
from pyrogram.types import Message
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
STREAMTAPE_LOGIN = os.getenv("STREAMTAPE_LOGIN")
STREAMTAPE_API_KEY = os.getenv("STREAMTAPE_API_KEY")
BASE_URL = os.getenv("BASE_URL")  # e.g. https://yourdomain.com

app = Client("streamtape_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def upload_to_streamtape(file_path):
    try:
        res = requests.get("https://api.streamtape.com/file/ul",
                           params={"login": STREAMTAPE_LOGIN, "key": STREAMTAPE_API_KEY})
        upload_url = res.json()["result"]["url"]
        with open(file_path, "rb") as f:
            upload_res = requests.post(upload_url, files={"file1": f})
        result = upload_res.json()
        if result["status"] == 200:
            return result["result"]["id"]
        else:
            return None
    except:
        return None

@app.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply("👋 Send me a video and I'll upload it to Streamtape and give you a watch page link.")

@app.on_message(filters.video | filters.document)
async def handle_video(client, message: Message):
    m = await message.reply("📥 Downloading...")
    try:
        file_path = await client.download_media(message)
        await m.edit("☁️ Uploading to Streamtape...")
        streamtape_id = upload_to_streamtape(file_path)
        os.remove(file_path)
        if streamtape_id:
            await m.edit(f"✅ Uploaded!
🎬 Watch here: {BASE_URL}/watch/{streamtape_id}")
        else:
            await m.edit("❌ Failed to upload to Streamtape.")
    except Exception as e:
        await m.edit(f"❌ Error: {e}")

app.run()
