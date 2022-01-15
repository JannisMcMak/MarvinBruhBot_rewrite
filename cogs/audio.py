from nextcord.ext import commands
import nextcord
from mutagen.mp3 import MP3
import time
import os
import asyncio

from util.views.selection import SimpleSelection
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


    @commands.command(aliases=["audio", "playmp3"])
    async def mp3(self, ctx, name: str = "list"):
        """Plays audio from file

        Parameters
        ----------
        name : str, optional
            Name of the file, by default "list" to display list of available files
        """

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
            log.info("Audio file: " + name)              
            filename = 'mp3s/' + name.lower() + '.mp3'
            await tts.play_in_channel(filename, ctx.author.voice.channel)


    @commands.command(aliases=["playyt", "yt", "search"])
    async def play(self, ctx, *search):
        """Plays audio from Youtube link or search string

        Parameters
        ----------
        name : str, optional
            Link to Youtube video or search string
        """      

        # parse arguments
        search = [*search]
        search = " ".join(search)
        url = ""

        # check if arg is url
        if search.startswith("https://"):
            url = search

        else:
            search_result = yt.YTDLSource.search_youtube(search)


            embed = nextcord.Embed(title="Search results", description=f"for *{search}*", color=0x01cdfe)
            
            for video_data in search_result:
                embed.add_field(name=str(search_result.index(video_data) + 1) + ". " + video_data["title"], 
                    value="by {} - ({})".format(video_data["channel"], video_data["duration"]), inline=True)
            embed.set_footer(text="Click button to choose video")
            
            view = SimpleSelection(5)
            message = await ctx.send(embed=embed, view=view)

            await view.wait()
            
            if view.choice is None:
                await message.delete()
                return

            video_choice = search_result[view.choice - 1]
        
            await message.delete()
            await ctx.send("Now playing `" + video_choice["title"] + "`")

            url = "https://youtube.com" + video_choice["url_suffix"]

        player = await yt.YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
        log.info("YTDL title: " + player.title)
        await yt.YTDLSource.play_in_channel(player, ctx.author.voice.channel)



    @commands.command()
    async def bruh(self, ctx):
        """Plays infamous audio clip"""        

        channel = ctx.author.voice.channel
        filename = 'mp3s/audio.mp3'

        await tts.play_in_channel(filename, channel)


    @commands.command(aliases=["stop", "dc"])
    async def disconnect(self, ctx):
        """Stops playing current audio and disconnects bot"""        

        for voice_client in self.bot.voice_clients:
            voice_client.stop()
            await voice_client.disconnect()


def setup(bot):
    bot.add_cog(Audio(bot))