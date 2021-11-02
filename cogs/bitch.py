from discord.ext import commands
import tts_util as tts


class Bitch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help='Bitch voice line')
    async def bitch(self, ctx, name, level: int = 0):
        i = level

        if name:
            base_line = await get_bitchass_line(i)
            text = base_line.format(name, name, name, name)

            filename = await tts.write_mp3(text, "eng", True)

            await tts.play_in_channel(filename, ctx.author.channel)

        else:
            await ctx.send('No name provided.')

    @commands.command(help='Bitch voice line (Twitch TTS)')
    async def bitcht(self, ctx, name, level: int = 0):
        i = level

        if name:
            base_line = await get_bitchass_line(i)
            text = base_line.format(name, name, name, name)

            filename = await tts.write_mp3_twitch(text, True)
            if filename != None:
                await tts.play_in_channel(filename, ctx.author.channel)

            else:
                await ctx.send('Too long')
        else:
            await ctx.send('No name provided.')


async def get_bitchass_line(i):
    switcher = {
        1: '{} is a little bitch ass bitch bitch why so dumb hahah stupid hahah dumb {} lmao bitch ass bitch hahah small cock no balls bitch ass bitch',
        2: '{} is a little bitch ass bitch bitch why so dumb hahah stupid hahah dumb {} lmao bitch ass bitch hahah small cock no balls bitch ass bitch bitch bitch bitch bitch bitch ok again bitch bitch bich bitch bitch lmao',
        3: '{} is a little bitch ass bitch bitch why so dumb hahah stupid hahah dumb {} lmao bitch ass bitch hahah small cock no balls bitch ass bitch bitch bitch bitch bitch bitch ok again bitch bitch bich bitch bitch lmao {} is so dumb hahah such a bitch look at him lmao haha bitch ass bitch bitch',
        4: '{} is a little bitch ass bitch bitch why so dumb hahah stupid hahah dumb {} lmao bitch ass bitch hahah small cock no balls bitch ass bitch bitch bitch bitch bitch bitch ok again bitch bitch bich bitch bitch lmao {} is so dumb hahah such a bitch look at him lmao haha bitch ass bitch bitch u are such a bitch lmao i cant believe how fucking stupid you are bitch ass bitch stop existing you bitch ass bitch hahaahh bitch lmao bitch i hate you your life is a bruh momentum just like mine hahah lmao fuck you {} stupid bitch ass bitch bitch bitch',
        5: '{} is a little bitch ass bitch bitch why so dumb hahah stupid hahah dumb lmao bitch ass bitch hahah small cock no balls bitch ass bitch bitch bitch bitch bitch bitch ok again bitch bitch bich bitch bitch lmao {} is so dumb hahah such a bitch look at him lmao haha bitch ass bitch bitch u are such a bitch lmao i cant believe how fucking stupid you are bitch ass bitch stop existing you bitch ass bitch hahaahh bitch lmao bitch i hate you your life is a bruh momentum just like mine hahah lmao fuck you stupid bitch ass bitch bitch bitch imagine being {} hahah i cant believe how stupid this bitch is lmao hahahah its funny because he is so fucking dumb hahah bitch bitch bitch bitch bitch bitch bitch bitch bitch bitch bitch bitch bitch bitch bitch bitch bitch bitch bitch bitch bitch bitch bitch bitch bitch bitch bitch bitch bitch bitch bitch bitch bitch bitch bitch lmao fuck you {} bitch ass bitch bitch'
    }

    return switcher.get(i, "{} is a little bitch")


def setup(bot):
    bot.add_cog(Bitch(bot))