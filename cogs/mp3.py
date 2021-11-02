from discord.ext import commands
import discord
import util.tts_util as tts
from mutagen.mp3 import MP3
import time
import os


class Mp3s(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help='Play mp3')
    async def play(self, ctx, name: str = "list"):

        if name == 'list':
            mp3s = os.listdir("../mp3s")
            embed = discord.Embed(title="Mp3s", color=0x01cdfe)

            for mp3 in mp3s:
                name = mp3.split('.')
                try:
                    audio = MP3('./mp3s/' + name[0] + '.mp3')
                    audio_length = time.strftime(
                        '%M:%S', time.gmtime(audio.info.length))
                    embed.add_field(
                        name=name[0], value=audio_length, inline=True)
                except Exception as err:
                    print(err)

            await ctx.send(embed=embed)

        else:
            print('Mp3: ' + name)
            filename = '../mp3s/' + name.lower() + '.mp3'

            await tts.play_in_channel(filename, ctx.author.channel)


    @commands.command()
    async def bruh(self, ctx):
        channel = ctx.author.voice.channel
        filename = 'mp3s/audio.mp3'

        await tts.play_in_channel(filename, channel)