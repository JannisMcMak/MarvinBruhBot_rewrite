from nextcord.ext import commands
import nextcord
import requests
import operator
import config

from util.db_handler import DBInfoHandler


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

        embed = nextcord.Embed(title=" ")
        embed.set_author(name="{}'s Poll".format(
            host.name), icon_url=host.avatar_url)
        embed.add_field(name=t, value="?", inline=False)
        embed.set_footer(text="React to cast your vote")

        msg = await ctx.send(embed=embed)

        for emoji in emojis:
            emoji = nextcord.utils.get(ctx.guild.emojis, name=emoji)
            await msg.add_reaction(emoji)


    @commands.command()
    async def leaderboard(self, ctx, game: str = "list"):
        """Displays leaderboards

        Parameters
        ----------
        game : str
            Which leaderboard to display. Choose from "counting", "cps". "list" to display available leaderboards.
        """

        db_handler = DBInfoHandler()
        minigames = db_handler.get_minigame_list()
        
        if game == "list":
            embed = nextcord.Embed(title="Liste aller Leaderboards", color=0x01cdfe)
            embed.set_footer(text="#leaderboard <name> um Leaderboard anzuzeigen")

            minigames_string = ""
            for minigame in minigames:
                minigames_string += minigame + "\n"

            embed.add_field(name="Minigames", value=minigames_string, inline=True)
            embed.add_field(name="Andere", value="counting", inline=True)
            
            await ctx.send(embed=embed)
        
        
        elif game == "counting":
            r = requests.get(config.COUNTING_BOT_API_LINK)
            d = r.json()

            sorted_dict = dict(
                sorted(d.items(), key=operator.itemgetter(1), reverse=True))
            del sorted_dict["count"]

            print(sorted_dict)

            url = ctx.guild.get_member_named(next(iter(sorted_dict))).avatar_url

            embed = nextcord.Embed(title="COUNTING LEADERBOARD", color=0x01cdfe)
            embed.set_thumbnail(url=url)

            for k in sorted_dict:
                embed.add_field(name=k, value=sorted_dict[k], inline=False)

            await ctx.send(embed=embed)

        
        elif game in minigames:
            highscores, wins = db_handler.get_leaderboard(game)
            
            embed = nextcord.Embed(title=f"{game.upper()} LEADERBOARD", color=0x01cdfe)
            embed.set_thumbnail(url=config.CPS_LOGO_URL)

            highscore_string = ""
            win_string = ""
            for user_id, value in highscores.items():
                highscore_string += f"\n **{list(highscores).index(user_id) + 1}:** {nextcord.utils.get(self.bot.get_all_members(), id=user_id).name} (*{value}*)"

            for user_id, value in wins.items():
                win_string += f"\n **{list(wins).index(user_id) + 1}:** {nextcord.utils.get(self.bot.get_all_members(), id=user_id).name} (*{value}*)"
        
        
            embed.add_field(name="Win streak", value=highscore_string)
            embed.add_field(name="Wins", value=win_string, inline=True)

            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Stats(bot))
