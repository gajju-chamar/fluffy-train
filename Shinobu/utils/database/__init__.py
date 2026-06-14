# Shinobu Music Bot
# Owner: @Sanji_fr

from .approveddatabase import *
from .assistantdatabase import *
from .memorydatabase import *
from .mongodatabase import *

# Cheat Code Bypass for missing private chat functions
async def is_served_private_chat(chat_id: int) -> bool:
    return True

async def add_private_chat(chat_id: int):
    pass

async def remove_private_chat(chat_id: int):
    pass

async def get_private_served_chats() -> list:
    return []
