from nextcord.ext import commands
import nextcord

import os
import shutil
import sys
import config
from threading import Thread

from util.logger import Logger
from web.web import run_apiserver

log = Logger('Main')

intents = nextcord.Intents.default()
intents.members = True

if len(sys.argv) > 1 and sys.argv[1] == "test":
    PREFIX = "."

    TOKEN = config.TEST_BOT_TOKEN2 if len(sys.argv) > 2 and sys.argv[2] == "2" else config.TEST_BOT_TOKEN

else:
    PREFIX = config.BOT_PREFIX
    TOKEN = config.BOT_TOKEN

bot = commands.Bot(
    command_prefix=PREFIX, case_insensitive=True, intents=intents)

#bot.remove_command('help')


def clear_cache():
    """Clears the tempory file directory"""

    log.debug('Clearing cache...')
    folder = 'cache'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            log.error('Error clearing cache: {}'.format(e))


clear_cache()


bot.load_extension("cogs.tts")
bot.load_extension("cogs.audio")
bot.load_extension("cogs.bitch")
bot.load_extension("cogs.minigames")
bot.load_extension("cogs.stats")
bot.load_extension("cogs.other")
bot.load_extension("cogs.tasks")
bot.load_extension("cogs.admin")

if not len(sys.argv) > 1:
    bot.load_extension("cogs.events")
#bot.load_extension("cogs.help")

if config.API_SERVER_RUN_BY_DEFAULT:
    try:
        Thread(target=run_apiserver).start()
    except (KeyboardInterrupt, SystemExit, SystemError):
        log.debug("API-Webserver stopped.")

    log.debug("API-Webserver started!")

bot.run(TOKEN)