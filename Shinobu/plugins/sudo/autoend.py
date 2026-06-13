# Shinobu Music Bot
# Owner: @Sanji_fr

from pyrogram import filters

from strings import get_command
from Shinobu import app
from Shinobu.misc import SUDOERS
from Shinobu.utils.database import autoend_off, autoend_on

AUTOEND_COMMAND = get_command("AUTOEND_COMMAND")


@app.on_message(filters.command(AUTOEND_COMMAND) & SUDOERS)
async def auto_end_stream(client, message):
    usage = "**Usage:**\n\n/autoend [enable|disable]"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    state = message.text.split(None, 1)[1].strip().lower()
    if state == "enable":
        await autoend_on()
        await message.reply_text(
            "Auto end stream enabled. Bot will leave voice chat after 3 mins of inactivity."
        )
    elif state == "disable":
        await autoend_off()
        await message.reply_text("Auto end stream disabled.")
    else:
        await message.reply_text(usage)