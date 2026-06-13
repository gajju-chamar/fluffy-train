# Shinobu Music Bot
# Owner: @Sanji_fr
 
from .logging import LOGGER
from .core.bot import ShinobuBot
from .core.userbot import Userbot
from .platforms import SpotifyAPI, YouTubeAPI
 
# Bot client instance
app = ShinobuBot()
 
# Assistant userbot instances
userbot = Userbot()
 
# Platform API instances
YouTube = YouTubeAPI()
Spotify = SpotifyAPI()
 