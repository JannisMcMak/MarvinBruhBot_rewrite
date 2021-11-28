from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import signal
from watchgod import awatch

from util.logger import Logger

log = Logger('Admin')


class Administration(commands.Cog):
    """
    Utility commands for administration
    """
    
    def __init__(self, bot):
        self.bot = bot
        load_dotenv()

        if os.environ["DEV"] == "yes":
            log.debug("Watchtower enabled!")
            self.watchtower.start()

    @commands.command()
    async def restart(self, ctx):
        """Restarts the container"""        

        if ctx.author.id == int(os.environ["ADMIN_USER"]):
            log.warn("Restarting container...")

            os.kill(os.getpid(), signal.SIGTERM)
        else:
            await ctx.send("Nur coole Leute dürfen das!")


    @commands.command()
    async def selfdestruct(self, ctx):
        """Selfdestruct 2.0 (try it)"""        

        await ctx.author.kick()


    @commands.command()
    async def reload(self, ctx, *cogs):
        """Reloads codebase

        Parameters
        ----------
        *cogs : str
            Cog(s) to reload
        """        

        if ctx.author.id == int(os.environ["ADMIN_USER"]):
            log.warn("Reloading cogs: " + ", ".join(cogs))

            for cog in cogs:
                self.bot.reload_extension("cogs." + cog)
        else:
            await ctx.send("Nur coole Leute dürfen das!")


    @tasks.loop(seconds=5)
    async def watchtower(self):
        """Loop that watches for file changes in cogs/. Enabled in dev-mode"""        

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
