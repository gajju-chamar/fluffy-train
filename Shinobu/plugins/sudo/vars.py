# Shinobu Music Bot
# Owner: @Sanji_fr

import asyncio

from pyrogram import filters

import config
from Shinobu import app
from Shinobu.misc import SUDOERS
from Shinobu.utils.formatters import convert_bytes

VARS_COMMAND = "vars"


@app.on_message(filters.command(VARS_COMMAND) & SUDOERS)
async def varsFunc(client, message):
    mystic = await message.reply_text("Fetching config, please wait...")
    playlist_limit = config.SERVER_PLAYLIST_LIMIT
    fetch_playlist = config.PLAYLIST_FETCH_LIMIT
    song = config.SONG_DOWNLOAD_DURATION
    play_duration = config.DURATION_LIMIT_MIN
    cm = config.CLEANMODE_DELETE_MINS
    auto_leave = config.AUTO_LEAVE_ASSISTANT_TIME
    yt_sleep = config.YOUTUBE_DOWNLOAD_EDIT_SLEEP
    ass = "Yes" if config.AUTO_LEAVING_ASSISTANT == str(True) else "No"
    down = "Yes" if config.AUTO_DOWNLOADS_CLEAR == str(True) else "No"
    spotify = "Yes" if config.SPOTIFY_CLIENT_ID and config.SPOTIFY_CLIENT_SECRET else "No"
    genius = "Yes" if config.GENIUS_API_KEY else "No"
    owners = ", ".join([str(i) for i in config.OWNER_ID])
    tg_aud = convert_bytes(config.TG_AUDIO_FILESIZE_LIMIT)
    text = f"""**SHINOBU CONFIG:**

**Basic:**
`MUSIC_BOT_NAME` : **{config.MUSIC_BOT_NAME}**
`OWNER_ID` : **{owners}**
`DURATION_LIMIT` : **{play_duration} min**
`SONG_DOWNLOAD_LIMIT` : **{song} min**

**Playlist:**
`SERVER_PLAYLIST_LIMIT` : **{playlist_limit}**
`PLAYLIST_FETCH_LIMIT` : **{fetch_playlist}**

**Assistant:**
`AUTO_LEAVING_ASSISTANT` : **{ass}**
`ASSISTANT_LEAVE_TIME` : **{auto_leave} sec**

**Downloader:**
`AUTO_DOWNLOADS_CLEAR` : **{down}**
`YOUTUBE_EDIT_SLEEP` : **{yt_sleep} sec**

**Clean Mode:**
`CLEANMODE_MINS` : **{cm} min**

**File Limit:**
`TG_AUDIO_FILESIZE_LIMIT` : **{tg_aud}**

**Integrations:**
`SPOTIFY` : **{spotify}**
`GENIUS_API_KEY` : **{genius}**
"""
    await asyncio.sleep(1)
    await mystic.edit_text(text)