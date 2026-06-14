# Shinobu Music Bot
# Owner: @Sanji_fr

from .approveddatabase import *
from .assistantdatabase import *
from .memorydatabase import *
from .mongodatabase import *

# Cheat Code Bypass for missing private chat function
async def is_served_private_chat(chat_id: int) -> bool:
    return True
