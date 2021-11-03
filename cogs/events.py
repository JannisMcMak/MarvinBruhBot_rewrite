from discord.ext import commands
import discord
import util.tts_util as tts
import random
import json
import os

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Loading...")
        print(f'{self.bot.user} has connected to Discord!')

        n = []
        for g in self.bot.guilds:
            n.append(g.name)

        print("Servers: " + ",".join(n))


    #Event to change Rich Presence to called game
    @commands.Cog.listener()
    async def on_message(self, message):
        zrocken_channels = [714452232791261246,
                            396671581558013952, 836988148814184509]

        if message.channel.id in zrocken_channels:
            roles = message.channel.guild.roles
            for role in roles:
                if role.mention in message.content:
                    print(role)
                    await self.bot.change_presence(activity=discord.Game(name=role.name))

        #await self.bot.process_commands(message)


    #Event to monitor user voice activity
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.id == os.environ["SIMON_TRACKED_USER"]:
            if after.channel is not None:
                print("Simon joined channel: " + after.channel.name)

                with open('hidden/simon_combinations.json', 'r') as f:
                    data = json.load(f)
                    combination = random.choice(data)

                filename = await tts.write_mp3(" ".join(combination), "de", True)
                await tts.play_in_channel(filename, after.channel)

def setup(bot):
    bot.add_cog(Events(bot))