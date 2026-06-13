# Shinobu Music Bot
# Owner: @Sanji_fr

import asyncio
import speedtest

from pyrogram import filters
from strings import get_command
from Shinobu import app
from Shinobu.misc import SUDOERS

SPEEDTEST_COMMAND = get_command("SPEEDTEST_COMMAND")


def testspeed():
    test = speedtest.Speedtest()
    test.get_best_server()
    test.download()
    test.upload()
    test.results.share()
    return test.results.dict()


@app.on_message(filters.command(SPEEDTEST_COMMAND) & SUDOERS)
async def speedtest_function(client, message):
    m = await message.reply_text("Running speed test, please wait...")
    loop = asyncio.get_event_loop()
    try:
        result = await loop.run_in_executor(None, testspeed)
    except Exception as e:
        return await m.edit(f"Speed test failed: `{e}`")
    output = (
        f"**Speedtest Results**\n\n"
        f"**ISP:** {result['client']['isp']}\n"
        f"**Country:** {result['client']['country']}\n\n"
        f"**Server:** {result['server']['name']}\n"
        f"**Server Country:** {result['server']['country']}\n"
        f"**Sponsor:** {result['server']['sponsor']}\n"
        f"**Latency:** {result['server']['latency']}\n"
        f"**Ping:** {result['ping']}"
    )
    await app.send_photo(
        chat_id=message.chat.id,
        photo=result["share"],
        caption=output,
    )
    await m.delete()