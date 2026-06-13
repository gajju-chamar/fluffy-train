# Shinobu Music Bot
# Owner: @Sanji_fr

import asyncio
from datetime import datetime, timedelta

from pyrogram import filters
from pyrogram.errors import FloodWait
from pyrogram.raw import types

import config
from config import adminlist, chatstats, clean, userstats
from strings import get_command
from Shinobu import app, userbot
from Shinobu.misc import SUDOERS
from Shinobu.utils.database import (
    get_active_chats,
    get_authuser_names,
    get_client,
    get_particular_top,
    get_served_chats,
    get_served_users,
    get_user_top,
    is_cleanmode_on,
    set_queries,
    update_particular_top,
    update_user_top,
)
from Shinobu.utils.decorators.language import language
from Shinobu.utils.formatters import alpha_to_int

BROADCAST_COMMAND = get_command("BROADCAST_COMMAND")
AUTO_DELETE = config.CLEANMODE_DELETE_MINS
AUTO_SLEEP = 5
IS_BROADCASTING = False
cleanmode_group = 15


@app.on_raw_update(group=cleanmode_group)
async def clean_mode(client, update, users, chats):
    global IS_BROADCASTING
    if IS_BROADCASTING:
        return
    try:
        if not isinstance(update, types.UpdateReadChannelOutbox):
            return
    except:
        return
    if users:
        return
    if chats:
        return
    message_id = update.max_id
    chat_id = int(f"-100{update.channel_id}")
    if not await is_cleanmode_on(chat_id):
        return
    if chat_id not in clean:
        clean[chat_id] = []
    time_now = datetime.now()
    put = {
        "msg_id": message_id,
        "timer_after": time_now + timedelta(minutes=AUTO_DELETE),
    }
    clean[chat_id].append(put)
    await set_queries(1)


@app.on_message(filters.command(BROADCAST_COMMAND) & SUDOERS)
@language
async def broadcast_message(client, message, _):
    global IS_BROADCASTING
    if message.reply_to_message:
        x = message.reply_to_message.message_id
        y = message.chat.id
    else:
        if len(message.command) < 2:
            return await message.reply_text(_["broad_5"])
        query = message.text.split(None, 1)[1]
        for flag in ("-pin", "-nobot", "-pinloud", "-assistant", "-user"):
            query = query.replace(flag, "")
        if not query.strip():
            return await message.reply_text(_["broad_6"])

    IS_BROADCASTING = True

    # Broadcast to chats via bot
    if "-nobot" not in message.text:
        sent = 0
        pin = 0
        chats = [int(c["chat_id"]) for c in await get_served_chats()]
        for i in chats:
            try:
                m = (
                    await app.forward_messages(i, y, x)
                    if message.reply_to_message
                    else await app.send_message(i, text=query)
                )
                if "-pin" in message.text:
                    try:
                        await m.pin(disable_notification=True)
                        pin += 1
                    except Exception:
                        continue
                elif "-pinloud" in message.text:
                    try:
                        await m.pin(disable_notification=False)
                        pin += 1
                    except Exception:
                        continue
                sent += 1
            except FloodWait as e:
                flood_time = int(e.x)
                if flood_time > 200:
                    continue
                await asyncio.sleep(flood_time)
            except Exception:
                continue
        try:
            await message.reply_text(_["broad_1"].format(sent, pin))
        except:
            pass

    # Broadcast to users via bot
    if "-user" in message.text:
        susr = 0
        served_users = [int(u["user_id"]) for u in await get_served_users()]
        for i in served_users:
            try:
                await (
                    app.forward_messages(i, y, x)
                    if message.reply_to_message
                    else app.send_message(i, text=query)
                )
                susr += 1
            except FloodWait as e:
                flood_time = int(e.x)
                if flood_time > 200:
                    continue
                await asyncio.sleep(flood_time)
            except Exception:
                pass
        try:
            await message.reply_text(_["broad_7"].format(susr))
        except:
            pass

    # Broadcast via assistant accounts
    if "-assistant" in message.text:
        aw = await message.reply_text(_["broad_2"])
        text = _["broad_3"]
        from Shinobu.core.userbot import assistants

        for num in assistants:
            sent = 0
            client = await get_client(num)
            async for dialog in client.iter_dialogs():
                try:
                    await (
                        client.forward_messages(dialog.chat.id, y, x)
                        if message.reply_to_message
                        else client.send_message(dialog.chat.id, text=query)
                    )
                    sent += 1
                except FloodWait as e:
                    flood_time = int(e.x)
                    if flood_time > 200:
                        continue
                    await asyncio.sleep(flood_time)
                except Exception as e:
                    continue
            text += _["broad_4"].format(num, sent)
        try:
            await aw.edit_text(text)
        except:
            pass

    IS_BROADCASTING = False


async def auto_clean():
    while not await asyncio.sleep(AUTO_SLEEP):
        try:
            for chat_id in chatstats:
                for dic in chatstats[chat_id]:
                    vidid = dic["vidid"]
                    title = dic["title"]
                    chatstats[chat_id].pop(0)
                    spot = await get_particular_top(chat_id, vidid)
                    next_spot = (spot["spot"] + 1) if spot else 1
                    new_spot = {"spot": next_spot, "title": title}
                    await update_particular_top(chat_id, vidid, new_spot)
            for user_id in userstats:
                for dic in userstats[user_id]:
                    vidid = dic["vidid"]
                    title = dic["title"]
                    userstats[user_id].pop(0)
                    spot = await get_user_top(user_id, vidid)
                    next_spot = (spot["spot"] + 1) if spot else 1
                    new_spot = {"spot": next_spot, "title": title}
                    await update_user_top(user_id, vidid, new_spot)
        except:
            continue
        try:
            for chat_id in clean:
                if chat_id == config.LOG_GROUP_ID:
                    continue
                for x in clean[chat_id]:
                    if datetime.now() > x["timer_after"]:
                        try:
                            await app.delete_messages(chat_id, x["msg_id"])
                        except FloodWait as e:
                            await asyncio.sleep(e.x)
                        except:
                            continue
        except:
            continue
        try:
            served_chats = await get_active_chats()
            for chat_id in served_chats:
                if chat_id not in adminlist:
                    adminlist[chat_id] = []
                    admins = await app.get_chat_members(
                        chat_id, filter="administrators"
                    )
                    for user in admins:
                        if user.can_manage_voice_chats:
                            adminlist[chat_id].append(user.user.id)
                    authusers = await get_authuser_names(chat_id)
                    for user in authusers:
                        user_id = await alpha_to_int(user)
                        adminlist[chat_id].append(user_id)
        except:
            continue


asyncio.create_task(auto_clean())