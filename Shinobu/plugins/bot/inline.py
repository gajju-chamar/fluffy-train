# Shinobu Music Bot
# Owner: @Sanji_fr

from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultPhoto,
)
from youtubesearchpython.__future__ import VideosSearch

from config import BANNED_USERS, MUSIC_BOT_NAME
from Shinobu import app
from Shinobu.utils.inlinequery import answer


@app.on_inline_query(~BANNED_USERS)
async def inline_query_handler(client, query):
    text = query.query.strip().lower()
    answers = []
    if text.strip() == "":
        try:
            await client.answer_inline_query(query.id, results=answer, cache_time=10)
        except:
            return
    else:
        a = VideosSearch(text, limit=20)
        result = (await a.next()).get("result")
        for x in range(15):
            title = (result[x]["title"]).title()
            duration = result[x]["duration"]
            views = result[x]["viewCount"]["short"]
            thumbnail = result[x]["thumbnails"][0]["url"].split("?")[0]
            channel = result[x]["channel"]["name"]
            channellink = result[x]["channel"]["link"]
            link = result[x]["link"]
            published = result[x]["publishedTime"]
            description = f"{views} | {duration} | {channel} | {published}"
            buttons = InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="▶️ Play on YouTube", url=link)]]
            )
            searched_text = (
                f"❇️ **Title:** [{title}]({link})\n\n"
                f"⏳ **Duration:** {duration}\n"
                f"👀 **Views:** `{views}`\n"
                f"⏰ **Published:** {published}\n"
                f"🎥 **Channel:** [{channel}]({channellink})\n\n"
                f"_Reply with /play on this message to stream it in voice chat._\n\n"
                f"⚡️ **Inline Search by {MUSIC_BOT_NAME}**"
            )
            answers.append(
                InlineQueryResultPhoto(
                    photo_url=thumbnail,
                    title=title,
                    thumb_url=thumbnail,
                    description=description,
                    caption=searched_text,
                    reply_markup=buttons,
                )
            )
        try:
            return await client.answer_inline_query(query.id, results=answers)
        except:
            return