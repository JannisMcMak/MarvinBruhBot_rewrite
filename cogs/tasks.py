import discord
from discord.ext import commands, tasks

from datetime import datetime, timedelta
import pytz
from dotenv import load_dotenv
import os

import util
import util.tts_util as tts

log = util.logger.Logger('Tasks')


class Tasks(commands.Cog):
    """
    Performs repeating tasks
    """

    def __init__(self, bot):
        load_dotenv()

        self.bot = bot
        self.rl_tournament_time = os.environ["RL_TOURNAMENT_TIME"]

        if os.environ["HOURLY_TIME_NOTIFICATIONS"] == "yes":
            log.debug("Hourly time notifications enabled!")
            self.time_loop.start()


    @commands.command(help="Toggle hourly time notifications")
    async def uhr(self, ctx):
        if self.time_loop.is_running() and not self.time_loop.is_being_cancelled():
            log.info("Hourly notifications enabled!")
            self.time_loop.start()
            await ctx.send("Hourly notifications enabled!")
        else:
            log.info("Hourly notifications disabled!")
            self.time_loop.cancel()
            await ctx.send("Hourly notifications disabled!")

    @tasks.loop(seconds=60)
    async def time_loop(self):
        minutes = (datetime.now(tz=pytz.timezone(os.environ["TZ"]))).strftime('%M')
        if "00" in minutes:
            hour = (datetime.now(tz=pytz.timezone(os.environ["TZ"]))).strftime('%I')

            text = await util.utilities.get_time_notification(int(hour))

            guild = None
            for g in self.bot.guilds:
                if g.id == int(os.environ["MAIN_GUILD"]):
                    guild = g

            channel = None
            if guild is not None:
                for c in guild.voice_channels:
                    if channel is None or len(channel.members) < len(c.members):
                        channel = c
            
            if channel is not None:
                filename = await tts.write_mp3_twitch(text, True)
                await tts.play_in_channel(filename, channel)


    @commands.command(help="Rocket League tournament notifications")
    async def tournament(self, ctx, action: str = "toggle", time: str = os.environ["RL_TOURNAMENT_TIME"]):

        async def start_loop():
            self.rl_tournament_time = time

            intervals = os.environ["RL_TOURNAMENT_INTERVALS"].split(",")
            team_ids = os.environ["RL_TOURNAMENT_TEAM_IDS"].split(",")
            for i in intervals:
                intervals[intervals.index(i)] = int(i)
            for i in team_ids:
                team_ids[team_ids.index(i)] = int(i)

            log.info("Starting RL tournament notifier for tournament at {}...".format(time))
            await ctx.send("Starting RL tournament notifier...")
            self.tournament_notifier.start(user=ctx.author, intervals=intervals, team_ids=team_ids)        
        
        async def stop_loop():
            log.info("Stopping RL tournament notifier...")
            await ctx.send("Stopping RL tournament notifier...")
            self.tournament_notifier.cancel()  
        

        if action in ["active", "notify", "activate", "enable", "start"] or action == "toggle" and not self.tournament_notifier.is_running():
            if self.tournament_notifier.is_running():
                await ctx.send("RL tournament notifier is already running.")
                return
            
            await start_loop()
            return

        if action in ["deactivate", "disable", "stop", "cancel", "toggle"] and self.tournament_notifier.is_running():
            await stop_loop()
            return


        if action in ["status", "info"]:
            if not self.tournament_notifier.is_running() or self.tournament_notifier.is_being_cancelled():
                await ctx.send("RL tournament notifier is not running...")
            else:
                await ctx.send("RL tournament notifier is running for tournament at " + str(self.rl_tournament_time))
            

    @tasks.loop(seconds=60)
    async def tournament_notifier(self, intervals, user, team_ids):   
        for interval in intervals:
            current_time = (datetime.now(tz=pytz.timezone(os.environ["TZ"])) + timedelta(hours=0, minutes=interval)).strftime('%H:%M')

            if current_time == self.rl_tournament_time:
                text = "Attention epic Rocket League gamers! The tournament starts in {}"
                
                if interval == 0:
                    log.success("RL Tournament loop finished!")
                    self.tournament_notifier.cancel()
                    return

                elif interval < 60:
                    text = text.format(str(interval) + " minutes!")
                else:
                    text = text.format(str(int(interval / 60)) + " hours!")

                try:
                    channel = user.voice.channel
                    voice_states = channel.voice_states
                except:
                    channel = None
                    voice_states = {}
                

                for team_id in team_ids:
                    if team_id not in voice_states:
                        member = discord.utils.get(self.bot.get_all_members(), id=team_id)
                        await member.send(text)

                filename = await tts.write_mp3_twitch(text, True)
                await tts.play_in_channel(filename, channel)

    
def setup(bot):
    bot.add_cog(Tasks(bot))