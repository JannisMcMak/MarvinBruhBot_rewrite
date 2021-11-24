from discord.ext import commands, tasks

from datetime import datetime, timedelta
import pytz
from dotenv import load_dotenv
import os

import util
import util.tts_util as tts

log = util.logger.Logger('Tasks')


class Tasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        load_dotenv()


    @commands.command(help="Rocket League tournament notifications")
    async def tournament(self, ctx, action: str = "toggle", time: str = os.environ["RL_TOURNAMENT_TIME"]):
        intervals = os.environ["RL_TOURNAMENT_INTERVALS"].split(",")
        for i in intervals:
            intervals[intervals.index(i)] = int(i)

        async def start_loop():
            log.info("Starting RL tournament notifier for tournament at {}...".format(time))
            await ctx.send("Starting RL tournament notifier...")
            self.tournament_notifier.start(user=ctx.author, intervals=intervals, time=time)        
        
        async def stop_loop():
            log.info("Stopping RL tournament notifier...")
            await ctx.send("Stopping RL tournament notifier...")
            self.tournament_notifier.cancel()  
        

        if action in ["active", "notify", "activate", "enable", "start", "toggle"] and not self.tournament_notifier.is_running():
            if self.tournament_notifier.is_running():
                await ctx.send("RL tournament notifier is already running.")

            await start_loop()
            return

        if action in ["deactivate", "disable", "stop", "cancel", "toggle"] and self.tournament_notifier.is_running():
            await stop_loop()
            return



    @tasks.loop(seconds=60)
    async def tournament_notifier(self, intervals, user, time):   
        for interval in intervals:
            current_time = (datetime.now(tz=pytz.timezone(os.environ["TZ"])) + timedelta(hours=0, minutes=interval)).strftime('%H:%M')

            if current_time == time:
                text = "Attention epic Rocket League gamers! The tournament starts in {}"
                
                if interval == 0:
                    log.success("RL Tournament loop finished!")
                    self.tournament_notifier.cancel()
                    return

                elif interval < 60:
                    text = text.format(str(interval) + "minutes")
                else:
                    text = text.format(str(int(interval / 60)) + "hours")

                
                filename = await tts.write_mp3_twitch(text, True)
                await tts.play_in_channel(filename, user.voice.channel)

                # DM notifs

            

def setup(bot):
    bot.add_cog(Tasks(bot))