from discord.ext import commands
import util.tts_util as tts


class TTS(commands.Cog):
    """
    Plays Text To Speech messages
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def versuh(self, ctx, *text):
        """Plays TTS message in German

        Parameters
        ----------
        text : str
            Message to play
        """

        filename = await tts.write_mp3(text)

        await tts.play_in_channel(filename, ctx.author.voice.channel)

    @commands.command()
    async def versuhe(self, ctx, *text):
        """Plays TTS message in English

        Parameters
        ----------
        text : str
            Message to play
        """

        filename = await tts.write_mp3(text, "eng")

        await tts.play_in_channel(filename, ctx.author.voice.channel)

    @commands.command()
    async def versuhi(self, ctx, *text):
        """Plays TTS message in English (with Indian accent)

        Parameters
        ----------
        text : str
            Message to play
        """

        filename = await tts.write_mp3(text, "ind")

        await tts.play_in_channel(filename, ctx.author.voice.channel)

    @commands.command()
    async def versuht(self, ctx, *text):
        """Plays TTS message with Brian's voice (from Twitch donation messages)

        Parameters
        ----------
        text : str
            Message to play
        """

        filename = await tts.write_mp3_twitch(text)
        
        if filename != None:
            await tts.play_in_channel(filename, ctx.author.voice.channel)
        else:
            await ctx.send('Text was too long')

    @commands.command()
    async def versuhp(self, ctx, *text):
        """Plays TTS message with german female voice

        Parameters
        ----------
        text : str
            Message to play
        """

        filename = await tts.write_mp3_ibm(text, lang="p")
        
        if filename != None:
            await tts.play_in_channel(filename, ctx.author.voice.channel)
        else:
            await ctx.send('Text was too long')

def setup(bot):
    bot.add_cog(TTS(bot))