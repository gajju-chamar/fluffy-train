# Shinobu Music Bot
# Owner: @Sanji_fr

import random

from Shinobu import userbot
from Shinobu.core.mongo import mongodb

db = mongodb.assistants

assistantdict = {}


async def get_client(assistant: int):
    if int(assistant) == 1:
        return userbot.one
    elif int(assistant) == 2:
        return userbot.two
    elif int(assistant) == 3:
        return userbot.three
    elif int(assistant) == 4:
        return userbot.four
    elif int(assistant) == 5:
        return userbot.five


async def set_assistant(chat_id):
    from Shinobu.core.userbot import assistants

    ran_assistant = random.choice(assistants)
    assistantdict[chat_id] = ran_assistant
    await db.update_one(
        {"chat_id": chat_id},
        {"$set": {"assistant": ran_assistant}},
        upsert=True,
    )
    client = await get_client(ran_assistant)
    return client


async def get_assistant(chat_id: int):
    from Shinobu.core.userbot import assistants

    assistant = assistantdict.get(chat_id)
    if not assistant:
        dbassistant = await db.find_one({"chat_id": chat_id})
        if not dbassistant:
            client = await set_assistant(chat_id)
            return client
        else:
            got_assis = dbassistant["assistant"]
            if got_assis in assistants:
                assistantdict[chat_id] = got_assis
                client = await get_client(got_assis)
                return client
            else:
                client = await set_assistant(chat_id)
                return client
    else:
        if assistant in assistants:
            client = await get_client(assistant)
            return client
        else:
            client = await set_assistant(chat_id)
            return client


async def set_calls_assistant(chat_id):
    from Shinobu.core.userbot import assistants

    ran_assistant = random.choice(assistants)
    assistantdict[chat_id] = ran_assistant
    await db.update_one(
        {"chat_id": chat_id},
        {"$set": {"assistant": ran_assistant}},
        upsert=True,
    )
    return ran_assistant


async def group_assistant(self, chat_id: int) -> int:
    from Shinobu.core.userbot import assistants

    assistant = assistantdict.get(chat_id)
    if not assistant:
        dbassistant = await db.find_one({"chat_id": chat_id})
        if not dbassistant:
            assis = await set_calls_assistant(chat_id)
        else:
            assis = dbassistant["assistant"]
            if assis in assistants:
                assistantdict[chat_id] = assis
            else:
                assis = await set_calls_assistant(chat_id)
    else:
        if assistant in assistants:
            assis = assistant
        else:
            assis = await set_calls_assistant(chat_id)

    if int(assis) == 1:
        return self.one
    elif int(assis) == 2:
        return self.two
    elif int(assis) == 3:
        return self.three
    elif int(assis) == 4:
        return self.four
    elif int(assis) == 5:
        return self.five