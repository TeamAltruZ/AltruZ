import os
from pyrogram.types import Message

from altruz import ALTRUZ, HELP, CMD_HELP
from config import Config
from altruz.helpers.pyrogram_help import get_arg
from altruz.core.main_cmd import altruz_on_cmd, e_or_r


# Help
HELP.update(
    {
        "**⚡ Userbot**": "`alive`, `installer`, `updater`, `repo`",
        "**🔥 Animations": "`greetings`",
        "**👨‍💻 Dev**": "`eval`",
        "**🗂 Modules**": "`paste`, `short_url`, `search`, `pictools`, `arq`, `telegraph`, `cloud`",
        "**📂 Database**": "`stickers`, `owner`, `sudos`, `afk`, `globals`, `groups`",
        "\n**Usage**": "`.help` [module_name]"
    }
)

mod_file = os.path.basename(__file__)

@altruz_on_cmd(command="help", modlue=mod_file)
async def help(_, message: Message):
    args = get_arg(message)
    help_user_msg = await e_or_r(altruz_message=message, msg_text="`Processing...`")
    if not args:
        text = "**Available Commands**\n\n"
        for key, value in HELP.items():
            text += f"{key}: {value}\n\n"
        await help_user_msg.edit(text)
        return
    else:
        module_help = CMD_HELP.get(args, False)
        if not module_help:
            await help_user_msg.edit("`Invalid Module Name!`")
            return
        else:
            await help_user_msg.edit(module_help)
