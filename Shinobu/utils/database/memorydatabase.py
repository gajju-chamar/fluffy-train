# Shinobu Music Bot
# Owner: @Sanji_fr

from Shinobu.core.mongo import mongodb

channeldb = mongodb.cplaymode
commanddb = mongodb.commands
cleandb = mongodb.cleanmode
playmodedb = mongodb.playmode
playtypedb = mongodb.playtypedb
langdb = mongodb.language
authdb = mongodb.adminauth
onoffdb = mongodb.onoffper
autoenddb = mongodb.autoend

# In-memory caches
loop = {}
playtype = {}
playmode = {}
channelconnect = {}
langm = {}
pause = {}
mute = {}
audio = {}
active = []
command = []
cleanmode = []
nonadmin = {}
maintenance = []
autoend = {}


# Auto End Stream

async def is_autoend() -> bool:
    chat_id = 123
    mode = autoend.get(chat_id)
    if not mode:
        user = await autoenddb.find_one({"chat_id": chat_id})
        if not user:
            autoend[chat_id] = False
            return False
        autoend[chat_id] = True
        return True
    return mode


async def autoend_on():
    chat_id = 123
    autoend[chat_id] = True
    user = await autoenddb.find_one({"chat_id": chat_id})
    if not user:
        return await autoenddb.insert_one({"chat_id": chat_id})


async def autoend_off():
    chat_id = 123
    autoend[chat_id] = False
    user = await autoenddb.find_one({"chat_id": chat_id})
    if user:
        return await autoenddb.delete_one({"chat_id": chat_id})


# Loop Play

async def get_loop(chat_id: int) -> int:
    lop = loop.get(chat_id)
    if not lop:
        return 0
    return lop


async def set_loop(chat_id: int, mode: int):
    loop[chat_id] = mode


# Channel Play IDs

async def get_cmode(chat_id: int) -> int:
    mode = channelconnect.get(chat_id)
    if not mode:
        mode = await channeldb.find_one({"chat_id": chat_id})
        if not mode:
            return None
        channelconnect[chat_id] = mode["mode"]
        return mode["mode"]
    return mode


async def set_cmode(chat_id: int, mode: int):
    channelconnect[chat_id] = mode
    await channeldb.update_one(
        {"chat_id": chat_id}, {"$set": {"mode": mode}}, upsert=True
    )


# Play Type — Admins Only or Everyone

async def get_playtype(chat_id: int) -> str:
    mode = playtype.get(chat_id)
    if not mode:
        mode = await playtypedb.find_one({"chat_id": chat_id})
        if not mode:
            playtype[chat_id] = "Everyone"
            return "Everyone"
        playtype[chat_id] = mode["mode"]
        return mode["mode"]
    return mode


async def set_playtype(chat_id: int, mode: str):
    playtype[chat_id] = mode
    await playtypedb.update_one(
        {"chat_id": chat_id}, {"$set": {"mode": mode}}, upsert=True
    )


# Play Mode — Inline or Direct

async def get_playmode(chat_id: int) -> str:
    mode = playmode.get(chat_id)
    if not mode:
        mode = await playmodedb.find_one({"chat_id": chat_id})
        if not mode:
            playmode[chat_id] = "Direct"
            return "Direct"
        playmode[chat_id] = mode["mode"]
        return mode["mode"]
    return mode


async def set_playmode(chat_id: int, mode: str):
    playmode[chat_id] = mode
    await playmodedb.update_one(
        {"chat_id": chat_id}, {"$set": {"mode": mode}}, upsert=True
    )


# Language

async def get_lang(chat_id: int) -> str:
    mode = langm.get(chat_id)
    if not mode:
        lang = await langdb.find_one({"chat_id": chat_id})
        if not lang:
            langm[chat_id] = "en"
            return "en"
        langm[chat_id] = lang["lang"]
        return lang["lang"]
    return mode


async def set_lang(chat_id: int, lang: str):
    langm[chat_id] = lang
    await langdb.update_one(
        {"chat_id": chat_id}, {"$set": {"lang": lang}}, upsert=True
    )


# Muted

async def is_muted(chat_id: int) -> bool:
    return mute.get(chat_id, False)


async def mute_on(chat_id: int):
    mute[chat_id] = True


async def mute_off(chat_id: int):
    mute[chat_id] = False


# Pause / Playing

async def is_music_playing(chat_id: int) -> bool:
    return pause.get(chat_id, False)


async def music_on(chat_id: int):
    pause[chat_id] = True


async def music_off(chat_id: int):
    pause[chat_id] = False


# Active Voice Chats

async def get_active_chats() -> list:
    return active


async def is_active_chat(chat_id: int) -> bool:
    return chat_id in active


async def add_active_chat(chat_id: int):
    if chat_id not in active:
        active.append(chat_id)


async def remove_active_chat(chat_id: int):
    if chat_id in active:
        active.remove(chat_id)


# Delete Command Mode

async def is_commanddelete_on(chat_id: int) -> bool:
    return chat_id not in command


async def commanddelete_off(chat_id: int):
    if chat_id not in command:
        command.append(chat_id)


async def commanddelete_on(chat_id: int):
    try:
        command.remove(chat_id)
    except ValueError:
        pass


# Clean Mode

async def is_cleanmode_on(chat_id: int) -> bool:
    return chat_id not in cleanmode


async def cleanmode_off(chat_id: int):
    if chat_id not in cleanmode:
        cleanmode.append(chat_id)


async def cleanmode_on(chat_id: int):
    try:
        cleanmode.remove(chat_id)
    except ValueError:
        pass


# Non-Admin Chat

async def check_nonadmin_chat(chat_id: int) -> bool:
    user = await authdb.find_one({"chat_id": chat_id})
    return bool(user)


async def is_nonadmin_chat(chat_id: int) -> bool:
    mode = nonadmin.get(chat_id)
    if not mode:
        user = await authdb.find_one({"chat_id": chat_id})
        if not user:
            nonadmin[chat_id] = False
            return False
        nonadmin[chat_id] = True
        return True
    return mode


async def add_nonadmin_chat(chat_id: int):
    nonadmin[chat_id] = True
    if await check_nonadmin_chat(chat_id):
        return
    return await authdb.insert_one({"chat_id": chat_id})


async def remove_nonadmin_chat(chat_id: int):
    nonadmin[chat_id] = False
    if not await check_nonadmin_chat(chat_id):
        return
    return await authdb.delete_one({"chat_id": chat_id})


# On / Off

async def is_on_off(on_off: int) -> bool:
    onoff = await onoffdb.find_one({"on_off": on_off})
    return bool(onoff)


async def add_on(on_off: int):
    if await is_on_off(on_off):
        return
    return await onoffdb.insert_one({"on_off": on_off})


async def add_off(on_off: int):
    if not await is_on_off(on_off):
        return
    return await onoffdb.delete_one({"on_off": on_off})


# Maintenance

async def is_maintenance():
    if not maintenance:
        get = await onoffdb.find_one({"on_off": 1})
        if not get:
            maintenance.clear()
            maintenance.append(2)
            return True
        else:
            maintenance.clear()
            maintenance.append(1)
            return False
    return 1 not in maintenance


async def maintenance_off():
    maintenance.clear()
    maintenance.append(2)
    if not await is_on_off(1):
        return
    return await onoffdb.delete_one({"on_off": 1})


async def maintenance_on():
    maintenance.clear()
    maintenance.append(1)
    if await is_on_off(1):
        return
    return await onoffdb.insert_one({"on_off": 1})


# Audio Bitrate

from pytgcalls.types import (
    HighQualityAudio,
    LowQualityAudio,
    MediumQualityAudio,
)


async def save_audio_bitrate(chat_id: int, bitrate: str):
    audio[chat_id] = bitrate


async def get_aud_bit_name(chat_id: int) -> str:
    return audio.get(chat_id, "High")


async def get_audio_bitrate(chat_id: int):
    mode = audio.get(chat_id)
    if not mode or mode == "High":
        return HighQualityAudio()
    elif mode == "Medium":
        return MediumQualityAudio()
    elif mode == "Low":
        return LowQualityAudio()
    return MediumQualityAudio()