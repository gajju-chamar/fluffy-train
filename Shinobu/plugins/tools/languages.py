# Shinobu Music Bot
# Owner: @Sanji_fr

from pykeyboard import InlineKeyboard
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, Message

from config import BANNED_USERS
from strings import get_command, get_string, languages_present
from Shinobu import app
from Shinobu.utils.database import get_lang, set_lang
from Shinobu.utils.decorators import ActualAdminCB, language, languageCB


def languages_keyboard(_):
    keyboard = InlineKeyboard(row_width=3)
    keyboard.add(
        *[
            InlineKeyboardButton(
                text=languages_present[i],
                callback_data=f"languages:{i}",
            )
            for i in languages_present
        ]
    )
    keyboard.row(
        InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="settingsback_helper"),
        InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close"),
    )
    return keyboard


LANGUAGE_COMMAND = get_command("LANGUAGE_COMMAND")


@app.on_message(
    filters.command(LANGUAGE_COMMAND)
    & filters.group
    & ~filters.edited
    & ~BANNED_USERS
)
@language
async def langs_command(client, message: Message, _):
    keyboard = languages_keyboard(_)
    await message.reply_text(
        _["setting_1"].format(message.chat.title, message.chat.id),
        reply_markup=keyboard,
    )


@app.on_callback_query(filters.regex("LG") & ~BANNED_USERS)
@languageCB
async def languagecb(client, CallbackQuery, _):
    try:
        await CallbackQuery.answer()
    except:
        pass
    keyboard = languages_keyboard(_)
    return await CallbackQuery.edit_message_reply_markup(reply_markup=keyboard)


@app.on_callback_query(filters.regex(r"languages:(.*?)") & ~BANNED_USERS)
@ActualAdminCB
async def language_markup(client, CallbackQuery, _):
    lang = (CallbackQuery.data).split(":")[1]
    old = await get_lang(CallbackQuery.message.chat.id)
    if str(old) == str(lang):
        return await CallbackQuery.answer(
            "You're already using this language.", show_alert=True
        )
    try:
        _ = get_string(lang)
        await CallbackQuery.answer("Language changed successfully.", show_alert=True)
    except:
        return await CallbackQuery.answer(
            "Failed to change language or language is under update.",
            show_alert=True,
        )
    await set_lang(CallbackQuery.message.chat.id, lang)
    keyboard = languages_keyboard(_)
    return await CallbackQuery.edit_message_reply_markup(reply_markup=keyboard)