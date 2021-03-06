from nextcord.ext import commands

import util.tts_util as tts
import util


class Bitch(commands.Cog):
    """
    Plays custom Bitch voicelines
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bitch(self, ctx, name, level: int = 0):
        """Plays bitch voice line

        Parameters
        ----------
        name : str
            Name of the person
        level : int, optional
            Length of the voice line, by default 0
        """        

        i = level   

        if name:
            base_line = await util.utilities.get_bitch_voiceline(i)
            text = base_line.format(name, name, name, name)

            filename = await tts.write_mp3(text, "eng", True)

            await tts.play_in_channel(filename, ctx.author.voice.channel)

        else:
            await ctx.send('No name provided.')

    @commands.command()
    async def bitcht(self, ctx, name, level: int = 0):
        """Plays bitch voice line with Twitch TTS

        Parameters
        ----------
        name : str
            Name of the person
        level : int, optional
            Length of the voice line, by default 0
        """     

        i = level

        if name:
            base_line = await util.utilities.get_bitch_voiceline(i)
            text = base_line.format(name, name, name, name)

            filename = await tts.write_mp3_twitch(text, True)
            if filename != None:
                await tts.play_in_channel(filename, ctx.author.voice.channel)

            else:
                await ctx.send('Too long')
        else:
            await ctx.send('No name provided.')


def setup(bot):
    bot.add_cog(Bitch(bot))