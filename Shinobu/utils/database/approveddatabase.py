from Shinobu.core.mongo import mongodb

approved_db = mongodb.approved_chats


async def is_approved_chat(chat_id: int) -> bool:
    chat = await approved_db.find_one({"chat_id": chat_id})
    return bool(chat)


async def approve_chat(chat_id: int):
    if not await is_approved_chat(chat_id):
        await approved_db.insert_one({"chat_id": chat_id})


async def unapprove_chat(chat_id: int):
    await approved_db.delete_one({"chat_id": chat_id})


async def get_approved_chats() -> list:
    chats = approved_db.find({})
    return [doc["chat_id"] async for doc in chats]