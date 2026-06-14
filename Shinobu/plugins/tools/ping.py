# Shinobu Music Bot
# Owner: @Sanji_fr

from datetime import datetime

from pyrogram import filters
from pyrogram.types import Message

from config import BANNED_USERS, MUSIC_BOT_NAME
from strings import get_command
from Shinobu import app
from Shinobu.core.call import Shinobu
from Shinobu.utils import bot_sys_stats
from Shinobu.utils.decorators.language import language

PING_COMMAND = get_command("PING_COMMAND")


@app.on_message(
    filters.command(PING_COMMAND)
    & filters.group
    
    & ~BANNED_USERS
)
@language
async def ping_com(client, message: Message, _):
    response = await message.reply_photo(
        photo="assets/Ping.jpeg",
        caption=_["ping_1"],
    )
    start = datetime.now()
    pytgping = await Shinobu.ping()
    UP, CPU, RAM, DISK = await bot_sys_stats()
    resp = (datetime.now() - start).microseconds / 1000
    await response.edit_caption(
        _["ping_2"].format(MUSIC_BOT_NAME, resp, UP, DISK, CPU, RAM, pytgping)
    )