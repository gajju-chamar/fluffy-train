# Shinobu Music Bot
# Owner: @Sanji_fr

import asyncio
import platform
from sys import version as pyver

import psutil
from pyrogram import __version__ as pyrover
from pyrogram import filters
from pyrogram.errors import MessageIdInvalid
from pyrogram.types import CallbackQuery, InputMediaPhoto, Message
from pytgcalls.__version__ import __version__ as pytgver

import config
from config import BANNED_USERS, MUSIC_BOT_NAME
from strings import get_command
from Shinobu import app
from Shinobu.core.userbot import assistants
from Shinobu.misc import SUDOERS, pymongodb
from Shinobu.plugins import ALL_MODULES
from Shinobu.utils.database import (
    get_global_tops,
    get_particulars,
    get_queries,
    get_served_chats,
    get_served_users,
    get_sudoers,
    get_top_chats,
    get_topp_users,
)
from Shinobu.utils.decorators.language import language, languageCB
from Shinobu.utils.inline.stats import (
    back_stats_buttons,
    back_stats_markup,
    get_stats_markup,
    overallback_stats_markup,
    stats_buttons,
    top_ten_stats_markup,
)

loop = asyncio.get_event_loop()

GSTATS_COMMAND = get_command("GSTATS_COMMAND")
STATS_COMMAND = get_command("STATS_COMMAND")

STATS_IMG = "assets/Stats.jpeg"
GLOBAL_IMG = "assets/Global.jpeg"


@app.on_message(
    filters.command(STATS_COMMAND)
    & filters.group
    & ~filters.edited
    & ~BANNED_USERS
)
@language
async def stats_global(client, message: Message, _):
    upl = stats_buttons(_, True if message.from_user.id in SUDOERS else False)
    await message.reply_photo(
        photo=STATS_IMG,
        caption=_["gstats_11"].format(config.MUSIC_BOT_NAME),
        reply_markup=upl,
    )


@app.on_message(
    filters.command(GSTATS_COMMAND)
    & filters.group
    & ~filters.edited
    & ~BANNED_USERS
)
@language
async def gstats_global(client, message: Message, _):
    mystic = await message.reply_text(_["gstats_1"])
    stats = await get_global_tops()
    if not stats:
        await asyncio.sleep(1)
        return await mystic.edit(_["gstats_2"])

    def get_stats():
        results = {}
        for i in stats:
            results[str(i)] = stats[i]["spot"]
        list_arranged = dict(
            sorted(results.items(), key=lambda item: item[1], reverse=True)
        )
        if not results:
            return None, None
        for vidid, count in list_arranged.items():
            if vidid in ("telegram", "soundcloud"):
                continue
            return vidid, count
        return None, None

    try:
        videoid, co = await loop.run_in_executor(None, get_stats)
    except Exception as e:
        print(e)
        return
    if not videoid:
        return await mystic.edit(_["gstats_2"])
    title, duration_min, duration_sec, vidid = await app.YouTube.details(videoid, True) if hasattr(app, 'YouTube') else (videoid, "N/A", 0, videoid)
    final = (
        f"**Top Most Played Track on {MUSIC_BOT_NAME}**\n\n"
        f"**Title:** {videoid}\n\n"
        f"Played **{co}** times"
    )
    upl = get_stats_markup(_, True if message.from_user.id in SUDOERS else False)
    await message.reply_photo(photo=STATS_IMG, caption=final, reply_markup=upl)
    await mystic.delete()


@app.on_callback_query(filters.regex("GetStatsNow") & ~BANNED_USERS)
@languageCB
async def top_users_ten(client, CallbackQuery: CallbackQuery, _):
    chat_id = CallbackQuery.message.chat.id
    callback_data = CallbackQuery.data.strip()
    what = callback_data.split(None, 1)[1]
    upl = back_stats_markup(_)
    try:
        await CallbackQuery.answer()
    except:
        pass
    mystic = await CallbackQuery.edit_message_text(
        _["gstats_3"].format(
            f"of {CallbackQuery.message.chat.title}" if what == "Here" else what
        )
    )
    if what == "Tracks":
        stats = await get_global_tops()
    elif what == "Chats":
        stats = await get_top_chats()
    elif what == "Users":
        stats = await get_topp_users()
    elif what == "Here":
        stats = await get_particulars(chat_id)
    if not stats:
        await asyncio.sleep(1)
        return await mystic.edit(_["gstats_2"], reply_markup=upl)
    queries = await get_queries()

    def get_stats():
        results = {}
        for i in stats:
            top_list = (
                stats[i] if what in ["Chats", "Users"] else stats[i]["spot"]
            )
            results[str(i)] = top_list
        list_arranged = dict(
            sorted(results.items(), key=lambda item: item[1], reverse=True)
        )
        if not results:
            return None, None
        msg = ""
        limit = 0
        total_count = 0
        if what in ["Tracks", "Here"]:
            for items, count in list_arranged.items():
                total_count += count
                if limit == 10:
                    continue
                limit += 1
                details = stats.get(items)
                title = (details["title"][:35]).title()
                if items in ("telegram", "soundcloud"):
                    continue
                msg += f"🔗 [{title}](https://www.youtube.com/watch?v={items}) **played {count} times**\n\n"
            temp = (
                _["gstats_4"].format(queries, config.MUSIC_BOT_NAME, len(stats), total_count, limit)
                if what == "Tracks"
                else _["gstats_7"].format(len(stats), total_count, limit)
            )
            msg = temp + msg
        return msg, list_arranged

    try:
        msg, list_arranged = await loop.run_in_executor(None, get_stats)
    except Exception as e:
        print(e)
        return
    limit = 0
    if what in ["Users", "Chats"]:
        for items, count in list_arranged.items():
            if limit == 10:
                break
            try:
                extract = (
                    (await app.get_users(items)).first_name
                    if what == "Users"
                    else (await app.get_chat(items)).title
                )
                if extract is None:
                    continue
                await asyncio.sleep(0.5)
            except:
                continue
            limit += 1
            msg += f"🔗 `{extract}` played {count} times.\n\n"
        temp = (
            _["gstats_5"].format(limit, MUSIC_BOT_NAME)
            if what == "Chats"
            else _["gstats_6"].format(limit, MUSIC_BOT_NAME)
        )
        msg = temp + msg
    med = InputMediaPhoto(media=GLOBAL_IMG, caption=msg)
    try:
        await CallbackQuery.edit_message_media(media=med, reply_markup=upl)
    except MessageIdInvalid:
        await CallbackQuery.message.reply_photo(photo=GLOBAL_IMG, caption=msg, reply_markup=upl)


@app.on_callback_query(filters.regex("TopOverall") & ~BANNED_USERS)
@languageCB
async def overall_stats(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    what = callback_data.split(None, 1)[1]
    upl = overallback_stats_markup(_) if what != "s" else back_stats_buttons(_)
    try:
        await CallbackQuery.answer()
    except:
        pass
    await CallbackQuery.edit_message_text(_["gstats_8"])
    served_chats = len(await get_served_chats())
    served_users = len(await get_served_users())
    total_queries = await get_queries()
    blocked = len(BANNED_USERS)
    sudoers = len(SUDOERS)
    mod = len(ALL_MODULES)
    assistant = len(assistants)
    ass = "Yes" if config.AUTO_LEAVING_ASSISTANT == str(True) else "No"
    text = (
        f"**Bot Stats and Information:**\n\n"
        f"**Modules Loaded:** {mod}\n"
        f"**Served Chats:** {served_chats}\n"
        f"**Served Users:** {served_users}\n"
        f"**Blocked Users:** {blocked}\n"
        f"**Sudo Users:** {sudoers}\n\n"
        f"**Total Queries:** {total_queries}\n"
        f"**Total Assistants:** {assistant}\n"
        f"**Auto Leave Assistant:** {ass}\n"
        f"**Clean Mode Duration:** {config.CLEANMODE_DELETE_MINS} mins\n\n"
        f"**Play Duration Limit:** {config.DURATION_LIMIT_MIN} mins\n"
        f"**Song Download Limit:** {config.SONG_DOWNLOAD_DURATION} mins\n"
        f"**Server Playlist Limit:** {config.SERVER_PLAYLIST_LIMIT}\n"
        f"**Playlist Fetch Limit:** {config.PLAYLIST_FETCH_LIMIT}"
    )
    med = InputMediaPhoto(media=STATS_IMG, caption=text)
    try:
        await CallbackQuery.edit_message_media(media=med, reply_markup=upl)
    except MessageIdInvalid:
        await CallbackQuery.message.reply_photo(photo=STATS_IMG, caption=text, reply_markup=upl)


@app.on_callback_query(filters.regex("bot_stats_sudo"))
@languageCB
async def sudo_stats(client, CallbackQuery, _):
    if CallbackQuery.from_user.id not in SUDOERS:
        return await CallbackQuery.answer("Only for Sudo Users", show_alert=True)
    callback_data = CallbackQuery.data.strip()
    what = callback_data.split(None, 1)[1]
    upl = overallback_stats_markup(_) if what != "s" else back_stats_buttons(_)
    try:
        await CallbackQuery.answer()
    except:
        pass
    await CallbackQuery.edit_message_text(_["gstats_8"])
    sc = platform.system()
    p_core = psutil.cpu_count(logical=False)
    t_core = psutil.cpu_count(logical=True)
    ram = str(round(psutil.virtual_memory().total / (1024.0**3))) + " GB"
    try:
        cpu_freq = psutil.cpu_freq().current
        cpu_freq = f"{round(cpu_freq / 1000, 2)}GHz" if cpu_freq >= 1000 else f"{round(cpu_freq, 2)}MHz"
    except:
        cpu_freq = "Unable to fetch"
    hdd = psutil.disk_usage("/")
    served_chats = len(await get_served_chats())
    served_users = len(await get_served_users())
    total_queries = await get_queries()
    blocked = len(BANNED_USERS)
    sudoers = len(await get_sudoers())
    db = pymongodb
    call = db.command("dbstats")
    datasize = str(call["dataSize"] / 1024)
    storage = call["storageSize"] / 1024
    objects = call["objects"]
    collections = call["collections"]
    status = db.command("serverStatus")
    query = status["opcounters"]["query"]
    mongouptime = str(status["uptime"] / 86400)
    text = (
        f"**Bot Stats and Information:**\n\n"
        f"**Platform:** {sc}\n"
        f"**RAM:** {ram}\n"
        f"**Physical Cores:** {p_core}\n"
        f"**Total Cores:** {t_core}\n"
        f"**CPU Frequency:** {cpu_freq}\n\n"
        f"**Python:** {pyver.split()[0]}\n"
        f"**Pyrogram:** {pyrover}\n"
        f"**PyTgCalls:** {pytgver}\n\n"
        f"**Storage Total:** {str(hdd.total / (1024.0**3))[:4]} GiB\n"
        f"**Storage Used:** {str(hdd.used / (1024.0**3))[:4]} GiB\n"
        f"**Storage Free:** {str(hdd.free / (1024.0**3))[:4]} GiB\n\n"
        f"**Served Chats:** {served_chats}\n"
        f"**Served Users:** {served_users}\n"
        f"**Blocked Users:** {blocked}\n"
        f"**Sudo Users:** {sudoers}\n\n"
        f"**Mongo Uptime:** {mongouptime[:4]} days\n"
        f"**DB Size:** {datasize[:6]} MB\n"
        f"**DB Storage:** {storage} MB\n"
        f"**DB Collections:** {collections}\n"
        f"**DB Objects:** {objects}\n"
        f"**DB Queries:** `{query}`\n"
        f"**Bot Queries:** `{total_queries}`"
    )
    med = InputMediaPhoto(media=STATS_IMG, caption=text)
    try:
        await CallbackQuery.edit_message_media(media=med, reply_markup=upl)
    except MessageIdInvalid:
        await CallbackQuery.message.reply_photo(photo=STATS_IMG, caption=text, reply_markup=upl)


@app.on_callback_query(
    filters.regex(pattern=r"^(TOPMARKUPGET|GETSTATS|GlobalStats)$") & ~BANNED_USERS
)
@languageCB
async def back_buttons(client, CallbackQuery, _):
    try:
        await CallbackQuery.answer()
    except:
        pass
    command = CallbackQuery.matches[0].group(1)
    if command == "TOPMARKUPGET":
        upl = top_ten_stats_markup(_)
        med = InputMediaPhoto(media=GLOBAL_IMG, caption=_["gstats_9"])
        try:
            await CallbackQuery.edit_message_media(media=med, reply_markup=upl)
        except MessageIdInvalid:
            await CallbackQuery.message.reply_photo(photo=GLOBAL_IMG, caption=_["gstats_9"], reply_markup=upl)
    elif command == "GlobalStats":
        upl = get_stats_markup(_, True if CallbackQuery.from_user.id in SUDOERS else False)
        med = InputMediaPhoto(media=GLOBAL_IMG, caption=_["gstats_10"].format(config.MUSIC_BOT_NAME))
        try:
            await CallbackQuery.edit_message_media(media=med, reply_markup=upl)
        except MessageIdInvalid:
            await CallbackQuery.message.reply_photo(photo=GLOBAL_IMG, caption=_["gstats_10"].format(config.MUSIC_BOT_NAME), reply_markup=upl)
    elif command == "GETSTATS":
        upl = stats_buttons(_, True if CallbackQuery.from_user.id in SUDOERS else False)
        med = InputMediaPhoto(media=STATS_IMG, caption=_["gstats_11"].format(config.MUSIC_BOT_NAME))
        try:
            await CallbackQuery.edit_message_media(media=med, reply_markup=upl)
        except MessageIdInvalid:
            await CallbackQuery.message.reply_photo(photo=STATS_IMG, caption=_["gstats_11"].format(config.MUSIC_BOT_NAME), reply_markup=upl)