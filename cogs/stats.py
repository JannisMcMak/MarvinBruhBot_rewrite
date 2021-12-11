from discord.ext import commands
import discord
import requests
import operator
import config

from util.db_handler import DBHandler


class Stats(commands.Cog):
    """
    Shows statistics
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Create poll")
    async def poll(self, ctx, *topic):
        """Creates a poll for others to vote on

        Parameters
        ----------
        topic : *str
            Topic of the poll
        """

        emojis = ['YES', 'NO']

        host = ctx.author

        t = ''.join(topic)

        embed = discord.Embed(title=" ")
        embed.set_author(name="{}'s Poll".format(
            host.name), icon_url=host.avatar_url)
        embed.add_field(name=t, value="?", inline=False)
        embed.set_footer(text="React to cast your vote")

        msg = await ctx.send(embed=embed)

        for emoji in emojis:
            emoji = discord.utils.get(ctx.guild.emojis, name=emoji)
            await msg.add_reaction(emoji)


    @commands.command()
    async def leaderboard(self, ctx, game: str = "list"):
        """Displays leaderboards

        Parameters
        ----------
        game : str
            Which leaderboard to display. Choose from "counting", "cps".
        """        """"""

        if game == "list":
            #Display list of available leaderboards
            #TODO
            pass
        
        elif game == "counting":
            r = requests.get(config.COUNTING_BOT_API_LINK)
            d = r.json()

            sorted_dict = dict(
                sorted(d.items(), key=operator.itemgetter(1), reverse=True))
            del sorted_dict["count"]

            print(sorted_dict)

            url = ctx.guild.get_member_named(next(iter(sorted_dict))).avatar_url

            embed = discord.Embed(title="COUNTING LEADERBOARD", color=0x01cdfe)
            embed.set_thumbnail(url=url)

            for k in sorted_dict:
                embed.add_field(name=k, value=sorted_dict[k], inline=False)

            await ctx.send(embed=embed)

        elif game == "cps":
            db = DBHandler(ctx.author.id, minigame='cps')
            highscores, wins = db.get_leaderboard()
            
            embed = discord.Embed(title="CPS LEADERBOARD", color=0x01cdfe)
            embed.set_thumbnail(url=config.CPS_LOGO_URL)

            highscore_string = ""
            win_string = ""
            for user_id, value in highscores.items():
                highscore_string += f"\n **{list(highscores).index(user_id) + 1}:** {discord.utils.get(self.bot.get_all_members(), id=user_id).name} (*{value}*)"

            for user_id, value in wins.items():
                win_string += f"\n **{list(wins).index(user_id) + 1}:** {discord.utils.get(self.bot.get_all_members(), id=user_id).name} (*{value}*)"
        
        
            embed.add_field(name="Win streak", value=highscore_string)
            embed.add_field(name="Wins", value=win_string, inline=True)

            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Stats(bot))
