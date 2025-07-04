from pyrogram import Client, filters
from pyrogram.types import Message
import os, json

API_ID = 23455230
API_HASH = "1740e4541ec18b9cdd3e5ff6f3687d46"
BOT_TOKEN = "7140345540:AAHYzt2feDZBS8GqSmeAlPA1lawUYEIP7Q8"

app = Client("demand_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

if not os.path.exists("users.json"):
    with open("users.json", "w") as f:
        json.dump([], f)

def save_user(user_id):
    with open("users.json", "r+") as f:
        users = json.load(f)
        if user_id not in users:
            users.append(user_id)
            f.seek(0)
            json.dump(users, f)
            f.truncate()

@app.on_message(filters.command("start") & filters.private)
async def start(client, message: Message):
    save_user(message.from_user.id)
    await message.reply_text(
        "**👋 Welcome to ᎮᏗᏒᏗᎴᎥᏕᏋ🚩**\n\n"
        "📩 Apna demand bhejo — hum try karenge wo jaldi se laane ka - 🎥 Video, 📚 Notes, 📄 PDF\n"
         "🔒 All requests are private\n"
         "👇 Just send your request now!\n"
    )

@app.on_message(filters.private & filters.text & ~filters.command(["start", "broadcast", "stats"]))
async def handle_demand(client, message: Message):
    demand = message.text
    await message.reply_text(
        f"✅ Your demand has been received!\n\n📝 *Request:* `{demand}`\n\nWe'll try to fulfill it soon. Stay tuned!",
        quote=True
    )

ADMIN_ID = 6332321765

@app.on_message(filters.command("broadcast") & filters.user(ADMIN_ID))
async def broadcast_handler(client, message: Message):
    success, fail = 0, 0
    with open("users.json", "r") as f:
        users = json.load(f)

    for user_id in users:
        try:
            if message.reply_to_message:
                reply = message.reply_to_message
                if reply.text:
                    await client.send_message(user_id, reply.text)
                elif reply.photo:
                    await client.send_photo(user_id, reply.photo.file_id, caption=reply.caption or "")
                elif reply.document:
                    await client.send_document(user_id, reply.document.file_id, caption=reply.caption or "")
                elif reply.video:
                    await client.send_video(user_id, reply.video.file_id, caption=reply.caption or "")
                elif reply.audio:
                    await client.send_audio(user_id, reply.audio.file_id, caption=reply.caption or "")
                else:
                    continue
            else:
                parts = message.text.split(None, 1)
                if len(parts) > 1:
                    await client.send_message(user_id, parts[1])
                else:
                    continue
            success += 1
        except:
            fail += 1

    await message.reply_text(f"📢 Broadcast Summary:\n✅ Sent: {success}\n❌ Failed: {fail}")

@app.on_message(filters.command("stats") & filters.user(ADMIN_ID))
async def show_stats(client, message: Message):
    with open("users.json", "r") as f:
        users = json.load(f)

    total = len(users)
    active = 0
    for user_id in users:
        try:
            await client.send_chat_action(user_id, "typing")
            active += 1
        except:
            continue

    blocked = total - active

    await message.reply_text(
        f"📊 **Bot Stats:**\n\n"
        f"👥 Total Users: {total}\n"
        f"✅ Active: {active}\n"
        f"❌ Blocked/Inactive: {blocked}"
    )

app.run()
