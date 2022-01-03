import asyncio
import sys
import os
import requests
import heroku3

from os import environ, execle, path, remove
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

from altruz import ALTRUZ, CMD_HELP
from config import Config
from altruz.helpers.pyrogram_help import get_arg
from altruz.core.main_cmd import altruz_on_cmd, e_or_r


# Help
CMD_HELP.update(
    {
        "updater": """
**Updater**
   `update` - To Updater Your Userbot
   `restart` - To Restart Your Userbot (Heroku Only)
   `logs` - To Get Logs of Your Userbot (Heroku Only)
"""
    }
)

mod_file = os.path.basename(__file__)

UPSTREAM_REPO_URL = "https://github.com/TeamAltruZ/AltruZ"
requirements_path = path.join(
    path.dirname(path.dirname(path.dirname(__file__))), "requirements.txt"
)


async def gen_chlog(repo, diff):
    ch_log = ""
    d_form = "On %d/%m/%y at %H:%M:%S"
    for c in repo.iter_commits(f"HEAD..upstream/{diff}", max_count=10):
        ch_log += f"**#{c.count()}** : {c.committed_datetime.strftime(d_form)} : [{c.summary}]({UPSTREAM_REPO_URL.rstrip('/')}/commit/{c}) by `{c.author}`\n"
    return ch_log


async def updateme_requirements():
    reqs = str(requirements_path)
    try:
        process = await asyncio.create_subprocess_shell(
            " ".join([sys.executable, "-m", "pip", "install", "-r", reqs]),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.communicate()
        return process.returncode
    except Exception as e:
        return repr(e)


@altruz_on_cmd(command="update", modlue=mod_file)
async def upstream(client, message):
    status = await e_or_r(altruz_message=message, msg_text=f"`Checking For Updates from` [AltruZ]({UPSTREAM_REPO_URL})")
    conf = get_arg(message)
    off_repo = UPSTREAM_REPO_URL
    txt = "`Oops! Updater Can't Continue...`"
    txt += "\n\n**LOGTRACE:**\n"
    try:
        repo = Repo(search_parent_directories=True)
    except InvalidGitRepositoryError as error:
        if conf != "now":
            pass
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        repo.create_head("master", origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)
    ac_br = repo.active_branch.name
    if ac_br != "master":
        await status.edit(f"""
`❌ Can't update your AltruZ becuase you're using a custom branch. ❌`
            
**Default Branch:** `master`
**You are on:** `{ac_br}`
`Please change to master branch.`"""
        )
        return repo.__del__()
    try:
        repo.create_remote("upstream", off_repo)
    except BaseException:
        pass
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)
    if "now" not in conf:
        changelog = await gen_chlog(repo, diff=ac_br)
        if changelog:
            req_ver = requests.get("https://raw.githubusercontent.com/TeamAltruZ/AltruZ/main/cache/altruz_data.json")
            changelog_str = f"""
**New Updates are available for AltruZ**
`Branch:` [{ac_br}]({UPSTREAM_REPO_URL}/tree/{ac_br})
**Next Version:** `{req_ver.json()["version"]}`
**Change** \n\n{changelog}"""
            if len(changelog_str) > 4096:
                await status.edit("`Changelog is too big, sending it as a file!`")
                file = open("ALTRUZ_git_commit_log.txt", "w+")
                file.write(changelog_str)
                file.close()
                await ALTRUZ.send_document(
                    message.chat.id,
                    "ALTRUZ_git_commit_log.txt",
                    caption=f"Do `{Config.CMD_PREFIX}update now` to update your AltruZ",
                    reply_to_message_id=status.message_id,
                )
                remove("ALTRUZ_git_commit_log.txt")
            else:
                return await status.edit(
                    f"{changelog_str}\n\nDo `.update now` to update your AltruZ",
                    disable_web_page_preview=True,
                )
        else:
            await status.edit(
                f"**✨ AltruZ is Up-to-date** \n\n**Branch:** [{ac_br}]({UPSTREAM_REPO_URL}/tree/{ac_br})\n",
                disable_web_page_preview=True,
            )
            repo.__del__()
        return
    if Config.HEROKU_API_KEY is not None:
        heroku = heroku3.from_key(Config.HEROKU_API_KEY)
        heroku_app = None
        heroku_applications = heroku.apps()
        if not Config.HEROKU_APP_NAME:
            await status.edit("**Error:** `Please add HEROKU_APP_NAME variable to continue update!`")
            return repo.__del__()
        for app in heroku_applications:
            if app.name == Config.HEROKU_APP_NAME:
                heroku_app = app
                break
        if heroku_app is None:
            await status.edit(f"{txt}\n`Invalid Heroku Vars!`")
            return repo.__del__()
        await status.edit(
            "`Userbot Dyno Build is in Progress!`"
        )
        ups_rem.fetch(ac_br)
        repo.git.reset("--hard", "FETCH_HEAD")
        heroku_git_url = heroku_app.git_url.replace(
            "https://", "https://api:" + Config.HEROKU_API_KEY + "@"
        )
        if "heroku" in repo.remotes:
            remote = repo.remote("heroku")
            remote.set_url(heroku_git_url)
        else:
            remote = repo.create_remote("heroku", heroku_git_url)
        try:
            remote.push(refspec=f"HEAD:refs/heads/{ac_br}", force=True)
        except GitCommandError as error:
            pass
        await status.edit("`Successfully Updated!` \n**Restarting Now...**")
    else:
        try:
            ups_rem.pull(ac_br)
        except GitCommandError:
            repo.git.reset("--hard", "FETCH_HEAD")
        await updateme_requirements()
        await status.edit("`🎉 Successfully Updated!` \n**Restarting Now...**",)
        args = [sys.executable, "-m" "altruz"]
        execle(sys.executable, *args, environ)
        return

# Userbot restart module
async def restart_altruz():
    if Config.HEROKU_API_KEY is not None:
        heroku_conn = heroku3.from_key(Config.HEROKU_API_KEY)
        server = heroku_conn.app(Config.HEROKU_APP_NAME)
        server.restart()
    else:
        args = [sys.executable, "-m" "altruz"]
        execle(sys.executable, *args, environ)
        exit()

@altruz_on_cmd(command="restart", modlue=mod_file)
async def restart(client, message):
    restart_msg = await e_or_r(altruz_message=message, msg_text="`Processing...`")
    await restart_msg.edit("`AltruZ is restarting! Please wait...`")
    try:
        await restart_altruz()
    except Exception as e:
        await restart_msg.edit(f"**Error:** `{e}`")


@altruz_on_cmd(command="logs", modlue=mod_file)
async def log(client, message):
    try:
        await e_or_r(altruz_message=message, msg_text="`Getting Logs`")
        heroku_conn = heroku3.from_key(Config.HEROKU_API_KEY)
        server = heroku_conn.get_app_log(Config.HEROKU_APP_NAME, dyno='worker', lines=100, source='app', timeout=100)
        f_logs = server
        if len(f_logs) > 4096:
            file = open("logs.txt", "w+")
            file.write(f_logs)
            file.close()
            await ALTRUZ.send_document(message.chat.id, "logs.txt", caption=f"Logs of `{Config.HEROKU_APP_NAME}`")
            remove("logs.txt")
    except Exception as e:
        await message.edit(f"**Error:** `{e}`")
