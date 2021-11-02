from discord.ext import commands
import tts_util as tts


class TTS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help='TTS German')
    async def versuh(self, ctx, *text):
        print(text)
        print(ctx.author.name)

        filename = await tts.write_mp3(text)

        await tts.play_in_channel(filename, ctx.author.channel)

    @commands.command(help='TTS English')
    async def versuhe(self, ctx, *text):
        print(text)
        print(ctx.author.name)

        filename = await tts.write_mp3(text, "eng")

        await tts.play_in_channel(filename, ctx.author.channel)

    @commands.command(help='TTS Indian')
    async def versuhi(self, ctx, *text):
        print(text)
        print(ctx.author.name)

        filename = await tts.write_mp3(text, "ind")

        await tts.play_in_channel(filename, ctx.author.channel)

    @commands.command(help='Twitch TTS')
    async def versuht(self, ctx, *text):
        print(text)
        print(ctx.author.name)

        filename = await tts.write_mp3_twitch(text)
        if filename != None:
            await tts.play_in_channel(filename, ctx.author.channel)

        else:
            await ctx.send('Text was too long')


def setup(bot):
    bot.add_cog(TTS(bot))