# Shinobu Music Bot
# Owner: @Sanji_fr

import asyncio
import os
import re
from typing import Union

import yt_dlp
from pyrogram.types import Message
from youtubesearchpython.__future__ import VideosSearch

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

    async def details(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        search_data = await results.next()
        
        if not search_data or not search_data.get("result"):
            raise Exception("No search results found on YouTube.")
            
        result = search_data["result"][0]
        title = result.get("title", "Unknown Title")
        duration_min = result.get("duration", "None")
        vidid = result.get("id")
        
        if str(duration_min) == "None":
            duration_sec = 0
        else:
            duration_sec = int(time_to_seconds(duration_min))
        return title, duration_min, duration_sec, vidid

    async def title(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        search_data = await results.next()
        if not search_data or not search_data.get("result"):
            return "Unknown Title"
        return search_data["result"][0].get("title", "Unknown Title")

    async def duration(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        search_data = await results.next()
        if not search_data or not search_data.get("result"):
            return "None"
        return search_data["result"][0].get("duration", "None")

    async def track(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        search_data = await results.next()
        
        # SAFETY NET: If search fails, throw an error to be caught by play.py
        if not search_data or not search_data.get("result"):
            raise Exception("No search results found on YouTube.")
            
        result = search_data["result"][0]
        title = result.get("title", "Unknown Title")
        duration_min = result.get("duration", "None")
        vidid = result.get("id")
        yturl = result.get("link")
        
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
        # Hard cap at 20 tracks
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
        a = VideosSearch(link, limit=10)
        search_data = await a.next()
        
        if not search_data or not search_data.get("result"):
            raise Exception("No search results found on YouTube.")
            
        result = search_data["result"]
        # Make sure the query_type index doesn't go out of bounds
        if query_type >= len(result):
            query_type = 0
            
        title = result[query_type].get("title", "Unknown Title")
        duration_min = result[query_type].get("duration", "None")
        vidid = result[query_type].get("id")
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
            # Best native audio — no re-encoding, CPU friendly for free tier hosting
            ydl_opts = {
                "format": "bestaudio[ext=opus]/bestaudio[ext=m4a]/bestaudio/best",
                "outtmpl": "downloads/%(id)s.%(ext)s",
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "no_warnings": True,
            }
            # IF YOU EVER ADD A COOKIES.TXT FILE TO YOUR REPO, UNCOMMENT THE LINE BELOW
            # ydl_opts["cookiefile"] = "cookies.txt"
            
            x = yt_dlp.YoutubeDL(ydl_opts)
            info = x.extract_info(link, False)
            xyz = os.path.join("downloads", f"{info['id']}.{info['ext']}")
            if os.path.exists(xyz):
                return xyz
            x.download([link])
            return xyz

        def song_audio_dl():
            # Download as named mp3 for /song command
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
            # IF YOU EVER ADD A COOKIES.TXT FILE TO YOUR REPO, UNCOMMENT THE LINE BELOW
            # ydl_opts["cookiefile"] = "cookies.txt"
            
            x = yt_dlp.YoutubeDL(ydl_opts)
            x.download([link])

        if songaudio:
            await loop.run_in_executor(None, song_audio_dl)
            return f"downloads/{title}.mp3"

        # Standard stream download
        downloaded_file = await loop.run_in_executor(None, audio_dl)
        return downloaded_file, True
