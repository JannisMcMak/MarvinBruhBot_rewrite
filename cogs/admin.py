from discord.ext import commands
import sys

class Administration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help='Selfdestruct')
    async def exit(self, ctx):
        await ctx.author.kick()

    @commands.command(help='Selfdestruct 2.0 (try it)')
    async def selfdestruct(self, ctx):
        await ctx.author.kick()

    @commands.command(help="Reload codebase")
    async def reload(self, ctx):
        sys.exit(1)


def setup(bot):
    bot.add_cog(Administration(bot))