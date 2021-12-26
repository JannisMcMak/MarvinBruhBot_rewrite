from nextcord.ext import commands, tasks

from datetime import datetime, timedelta
import pytz
import config

import util
import util.tts_util as tts

log = util.logger.Logger('Tasks')


class Tasks(commands.Cog):
    """
    Performs repeating tasks
    """

    def __init__(self, bot):
        self.bot = bot
        self.rl_tournament_time = config.RL_TOURNAMENT_TIME

        if config.TIME_NOTIFICATIONS_BY_DEFAULT:
            log.debug("Hourly time notifications enabled!")
            self.time_loop.start()


    @commands.command()
    async def uhr(self, ctx):
        """Toggles hourly time notifications"""

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
        """Loop that performs hourly time notifications"""

        minutes = (datetime.now(tz=pytz.timezone(config.TZ))).strftime('%M')
        if "00" in minutes:
            hour = (datetime.now(tz=pytz.timezone(config.TZ))).strftime('%I')

            text = await util.utilities.get_time_notification(int(hour))

            guild = None
            for g in self.bot.guilds:
                if g.id == config.MAIN_GUILD:
                    guild = g

            channel = None
            if guild is not None:
                for c in guild.voice_channels:
                    if channel is None or len(channel.members) < len(c.members):
                        channel = c
            
            if channel is not None and len(channel.members) > 0:
                filename = await tts.write_mp3_twitch(text, True)
                await tts.play_in_channel(filename, channel)



    @commands.command()
    async def tournament(self, ctx, action: str = "toggle", time: str = config.RL_TOURNAMENT_TIME):
        """Manages Rocket League tournament notifications

        Parameters
        ----------
        action : str, optional
            Action to perform, e.g. "enable/disable" or "activate/deactivate. "info" to show general information. By default "toggle"
        time : str, optional
            The time when the tournament starts, by default 23:00
        """

        async def start_loop():
            self.rl_tournament_time = time

            intervals = config.RL_TOURNAMENT_INTERVALS
            team_ids = config.RL_TEAM_MEMBER_IDS
            for i in intervals:
                intervals[intervals.index(i)] = int(i)
            for i in team_ids:
                team_ids[team_ids.index(i)] = int(i)

            log.info("Starting RL tournament notifier for tournament at {}...".format(time))
            await ctx.send("Starting RL tournament notifier...")
            self.tournament_notifier.start(ctx=ctx, intervals=intervals, team_ids=team_ids)        
        
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
    async def tournament_notifier(self, intervals, ctx, team_ids):   
        """Loop that performs Rocket League tournament notifications"""

        for interval in intervals:
            current_time = (datetime.now(tz=pytz.timezone(config.TZ)) + timedelta(hours=0, minutes=interval - 1)).strftime('%H:%M')

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


                channel = None
                voice_channels = []
                for team_member_id in team_ids:
                    try:
                        member = ctx.guild.get_member(team_member_id)
                        channel = member.voice.channel
                        voice_channels.append(channel)
                    except:
                        log.info("Sending notification to " + member.name)
                        
                        if team_member_id == config.RL_TEAM_MEMBER_IDS[2]:
                            member = ctx.guild.get_member(config.RL_TEAM_NOTIFICATION_IDS[0])
                        
                        await member.send(text)
                        
                        
                filename = await tts.write_mp3_twitch(text, True)
                await tts.play_in_channel(filename, channel)

    
def setup(bot):
    bot.add_cog(Tasks(bot))