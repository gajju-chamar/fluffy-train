# Shinobu Music Bot
# Owner: @Sanji_fr

import re

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from youtubesearchpython.__future__ import VideosSearch

import config


class SpotifyAPI:
    def __init__(self):
        self.regex = r"^(https:\/\/open.spotify.com\/)(.*)$"
        if config.SPOTIFY_CLIENT_ID and config.SPOTIFY_CLIENT_SECRET:
            self.spotify = spotipy.Spotify(
                client_credentials_manager=SpotifyClientCredentials(
                    config.SPOTIFY_CLIENT_ID,
                    config.SPOTIFY_CLIENT_SECRET,
                )
            )
        else:
            self.spotify = None

    async def valid(self, link: str):
        return bool(re.search(self.regex, link))

    async def track(self, link: str):
        track = self.spotify.track(link)
        # Build search query: track name + artists
        info = track["name"]
        for artist in track["artists"]:
            fetched = f' {artist["name"]}'
            if "Various Artists" not in fetched:
                info += fetched
        # Resolve to YouTube
        results = VideosSearch(info, limit=1)
        for result in (await results.next())["result"]:
            ytlink = result["link"]
            title = result["title"]
            vidid = result["id"]
            duration_min = result["duration"]
        track_details = {
            "title": title,
            "link": ytlink,
            "vidid": vidid,
            "duration_min": duration_min,
        }
        return track_details, vidid

    async def playlist(self, url):
        playlist = self.spotify.playlist(url)
        playlist_id = playlist["id"]
        results = []
        # Hard cap at 20 tracks
        for item in playlist["tracks"]["items"][:20]:
            music_track = item["track"]
            if not music_track:
                continue
            info = music_track["name"]
            for artist in music_track["artists"]:
                fetched = f' {artist["name"]}'
                if "Various Artists" not in fetched:
                    info += fetched
            results.append(info)
        return results, playlist_id

    async def album(self, url):
        album = self.spotify.album(url)
        album_id = album["id"]
        results = []
        # Hard cap at 20 tracks
        for item in album["tracks"]["items"][:20]:
            info = item["name"]
            for artist in item["artists"]:
                fetched = f' {artist["name"]}'
                if "Various Artists" not in fetched:
                    info += fetched
            results.append(info)
        return results, album_id

    async def artist(self, url):
        artistinfo = self.spotify.artist(url)
        artist_id = artistinfo["id"]
        results = []
        artisttoptracks = self.spotify.artist_top_tracks(url)
        # Hard cap at 20 tracks
        for item in artisttoptracks["tracks"][:20]:
            info = item["name"]
            for artist in item["artists"]:
                fetched = f' {artist["name"]}'
                if "Various Artists" not in fetched:
                    info += fetched
            results.append(info)
        return results, artist_id