from discord.ext import commands
import discord

import requests
import os
import json
import random
import asyncio

import util
import tts_util as tts


class Other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Random Simon Name Generator")
    async def simon(self, ctx, arg=None):
        if arg is None:
            with open('hidden/simon_combinations.json', 'r') as f:
              data = json.load(f)
              combination = random.choice(data)
            
            await ctx.send(" ".join(combination))

        else:
            await ctx.send("Alle Kombinationen: " + os.environ["SIMON_COMBINATIONS_WEB_LINK"])

    @commands.command(help="MC server utilities")
    async def server(self, ctx, arg=None):
        if arg == "ip":
            await ctx.send(os.environ["MC_SERVER_IP"])

        elif arg == "list":
            r = requests.get("https://api.mcsrvstat.us/2/" + os.environ["MC_SERVER_IP"])
            r = r.json()
            p = r["players"]

            await ctx.send("Online Players: " + ", ".join(p["list"]))

        else:
            r = requests.get("https://api.mcsrvstat.us/2/" + os.environ["MC_SERVER_IP"])
            r = r.json()
            p = r["players"]

            status = r["online"]

            if status:
                await ctx.send("Server online! ({}/{})".format(str(p["online"]), str(p["max"])))

            else:
                await ctx.send("Server offline! Request to start? `y/n`")
                msg = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author and message.channel.id == ctx.channel.id)
                if msg.content.lower() in ["yes", "y"]:
                    r = requests.post("https://push.techulus.com/api/v1/notify/{}?title={}&body={}".format(
                        os.environ['PUSH_API_KEY'], "Server Request", "by " + ctx.author.name))

                    await ctx.send("Request sent!")


    @commands.command(help="Wake up someone")
    async def wake(self, ctx, user: discord.Member, count: int = 3):
        channels = ctx.guild.voice_channels
        user_channel = user.voice.channel

        if user_channel is None:
            await ctx.send('User is not in a channel')
            raise Exception

        if not user.voice.self_deaf:
            if not user.voice.self_mute:
                await ctx.send('This guy is not afk')
                raise Exception

        if count > 10:
            await ctx.send('lil too much')
            raise Exception

        for i in range(count - 1):
            try:
                a = random.randint(0, len(channels) - 1)
                await user.move_to(channels[a], reason="Wake")
            except Exception as e:
                print(e)

            await asyncio.sleep(0.5)

        await user.move_to(user_channel)


    @commands.command(help='Gedichte von Dichtern')
    async def gedicht(self, ctx, i: int = 0):
        print('Gedicht')

        text = await util.util.get_gedicht(i)

        filename = await tts.write_mp3(text, "de", True)
        channel = ctx.author.voice.channel

        await tts.play_in_channel(filename, channel)


def setup(bot):
    bot.add_cog(Other(bot))