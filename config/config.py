# Shinobu Music Bot
# Owner: @Sanji_fr
# Licensed under GNU v3.0

import sys
from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

# Dual-nature env loading:
# - On VPS/Docker: reads from .env file
# - On Render/Railway/Replit: reads from platform-injected environment secrets
# Both flow through os.environ — no code change needed between platforms.
load_dotenv()

# ── Mandatory Vars ────────────────────────────────────────────────────────────

# Get from https://my.telegram.org
API_ID = int(getenv("API_ID", ""))
API_HASH = getenv("API_HASH")

# Get from @BotFather on Telegram
BOT_TOKEN = getenv("BOT_TOKEN")

# MongoDB URI — https://www.mongodb.com/atlas
MONGO_DB_URI = getenv("MONGO_DB_URI", None)

# Private group/supergroup ID for bot logs (must start with -100)
LOG_GROUP_ID = int(getenv("LOG_GROUP_ID", ""))

# Your bot's display name
MUSIC_BOT_NAME = getenv("MUSIC_BOT_NAME", "Shinobu")

# Owner Telegram User ID (integer)
OWNER_ID = list(map(int, getenv("OWNER_ID", "").split()))

# Pyrogram String Sessions for assistant accounts (up to 5)
STRING1 = getenv("STRING_SESSION", None)
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)

# ── Spotify ───────────────────────────────────────────────────────────────────
# Get from https://developer.spotify.com/dashboard
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", None)
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", None)

# ── Lyrics ────────────────────────────────────────────────────────────────────
# Get from https://genius.com/api-clients
GENIUS_API_KEY = getenv("GENIUS_API_KEY", None)

# ── Audio Limits ──────────────────────────────────────────────────────────────

# Max duration for streaming in voice chat (minutes)
DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", "80"))

# Max duration for downloading songs (minutes)
SONG_DOWNLOAD_DURATION = int(getenv("SONG_DOWNLOAD_DURATION_LIMIT", "180"))

# Max audio file size streamable from Telegram (bytes) — default 100MB
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", "104857600"))

# ── Playlist ──────────────────────────────────────────────────────────────────

# Max tracks fetched from a YouTube/Spotify playlist — hard capped at 20
PLAYLIST_FETCH_LIMIT = min(int(getenv("PLAYLIST_FETCH_LIMIT", "20")), 20)

# Max playlists a user can save on the server
SERVER_PLAYLIST_LIMIT = int(getenv("SERVER_PLAYLIST_LIMIT", "30"))

# ── Assistant Behaviour ───────────────────────────────────────────────────────

AUTO_LEAVING_ASSISTANT = getenv("AUTO_LEAVING_ASSISTANT", None)
AUTO_LEAVE_ASSISTANT_TIME = int(getenv("ASSISTANT_LEAVE_TIME", "5400"))
CLEANMODE_DELETE_MINS = int(getenv("CLEANMODE_MINS", "5"))
AUTO_DOWNLOADS_CLEAR = getenv("AUTO_DOWNLOADS_CLEAR", None)

# ── Downloader Timings ────────────────────────────────────────────────────────

YOUTUBE_DOWNLOAD_EDIT_SLEEP = int(getenv("YOUTUBE_EDIT_SLEEP", "3"))

# ── Bot Behaviour ─────────────────────────────────────────────────────────────

SET_CMDS = getenv("SET_CMDS", False)

# ── Internal State (do not modify) ────────────────────────────────────────────

BANNED_USERS = filters.user()
YTDOWNLOADER = 1
LOG = 2
LOG_FILE_NAME = "shinobu_logs.txt"

adminlist = {}
lyrical = {}
chatstats = {}
userstats = {}
clean = {}
autoclean = []

# ── Derived Values ────────────────────────────────────────────────────────────

def time_to_seconds(time):
    stringt = str(time)
    return sum(
        int(x) * 60**i
        for i, x in enumerate(reversed(stringt.split(":")))
    )

DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))
SONG_DOWNLOAD_DURATION_LIMIT = int(time_to_seconds(f"{SONG_DOWNLOAD_DURATION}:00"))

# ── Startup Validation ────────────────────────────────────────────────────────

if MUSIC_BOT_NAME and not MUSIC_BOT_NAME.isascii():
    print("[ERROR] MUSIC_BOT_NAME must not contain special characters or styled fonts.")
    sys.exit()