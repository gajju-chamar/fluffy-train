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
        def do_search():
            logging.warning(f"--- STARTING SEARCH FOR: {query} ---")
            
            # FORMAT THE QUERY
            if "http" in query and not re.search(r"(?:youtube\.com|youtu\.be)", query):
                search_query = f"ytsearch{limit}:{query}"
            elif "http" in query:
                search_query = query
            else:
                search_query = f"ytsearch{limit}:{query}"

            # METHOD 1: Standard yt-dlp search
            try:
                logging.warning("-> Attempting Method 1: Standard Search")
                ydl_opts = {"quiet": True, "extract_flat": True, "skip_download": True, "no_warnings": True}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(search_query, download=False)
                    if info and "entries" in info:
                        entries = list(info["entries"])
                        if entries:
                            logging.warning("-> SUCCESS: Found via Method 1")
                            return entries[:limit]
                    elif info and "id" in info:
                        return [info]
            except Exception as e:
                logging.error(f"-> Method 1 Failed: {e}")

            # METHOD 2: Raw Web Scrape (Bypasses API/Captcha walls)
            try:
                logging.warning("-> Attempting Method 2: Raw Web Scrape")
                import urllib.request
                import urllib.parse
                if "http" not in query:
                    encoded_query = urllib.parse.quote(query)
                    url = f"https://www.youtube.com/results?search_query={encoded_query}"
                    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
                    html = urllib.request.urlopen(req, timeout=5).read().decode('utf-8', errors='ignore')
                    vid_ids = re.findall(r"watch\?v=(\S{11})", html)
                    
                    if vid_ids:
                        vidid = vid_ids[0]
                        logging.warning(f"-> SUCCESS: Raw Scrape found ID: {vidid}. Fetching metadata with cookies...")
                        # Use cookies to safely fetch the details of this specific video
                        opts = {"quiet": True, "skip_download": True, "cookiefile": "cookies.txt"}
                        with yt_dlp.YoutubeDL(opts) as ydl:
                            info = ydl.extract_info(f"https://www.youtube.com/watch?v={vidid}", download=False)
                            if info:
                                return [info]
            except Exception as e:
                logging.error(f"-> Method 2 Failed: {e}")

            # METHOD 3: yt-dlp search WITH Cookies
            try:
                logging.warning("-> Attempting Method 3: Cookie Search")
                ydl_opts = {"quiet": True, "extract_flat": True, "skip_download": True, "cookiefile": "cookies.txt"}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(search_query, download=False)
                    if info and "entries" in info:
                        entries = list(info["entries"])
                        if entries:
                            logging.warning("-> SUCCESS: Found via Method 3")
                            return entries[:limit]
                    elif info and "id" in info:
                        return [info]
            except Exception as e:
                logging.error(f"-> Method 3 Failed: {e}")

            logging.error("--- ALL SEARCH METHODS FAILED ---")
            return []
                
        return await loop.run_in_executor(None, do_search)

    async def details(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]

        results = await self._search(link, limit=1)
        if not results:
            raise Exception("No search results found on YouTube.")

        result = results[0]
        title = result.get("title", "Unknown Title")
        dur_sec = result.get("duration", 0)
        
        if dur_sec:
            m, s = divmod(dur_sec, 60)
            duration_min = f"{int(m):02d}:{int(s):02d}"
            duration_sec = int(dur_sec)
        else:
            duration_min = "None"
            duration_sec = 0
            
        vidid = result.get("id")
        return title, duration_min, duration_sec, vidid

    async def title(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = await self._search(link, limit=1)
        if not results:
            return "Unknown Title"
        return results[0].get("title", "Unknown Title")

    async def duration(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = await self._search(link, limit=1)
        if not results:
            return "None"
            
        dur_sec = results[0].get("duration", 0)
        if dur_sec:
            m, s = divmod(dur_sec, 60)
            return f"{int(m):02d}:{int(s):02d}"
        return "None"

    async def track(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]

        results = await self._search(link, limit=1)
        if not results:
            raise Exception("No search results found on YouTube.")

        result = results[0]
        title = result.get("title", "Unknown Title")
        dur_sec = result.get("duration", 0)
        
        if dur_sec:
            m, s = divmod(dur_sec, 60)
            duration_min = f"{int(m):02d}:{int(s):02d}"
        else:
            duration_min = "None"
            
        vidid = result.get("id")
        yturl = f"https://www.youtube.com/watch?v={vidid}"

        track_details = {
            "title": title,
            "link": yturl,
            "vidid": vidid,
            "duration_min": duration_min,
        }
        return track_details, vidid

    async def playlist(self, link, limit, user_id, videoid: Union[bool, str] = None):
        if videoid:
            link = self.listbase + link
        if "&" in link:
            link = link.split("&")[0]
        limit = min(limit, 20)
        playlist = await shell_cmd(
            f"yt-dlp -i --get-id --flat-playlist --playlist-end {limit} --skip-download {link}"
        )
        try:
            result = [x for x in playlist.split("\n") if x]
        except:
            result = []
        return result

    async def slider(
        self,
        link: str,
        query_type: int,
        videoid: Union[bool, str] = None,
    ):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]

        results = await self._search(link, limit=10)
        if not results:
            raise Exception("No search results found on YouTube.")

        if query_type >= len(results):
            query_type = 0

        result = results[query_type]
        title = result.get("title", "Unknown Title")
        dur_sec = result.get("duration", 0)
        
        if dur_sec:
            m, s = divmod(dur_sec, 60)
            duration_min = f"{int(m):02d}:{int(s):02d}"
        else:
            duration_min = "None"
            
        vidid = result.get("id")
        return title, duration_min, vidid

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
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "no_warnings": True,
            }
            ydl_opts["cookiefile"] = "cookies.txt" 
            
            x = yt_dlp.YoutubeDL(ydl_opts)
            info = x.extract_info(link, False)
            xyz = os.path.join("downloads", f"{info['id']}.{info['ext']}")
            if os.path.exists(xyz):
                return xyz
            x.download([link])
            return xyz

        def song_audio_dl():
            fpath = f"downloads/{title}.%(ext)s"
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": fpath,
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "no_warnings": True,
                "prefer_ffmpeg": True,
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "320",
                    }
                ],
            }
            ydl_opts["cookiefile"] = "cookies.txt" 
            
            x = yt_dlp.YoutubeDL(ydl_opts)
            x.download([link])

        if songaudio:
            await loop.run_in_executor(None, song_audio_dl)
            return f"downloads/{title}.mp3"

        downloaded_file = await loop.run_in_executor(None, audio_dl)
        return downloaded_file, True
