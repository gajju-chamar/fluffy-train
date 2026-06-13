# Shinobu Music Bot
# Owner: @Sanji_fr

import random

from pyrogram import filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup

from config import AUTO_DOWNLOADS_CLEAR, BANNED_USERS, adminlist
from Shinobu import YouTube, app
from Shinobu.core.call import Shinobu
from Shinobu.misc import SUDOERS, db
from Shinobu.utils.database import (
    is_active_chat,
    is_music_playing,
    is_muted,
    is_nonadmin_chat,
    music_off,
    music_on,
    mute_off,
    mute_on,
    set_loop,
)
from Shinobu.utils.decorators.language import languageCB
from Shinobu.utils.formatters import seconds_to_min
from Shinobu.utils.inline.play import (
    panel_markup_1,
    panel_markup_2,
    panel_markup_3,
    stream_markup,
    telegram_markup,
)
from Shinobu.utils.stream.autoclear import auto_clean
from Shinobu.utils.thumbnails import gen_thumb

wrong = {}


@app.on_callback_query(filters.regex("PanelMarkup") & ~BANNED_USERS)
@languageCB
async def markup_panel(client, CallbackQuery: CallbackQuery, _):
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    videoid, chat_id = callback_request.split("|")
    chat_id = CallbackQuery.message.chat.id
    buttons = panel_markup_1(_, videoid, chat_id)
    try:
        await CallbackQuery.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except:
        return
    if chat_id not in wrong:
        wrong[chat_id] = {}
    wrong[chat_id][CallbackQuery.message.message_id] = False


@app.on_callback_query(filters.regex("MainMarkup") & ~BANNED_USERS)
@languageCB
async def del_back_playlist(client, CallbackQuery, _):
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    videoid, chat_id = callback_request.split("|")
    if videoid == str(None):
        buttons = telegram_markup(_, chat_id)
    else:
        buttons = stream_markup(_, videoid, chat_id)
    chat_id = CallbackQuery.message.chat.id
    try:
        await CallbackQuery.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except:
        return
    if chat_id not in wrong:
        wrong[chat_id] = {}
    wrong[chat_id][CallbackQuery.message.message_id] = True


@app.on_callback_query(filters.regex("Pages") & ~BANNED_USERS)
@languageCB
async def pages_callback(client, CallbackQuery, _):
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    state, pages, videoid, chat = callback_request.split("|")
    chat_id = int(chat)
    pages = int(pages)
    if state == "Forw":
        if pages == 0:
            buttons = panel_markup_2(_, videoid, chat_id)
        elif pages == 2:
            buttons = panel_markup_1(_, videoid, chat_id)
        elif pages == 1:
            buttons = panel_markup_3(_, videoid, chat_id)
    if state == "Back":
        if pages == 2:
            buttons = panel_markup_2(_, videoid, chat_id)
        elif pages == 1:
            buttons = panel_markup_1(_, videoid, chat_id)
        elif pages == 0:
            buttons = panel_markup_3(_, videoid, chat_id)
    try:
        await CallbackQuery.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except:
        return


@app.on_callback_query(filters.regex("ADMIN") & ~BANNED_USERS)
@languageCB
async def admin_callback(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    command, chat = callback_request.split("|")
    chat_id = int(chat)
    if not await is_active_chat(chat_id):
        return await CallbackQuery.answer(_["general_6"], show_alert=True)
    mention = CallbackQuery.from_user.mention
    is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
    if not is_non_admin:
        if CallbackQuery.from_user.id not in SUDOERS:
            admins = adminlist.get(CallbackQuery.message.chat.id)
            if not admins:
                return await CallbackQuery.answer(_["admin_18"], show_alert=True)
            if CallbackQuery.from_user.id not in admins:
                return await CallbackQuery.answer(_["admin_19"], show_alert=True)

    if command == "Pause":
        if not await is_music_playing(chat_id):
            return await CallbackQuery.answer(_["admin_1"], show_alert=True)
        await CallbackQuery.answer()
        await music_off(chat_id)
        await Shinobu.pause_stream(chat_id)
        await CallbackQuery.message.reply_text(_["admin_2"].format(mention))

    elif command == "Resume":
        if await is_music_playing(chat_id):
            return await CallbackQuery.answer(_["admin_3"], show_alert=True)
        await CallbackQuery.answer()
        await music_on(chat_id)
        await Shinobu.resume_stream(chat_id)
        await CallbackQuery.message.reply_text(_["admin_4"].format(mention))

    elif command in ("Stop", "End"):
        await CallbackQuery.answer()
        await Shinobu.stop_stream(chat_id)
        await set_loop(chat_id, 0)
        await CallbackQuery.message.reply_text(_["admin_9"].format(mention))

    elif command == "Mute":
        if await is_muted(chat_id):
            return await CallbackQuery.answer(_["admin_5"], show_alert=True)
        await CallbackQuery.answer()
        await mute_on(chat_id)
        await Shinobu.mute_stream(chat_id)
        await CallbackQuery.message.reply_text(_["admin_6"].format(mention))

    elif command == "Unmute":
        if not await is_muted(chat_id):
            return await CallbackQuery.answer(_["admin_7"], show_alert=True)
        await CallbackQuery.answer()
        await mute_off(chat_id)
        await Shinobu.unmute_stream(chat_id)
        await CallbackQuery.message.reply_text(_["admin_8"].format(mention))

    elif command == "Loop":
        await CallbackQuery.answer()
        await set_loop(chat_id, 3)
        await CallbackQuery.message.reply_text(_["admin_25"].format(mention, 3))

    elif command == "Shuffle":
        check = db.get(chat_id)
        if not check:
            return await CallbackQuery.answer(_["admin_21"], show_alert=True)
        try:
            popped = check.pop(0)
        except:
            return await CallbackQuery.answer(_["admin_22"], show_alert=True)
        check = db.get(chat_id)
        if not check:
            check.insert(0, popped)
            return await CallbackQuery.answer(_["admin_22"], show_alert=True)
        await CallbackQuery.answer()
        random.shuffle(check)
        check.insert(0, popped)
        await CallbackQuery.message.reply_text(_["admin_23"].format(mention))

    elif command == "Skip":
        check = db.get(chat_id)
        txt = f"Skipped by {mention}"
        popped = None
        try:
            popped = check.pop(0)
            if popped and AUTO_DOWNLOADS_CLEAR == str(True):
                await auto_clean(popped)
            if not check:
                await CallbackQuery.edit_message_text(txt)
                await CallbackQuery.message.reply_text(_["admin_10"].format(mention))
                try:
                    return await Shinobu.stop_stream(chat_id)
                except:
                    return
        except:
            try:
                await CallbackQuery.edit_message_text(txt)
                await CallbackQuery.message.reply_text(_["admin_10"].format(mention))
                return await Shinobu.stop_stream(chat_id)
            except:
                return

        await CallbackQuery.answer()
        queued = check[0]["file"]
        title = (check[0]["title"]).title()
        user = check[0]["by"]
        videoid = check[0]["vidid"]
        db[chat_id][0]["played"] = 0

        if "live_" in queued:
            n, link = await YouTube.video(videoid, True)
            if n == 0:
                return await CallbackQuery.message.reply_text(_["admin_11"].format(title))
            try:
                await Shinobu.skip_stream(chat_id, link)
            except Exception:
                return await CallbackQuery.message.reply_text(_["call_9"])
            img = await gen_thumb(title, check[0]["dur"], user)
            button = telegram_markup(_, chat_id)
            run = await CallbackQuery.message.reply_photo(
                photo=img,
                caption=_["stream_1"].format(
                    user, f"https://t.me/{app.username}?start=info_{videoid}"
                ),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
            await CallbackQuery.edit_message_text(txt)

        elif "vid_" in queued:
            mystic = await CallbackQuery.message.reply_text(
                _["call_10"], disable_web_page_preview=True
            )
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
            run = await CallbackQuery.message.reply_photo(
                photo=img,
                caption=_["stream_1"].format(
                    user, f"https://t.me/{app.username}?start=info_{videoid}"
                ),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "stream"
            await CallbackQuery.edit_message_text(txt)
            await mystic.delete()

        elif "index_" in queued:
            try:
                await Shinobu.skip_stream(chat_id, videoid)
            except Exception:
                return await CallbackQuery.message.reply_text(_["call_9"])
            img = await gen_thumb(title, check[0]["dur"], user)
            button = telegram_markup(_, chat_id)
            run = await CallbackQuery.message.reply_photo(
                photo=img,
                caption=_["stream_2"].format(user),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
            await CallbackQuery.edit_message_text(txt)

        else:
            try:
                await Shinobu.skip_stream(chat_id, queued)
            except Exception:
                return await CallbackQuery.message.reply_text(_["call_9"])
            img = await gen_thumb(title, check[0]["dur"], user)
            button = stream_markup(_, videoid, chat_id)
            run = await CallbackQuery.message.reply_photo(
                photo=img,
                caption=_["stream_1"].format(
                    user, f"https://t.me/{app.username}?start=info_{videoid}"
                ),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "stream"
            await CallbackQuery.edit_message_text(txt)

    else:
        # Seek commands (1=back10, 2=fwd10, 3=back30, 4=fwd30)
        playing = db.get(chat_id)
        if not playing:
            return await CallbackQuery.answer(_["queue_2"], show_alert=True)
        duration_seconds = int(playing[0]["seconds"])
        if duration_seconds == 0:
            return await CallbackQuery.answer(_["admin_30"], show_alert=True)
        file_path = playing[0]["file"]
        if "index_" in file_path or "live_" in file_path:
            return await CallbackQuery.answer(_["admin_30"], show_alert=True)
        duration_played = int(playing[0]["played"])
        duration_to_skip = 10 if int(command) in [1, 2] else 30
        duration = playing[0]["dur"]
        if int(command) in [1, 3]:
            if (duration_played - duration_to_skip) <= 10:
                bet = seconds_to_min(duration_played)
                return await CallbackQuery.answer(
                    f"Cannot seek back — already at {bet} mins of {duration} mins.",
                    show_alert=True,
                )
            to_seek = duration_played - duration_to_skip + 1
        else:
            if (duration_seconds - (duration_played + duration_to_skip)) <= 10:
                bet = seconds_to_min(duration_played)
                return await CallbackQuery.answer(
                    f"Cannot seek forward — too close to end. At {bet} mins of {duration} mins.",
                    show_alert=True,
                )
            to_seek = duration_played + duration_to_skip + 1
        await CallbackQuery.answer()
        mystic = await CallbackQuery.message.reply_text(_["admin_32"])
        try:
            await Shinobu.seek_stream(
                chat_id,
                file_path,
                seconds_to_min(to_seek),
                duration,
            )
        except:
            return await mystic.edit_text(_["admin_34"])
        if int(command) in [1, 3]:
            db[chat_id][0]["played"] -= duration_to_skip
        else:
            db[chat_id][0]["played"] += duration_to_skip
        await mystic.edit_text(
            f"{_['admin_33'].format(seconds_to_min(to_seek))}\n\nChanges done by: {mention}"
        )