import time
import os
import json

from datetime import datetime
from pyrogram import __version__ as pyrogram_version
from pyrogram.types import Message
from sys import version_info

from altruz import ALTRUZ, CMD_HELP, StartTime
from altruz.helpers.pyrogram_help import get_arg
from altruz.core.altruz_database.altruz_db_conf import set_custom_alive_msg, get_custom_alive_msg, set_custom_var, get_custom_var
from altruz.core.main_cmd import altruz_on_cmd, e_or_r
from altruz.core.startup_checks import check_or_set_log_channel
from .telegraph import upload_to_tgraph
from config import Config


# Help Message!
CMD_HELP.update(
    {
        "alive": f"""
**Alive,**
  ➥ `alive` - To Check If Your AltruZ is Alive
  ➥ `ping` - To Check Ping Speed
  ➥ `setalive` - To Set Custom Alive Message
  ➥ `getalive` - To Get current alive message
**Example:**
  ➥ `setalive`,
   ⤷ Send with alive text = `{Config.CMD_PREFIX}setalive This is the alive text`
   ⤷ Reply to a text message with `{Config.CMD_PREFIX}setalive`
"""
    }
)

mod_file = os.path.basename(__file__)

# Get python version
python_version = f"{version_info[0]}.{version_info[1]}.{version_info[2]}"
# Conver time in to readable format
def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "
    time_list.reverse()
    ping_time += ":".join(time_list)
    return ping_time

# Get current version of Altruz
def get_altruz_version():
    with open("cache/altruz_data.json", "r") as jsn_f:
        ver = json.load(jsn_f)
        return ver["version"]


# Alive Message
@altruz_on_cmd(command="alive", modlue=mod_file)
async def pyroalive(_, message: Message):
    uptime = get_readable_time((time.time() - StartTime))
    alive_bef_msg = await e_or_r(altruz_message=message, msg_text="`Processing..`")
    # Alive Message
    get_alive_msg = await get_custom_alive_msg()
    custom_alive_msg = get_alive_msg if get_alive_msg else "Heya, I'm Using Nexa Userbot"
    # Alive Pic
    get_alive_pic = await get_custom_var(var="ALIVE_PIC")
    alive_pic = get_alive_pic if get_alive_pic else "cache/AltruZ.jpg"
    ALTRUZ_VERSION = get_altruz_version()
    alive_msg = f"""
      》 **{custom_alive_msg}**
      • Usᴇʀʙᴏᴛ Is: OɴʟIɴᴇ
         =====Sʏsᴛᴇᴍ Iɴғᴏʀᴍᴀᴛiᴏɴ=====  
    **• AltruZ Vᴇʀsiᴏɴ:** `{ALTRUZ_VERSION}`
    **• Pʏᴛʜᴏɴ:** `{python_version}`
    **• Pʏʀᴏɢʀᴀᴍ:** `{pyrogram_version}`
    **• Uᴘᴛiᴍᴇ:** `{uptime}`
    **• Sᴜᴘᴘᴏʀᴛ:** @TheAltruZ 
    **• Dᴀᴛᴀʙᴀsᴇ:** `Mongo Atlas`
    **• Dᴀᴛᴀʙᴀsᴇ Sᴛᴀᴛᴜs:** `Fᴜɴᴄᴛɪᴏɴᴀʟ`
    **• Cᴜʀʀᴇɴᴛ Bʀᴀɴᴄʜ:** `Mᴀsᴛᴇʀ`
    **• Hᴇʀᴏᴋᴜ Dᴀᴛᴀʙᴀsᴇ:** `AWS`
         ============================
"""
    await alive_bef_msg.delete()
    await ALTRUZ.send_photo(chat_id=message.chat.id, photo=alive_pic, caption=alive_msg)

# Ping
@altruz_on_cmd(command=["ping"], modlue=mod_file)
async def pingme(_, message: Message):
    ping_msg = await e_or_r(altruz_message=message, msg_text="`Processing..`")
    start = datetime.now()
    end = datetime.now()
    ping_time = (end - start).microseconds / 1000
    await ping_msg.edit(f"**Pong⚡**\nSpeed 》 `{ping_time} ms` \n\n ~ **Im Fastest my Master!**", disable_web_page_preview=True)

# Set custom alive message
@altruz_on_cmd(command="setalive", modlue=mod_file)
async def set_alive(_, message: Message):
    alive_r_msg = await e_or_r(altruz_message=message, msg_text="`Processing...`")
    c_alive_msg = get_arg(message)
    r_msg = message.reply_to_message
    if not c_alive_msg:
        if r_msg:
            c_alive_msg = r_msg.text
        else:
            return await alive_r_msg.edit("`Please reply to a text message!`")
    await set_custom_alive_msg(a_text=c_alive_msg)
    await alive_r_msg.edit("`Successfully Updated Custom Alive Message!`")

# Get custom alive message
@altruz_on_cmd(command="getalive", modlue=mod_file)
async def get_alive(_, message: Message):
    g_alive_msg = await e_or_r(altruz_message=message, msg_text="`Processing...`")
    try:
        get_al = await get_custom_alive_msg()
        saved_alive_msg = get_al if get_al else "No Custom Message is saved!"
        await g_alive_msg.edit(f"**Current Alive Message:** \n{saved_alive_msg}")
    except Exception as e:
        print(e)

# Set custom alive picture
@altruz_on_cmd(command="setalivepic", modlue=mod_file)
async def set_alive_pic(_, message: Message):
    cust_alive = await e_or_r(altruz_message=message, msg_text="`Processing...`")
    r_msg = message.reply_to_message
    if r_msg.photo or r_msg.animation:
        alive_pic = await r_msg.download()
        alive_url = await upload_to_tgraph(alive_pic)
        await set_custom_var(var="ALIVE_PIC", value=alive_url)
        await cust_alive.edit(f"`Successfully Saved Custom Alive Picture!` \n\n**Preview:** [Click here]({alive_url})")
    else:
        await cust_alive.edit("`Reply to a photo or gif 😑!`")


@altruz_on_cmd(command="clc", modlue=mod_file)
async def egg_clc(_, message: Message):
    clc_func = await check_or_set_log_channel()
    lc_id = clc_func[1] if clc_func[1]  else None
    await e_or_r(altruz_message=message, msg_text=f"**Is Log Channel Set?** `{clc_func[0]}` \n**Channel ID:** `{lc_id}`")
