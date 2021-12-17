from nextcord.ext import commands
import nextcord
from mutagen.mp3 import MP3
import time
import os
import asyncio

import util.tts_util as tts
import util.yt_util as yt
import util

log = util.logger.Logger('Mp3s')


class Audio(commands.Cog):
    """
    Plays audio from Mp3 files and Youtube
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def play(self, ctx, name: str = "list", *search):
        """Plays audio from file or Youtube link

        Parameters
        ----------
        name : str, optional
            Name of the file or link to Youtube video, by default "list" (lists available audio files)
        """      
        if len(search) == 0:
            if name == 'list':
                mp3s = os.listdir("mp3s/")
                embed = nextcord.Embed(title="Mp3s", color=0x01cdfe)

                for mp3 in mp3s:
                    name = mp3.split('.')
                    try:
                        audio = MP3('mp3s/' + name[0] + '.mp3')
                        audio_length = time.strftime(
                            '%M:%S', time.gmtime(audio.info.length))
                        embed.add_field(
                            name=name[0], value=audio_length, inline=True)
                    except Exception as err:
                        log.error(err)

                await ctx.send(embed=embed)

            else:
                if name.startswith("https://"):
                    player = await yt.YTDLSource.from_url(name, loop=self.bot.loop, stream=True)
                    log.info("YTDL title: " + player.title)
                    await yt.YTDLSource.play_in_channel(player, ctx.author.voice.channel)
                
                else:
                    log.info("Audio file: " + name)              
                    filename = 'mp3s/' + name.lower() + '.mp3'
                    await tts.play_in_channel(filename, ctx.author.voice.channel)

        else:
            search = [*search]
            search.insert(0, name)
            search = " ".join(search)
            search_result = yt.YTDLSource.search_youtube(search)

            choice_emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]


            embed = nextcord.Embed(title="Search results", description=f"for *{search}*", color=0x01cdfe)
            
            for video_data in search_result:
                embed.add_field(name=str(search_result.index(video_data) + 1) + ". " + video_data["title"], 
                    value="by {} - ({})".format(video_data["channel"], video_data["duration"]), inline=True)
            embed.set_footer(text="React to choose video")
            message = await ctx.send(embed=embed)
            
            for emoji in choice_emojis:
                await message.add_reaction(emoji)
            
            check = lambda r, u: u == ctx.author and str(r.emoji) in choice_emojis

            try:
                reaction, user = await self.bot.wait_for("reaction_add", check=check, timeout=20)
            except asyncio.TimeoutError:
                await message.delete()
                return

            video_choice = search_result[choice_emojis.index(str(reaction.emoji))]
            await message.delete()
            await ctx.send("Now playing `" + video_choice["title"] + "`")

            player = await yt.YTDLSource.from_url("https://youtube.com" + video_choice["url_suffix"], loop=self.bot.loop, stream=True)
            log.info("YTDL title: " + player.title)
            await yt.YTDLSource.play_in_channel(player, ctx.author.voice.channel)



    @commands.command()
    async def bruh(self, ctx):
        """Plays infamous audio clip"""        

        channel = ctx.author.voice.channel
        filename = 'mp3s/audio.mp3'

        await tts.play_in_channel(filename, channel)


    @commands.command()
    async def disconnect(self, ctx):
        """Stops playing current audio and disconnects bot"""        

        for voice_client in self.bot.voice_clients:
            voice_client.stop()
            await voice_client.disconnect()


    @commands.command()
    async def stop(self, ctx):
        """Stops playing current audio and disconnects bot"""        

        for voice_client in self.bot.voice_clients:
            voice_client.stop()
            await voice_client.disconnect()



def setup(bot):
    bot.add_cog(Audio(bot))