import os
import re
import urllib
import urllib.parse
import requests

from pyrogram import filters
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from altruz import ALTRUZ, CMD_HELP
from altruz.helpers.pyrogram_help import get_arg
from altruz.core.main_cmd import altruz_on_cmd, e_or_r
from config import Config


# Help
CMD_HELP.update(
    {
        "search": f"""
**Search**
  ➥ `duck_s` - To Get Search Link In DuckDuckGo
  ➥ `google` - To Search In Google
**Example:**
  ➥ `duck_s`,
   ⤷ Send command with query = `{Config.CMD_PREFIX}duck_s AltruZ`
  ➥ `google`,
   ⤷ Send command with query = `{Config.CMD_PREFIX}google AltruZ`
   ⤷ Reply to a text message = `{Config.CMD_PREFIX}google` (Reply to a text message)
"""
    }
)

mod_file = os.path.basename(__file__)

@altruz_on_cmd(command="duck_s", modlue=mod_file)
async def duckduckg_s(client, message):
    pablo = await e_or_r(altruz_message=message, msg_text="`Searcing in DuckDuckGo...`")
    query = get_arg(message)
    if not query:
        await pablo.edit("`Give Something to Search!`")
        return
    sample_url = "https://duckduckgo.com/?q={}".format(query.replace(" ", "+"))
    link = sample_url.rstrip()
    await pablo.edit(f"**Query:** \n`{query}` \n\n**Result(s):** \n{link}")


@altruz_on_cmd(command="google", modlue=mod_file)
async def google_s(client, message):
    pablo = await e_or_r(altruz_message=message, msg_text="`Searching in Google...`")
    query = get_arg(message)
    replied_msg = message.reply_to_message
    if not query:
        try:
            if replied_msg:
                query = replied_msg.text
        except:
            await pablo.edit("`Give Something to Search!`")
            return
    query = urllib.parse.quote_plus(query)
    number_result = 8
    ua = UserAgent()
    google_url = (
        "https://www.google.com/search?q=" + query + "&num=" + str(number_result)
    )
    response = requests.get(google_url, {"User-Agent": ua.random})
    soup = BeautifulSoup(response.text, "html.parser")
    result_div = soup.find_all("div", attrs={"class": "ZINbbc"})
    links = []
    titles = []
    descriptions = []
    for r in result_div:
        try:
            link = r.find("a", href=True)
            title = r.find("div", attrs={"class": "vvjwJb"}).get_text()
            description = r.find("div", attrs={"class": "s3v9rd"}).get_text()
            if link != "" and title != "" and description != "":
                links.append(link["href"])
                titles.append(title)
                descriptions.append(description)

        except:
            continue
    to_remove = []
    clean_links = []
    for i, l in enumerate(links):
        clean = re.search("\/url\?q\=(.*)\&sa", l)
        if clean is None:
            to_remove.append(i)
            continue
        clean_links.append(clean.group(1))
    for x in to_remove:
        del titles[x]
        del descriptions[x]
    msg = ""

    for tt, liek, d in zip(titles, clean_links, descriptions):
        msg += f"[{tt}]({liek})\n`{d}`\n\n"
    await pablo.edit(f"**Query:** \n`{query}` \n\n**Result(s):** \n{msg}")
