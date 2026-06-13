# Shinobu Music Bot
# Owner: @Sanji_fr

import sys

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient

import config
from ..logging import LOGGER


if not config.MONGO_DB_URI:
    LOGGER(__name__).error(
        "MONGO_DB_URI is not set. Please provide a MongoDB connection string."
    )
    sys.exit()

_mongo_async_ = AsyncIOMotorClient(config.MONGO_DB_URI)
_mongo_sync_ = MongoClient(config.MONGO_DB_URI)

mongodb = _mongo_async_.Shinobu
pymongodb = _mongo_sync_.Shinobu