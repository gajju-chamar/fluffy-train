# Shinobu Music Bot
# Owner: @Sanji_fr

import asyncio

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtubesearchpython.__future__ import VideosSearch

import config
from config import BANNED_USERS, OWNER_ID
from strings import get_command, get_string
from Shinobu import YouTube, app
from Shinobu.misc import SUDOERS
from Shinobu.plugins.play.playlist import del_plist_msg
from Shinobu.plugins.sudo.sudoers import sudoers_list
from Shinobu.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_assistant,
    get_lang,
    get_userss,
    is_approved_chat,
    is_on_off,
    is_served_private_chat,
)
from Shinobu.utils.decorators.language import LanguageStart
from Shinobu.utils.inline import help_pannel, private_panel, start_pannel

loop = asyncio.get_event_loop()


@app.on_message(
    filters.command(get_command("START_COMMAND"))
    & filters.private
    
    & ~BANNED_USERS
)
@LanguageStart
async def start_comm(client, message: Message, _):
    await add_served_user(message.from_user.id)
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name[0:4] == "help":
            keyboard = help_pannel(_)
            return await message.reply_text(_["help_1"], reply_markup=keyboard)
        if name[0:4] == "song":
            return await message.reply_text(_["song_2"])
        if name[0:3] == "sta":
            m = await message.reply_text("🔎 Fetching your personal stats...")
            stats = await get_userss(message.from_user.id)
            tot = len(stats)
            if not stats:
                await asyncio.sleep(1)
                return await m.edit(_["ustats_1"])

            def get_stats():
                msg = ""
                limit = 0
                results = {}
                for i in stats:
                    results[str(i)] = stats[i]["spot"]
                list_arranged = dict(
                    sorted(results.items(), key=lambda item: item[1], reverse=True)
                )
                if not results:
                    return None, None
                tota = 0
                videoid = None
                for vidid, count in list_arranged.items():
                    tota += count
                    if limit == 0:
                        videoid = vidid
                    if limit < 10:
                        limit_inc = limit + 1
                        details = stats.get(vidid)
                        title = (details["title"][:35]).title()
                        msg += f"🔗 [{title}](https://www.youtube.com/watch?v={vidid}) **played {count} times**\n\n"
                    limit += 1
                msg = _["ustats_2"].format(tot, tota, min(limit, 10)) + msg
                return videoid, msg

            try:
                videoid, msg = await loop.run_in_executor(None, get_stats)
            except Exception as e:
                print(e)
                return
            await m.delete()
            await message.reply_text(msg)
            return
        if name[0:3] == "sud":
            await sudoers_list(client=client, message=message, _=_)
            return
        if name[0:3] == "lyr":
            query = (str(name)).replace("lyrics_", "", 1)
            lyrical = config.lyrical
            lyrics = lyrical.get(query)
            if lyrics:
                return await message.reply_text(lyrics)
            else:
                return await message.reply_text("Failed to get lyrics.")
        if name[0:3] == "del":
            await del_plist_msg(client=client, message=message, _=_)
        if name[0:3] == "inf":
            m = await message.reply_text("🔎 Fetching info...")
            query = f"https://www.youtube.com/watch?v={(str(name)).replace('info_', '', 1)}"
            results = VideosSearch(query, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
            searched_text = (
                f"🔍 **Video Track Information**\n\n"
                f"❇️ **Title:** {title}\n\n"
                f"⏳ **Duration:** {duration}\n"
                f"👀 **Views:** `{views}`\n"
                f"⏰ **Published:** {published}\n"
                f"🎥 **Channel:** [{channel}]({channellink})\n"
                f"🔗 **Link:** [Watch Here]({link})\n\n"
                f"⚡️ _Powered by {config.MUSIC_BOT_NAME}_"
            )
            key = InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="🔄 Close", callback_data="close")]]
            )
            await m.delete()
            await message.reply_text(
                searched_text, reply_markup=key, disable_web_page_preview=True
            )
    else:
        try:
            await app.resolve_peer(OWNER_ID[0])
            OWNER = OWNER_ID[0]
        except:
            OWNER = None
        out = private_panel(_, app.username, OWNER)
        await message.reply_text(
            _["start_2"].format(config.MUSIC_BOT_NAME),
            reply_markup=InlineKeyboardMarkup(out),
        )
        if await is_on_off(config.LOG):
            await app.send_message(
                config.LOG_GROUP_ID,
                f"{message.from_user.mention} started the bot.\n\n"
                f"**User ID:** {message.from_user.id}\n"
                f"**Name:** {message.from_user.first_name}",
            )


@app.on_message(
    filters.command(get_command("START_COMMAND"))
    & filters.group
    
    & ~BANNED_USERS
)
@LanguageStart
async def testbot(client, message: Message, _):
    out = start_pannel(_)
    return await message.reply_text(
        _["start_1"].format(message.chat.title, config.MUSIC_BOT_NAME),
        reply_markup=InlineKeyboardMarkup(out),
    )


welcome_group = 2


@app.on_message(filters.new_chat_members, group=welcome_group)
async def welcome(client, message: Message):
    chat_id = message.chat.id
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
            if member.id == app.id:
                chat_type = message.chat.type
                if chat_type != "supergroup":
                    await message.reply_text(_["start_6"])
                    return await app.leave_chat(message.chat.id)
                if chat_id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_7"].format(
                            f"https://t.me/{app.username}?start=sudolist"
                        )
                    )
                    return await app.leave_chat(chat_id)
                # Approve system — bot stays silent unless approved
                if not await is_approved_chat(chat_id):
                    await message.reply_text(
                        "This group is not approved to use me. "
                        "Please ask my owner to approve this chat via /approve."
                    )
                    return await app.leave_chat(chat_id)
                await add_served_chat(chat_id)
                userbot = await get_assistant(message.chat.id)
                out = start_pannel(_)
                await message.reply_text(
                    _["start_3"].format(
                        config.MUSIC_BOT_NAME,
                        userbot.username,
                        userbot.id,
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                )
            if member.id in config.OWNER_ID:
                return await message.reply_text(
                    _["start_4"].format(config.MUSIC_BOT_NAME, member.mention)
                )
            if member.id in SUDOERS:
                return await message.reply_text(
                    _["start_5"].format(config.MUSIC_BOT_NAME, member.mention)
                )
        except:
            return