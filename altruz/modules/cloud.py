import os

from pyrogram.types import Message
from time import time
from gofile2 import Async_Gofile

from altruz import ALTRUZ, CMD_HELP
from altruz.core.main_cmd import altruz_on_cmd, e_or_r
from altruz.helpers.pyrogram_help import get_arg, progress_for_pyrogram
from config import Config


# Help
CMD_HELP.update(
    {
        "cloud": f"""
**Cloud Storages,**
   `gofile` - To upload telegram media to gofile.io
**Example:**
   `gofile`,
   ⤷ Reply to telegram media = `{Config.CMD_PREFIX}gofile` (Reply to a valid telegram media file)
      Tip: You can also send a description alongside with command!
"""
    }
)

mod_file = os.path.basename(__file__)


@altruz_on_cmd(command="gofile", modlue=mod_file)
async def gofiles_up(_, message: Message):
    gofile_msg = await e_or_r(altruz_message=message, msg_text="`Processing...`")
    r_go_f = message.reply_to_message
    go_f_arg = get_arg(message)
    if not r_go_f:
        return await gofile_msg.edit("`Reply to a telegram media to upload it to Gofile.io!`")
    await gofile_msg.edit("`Download has started! This may take a while!`")
    start_time = time()
    dl_go_f = await r_go_f.download(progress=progress_for_pyrogram, progress_args=("**💫 Downloading... 💫** \n", gofile_msg, start_time))
    desc = go_f_arg if go_f_arg else None
    # Gofile2 client
    go_client = Async_Gofile()
    await gofile_msg.edit("`Upload has started! This may take a while!`")
    upl_go_f = await go_client.upload(file=dl_go_f, description=desc)
    await gofile_msg.edit(f"**Successfully Uploaded!** \n\n**File Name:** `{upl_go_f['fileName']}` \n**Link:** {upl_go_f['downloadPage']}", disable_web_page_preview=True)
