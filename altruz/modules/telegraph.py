import os

from telegraph import Telegraph
from pyrogram.types import Message

from altruz import ALTRUZ, CMD_HELP
from altruz.core.main_cmd import altruz_on_cmd, e_or_r, altruz_on_cf
from altruz.helpers.pyrogram_help import get_arg, convert_to_image
from config import Config


# Help
CMD_HELP.update(
    {
        "telegraph": f"""
**Telegraph,**
  ✘ `telegraph` - To Paste Images/Text to Telegra.ph
**Example:**
  ✘ `telegraph`,
   ⤷ Reply to a message that contains text/image/mp4 file  = `{Config.CMD_PREFIX}telegraph`
     Tip: While pasting text to telegra.ph you can send title with command
"""
    }
)

mod_file = os.path.basename(__file__)


# Telegraph client
telegraph = Telegraph()
telegraph.create_account(short_name="AltruZ")

# Paste text to telegraph
async def paste_text_to_tgraph(title, text):
  try:
    altruz_usr = await ALTRUZ.get_me()
    f_name = altruz_usr.first_name
    u_name = altruz_usr.username
    if title is None:
      title = f_name if f_name is not None else "By AltruZ"
    t_response = telegraph.create_page(title=title, html_content=text, author_name=f_name if f_name is not None else "AltruZ", author_url=f"https://t.me/{u_name}" if u_name is not None else "https://github.com/TeamAltruZ/AltruZ")
    return f"{t_response['url']}"
  except Exception as e:
    return f"**Error:** {e}"

# Upload media to telegraph
async def upload_to_tgraph(file):
  try:
    t_response = telegraph.upload_file(file)[0]["src"]
    return f"https://telegra.ph/{t_response}"
  except Exception as e:
    return f"**Error:** {e}"


@altruz_on_cmd(command="telegraph", modlue=mod_file)
async def telegraph_up(_, message: Message):
    tgraph_msg = await e_or_r(altruz_message=message, msg_text="`Processing...`")
    r_msg = message.reply_to_message
    arg_txt = get_arg(message)
    if r_msg:
      # Photo / Video or Video note
      if r_msg.photo or r_msg.video or r_msg.video_note:
        r_content = await r_msg.download()
      # Stickers
      elif r_msg.sticker:
        r_content = await convert_to_image(message=r_msg, client=ALTRUZ)
      # Text messages
      elif r_msg.text:
        r_content = r_msg.text
        # Set title if provided by user
        if arg_txt:
          t_title = arg_txt
        else:
          t_title = None
        # Paste text to telegraph
        t_pasted = await paste_text_to_tgraph(title=t_title, text=r_content)
      else:
        tgraph_msg.edit("`No Supported Media or Text to paste!`")
      # Paste media to telegraph
      t_pasted = await upload_to_tgraph(r_content)
      # Edit message with the telegraph link
      await tgraph_msg.edit(f"**Telegraph Link:** {t_pasted}")
    else:
      return await tgraph_msg.edit("Reply to a message that contains `text`/`image` or `mp4 file`!")
