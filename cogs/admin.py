from nextcord.ext import commands, tasks
import signal
from watchgod import awatch
import os

from util.logger import Logger
import config
from web.web import stop_apiserver

log = Logger('Admin')


class Administration(commands.Cog):
    """
    Utility commands for administration
    """
    
    def __init__(self, bot):
        self.bot = bot

        if config.DEV_MODE_BY_DEFAULT:
            log.debug("Watchtower enabled!")
            self.watchtower.start()


    @commands.command()
    async def restart(self, ctx):
        """Restarts the container"""        

        if ctx.author.id in config.ADMIN_USERS:
            log.warn("Restarting container...")
            
            if config.API_SERVER_RUN_BY_DEFAULT:
                log.debug("Shutting down API-Webserver...")
                stop_apiserver()
            
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

        if ctx.author.id in config.ADMIN_USERS:
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
