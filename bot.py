from discord.ext import commands
import discord
import os
from dotenv import load_dotenv


os.system('chmod +777 ./ffmpeg')


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


bot.load_extension("cogs.admin")
bot.load_extension("cogs.bitch")
bot.load_extension("cogs.mp3")
bot.load_extension("cogs.other")
bot.load_extension("cogs.stats")
bot.load_extension("cogs.tts")

bot.run(TOKEN)
