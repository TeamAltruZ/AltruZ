import asyncio
from pyrogram.errors import YouBlockedUser
from altruz import ALTRUZ
from altruz.core.altruz_database.altruz_db_conf import set_log_channel, get_log_channel, set_arq_key, get_arq_key
from config import Config

# Log Channel Checker
async def check_or_set_log_channel():
    try:
        al_log_channel = await get_log_channel()
        if al_log_channel:
            return [True, al_log_channel]
        else:
            log_channel = await ALTRUZ.create_channel(title="AltruZ Logz", description="Logs of your AltruZ UserBot")
            welcome_to_altruz = f"""
**AltruZ Started!**
Congratulations,
AltruZ had been deployed Successfully!
======== Support ========
Channel ➥ [Join](https://t.me/TheAltruZ)
Group ➥ [Join](https://t.me/AltruZChat)
=========================
<||Important Note||>
➥ Master Please Don't Delete/Leave this Channel or I will now work!
➥ Join Support Group/Channel for my proper Functions!
➥ If you got banned from Group just stay in the channel!
"""
            log_channel_id = log_channel.id
            await set_log_channel(log_channel_id)
            await ALTRUZ.send_message(chat_id=log_channel_id, text=welcome_to_altruz, disable_web_page_preview=True)
            return [True, log_channel_id]
    except Exception as e:
        print(f"Error \n\n{e} \n\nPlease check all variables and try again! \nReport this with logs at @AltruZChat if the problem Exists!")
        exit()


# ARQ API KEY Checker
async def check_arq_api():
    try:
        try:
            await ALTRUZ.send_message("ARQRobot", "/start")
        except YouBlockedUser:
            await ALTRUZ.unblock_user("ARQRobot")
            await asyncio.sleep(0.2)
            await ALTRUZ.send_message("ARQRobot", "/start")
        await asyncio.sleep(0.5)
        await ALTRUZ.send_message("ARQRobot", "/get_key")
        get_h = (await ALTRUZ.get_history("ARQRobot", 1))[0]
        g_history = get_h.text
        if "X-API-KEY:" not in g_history:
            altruz_user = await ALTRUZ.get_me()
            arq_acc_name = altruz_user.first_name if altruz_user.first_name else f"Unknown_{altruz_user.id}"
            await asyncio.sleep(0.4)
            await ALTRUZ.send_message("ARQRobot", f"{arq_acc_name}")
            await asyncio.sleep(0.3)
            gib_history = (await ALTRUZ.get_history("ARQRobot", 1))[0]
            g_history = gib_history.text
            arq_api_key = g_history.replace("X-API-KEY: ", "")
        else:
            arq_api_key = g_history.replace("X-API-KEY: ", "")
        is_arqed = await get_arq_key()
        if is_arqed is None:
            await set_arq_key(arq_api_key)
        else:
            pass
    except Exception as e:
        print(f"Error \n\n{e} \n\nThere was a problem while obtaining ARQ API KEY. However you can set it manually. Send, \n`{Config.CMD_PREFIX}setvar ARQ_API_KEY your_api_key_here`")
