from motor.motor_asyncio import AsyncIOMotorClient
from config import Config

mongodb = AsyncIOMotorClient(Config.MONGODB_URL)
altruz_mongodb = mongodb["ALTRUZ"]
