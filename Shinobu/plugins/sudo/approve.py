# Shinobu Music Bot
# Owner: @Sanji_fr

from pyrogram import filters
from pyrogram.types import Message

from config import OWNER_ID
from Shinobu import app
from Shinobu.utils.database import (
    approve_chat,
    get_approved_chats,
    is_approved_chat,
    unapprove_chat,
)


@app.on_message(filters.command("approve") & filters.user(OWNER_ID))
async def approve_chat_func(client, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "**Usage:** `/approve <chat_id>`\n\nApproves a group to use Shinobu."
        )
    try:
        chat_id = int(message.text.strip().split()[1])
    except ValueError:
        return await message.reply_text("Invalid chat ID. Please provide a valid integer.")
    if await is_approved_chat(chat_id):
        return await message.reply_text(f"Chat `{chat_id}` is already approved.")
    await approve_chat(chat_id)
    await message.reply_text(f"Chat `{chat_id}` has been approved~ 🦋\n\nShinobu will now respond there.")


@app.on_message(filters.command("unapprove") & filters.user(OWNER_ID))
async def unapprove_chat_func(client, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "**Usage:** `/unapprove <chat_id>`\n\nRemoves a group's approval."
        )
    try:
        chat_id = int(message.text.strip().split()[1])
    except ValueError:
        return await message.reply_text("Invalid chat ID. Please provide a valid integer.")
    if not await is_approved_chat(chat_id):
        return await message.reply_text(f"Chat `{chat_id}` isn't approved to begin with.")
    await unapprove_chat(chat_id)
    await message.reply_text(f"Chat `{chat_id}` has been unapproved. Shinobu will go silent there.")


@app.on_message(filters.command("approvedchats") & filters.user(OWNER_ID))
async def approved_chats_list(client, message: Message):
    chats = await get_approved_chats()
    if not chats:
        return await message.reply_text("No approved chats yet.")
    text = "**Approved Chats:**\n\n"
    count = 0
    for chat_id in chats:
        count += 1
        try:
            chat = await app.get_chat(chat_id)
            title = chat.title
        except Exception:
            title = "Unknown"
        text += f"{count}➤ {title} [`{chat_id}`]\n"
    await message.reply_text(text)