from discord.ext import commands
import discord

import requests
import os
import config
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

        combination = util.utilities.get_random_name_combination()
        combination_toprint = combination.replace("ä", "e")

        if action is None:            
            await ctx.send(combination_toprint)
        
        elif action == "v" or action == "voice":
            filename = await tts.write_mp3(combination, "de", True)
            await ctx.send(combination_toprint)
            await tts.play_in_channel(filename, ctx.author.voice.channel)
        else:
            await ctx.send("Alle Kombinationen: " + config.NAME_COMBINATIONS_URL)


    @commands.command()
    async def server(self, ctx, action="info"):
        """Minecraft server utilities

        Parameters
        ----------
        action : str, optional
            Action to perform. "info" to show general info, "list" to list online players, "ip" to show IP-address, by default "info"
        """

        if action == "ip":
            await ctx.send(config.MC_SERVER_IP)

        elif action == "list":
            r = requests.get("https://api.mcsrvstat.us/2/" + config.MC_SERVER_IP)
            r = r.json()
            p = r["players"]

            await ctx.send("Online Players: " + ", ".join(p["list"]))

        elif action == "info":
            r = requests.get("https://api.mcsrvstat.us/2/" + config.MC_SERVER_IP)
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
                        config.PUSH_API_KEY, "Server Request", "by " + ctx.author.name))

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


    @commands.command()
    async def gedicht(self, ctx, index: str = "0"):
        """Plays random Gedicht

        Parameters
        ----------
        i : str, optional
            Index of text entry. 0 for random. Can also be "list" to show available text entries, by default 0
        """

        try:
            text = util.utilities.get_gedicht(int(index))
        except:
            gedichte = util.utilities.get_gedicht(0, True)
            embed=discord.Embed(title="Liste aller Gedichte", description="von bekannten Dichtern wie DetlefJoost oder The Wok", color=0x01cdfe)
            embed.set_footer(text="#gedicht <index> für ein bestimmes Gedicht ")
            for index in gedichte:
                embed.add_field(name=index, value=gedichte[index], inline=False)            
            
            await ctx.send(embed=embed)
            return


        filename = await tts.write_mp3(text, "de", True)
        channel = ctx.author.voice.channel

        await tts.play_in_channel(filename, channel)


    @commands.command()
    async def ascii(self, ctx, text: str, size: int = 15, invert: bool = False):
        """Print ascii art from text

        Parameters
        ----------
        text : str
            Text to print
        size : int, optional
            Size of the ascii art (pt), by default 15
        invert : bool, optional
            Whether the ascii art should be inverted, by default False
        """

        rows = util.utilities.ascii(text, size, invert)

        text = "```\n"
        for row in rows:
            if not row.isspace() and any(c not in "#" for c in row):
                text += row + "\n"

        text += "```"

        await ctx.send(text)


def setup(bot):
    bot.add_cog(Other(bot))