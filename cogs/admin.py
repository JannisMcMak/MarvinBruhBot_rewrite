from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import signal
from watchgod import awatch

from util.logger import Logger

log = Logger('Admin')


class Administration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        load_dotenv()

        if os.environ["DEV"] == "yes":
            log.debug("Watchtower enabled!")
            self.watchtower.start()

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


    @tasks.loop(seconds=5)
    async def watchtower(self):
        async for changes in awatch('./cogs'):
            change = next(iter(changes))
            f = change[1]
            change = change[0]
            print(f)
            print(change)

            if "Change.modified" == str(change):
                try:
                    cog = f.split("/")[2]
                except:
                    cog = f.split("\\")[1]
                cog = cog.split(".")[0]

                log.warn("Reloading cog: " + cog)
                self.bot.reload_extension("cogs." + cog)

def setup(bot):
    bot.add_cog(Administration(bot))
