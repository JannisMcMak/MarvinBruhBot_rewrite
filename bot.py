from discord.ext import commands
import discord
import os
import shutil
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.members = True

load_dotenv()
TOKEN = os.environ['BOT_TOKEN']

bot = commands.Bot(command_prefix='<', case_insensitive=True, intents=intents)


@bot.event
async def on_ready():
    print("Loading...")
    print(f'{bot.user} has connected to Discord!')

    n = []
    for g in bot.guilds:
        n.append(g.name)

    print("Servers: " + ",".join(n))


@bot.event
async def on_message(message):
    zrocken_channels = [714452232791261246,
                        396671581558013952, 836988148814184509]

    if message.channel.id in zrocken_channels:
        roles = message.channel.guild.roles
        for role in roles:
            if role.mention in message.content:
                print(role)
                await bot.change_presence(activity=discord.Game(name=role.name))

    await bot.process_commands(message)


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

bot.run(TOKEN)
