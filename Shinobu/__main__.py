# Shinobu Music Bot
# Owner: @Sanji_fr

import asyncio
import importlib
import sys

from pyrogram import idle

import config
from config import BANNED_USERS
from Shinobu import LOGGER, app, userbot
from Shinobu.core.call import Shinobu
from Shinobu.core.dir import dirr
from Shinobu.core.git import git
from Shinobu.misc import dbb, sudo
from Shinobu.plugins import ALL_MODULES
from Shinobu.utils.database import get_banned_users, get_gbanned

loop = asyncio.get_event_loop()


async def init():
    # Verify at least one assistant session is configured
    if not any([
        config.STRING1, config.STRING2, config.STRING3,
        config.STRING4, config.STRING5,
    ]):
        LOGGER("Shinobu").error(
            "No assistant session vars defined. Please set at least STRING_SESSION."
        )
        return

    if not config.SPOTIFY_CLIENT_ID or not config.SPOTIFY_CLIENT_SECRET:
        LOGGER("Shinobu").warning(
            "Spotify vars not set. Spotify links won't work."
        )

    # Clean directories and pull git updates if configured
    dirr()
    git()

    # Initialize in-memory db and sudoers
    dbb()
    sudo()

    # Load banned users into filter
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass

    # Start bot
    await app.start()

    # Load all plugins
    for module in ALL_MODULES:
        importlib.import_module("Shinobu.plugins" + module)
    LOGGER("Shinobu.plugins").info("All modules loaded successfully.")

    # Start assistant userbots
    await userbot.start()

    # Start PyTgCalls
    await Shinobu.start()
    await Shinobu.decorators()

    LOGGER("Shinobu").info("Shinobu Music Bot started successfully~ 🦋")
    await idle()


if __name__ == "__main__":
    loop.run_until_complete(init())
    LOGGER("Shinobu").info("Shutting down Shinobu. Goodbye~ 🦋")