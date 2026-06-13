# Shinobu Music Bot
# Owner: @Sanji_fr

import random
import re
import string

import lyricsgenius as lg
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

import config
from config import BANNED_USERS, lyrical
from strings import get_command
from Shinobu import app
from Shinobu.utils.decorators.language import language

LYRICS_COMMAND = get_command("LYRICS_COMMAND")

if config.GENIUS_API_KEY:
    genius = lg.Genius(
        config.GENIUS_API_KEY,
        skip_non_songs=True,
        excluded_terms=["(Remix)", "(Live)"],
        remove_section_headers=True,
    )
    genius.verbose = False
else:
    genius = None


@app.on_message(
    filters.command(LYRICS_COMMAND) & ~filters.edited & ~BANNED_USERS
)
@language
async def lrsearch(client, message: Message, _):
    if not genius:
        return await message.reply_text(
            "Lyrics aren't available right now. The owner hasn't configured a Genius API key."
        )
    if len(message.command) < 2:
        return await message.reply_text(_["lyrics_1"])
    title = message.text.split(None, 1)[1]
    m = await message.reply_text(_["lyrics_2"])
    S = genius.search_song(title, get_full_info=False)
    if S is None:
        return await m.edit(_["lyrics_3"].format(title))
    ran_hash = "".join(
        random.choices(string.ascii_uppercase + string.digits, k=10)
    )
    lyric = S.lyrics
    if "Embed" in lyric:
        lyric = re.sub(r"\d*Embed", "", lyric)
    lyrical[ran_hash] = lyric
    upl = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton(
                text=_["L_B_1"],
                url=f"https://t.me/{app.username}?start=lyrics_{ran_hash}",
            )
        ]]
    )
    await m.edit(_["lyrics_4"], reply_markup=upl)