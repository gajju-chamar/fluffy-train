# Shinobu Music Bot
# Owner: @Sanji_fr

from pyrogram import filters
from pyrogram.types import Message

from strings import get_command, get_string
from Shinobu import app
from Shinobu.misc import SUDOERS
from Shinobu.utils.database import get_lang, is_maintenance, maintenance_off, maintenance_on

MAINTENANCE_COMMAND = get_command("MAINTENANCE_COMMAND")


@app.on_message(filters.command(MAINTENANCE_COMMAND) & SUDOERS)
async def maintenance(client, message: Message):
    try:
        language = await get_lang(message.chat.id)
        _ = get_string(language)
    except:
        _ = get_string("en")
    usage = _["maint_1"]
    if len(message.command) != 2:
        return await message.reply_text(usage)
    state = message.text.split(None, 1)[1].strip().lower()
    if state == "enable":
        if await is_maintenance():
            return await message.reply_text("Maintenance mode is already enabled.")
        await maintenance_on()
        await message.reply_text(_["maint_2"])
    elif state == "disable":
        if not await is_maintenance():
            return await message.reply_text("Maintenance mode is already disabled.")
        await maintenance_off()
        await message.reply_text(_["maint_3"])
    else:
        await message.reply_text(usage)