import asyncio

from pyrogram import idle
from alturz import ALTURZ
from alturz.modules import *
from alturz.core.startup_checks import check_or_set_log_channel, check_arq_api
from alturz.core.alturz_database.alturz_db_conf import get_log_channel
from config import Config


async def main_startup():
    print("""
|| AlturZ Userbot ||
Copyright (c) 2021 TeamAlturZ
"""
    )
    await ALTURZ.start()
    log_channel_id = await check_or_set_log_channel()
    await check_arq_api()
    try:
        await ALTURZ.send_message(chat_id=log_channel_id[1], text="Master, \n`AlturZ is now Online")
    except:
        print("WARNING: There was an error while creating the LOG_CHANNEL please add a one manually!")
    await idle()

loop = asyncio.get_event_loop()
loop.run_until_complete(main_startup())
