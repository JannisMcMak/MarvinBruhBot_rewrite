from discord.ext import commands
import discord
import os
import shutil
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.members = True

load_dotenv()
TOKEN = os.environ['BOT_TOKEN']

bot = commands.Bot(command_prefix='#', case_insensitive=True, intents=intents)



def clear_cache():
  print('Clearing cache...')
  folder = 'cache'
  for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
      if os.path.isfile(file_path) or os.path.islink(file_path):
        os.unlink(file_path)
      elif os.path.isdir(file_path):
        shutil.rmtree(file_path)
    except Exception as e:
      print('Error clearing cache: {}'.format(e))

clear_cache()


bot.load_extension("cogs.admin")
bot.load_extension("cogs.bitch")
bot.load_extension("cogs.mp3")
bot.load_extension("cogs.other")
bot.load_extension("cogs.stats")
bot.load_extension("cogs.tts")
bot.load_extension("cogs.events")

bot.run(TOKEN)
