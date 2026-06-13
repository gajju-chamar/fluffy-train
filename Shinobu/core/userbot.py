# Shinobu Music Bot
# Owner: @Sanji_fr

import sys

from pyrogram import Client

import config
from ..logging import LOGGER

assistants = []
assistantids = []


class Userbot(Client):
    def __init__(self):
        self.one = Client(
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_name=str(config.STRING1),
            no_updates=True,
        )
        self.two = Client(
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_name=str(config.STRING2),
            no_updates=True,
        )
        self.three = Client(
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_name=str(config.STRING3),
            no_updates=True,
        )
        self.four = Client(
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_name=str(config.STRING4),
            no_updates=True,
        )
        self.five = Client(
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_name=str(config.STRING5),
            no_updates=True,
        )

    async def _start_assistant(self, client, number: str):
        """Start a single assistant client and register it."""
        await client.start()
        try:
            await client.send_message(config.LOG_GROUP_ID, f"Assistant {number} awakened~ 🦋")
        except:
            LOGGER(__name__).error(
                f"Assistant {number} failed to access the log group. "
                "Make sure it's added to your log group and promoted as admin!"
            )
            sys.exit()
        get_me = await client.get_me()
        client.username = get_me.username
        client.id = get_me.id
        assistantids.append(get_me.id)
        client.name = (
            get_me.first_name + " " + get_me.last_name
            if get_me.last_name
            else get_me.first_name
        )
        LOGGER(__name__).info(f"Assistant {number} started as {client.name}")

    async def start(self):
        LOGGER(__name__).info("Starting assistant clients...")
        if config.STRING1:
            await self._start_assistant(self.one, "One")
            assistants.append(1)
        if config.STRING2:
            await self._start_assistant(self.two, "Two")
            assistants.append(2)
        if config.STRING3:
            await self._start_assistant(self.three, "Three")
            assistants.append(3)
        if config.STRING4:
            await self._start_assistant(self.four, "Four")
            assistants.append(4)
        if config.STRING5:
            await self._start_assistant(self.five, "Five")
            assistants.append(5)