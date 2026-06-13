# Shinobu Music Bot
# Owner: @Sanji_fr

from pyrogram import filters
from pyrogram.types import Message

from strings import get_command
from Shinobu import app
from Shinobu.misc import SUDOERS
from Shinobu.utils.database.memorydatabase import get_active_chats

ACTIVEVC_COMMAND = get_command("ACTIVEVC_COMMAND")


@app.on_message(filters.command(ACTIVEVC_COMMAND) & SUDOERS)
async def activevc(_, message: Message):
    mystic = await message.reply_text("Fetching active voice chats, please hold...")
    served_chats = await get_active_chats()
    text = ""
    j = 0
    for x in served_chats:
        try:
            chat = await app.get_chat(x)
            title = chat.title
        except Exception:
            title = "Private Group"
            chat = None
        if chat and chat.username:
            text += f"**{j + 1}.** [{title}](https://t.me/{chat.username}) [`{x}`]\n"
        else:
            text += f"**{j + 1}.** {title} [`{x}`]\n"
        j += 1
    if not text:
        await mystic.edit_text("No active voice chats right now.")
    else:
        await mystic.edit_text(
            f"**Active Voice Chats:**\n\n{text}",
            disable_web_page_preview=True,
        )