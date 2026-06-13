# Shinobu Music Bot
# Owner: @Sanji_fr

from .logging import LOGGER
from .core.bot import ShinobuBot
from .core.userbot import Userbot

# 1. Initialize the bots FIRST so they actually exist
app = ShinobuBot()
userbot = Userbot()

# 2. NOW we can import the platforms, because the bot is ready
from .platforms import SpotifyAPI, YouTubeAPI

# 3. Initialize the platforms
YouTube = YouTubeAPI()
Spotify = SpotifyAPI()
