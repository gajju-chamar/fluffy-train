# Shinobu Music Bot
# Owner: @Sanji_fr

import asyncio

from pyrogram import filters
from pyrogram.types import CallbackQuery, Message

from config import BANNED_USERS, MUSIC_BOT_NAME, adminlist
from strings import get_command
from Shinobu import app
from Shinobu.core.call import Shinobu
from Shinobu.misc import db
from Shinobu.utils.database import get_authuser_names, get_cmode
from Shinobu.utils.decorators import ActualAdminCB, AdminActual, language
from Shinobu.utils.formatters import alpha_to_int

RELOAD_COMMAND = get_command("RELOAD_COMMAND")
RESTART_COMMAND = get_command("RESTART_COMMAND")


@app.on_message(
    filters.command(RELOAD_COMMAND)
    & filters.group
    
    & ~BANNED_USERS
)
@language
async def reload_admin_cache(client, message: Message, _):
    try:
        chat_id = message.chat.id
        admins = await app.get_chat_members(chat_id, filter="administrators")
        authusers = await get_authuser_names(chat_id)
        adminlist[chat_id] = []
        for user in admins:
            if user.can_manage_voice_chats:
                adminlist[chat_id].append(user.user.id)
        for user in authusers:
            user_id = await alpha_to_int(user)
            adminlist[chat_id].append(user_id)
        await message.reply_text(_["admin_20"])
    except:
        await message.reply_text(
            "Failed to reload admin cache. Make sure the bot is an admin in this chat."
        )


@app.on_message(
    filters.command(RESTART_COMMAND)
    & filters.group
    
    & ~BANNED_USERS
)
@AdminActual
async def restartbot(client, message: Message, _):
    mystic = await message.reply_text(
        f"Please wait, restarting {MUSIC_BOT_NAME} for your chat..."
    )
    await asyncio.sleep(1)
    try:
        db[message.chat.id] = []
        await Shinobu.stop_stream(message.chat.id)
    except:
        pass
    chat_id = await get_cmode(message.chat.id)
    if chat_id:
        try:
            await app.get_chat(chat_id)
        except:
            pass
        try:
            db[chat_id] = []
            await Shinobu.stop_stream(chat_id)
        except:
            pass
    return await mystic.edit_text("Restarted successfully. Try playing now!")


@app.on_callback_query(filters.regex("close") & ~BANNED_USERS)
async def close_menu(_, CallbackQuery):
    try:
        await CallbackQuery.message.delete()
        await CallbackQuery.answer()
    except:
        return