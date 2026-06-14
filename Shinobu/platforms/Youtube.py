# Shinobu Music Bot
# Owner: @Sanji_fr

import asyncio
import os
import re
import logging
from typing import Union

import yt_dlp
from pyrogram.types import Message

import config
from Shinobu.utils.formatters import time_to_seconds


async def shell_cmd(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    out, errorz = await proc.communicate()
    if errorz:
        if "unavailable videos are hidden" in (errorz.decode("utf-8")).lower():
            return out.decode("utf-8")
        else:
            return errorz.decode("utf-8")
    return out.decode("utf-8")


class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"
        self.listbase = "https://youtube.com/playlist?list="
        self.reg = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

    async def exists(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        return bool(re.search(self.regex, link))

    async def url(self, message_1: Message) -> Union[str, None]:
        messages = [message_1]
        if message_1.reply_to_message:
            messages.append(message_1.reply_to_message)
        text = ""
        offset = None
        length = None
        for message in messages:
            if offset:
                break
            if message.entities:
                for entity in message.entities:
                    if entity.type == "url":
                        text = message.text or message.caption
                        offset, length = entity.offset, entity.length
                        break
            elif message.caption_entities:
                for entity in message.caption_entities:
                    if entity.type == "text_link":
                        return entity.url
        if offset is None:
            return None
        return text[offset: offset + length]

    async def _search(self, query, limit=1):
        loop = asyncio.get_running_loop()

        def do_search(q):
            logging.warning(f"--- STARTING SEARCH FOR: {q} ---")

            # Spotify plugin failsafe
            if "googleusercontent" in q or "image" in q:
                logging.warning("-> Caught Spotify image link. Reverting to generic search.")
                q = "Spotify Audio"

            if "http" in q and not re.search(r"(?:youtube\.com|youtu\.be)", q):
                search_query = f"ytsearch{limit}:{q}"
            elif "http" in q:
                search_query = q
            else:
                search_query = f"ytsearch{limit}:{q}"

            # METHOD 1: Standard Search
            try:
                logging.warning("-> Attempting Method 1: Standard Search")

                ydl_opts = {
                    "quiet": True,
                    "extract_flat": False,
                    "skip_download": True,
                    "no_warnings": True,
                    "noplaylist": True,
                    "cookiefile": "cookies.txt",
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(search_query, download=False)
                    logging.warning(f"SEARCH RESULT = {info}")

                    if info:
                        if "entries" in info:
                            entries = [e for e in info["entries"] if e]
                            if entries:
                                return entries[:limit]
                        elif "id" in info:
                            return [info]

            except Exception as e:
                logging.error(f"-> Method 1 Failed: {e}")

            # METHOD 2: Web Scrape
            try:
                logging.warning("-> Attempting Method 2: Raw Web Scrape")
                import urllib.request
                import urllib.parse
                if "http" not in q:
                    encoded_query = urllib.parse.quote(q)
                    url = f"https://www.youtube.com/results?search_query={encoded_query}"
                    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                    html = urllib.request.urlopen(req, timeout=5).read().decode('utf-8', errors='ignore')
                    vid_ids = re.findall(r"watch\?v=(\S{11})", html)
                    if vid_ids:
                        vidid = vid_ids[0]
                        opts = {
                            "quiet": True,
                            "skip_download": True,
                            "cookiefile": "cookies.txt",
                        }
                        with yt_dlp.YoutubeDL(opts) as ydl:
                            info = ydl.extract_info(f"https://www.youtube.com/watch?v={vidid}", download=False)
                            if info:
                                return [info]
            except Exception as e:
                logging.error(f"-> Method 2 Failed: {e}")
            return []

        return await loop.run_in_executor(None, do_search, query)

    async def details(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = await self._search(link, limit=1)
        if not results:
            raise Exception("No search results found on YouTube.")
        try:
            result = results[0]
            title = result.get("title") or "Unknown Title"
            dur_sec = result.get("duration")
            duration_min = f"{int(dur_sec//60):02d}:{int(dur_sec%60):02d}" if dur_sec else None
            duration_sec = int(dur_sec) if dur_sec else 0
            vidid = result.get("id") or result.get("url", "").split("v=")[-1][:11]
            return title, duration_min, duration_sec, vidid
        except Exception as e:
            logging.error(f"--- FATAL ERROR IN DETAILS ---: {e}")
            raise Exception(e)

    async def title(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        results = await self._search(link, limit=1)
        return results[0].get("title", "Unknown Title") if results else "Unknown Title"

    async def duration(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        results = await self._search(link, limit=1)
        dur = results[0].get("duration") if results else None
        return f"{int(dur//60):02d}:{int(dur%60):02d}" if dur else "None"

    async def track(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        results = await self._search(link, limit=1)
        if not results:
            raise Exception("No search results found.")
        try:
            res = results[0]
            dur = res.get("duration")
            return {
                "title": res.get("title", "Unknown"),
                "link": f"https://www.youtube.com/watch?v={res.get('id')}",
                "vidid": res.get("id"),
                "duration_min": f"{int(dur//60):02d}:{int(dur%60):02d}" if dur else None
            }, res.get("id")
        except Exception as e:
            logging.error(f"--- FATAL ERROR IN TRACK ---: {e}")
            raise Exception(e)

    async def playlist(self, link, limit, user_id, videoid: Union[bool, str] = None):
        limit = min(limit, 20)
        playlist = await shell_cmd(f"yt-dlp -i --get-id --flat-playlist --playlist-end {limit} --skip-download {link}")
        return [x for x in playlist.split("\n") if x]

    async def slider(self, link: str, query_type: int, videoid: Union[bool, str] = None):
        results = await self._search(link, limit=10)
        if not results:
            raise Exception("No search results found.")
        res = results[query_type if query_type < len(results) else 0]
        dur = res.get("duration")
        return res.get("title", "Unknown"), f"{int(dur//60):02d}:{int(dur%60):02d}" if dur else None, res.get("id")

    async def download(self, link: str, mystic, videoid: Union[bool, str] = None, songaudio: Union[bool, str] = None, title: Union[bool, str] = None) -> str:
        if videoid:
            link = self.base + link
        loop = asyncio.get_running_loop()

        def audio_dl():
            ydl_opts = {
                "format": "bestaudio[ext=opus]/bestaudio[ext=m4a]/bestaudio/best",
                "outtmpl": "downloads/%(id)s.%(ext)s",
                "quiet": True,
                "cookiefile": "cookies.txt",
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
                "cookiefile": "cookies.txt",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "320"
                }]
            }
            yt_dlp.YoutubeDL(ydl_opts).download([link])
            return fpath

        if songaudio:
            path = await loop.run_in_executor(None, song_audio_dl)
            return path
        return await loop.run_in_executor(None, audio_dl), True