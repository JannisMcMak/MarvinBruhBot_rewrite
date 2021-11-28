from discord.ext import commands
import discord

import requests
import os
import json
import random
import asyncio

import util
import util.tts_util as tts

log = util.logger.Logger('Other')


class Other(commands.Cog):
    """
    Miscellaneous commands
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def simon(self, ctx, action=None):
        """Random Simon Name Generator

        Parameters
        ----------
        action : str, optional
            Additional action to perform. "voice" to play in voice, "all" to view all combinations, by default None
        """        

        with open('hidden/simon_combinations.json', 'r') as f:
              data = json.load(f)
              combination = random.choice(data)

        if action is None:            
            await ctx.send(" ".join(combination))
        
        elif action == "v" or action == "voice":
            filename = await tts.write_mp3("".join(combination), "de", True)
            await ctx.send(" ".join(combination))
            await tts.play_in_channel(filename, ctx.author.voice.channel)
        else:
            await ctx.send("Alle Kombinationen: " + os.environ["SIMON_COMBINATIONS_WEB_LINK"])


    @commands.command()
    async def server(self, ctx, action="info"):
        """Minecraft server utilities

        Parameters
        ----------
        action : str, optional
            Action to perform. "info" to show general info, "list" to list online players, "ip" to show IP-address, by default "info"
        """

        if action == "ip":
            await ctx.send(os.environ["MC_SERVER_IP"])

        elif action == "list":
            r = requests.get("https://api.mcsrvstat.us/2/" + os.environ["MC_SERVER_IP"])
            r = r.json()
            p = r["players"]

            await ctx.send("Online Players: " + ", ".join(p["list"]))

        elif action == "info":
            r = requests.get("https://api.mcsrvstat.us/2/" + os.environ["MC_SERVER_IP"])
            r = r.json()

            status = r["online"]

            if status:
                p = r["players"]
                await ctx.send("Server online! ({}/{})".format(str(p["online"]), str(p["max"])))

            else:
                await ctx.send("Server offline! Request to start? `y/n`")
                msg = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author and message.channel.id == ctx.channel.id)
                if msg.content.lower() in ["yes", "y"]:
                    r = requests.post("https://push.techulus.com/api/v1/notify/{}?title={}&body={}".format(
                        os.environ['PUSH_API_KEY'], "Server Request", "by " + ctx.author.name))

                    await ctx.send("Request sent!")

        else:
            await ctx.send("Unknown action. Try `info`, `ip` or `list`")


    @commands.command()
    async def wake(self, ctx, user: discord.Member, count: int = 3):
        """Move someone between voice channel to wake them up

        Parameters
        ----------
        user : discord.Member
            User to move. Used with mention (@user)
        count : int, optional
            Number of times to move the user, by default 3, max 10
        """

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
                log.error(e)

            await asyncio.sleep(0.5)

        await user.move_to(user_channel)


    @commands.command(help='Gedichte von Dichtern')
    async def gedicht(self, ctx, i: int = 0):
        """Plays text from 'gedichte.json' file

        Parameters
        ----------
        i : int, optional
            Index of text entry. 0 for random, by default 0
        """

        text = await util.utilities.get_gedicht(i)

        filename = await tts.write_mp3(text, "de", True)
        channel = ctx.author.voice.channel

        await tts.play_in_channel(filename, channel)


def setup(bot):
    bot.add_cog(Other(bot))