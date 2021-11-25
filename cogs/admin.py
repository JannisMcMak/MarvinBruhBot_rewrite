from discord.ext import commands
from dotenv import load_dotenv
import os
import signal

from util.logger import Logger

log = Logger('Admin')


class Administration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        load_dotenv()

    @commands.command(help='Restart container')
    async def restart(self, ctx):
        if ctx.author.id == int(os.environ["ADMIN_USER"]):
            log.warn("Restarting container...")

            os.kill(os.getpid(), signal.SIGTERM)
        else:
            await ctx.send("Nur coole Leute dürfen das!")


    @commands.command(help='Selfdestruct 2.0 (try it)')
    async def selfdestruct(self, ctx):
        await ctx.author.kick()


    @commands.command(help="Reload codebase")
    async def reload(self, ctx, *cogs):
        if ctx.author.id == int(os.environ["ADMIN_USER"]):
            log.warn("Reloading cogs: " + ", ".join(cogs))

            for cog in cogs:
                self.bot.reload_extension("cogs." + cog)
        else:
            await ctx.send("Nur coole Leute dürfen das!")


def setup(bot):
    bot.add_cog(Administration(bot))
