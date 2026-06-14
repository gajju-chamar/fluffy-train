# Shinobu Music Bot
# Owner: @Sanji_fr

import sys

from pyrogram import Client
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import BotCommand

import config
from ..logging import LOGGER


class ShinobuBot(Client):
    def __init__(self):
        LOGGER(__name__).info("Starting Shinobu Bot...")
        super().__init__(
            "ShinobuMusicBot",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
        )

    async def start(self):
        await super().start()
        get_me = await self.get_me()
        self.username = get_me.username
        self.id = get_me.id

        try:
            await self.send_message(config.LOG_GROUP_ID, "Shinobu has awakened~ 🦋")
        except:
            LOGGER(__name__).error(
                "Bot failed to access the log group. "
                "Make sure the bot is added to your log group and promoted as admin!"
            )
            sys.exit()

        if config.SET_CMDS == str(True):
            try:
                await self.set_bot_commands(
                    [
                        BotCommand("ping", "Check if Shinobu is alive"),
                        BotCommand("play", "Play a song in voice chat"),
                        BotCommand("skip", "Skip to the next track"),
                        BotCommand("pause", "Pause the current song"),
                        BotCommand("resume", "Resume the paused song"),
                        BotCommand("end", "Stop music and clear the queue"),
                        BotCommand("shuffle", "Shuffle the current queue"),
                        BotCommand("playmode", "Change the default play mode"),
                        BotCommand("settings", "Open bot settings for this chat"),
                    ]
                )
            except:
                pass

        a = await self.get_chat_member(config.LOG_GROUP_ID, self.id)
        if a.status not in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
            LOGGER(__name__).error(
                "Please promote Shinobu as Admin in the log group."
            )
            sys.exit()

        if get_me.last_name:
            self.name = get_me.first_name + " " + get_me.last_name
        else:
            self.name = get_me.first_name

        LOGGER(__name__).info(f"Shinobu started as {self.name}")
