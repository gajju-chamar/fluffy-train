# Shinobu Music Bot
# Owner: @Sanji_fr
# Note: private.py is kept for compatibility but the approve system
# (approve.py) is the primary way to control which groups can use the bot.

from pyrogram import filters
from pyrogram.types import Message

from strings import get_command
from Shinobu import app
from Shinobu.misc import SUDOERS
from Shinobu.utils.database import (
    add_private_chat,
    get_private_served_chats,
    is_served_private_chat,
    remove_private_chat,
)
from Shinobu.utils.decorators.language import language

AUTHORIZE_COMMAND = get_command("AUTHORIZE_COMMAND")
UNAUTHORIZE_COMMAND = get_command("UNAUTHORIZE_COMMAND")
AUTHORIZED_COMMAND = get_command("AUTHORIZED_COMMAND")


@app.on_message(filters.command(AUTHORIZE_COMMAND) & SUDOERS)
@language
async def authorize(client, message: Message, _):
    if len(message.command) != 2:
        return await message.reply_text(_["pbot_1"])
    try:
        chat_id = int(message.text.strip().split()[1])
    except:
        return await message.reply_text(_["pbot_7"])
    if not await is_served_private_chat(chat_id):
        await add_private_chat(chat_id)
        await message.reply_text(_["pbot_3"])
    else:
        await message.reply_text(_["pbot_5"])


@app.on_message(filters.command(UNAUTHORIZE_COMMAND) & SUDOERS)
@language
async def unauthorize(client, message: Message, _):
    if len(message.command) != 2:
        return await message.reply_text(_["pbot_2"])
    try:
        chat_id = int(message.text.strip().split()[1])
    except:
        return await message.reply_text(_["pbot_7"])
    if not await is_served_private_chat(chat_id):
        return await message.reply_text(_["pbot_6"])
    await remove_private_chat(chat_id)
    return await message.reply_text(_["pbot_4"])


@app.on_message(filters.command(AUTHORIZED_COMMAND) & SUDOERS)
@language
async def authorized(client, message: Message, _):
    m = await message.reply_text(_["pbot_8"])
    served_chats = [int(c["chat_id"]) for c in await get_private_served_chats()]
    count = 0
    co = 0
    text = _["pbot_9"]
    msg = _["pbot_13"]
    for served_chat in served_chats:
        try:
            title = (await app.get_chat(served_chat)).title
            count += 1
            text += f"{count}: {title[:15]} [{served_chat}]\n"
        except Exception:
            co += 1
            msg += f"{co}: Unknown [{served_chat}]\n"
    if co == 0:
        return await m.edit(_["pbot_11"] if count == 0 else text)
    else:
        return await m.edit(text + msg if count > 0 else msg)