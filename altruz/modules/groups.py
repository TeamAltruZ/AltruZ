import os
import asyncio

from pyrogram.types import Message

from . import altruz_devs
from altruz import ALTRUZ, CMD_HELP
from altruz.core.main_cmd import altruz_on_cmd, e_or_r
from altruz.helpers.pyrogram_help import get_arg
from config import Config


# Help
CMD_HELP.update(
    {
        "groups": f"""
**Group Tools,**
  ✘ `purge` - To purge messages in a chat
  ✘ `ban` - To ban or kick a member in a chat
  ✘ `unban` - To unban a member in a chat
  ✘ `pin` - To pin a message in a chat
  ✘ `unpin` - To unpin a message or messages in a chat
**Example:**
  ✘ `purge`,
   ⤷ reply to a message = `{Config.CMD_PREFIX}purge`
  
  ✘ `ban`,
   ⤷ reply to a message (ban) = `{Config.CMD_PREFIX}ban`
   ⤷ send with user id (ban) = `{Config.CMD_PREFIX}ban 1234567`
   ⤷ reply to a message (kick) = `{Config.CMD_PREFIX}ban -k`
   ⤷ send with user id (kick) = `{Config.CMD_PREFIX}ban -k 1234567`
  
  ✘ `unban`,
   ⤷ reply to a message = `{Config.CMD_PREFIX}unban`
   ⤷ send with user id = `{Config.CMD_PREFIX}unban 1234567`
  
  ✘ `pin`,
   ⤷ reply to a message = `{Config.CMD_PREFIX}pin`
   ⤷ pin with no notification = `{Config.CMD_PREFIX}pin -dn`
  
  ✘ `unpin`,
   ⤷ reply to a message = `{Config.CMD_PREFIX}unpin`
   ⤷ unpin all messages = `{Config.CMD_PREFIX}unpin -all`
"""
    }
)

mod_file = os.path.basename(__file__)

# Purges
@altruz_on_cmd(command="purge", modlue=mod_file, admins_only=True)
async def purge_this(_, message: Message):
  p_msg = await e_or_r(altruz_message=message, msg_text="`Processing...`")
  if not message.reply_to_message:
    return await p_msg.edit("`Reply to a message to starting purge from!`")
  await p_msg.delete()
  mid_list = []
  for mid in range(message.reply_to_message.message_id, message.message_id):
    mid_list.append(mid)
    # If there are more than 100 messages ub'll start deleting
    if len(mid_list) == 100:
      await ALTRUZ.delete_messages(chat_id=message.chat.id, message_ids=mid_list, revoke=True) # Docs says revoke Defaults to True but...
      mid_list = []
    # Let's check if there are any other messages left to delete. Just like that 0.1% bacteria that can't be destroyed by soap
    if len(mid_list) > 0:
      await ALTRUZ.delete_messages(chat_id=message.chat.id, message_ids=mid_list, revoke=True)


# Bans / Kicks
@altruz_on_cmd(command="ban", modlue=mod_file, admins_only=True)
async def ban_usr(_, message: Message):
  b_k_msg = await e_or_r(altruz_message=message, msg_text="`Processing...`")
  r_msg = message.reply_to_message
  just_kick = False
  is_me = await ALTRUZ.get_me()
  args = get_arg(message)

  if args:
    ops_n_arg = args.split(None, 1)
    if ops_n_arg[1] == "-k":
      just_kick = True
    # let's just assume that it'suser id that want to ban
    else:
      b_usr_id = ops_n_arg[1]
  
  if r_msg:
    b_usr_id = r_msg.from_user.id
    if args:
      ops = args.split(None, 1)
      if ops[1] == "-k":
        just_kick = True

  if b_usr_id in altruz_devs:
    return await b_k_msg.edit("`Lmao! Tryna ban my devs? Using me?`")
  elif b_usr_id == is_me.id:
    return await b_k_msg.edit("`Why should I ban my self?`")
  # If command calls with -k flag ub'll just ban user and unban after 5 secs
  if just_kick:
    await message.chat.kick_member(user_id=int(b_usr_id))
    await b_k_msg.edit(f"**Kicked ✊** \n\n**User ID:** `{b_usr_id}` \n\n`⚠️ Unbanning after 5 secs! ⚠️`")
    asyncio.sleep(5)
    await message.chat.unban_member(user_id=int(b_usr_id))
  else:
    await message.chat.kick_member(user_id=int(b_usr_id))
    await b_k_msg.edit(f"**Banned 👊** \n\n**User ID:** `{b_usr_id}`")


# Unbans
@altruz_on_cmd(command="unban", modlue=mod_file, admins_only=True)
async def unban_usr(_, message: Message):
  u_msg = await e_or_r(altruz_message=message, msg_text="`Processing...`")
  r_msg = message.reply_to_message
  u_arg = get_arg(message)
  if r_msg:
    u_usr_id = r_msg.from_user.id
  elif u_arg:
    u_usr_id = u_arg
  else:
    return await u_msg.edit("`Give a user id to unban!`")
  await message.chat.unban_member(user_id=int(u_usr_id))
  await u_msg.edit(f"**Ubanned** \n\n**User ID:** `{u_usr_id}`")


# Pin message
@altruz_on_cmd(command="pin", modlue=mod_file, admins_only=True, only_groups=True)
async def pin_msg(_, message: Message):
  pin_msg = await e_or_r(altruz_message=message, msg_text="`Processing...`")
  r_msg = message.reply_to_message
  args = get_arg(message)
  if not r_msg:
    return await pin_msg.edit("`Reply to a message to pin it!`")
  if args and (args == "-dn"):
    await r_msg.pin(disable_notification=True)
  else:
    await r_msg.pin()
  await pin_msg.edit(f"[Message]({r_msg.link}) `Pinned successfully!`", disable_web_page_preview=True)


# Unpin message
@altruz_on_cmd(command="unpin", modlue=mod_file, admins_only=True, only_groups=True)
async def unpin_msg(_, message: Message):
  unpin_msg = await e_or_r(altruz_message=message, msg_text="`Processing...`")
  r_msg = message.reply_to_message
  args = get_arg(message)
  if args and (args == "-all"):
    chat_id = message.chat.id
    await NEXAUB.unpin_all_chat_messages(chat_id)
    await unpin_msg.edit("`Successfully unpinned all pinned messages in this chat!`")
  else:
    if not r_msg:
      return await unpin_msg.edit("`Reply to a pinned message to unpin it!`")
    await r_msg.unpin()
    await unpin_msg.edit(f"[Message]({r_msg.link}) `Unpinned successfully!`")
