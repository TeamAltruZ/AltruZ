from time import time
from pyrogram import Client
from config import Config

# Configs
HELP = {}
CMD_HELP = {}
StartTime = time()

ALTURZ = Client(
    api_hash=Config.API_HASH,
    api_id=Config.APP_ID,
    session_name=Config.PYRO_STR_SESSION
)
