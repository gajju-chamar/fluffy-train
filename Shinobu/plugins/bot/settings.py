# Shinobu Music Bot
# Owner: @Sanji_fr

from pyrogram import filters
from pyrogram.errors import MessageNotModified
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from config import BANNED_USERS, CLEANMODE_DELETE_MINS, MUSIC_BOT_NAME, OWNER_ID
from strings import get_command
from Shinobu import app
from Shinobu.utils.database import (
    add_nonadmin_chat,
    cleanmode_off,
    cleanmode_on,
    commanddelete_off,
    commanddelete_on,
    get_aud_bit_name,
    get_authuser,
    get_authuser_names,
    get_playmode,
    get_playtype,
    is_cleanmode_on,
    is_commanddelete_on,
    is_nonadmin_chat,
    remove_nonadmin_chat,
    save_audio_bitrate,
    set_playmode,
    set_playtype,
)
from Shinobu.utils.decorators.admins import ActualAdminCB
from Shinobu.utils.decorators.language import language, languageCB
from Shinobu.utils.inline.settings import (
    audio_quality_markup,
    auth_users_markup,
    cleanmode_settings_markup,
    playmode_users_markup,
    setting_markup,
)
from Shinobu.utils.inline.start import private_panel

SETTINGS_COMMAND = get_command("SETTINGS_COMMAND")


@app.on_message(
    filters.command(SETTINGS_COMMAND)
    & filters.group
    
    & ~BANNED_USERS
)
@language
async def settings_mar(client, message: Message, _):
    buttons = setting_markup(_)
    await message.reply_text(
        _["setting_1"].format(message.chat.title, message.chat.id),
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@app.on_callback_query(filters.regex("settings_helper") & ~BANNED_USERS)
@languageCB
async def settings_cb(client, CallbackQuery, _):
    try:
        await CallbackQuery.answer(_["set_cb_8"])
    except:
        pass
    buttons = setting_markup(_)
    return await CallbackQuery.edit_message_text(
        _["setting_1"].format(
            CallbackQuery.message.chat.title,
            CallbackQuery.message.chat.id,
        ),
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@app.on_callback_query(filters.regex("settingsback_helper") & ~BANNED_USERS)
@languageCB
async def settings_back_markup(client, CallbackQuery: CallbackQuery, _):
    try:
        await CallbackQuery.answer()
    except:
        pass
    if CallbackQuery.message.chat.type == "private":
        try:
            await app.resolve_peer(OWNER_ID[0])
            OWNER = OWNER_ID[0]
        except:
            OWNER = None
        buttons = private_panel(_, app.username, OWNER)
        return await CallbackQuery.edit_message_text(
            _["start_2"].format(MUSIC_BOT_NAME),
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        buttons = setting_markup(_)
        return await CallbackQuery.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )


async def gen_buttons_aud(_, aud):
    if aud == "High":
        buttons = audio_quality_markup(_, high=True)
    elif aud == "Medium":
        buttons = audio_quality_markup(_, medium=True)
    elif aud == "Low":
        buttons = audio_quality_markup(_, low=True)
    return buttons


# Non-admin info callbacks
@app.on_callback_query(
    filters.regex(
        pattern=r"^(SEARCHANSWER|PLAYMODEANSWER|PLAYTYPEANSWER|AUTHANSWER|CMANSWER|COMMANDANSWER|CM|AQ|PM|AU)$"
    )
    & ~BANNED_USERS
)
@languageCB
async def without_Admin_rights(client, CallbackQuery, _):
    command = CallbackQuery.matches[0].group(1)
    if command == "SEARCHANSWER":
        return await CallbackQuery.answer(_["setting_3"], show_alert=True)
    if command == "PLAYMODEANSWER":
        return await CallbackQuery.answer(_["setting_10"], show_alert=True)
    if command == "PLAYTYPEANSWER":
        return await CallbackQuery.answer(_["setting_11"], show_alert=True)
    if command == "AUTHANSWER":
        return await CallbackQuery.answer(_["setting_4"], show_alert=True)
    if command == "CMANSWER":
        return await CallbackQuery.answer(
            _["setting_9"].format(CLEANMODE_DELETE_MINS), show_alert=True
        )
    if command == "COMMANDANSWER":
        return await CallbackQuery.answer(_["setting_14"], show_alert=True)
    if command == "CM":
        try:
            await CallbackQuery.answer(_["set_cb_5"], show_alert=True)
        except:
            pass
        cle = True if await is_cleanmode_on(CallbackQuery.message.chat.id) else None
        sta = True if await is_commanddelete_on(CallbackQuery.message.chat.id) else None
        buttons = cleanmode_settings_markup(_, status=cle, dels=sta)
    if command == "AQ":
        try:
            await CallbackQuery.answer(_["set_cb_1"], show_alert=True)
        except:
            pass
        aud = await get_aud_bit_name(CallbackQuery.message.chat.id)
        buttons = await gen_buttons_aud(_, aud)
    if command == "PM":
        try:
            await CallbackQuery.answer(_["set_cb_4"], show_alert=True)
        except:
            pass
        playmode = await get_playmode(CallbackQuery.message.chat.id)
        Direct = True if playmode == "Direct" else None
        is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
        Group = True if not is_non_admin else None
        playty = await get_playtype(CallbackQuery.message.chat.id)
        Playtype = None if playty == "Everyone" else True
        buttons = playmode_users_markup(_, Direct, Group, Playtype)
    if command == "AU":
        try:
            await CallbackQuery.answer(_["set_cb_3"], show_alert=True)
        except:
            pass
        is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
        buttons = auth_users_markup(_, True) if not is_non_admin else auth_users_markup(_)
    try:
        return await CallbackQuery.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except MessageNotModified:
        return


# Audio Quality
@app.on_callback_query(
    filters.regex(pattern=r"^(LQA|MQA|HQA)$") & ~BANNED_USERS
)
@ActualAdminCB
async def aud_cb(client, CallbackQuery, _):
    command = CallbackQuery.matches[0].group(1)
    try:
        await CallbackQuery.answer(_["set_cb_6"], show_alert=True)
    except:
        pass
    if command == "LQA":
        await save_audio_bitrate(CallbackQuery.message.chat.id, "Low")
        buttons = audio_quality_markup(_, low=True)
    elif command == "MQA":
        await save_audio_bitrate(CallbackQuery.message.chat.id, "Medium")
        buttons = audio_quality_markup(_, medium=True)
    elif command == "HQA":
        await save_audio_bitrate(CallbackQuery.message.chat.id, "High")
        buttons = audio_quality_markup(_, high=True)
    try:
        return await CallbackQuery.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except MessageNotModified:
        return


# Play Mode Settings
@app.on_callback_query(
    filters.regex(pattern=r"^(MODECHANGE|CHANNELMODECHANGE|PLAYTYPECHANGE)$")
    & ~BANNED_USERS
)
@ActualAdminCB
async def playmode_ans(client, CallbackQuery, _):
    command = CallbackQuery.matches[0].group(1)
    is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)

    if command == "CHANNELMODECHANGE":
        if not is_non_admin:
            await add_nonadmin_chat(CallbackQuery.message.chat.id)
            Group = None
        else:
            await remove_nonadmin_chat(CallbackQuery.message.chat.id)
            Group = True
        playmode = await get_playmode(CallbackQuery.message.chat.id)
        Direct = True if playmode == "Direct" else None
        playty = await get_playtype(CallbackQuery.message.chat.id)
        Playtype = None if playty == "Everyone" else True
        buttons = playmode_users_markup(_, Direct, Group, Playtype)

    elif command == "MODECHANGE":
        try:
            await CallbackQuery.answer(_["set_cb_6"], show_alert=True)
        except:
            pass
        playmode = await get_playmode(CallbackQuery.message.chat.id)
        if playmode == "Direct":
            await set_playmode(CallbackQuery.message.chat.id, "Inline")
            Direct = None
        else:
            await set_playmode(CallbackQuery.message.chat.id, "Direct")
            Direct = True
        Group = True if not is_non_admin else None
        playty = await get_playtype(CallbackQuery.message.chat.id)
        Playtype = False if playty == "Everyone" else True
        buttons = playmode_users_markup(_, Direct, Group, Playtype)

    elif command == "PLAYTYPECHANGE":
        try:
            await CallbackQuery.answer(_["set_cb_6"], show_alert=True)
        except:
            pass
        playty = await get_playtype(CallbackQuery.message.chat.id)
        if playty == "Everyone":
            await set_playtype(CallbackQuery.message.chat.id, "Admin")
            Playtype = False
        else:
            await set_playtype(CallbackQuery.message.chat.id, "Everyone")
            Playtype = True
        playmode = await get_playmode(CallbackQuery.message.chat.id)
        Direct = True if playmode == "Direct" else None
        Group = True if not is_non_admin else None
        buttons = playmode_users_markup(_, Direct, Group, Playtype)

    try:
        return await CallbackQuery.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except MessageNotModified:
        return


# Auth Users Settings
@app.on_callback_query(
    filters.regex(pattern=r"^(AUTH|AUTHLIST)$") & ~BANNED_USERS
)
@ActualAdminCB
async def authusers_mar(client, CallbackQuery, _):
    command = CallbackQuery.matches[0].group(1)
    if command == "AUTHLIST":
        _authusers = await get_authuser_names(CallbackQuery.message.chat.id)
        if not _authusers:
            try:
                return await CallbackQuery.answer(_["setting_5"], show_alert=True)
            except:
                return
        try:
            await CallbackQuery.answer(_["set_cb_7"], show_alert=True)
        except:
            pass
        j = 0
        await CallbackQuery.edit_message_text(_["auth_6"])
        msg = _["auth_7"]
        for note in _authusers:
            _note = await get_authuser(CallbackQuery.message.chat.id, note)
            user_id = _note["auth_user_id"]
            admin_id = _note["admin_id"]
            admin_name = _note["admin_name"]
            try:
                user = await client.get_users(user_id)
                user = user.first_name
                j += 1
            except Exception:
                continue
            msg += f"{j}➤ {user}[`{user_id}`]\n"
            msg += f"   {_['auth_8']} {admin_name}[`{admin_id}`]\n\n"
        upl = InlineKeyboardMarkup(
            [[
                InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="AU"),
                InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close"),
            ]]
        )
        try:
            return await CallbackQuery.edit_message_text(msg, reply_markup=upl)
        except MessageNotModified:
            return

    try:
        await CallbackQuery.answer(_["set_cb_6"], show_alert=True)
    except:
        pass
    if command == "AUTH":
        is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
        if not is_non_admin:
            await add_nonadmin_chat(CallbackQuery.message.chat.id)
            buttons = auth_users_markup(_)
        else:
            await remove_nonadmin_chat(CallbackQuery.message.chat.id)
            buttons = auth_users_markup(_, True)
    try:
        return await CallbackQuery.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except MessageNotModified:
        return


# Clean Mode
@app.on_callback_query(
    filters.regex(pattern=r"^(CLEANMODE|COMMANDELMODE)$") & ~BANNED_USERS
)
@ActualAdminCB
async def cleanmode_mark(client, CallbackQuery, _):
    command = CallbackQuery.matches[0].group(1)
    try:
        await CallbackQuery.answer(_["set_cb_6"], show_alert=True)
    except:
        pass
    cle = None
    sta = None
    if command == "CLEANMODE":
        sta = True if await is_commanddelete_on(CallbackQuery.message.chat.id) else None
        if await is_cleanmode_on(CallbackQuery.message.chat.id):
            await cleanmode_off(CallbackQuery.message.chat.id)
        else:
            await cleanmode_on(CallbackQuery.message.chat.id)
            cle = True
    elif command == "COMMANDELMODE":
        cle = True if await is_cleanmode_on(CallbackQuery.message.chat.id) else None
        if await is_commanddelete_on(CallbackQuery.message.chat.id):
            await commanddelete_off(CallbackQuery.message.chat.id)
        else:
            await commanddelete_on(CallbackQuery.message.chat.id)
            sta = True
    buttons = cleanmode_settings_markup(_, status=cle, dels=sta)
    try:
        return await CallbackQuery.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except MessageNotModified:
        return