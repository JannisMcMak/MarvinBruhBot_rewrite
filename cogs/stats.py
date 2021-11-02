from discord.ext import commands
import discord
import requests
import operator
import os


class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Create poll")
    async def poll(self, ctx, *topic):
        emojis = ['YES', 'NO']

        host = ctx.author
        print(topic)
        t = ''.join(topic)

        embed = discord.Embed(title=" ")
        embed.set_author(name="{}'s Poll".format(
            host.name), icon_url=host.avatar_url)
        embed.add_field(name=t, value="?", inline=False)
        embed.set_footer(text="React to cast your vote")

        msg = await ctx.send(embed=embed)

        for emoji in emojis:
            emoji = discord.utils.get(ctx.guild, name=emoji)
            await msg.add_reaction(emoji)

    @commands.command(help="Counting leaderboard")
    async def leaderboard(self, ctx):
        r = requests.get(os.environ["COUNTING_API_LINK"])
        d = r.json()

        sorted_dict = dict(
            sorted(d.items(), key=operator.itemgetter(1), reverse=True))
        del sorted_dict["count"]

        url = ctx.author.get_member_named(next(iter(sorted_dict))).avatar_url

        embed = discord.Embed(title="COUNTING LEADERBOARD", color=0x01cdfe)
        embed.set_thumbnail(url=url)

        for k in sorted_dict:
            embed.add_field(name=k, value=sorted_dict[k], inline=False)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Stats(bot))
