# Shinobu Music Bot - Direct Pipe Override

import asyncio
import os
import re
import logging
import urllib.request
import urllib.parse
import yt_dlp
from pyrogram.types import Message
from typing import Union

# Helper for shell commands

async def shell_cmd(cmd):
proc = await asyncio.create_subprocess_shell(
cmd,
stdout=asyncio.subprocess.PIPE,
stderr=asyncio.subprocess.PIPE,
)
out, errorz = await proc.communicate()
return out.decode("utf-8")

class YouTubeAPI:
def **init**(self):
self.base = "https://www.youtube.com/watch?v="

```
async def url(self, message):
    if len(message.command) < 2:
        return None

    try:
        query = message.text.split(None, 1)[1].strip()
    except Exception:
        return None

    urls = [
        "youtube.com/",
        "youtu.be/",
        "spotify.com/",
        "soundcloud.com/",
    ]

    if any(x in query.lower() for x in urls):
        return query

    return None

async def _search(self, query, limit=1):
    loop = asyncio.get_running_loop()

    def do_search(q):
        # 1. Clean query for Spotify plugin artifacts
        if "googleusercontent" in q or "image" in q:
            q = "Spotify Audio"

        # 2. Primary Method: Direct Web Scrape (Bypasses API blocks)
        try:
            logging.warning(f"-> Direct-Pipe: Scraping {q}")
            encoded_query = urllib.parse.quote(q)
            url = f"https://www.youtube.com/results?search_query={encoded_query}"
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0"},
            )
            html = urllib.request.urlopen(
                req,
                timeout=8,
            ).read().decode("utf-8", errors="ignore")

            vid_ids = re.findall(r"watch\?v=(\S{11})", html)

            if vid_ids:
                vidid = vid_ids[0]

                opts = {
                    "quiet": True,
                    "skip_download": True,
                }

                with yt_dlp.YoutubeDL(opts) as ydl:
                    info = ydl.extract_info(
                        f"https://www.youtube.com/watch?v={vidid}",
                        download=False,
                    )

                    if info:
                        return [info]

        except Exception as e:
            logging.error(f"-> Direct-Pipe Failed: {e}")

        return []

    return await loop.run_in_executor(None, do_search, query)

async def track(self, link: str, videoid: Union[bool, str] = None):
    results = await self._search(link, limit=1)

    if not results:
        raise Exception("No search results found.")

    res = results[0]

    return {
        "title": res.get("title", "Unknown"),
        "link": f"https://www.youtube.com/watch?v={res.get('id')}",
        "vidid": res.get("id"),
        "duration_min": "00:00",
    }, res.get("id")

async def details(self, link: str, videoid: Union[bool, str] = None):
    results = await self._search(link, limit=1)

    if not results:
        raise Exception("No search results found.")

    res = results[0]

    return (
        res.get("title"),
        "00:00",
        0,
        res.get("id"),
    )

async def title(self, link: str, videoid: Union[bool, str] = None):
    res = await self._search(link, limit=1)
    return res[0].get("title") if res else "Unknown"

async def duration(self, link: str, videoid: Union[bool, str] = None):
    return "None"

async def playlist(
    self,
    link,
    limit,
    user_id,
    videoid: Union[bool, str] = None,
):
    playlist = await shell_cmd(
        f"yt-dlp -i --get-id --flat-playlist --playlist-end {limit} --skip-download {link}"
    )

    return [x for x in playlist.split("\n") if x]

async def slider(
    self,
    link: str,
    query_type: int,
    videoid: Union[bool, str] = None,
):
    results = await self._search(link, limit=10)

    if not results:
        raise Exception("No search results found.")

    res = results[query_type if query_type < len(results) else 0]

    return (
        res.get("title"),
        "00:00",
        res.get("id"),
    )

async def download(
    self,
    link: str,
    mystic,
    videoid: Union[bool, str] = None,
    songaudio: Union[bool, str] = None,
    title: Union[bool, str] = None,
) -> str:

    if videoid:
        link = self.base + link

    loop = asyncio.get_running_loop()

    def audio_dl():
        ydl_opts = {
            "format": "bestaudio[ext=opus]/bestaudio[ext=m4a]/bestaudio/best",
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "quiet": True,
        }

        x = yt_dlp.YoutubeDL(ydl_opts)

        info = x.extract_info(link, False)

        path = f"downloads/{info['id']}.{info['ext']}"

        if not os.path.exists(path):
            x.download([link])

        return path

    def song_audio_dl():
        fpath = f"downloads/{title}.mp3"

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": fpath,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "320",
                }
            ],
        }

        yt_dlp.YoutubeDL(ydl_opts).download([link])

        return fpath

    if songaudio:
        path = await loop.run_in_executor(None, song_audio_dl)
        return path

    return await loop.run_in_executor(None, audio_dl), True
```
