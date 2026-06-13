# Shinobu Music Bot
# Owner: @Sanji_fr

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, Message

import config
from config import BANNED_USERS
from strings import get_command
from Shinobu import YouTube, app
from Shinobu.core.call import Shinobu
from Shinobu.misc import db
from Shinobu.utils.database import get_loop
from Shinobu.utils.decorators import AdminRightsCheck
from Shinobu.utils.inline.play import stream_markup, telegram_markup
from Shinobu.utils.stream.autoclear import auto_clean
from Shinobu.utils.thumbnails import gen_thumb

SKIP_COMMAND = get_command("SKIP_COMMAND")


@app.on_message(
    filters.command(SKIP_COMMAND)
    & filters.group
    & ~filters.edited
    & ~BANNED_USERS
)
@AdminRightsCheck
async def skip(cli, message: Message, _, chat_id):
    if not len(message.command) < 2:
        loop = await get_loop(chat_id)
        if loop != 0:
            return await message.reply_text(_["admin_12"])
        state = message.text.split(None, 1)[1].strip()
        if state.isnumeric():
            state = int(state)
            check = db.get(chat_id)
            if check:
                count = len(check)
                if count > 2:
                    count = count - 1
                    if 1 <= state <= count:
                        for x in range(state):
                            popped = None
                            try:
                                popped = check.pop(0)
                            except:
                                return await message.reply_text(_["admin_16"])
                            if popped and config.AUTO_DOWNLOADS_CLEAR == str(True):
                                await auto_clean(popped)
                            if not check:
                                try:
                                    await message.reply_text(
                                        _["admin_10"].format(message.from_user.first_name)
                                    )
                                    await Shinobu.stop_stream(chat_id)
                                except:
                                    return
                                break
                    else:
                        return await message.reply_text(_["admin_15"].format(count))
                else:
                    return await message.reply_text(_["admin_14"])
            else:
                return await message.reply_text(_["queue_2"])
        else:
            return await message.reply_text(_["admin_13"])
    else:
        check = db.get(chat_id)
        popped = None
        try:
            popped = check.pop(0)
            if popped and config.AUTO_DOWNLOADS_CLEAR == str(True):
                await auto_clean(popped)
            if not check:
                await message.reply_text(
                    _["admin_10"].format(message.from_user.first_name)
                )
                try:
                    return await Shinobu.stop_stream(chat_id)
                except:
                    return
        except:
            try:
                await message.reply_text(
                    _["admin_10"].format(message.from_user.first_name)
                )
                return await Shinobu.stop_stream(chat_id)
            except:
                return

    queued = check[0]["file"]
    title = (check[0]["title"]).title()
    user = check[0]["by"]
    videoid = check[0]["vidid"]
    db[chat_id][0]["played"] = 0

    if "live_" in queued:
        n, link = await YouTube.video(videoid, True)
        if n == 0:
            return await message.reply_text(_["admin_11"].format(title))
        try:
            await Shinobu.skip_stream(chat_id, link)
        except Exception:
            return await message.reply_text(_["call_9"])
        img = await gen_thumb(title, check[0]["dur"], user)
        button = telegram_markup(_, chat_id)
        run = await message.reply_photo(
            photo=img,
            caption=_["stream_1"].format(
                user, f"https://t.me/{app.username}?start=info_{videoid}"
            ),
            reply_markup=InlineKeyboardMarkup(button),
        )
        db[chat_id][0]["mystic"] = run
        db[chat_id][0]["markup"] = "tg"

    elif "vid_" in queued:
        mystic = await message.reply_text(_["call_10"], disable_web_page_preview=True)
        try:
            file_path, direct = await YouTube.download(videoid, mystic, videoid=True)
        except:
            return await mystic.edit_text(_["call_9"])
        try:
            await Shinobu.skip_stream(chat_id, file_path)
        except Exception:
            return await mystic.edit_text(_["call_9"])
        img = await gen_thumb(title, check[0]["dur"], user)
        button = stream_markup(_, videoid, chat_id)
        run = await message.reply_photo(
            photo=img,
            caption=_["stream_1"].format(
                user, f"https://t.me/{app.username}?start=info_{videoid}"
            ),
            reply_markup=InlineKeyboardMarkup(button),
        )
        db[chat_id][0]["mystic"] = run
        db[chat_id][0]["markup"] = "stream"
        await mystic.delete()

    elif "index_" in queued:
        try:
            await Shinobu.skip_stream(chat_id, videoid)
        except Exception:
            return await message.reply_text(_["call_9"])
        img = await gen_thumb(title, check[0]["dur"], user)
        button = telegram_markup(_, chat_id)
        run = await message.reply_photo(
            photo=img,
            caption=_["stream_2"].format(user),
            reply_markup=InlineKeyboardMarkup(button),
        )
        db[chat_id][0]["mystic"] = run
        db[chat_id][0]["markup"] = "tg"

    else:
        try:
            await Shinobu.skip_stream(chat_id, queued)
        except Exception:
            return await message.reply_text(_["call_9"])
        img = await gen_thumb(title, check[0]["dur"], user)
        button = stream_markup(_, videoid, chat_id)
        run = await message.reply_photo(
            photo=img,
            caption=_["stream_1"].format(
                user, f"https://t.me/{app.username}?start=info_{videoid}"
            ),
            reply_markup=InlineKeyboardMarkup(button),
        )
        db[chat_id][0]["mystic"] = run
        db[chat_id][0]["markup"] = "stream"