# Shinobu Music Bot
# Owner: @Sanji_fr

import os

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaAudio, Message

from config import BANNED_USERS, SONG_DOWNLOAD_DURATION, SONG_DOWNLOAD_DURATION_LIMIT
from strings import get_command
from Shinobu import YouTube, app
from Shinobu.utils.decorators.language import language, languageCB
from Shinobu.utils.inline.song import song_markup
from Shinobu.utils.thumbnails import gen_thumb

SONG_COMMAND = get_command("SONG_COMMAND")


@app.on_message(
    filters.command(SONG_COMMAND)
    & filters.group
    & ~filters.edited
    & ~BANNED_USERS
)
@language
async def song_command_group(client, message: Message, _):
    upl = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton(
                text=_["SG_B_1"],
                url=f"https://t.me/{app.username}?start=song",
            )
        ]]
    )
    await message.reply_text(_["song_1"], reply_markup=upl)


@app.on_message(
    filters.command(SONG_COMMAND)
    & filters.private
    & ~filters.edited
    & ~BANNED_USERS
)
@language
async def song_command_private(client, message: Message, _):
    await message.delete()
    url = await YouTube.url(message)
    if url:
        if not await YouTube.exists(url):
            return await message.reply_text(_["song_5"])
        mystic = await message.reply_text(_["play_1"])
        title, duration_min, duration_sec, vidid = await YouTube.details(url)
        if str(duration_min) == "None":
            return await mystic.edit_text(_["song_3"])
        if int(duration_sec) > SONG_DOWNLOAD_DURATION_LIMIT:
            return await mystic.edit_text(
                _["play_4"].format(SONG_DOWNLOAD_DURATION, duration_min)
            )
        img = await gen_thumb(title, duration_min, "You")
        buttons = song_markup(_, vidid)
        await mystic.delete()
        return await message.reply_photo(
            img,
            caption=_["song_4"].format(title),
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        if len(message.command) < 2:
            return await message.reply_text(_["song_2"])
    mystic = await message.reply_text(_["play_1"])
    query = message.text.split(None, 1)[1]
    try:
        title, duration_min, duration_sec, vidid = await YouTube.details(query)
    except:
        return await mystic.edit_text(_["play_3"])
    if str(duration_min) == "None":
        return await mystic.edit_text(_["song_3"])
    if int(duration_sec) > SONG_DOWNLOAD_DURATION_LIMIT:
        return await mystic.edit_text(
            _["play_6"].format(SONG_DOWNLOAD_DURATION, duration_min)
        )
    img = await gen_thumb(title, duration_min, "You")
    buttons = song_markup(_, vidid)
    await mystic.delete()
    return await message.reply_photo(
        img,
        caption=_["song_4"].format(title),
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@app.on_callback_query(filters.regex(pattern=r"song_back") & ~BANNED_USERS)
@languageCB
async def songs_back_helper(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    stype, vidid = callback_request.split("|")
    buttons = song_markup(_, vidid)
    return await CallbackQuery.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex(pattern=r"song_helper") & ~BANNED_USERS)
@languageCB
async def song_helper_cb(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    stype, vidid = callback_request.split("|")
    try:
        await CallbackQuery.answer(_["song_6"], show_alert=True)
    except:
        pass
    # Audio only — fetch available audio formats
    try:
        formats_available, link = await YouTube.formats(vidid, True)
    except:
        return await CallbackQuery.edit_message_text(_["song_7"])
    from pykeyboard import InlineKeyboard
    from Shinobu.utils.formatters import convert_bytes
    keyboard = InlineKeyboard()
    done = []
    for x in formats_available:
        if "audio" not in x["format"]:
            continue
        if x["filesize"] is None:
            continue
        form = x["format_note"].title()
        if form in done:
            continue
        done.append(form)
        sz = convert_bytes(x["filesize"])
        keyboard.row(
            InlineKeyboardButton(
                text=f"{form} Quality — {sz}",
                callback_data=f"song_download audio|{x['format_id']}|{vidid}",
            )
        )
    keyboard.row(
        InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data=f"song_back audio|{vidid}"),
        InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close"),
    )
    return await CallbackQuery.edit_message_reply_markup(reply_markup=keyboard)


@app.on_callback_query(filters.regex(pattern=r"song_download") & ~BANNED_USERS)
@languageCB
async def song_download_cb(client, CallbackQuery, _):
    try:
        await CallbackQuery.answer("Downloading...")
    except:
        pass
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    stype, format_id, vidid = callback_request.split("|")
    mystic = await CallbackQuery.edit_message_text(_["song_8"])
    yturl = f"https://www.youtube.com/watch?v={vidid}"
    import yt_dlp, re
    with yt_dlp.YoutubeDL({"quiet": True}) as ytdl:
        x = ytdl.extract_info(yturl, download=False)
    title = re.sub(r"\W+", " ", (x["title"]).title())
    img = await gen_thumb(title, str(x.get("duration", 0)), "You")
    try:
        filename = await YouTube.download(
            yturl,
            mystic,
            songaudio=True,
            title=title,
        )
    except Exception as e:
        return await mystic.edit_text(_["song_9"].format(e))
    med = InputMediaAudio(
        media=filename,
        caption=title,
        thumb=img,
        title=title,
        performer=x.get("uploader", "Unknown"),
    )
    await mystic.edit_text(_["song_11"])
    await app.send_chat_action(
        chat_id=CallbackQuery.message.chat.id,
        action="upload_audio",
    )
    try:
        await CallbackQuery.edit_message_media(media=med)
    except Exception as e:
        print(e)
        return await mystic.edit_text(_["song_10"])
    os.remove(filename)