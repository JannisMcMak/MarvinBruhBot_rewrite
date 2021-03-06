from nextcord.ext import commands
import nextcord
import os

import config
import util.tts_util as tts
import util.utilities as utilities
from util.logger import Logger


log = Logger('Events')


class Events(commands.Cog):
    """
    Event and error handling (Nothing to see here)
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """Event that gets called while bot is starting"""

        log.success("|========================================================================|")

        log.info("Loading...")
        log.debug("Running with PID " + str(os.getpid()))
        log.success(f'{self.bot.user} has connected to Discord!')

        n = []
        for g in self.bot.guilds:
            n.append(g.name)

        log.info("Servers: " + ", ".join(n))

        log.success("|========================================================================|")

        # Custom 
        #conrad = self.bot.get_guild(config.MAIN_GUILD).get_member(352824619360845826)
        #print(conrad)
        #await conrad.edit(nick="IchBinEinDummerHurensohn")



    @commands.Cog.listener()
    async def on_message(self, message):
        """Event that gets called when any message is received. Used to change Rich Presence to requested game"""

        game_ping_channels = config.GAME_PING_CHANNELS
        for channel in game_ping_channels:
            game_ping_channels[game_ping_channels.index(channel)] = int(channel)

        if message.channel.id in game_ping_channels:
            roles = message.channel.guild.roles
            for role in roles:
                if role.mention in message.content:
                    log.info("Presence has been changed to " + role.name)
                    await self.bot.change_presence(activity=nextcord.Game(name=role.name))


    @commands.Cog.listener()
    async def on_command(self, ctx: commands.Context):
        """Event that gets called whenever a command is invoked by a user"""

        try:
            log = Logger(ctx.cog.qualified_name)
        except:
            log = Logger("Unknown")

        command_name = utilities.get_command_name(ctx.message)

        log.info("Command " + command_name.upper() + " invoked by " + ctx.author.name)


    #Error handling
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        """Event that gets called when an error occurs while executing a command"""

        log.error(str(error))
        log.debug(type(error))

        if isinstance(error, commands.errors.MissingRequiredArgument) or isinstance(error, commands.errors.BadArgument):
            help_command = "#help " + utilities.get_command_name(ctx.message)

            await ctx.send("Insufficent arguments. Try `" + help_command + "` to view required arguments.")

        elif "Already connected to a voice channel" in str(error):
            await ctx.send("Already connected to a channel.")

        elif "object has no attribute" in str(error):
            await ctx.send("Please connect to a voice channel first.")
        
        elif "Mp3 file does not exist." in str(error):
            await ctx.send("Mp3 file does not exist.")


    #Event to monitor user voice activity
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """Event that gets called when the voice state of any user changes"""

        if member.id in config.TRACKED_USERS:
            if after.channel is not None and before.self_mute == after.self_mute and before.self_deaf == after.self_deaf:
                if before.self_stream == after.self_stream and before.self_video == after.self_video:
                    log.info("Tracked user (" + member.name + ") joined channel: " + after.channel.name)

                    combination = utilities.get_random_name_combination()

                    filename = await tts.write_mp3(combination, "de", True)
                    await tts.play_in_channel(filename, after.channel)


def setup(bot):
    bot.add_cog(Events(bot))