import discord
from discord.ext import commands

import random
import asyncio

import config
from util.db_handler import DBHandler


class Minigames(commands.Cog):
    """
    Fun Minigames. Mainly developed by Professor
    """

    def __init__(self, bot):
        self.bot = bot
        self.cps_streak = 0
   
    
    
    @commands.command()
    async def cps(self, ctx):
        """Rock, Paper Scissors in nsfw (developed by Professor)"""

        db = DBHandler(ctx.author.id, minigame='cps')

        def gewinner(wahl, computer, wahl_emote):
            ergebnis = (wahl - computer) % 3
            if ergebnis == 0:
                if wahl == 1:
                    embed.set_footer(text ="Cock on cock? Seems kinda gay tbh...", icon_url=config.THONK_ICON_URL)
                embed.add_field(name=f"{wahl_emote} gleicht {computer_emote}", value=f"Unentschieden!", inline=False)
                embed.colour = 0xf6b26b
                self.cps_streak = 0


            elif ergebnis == 1:
                embed.add_field(name=f"{wahl_emote} schlägt {computer_emote}", value=f"{ctx.author.name} hat gewonnen", inline=False)
                embed.colour = 0x38761d
                self.cps_streak += 1
                db.increment_wins()
                if self.cps_streak > db.get_highscore():
                    db.new_highscore(self.cps_streak)

            elif ergebnis == 2:
                embed.add_field(name=f"{computer_emote} schlägt {wahl_emote}", value=f"{self.bot.user.name} hat gewonnen", inline=False)
                embed.colour = 0xbd3e34
                self.cps_streak = 0



        def ergebnisse(wahl):
            embed.clear_fields()
            embed.add_field(name=f"{self.bot.user.name}:", value=f"{computer_emote}", inline=False)
            embed.add_field(name=f"{ctx.author.name}:", value=f"{wahl}\n\u200b", inline=False)
            embed.add_field(name="Winning streak", value=str(self.cps_streak), inline=True)
            embed.add_field(name="Dein Highscore", value=str(db.get_highscore()), inline=True)
            embed.set_author(name="Nochmal spielen: 🔁")


        async def timeout():
            embed.clear_fields()
            embed.add_field(name=f"Spiel vorbei du Sack", value=f"Wenn du nochmal so lange brauchst komm ich persönlich vorbei", inline=False)
            await message.edit(embed=embed)
            await message.clear_reactions()


        embed = discord.Embed(title="\u200b\nCock, Petra, Sophia?\n\u200b", colour=0x8764B8)
        # embed.set_author(name="Cock, Petra, Sophia?\n\u200b")
        embed.set_thumbnail(url=config.CPS_LOGO_URL)
        embed.add_field(name="🍆 Cock", value="schlägt Petra.", inline=False)
        embed.add_field(name="🤰 Petra", value="schlägt Sophia.", inline=False)
        embed.add_field(name="💕 Sophia", value="schlägt Cock.", inline=False)

        
        if self.cps_streak > 0:
            embed.add_field(name="Winning streak", value=str(self.cps_streak), inline=True)
            embed.add_field(name="Dein Highscore", value=str(db.get_highscore()), inline=True)

        message = await ctx.send(embed=embed)
        await message.add_reaction("🍆")
        await message.add_reaction("🤰")
        await message.add_reaction("💕")


        check = lambda r, u: u == ctx.author and str(r.emoji) in "🍆🤰💕"  # r=reaction, u=user


        try:
            reaction, user = await self.bot.wait_for("reaction_add", check=check, timeout=20)
        except asyncio.TimeoutError:
            await timeout()
            return

        computer = random.randint(1,3)
        if computer == 1:
            computer_emote = "🍆 Cock"
        elif computer == 2:
            computer_emote = "💕 Sophia"
        else:
            computer_emote = "🤰 Petra"

        if str(reaction.emoji) == "🍆":
            ergebnisse("🍆 Cock")
            gewinner(1, computer, "🍆 Cock")
            await message.edit(embed=embed)
            await message.add_reaction("🔁")


        elif str(reaction.emoji) == "🤰":
            ergebnisse("🤰 Petra")
            gewinner(3, computer, "🤰 Petra")
            await message.edit(embed=embed)
            await message.add_reaction("🔁")


        elif str(reaction.emoji) == "💕":
            ergebnisse("💕 Sophia")
            gewinner(2, computer, "💕 Sophia")
            await message.edit(embed=embed)
            await message.add_reaction("🔁")

        check = lambda r, u: u == ctx.author and str(r.emoji) in "🔁"  # r=reaction, u=user

        try:
            reaction, user = await self.bot.wait_for("reaction_add", check=check, timeout=20)
        except asyncio.TimeoutError:
            embed.remove_author()
            await message.edit(embed=embed)
            await message.clear_reaction("🔁")
            return

        if str(reaction.emoji) == "🔁":
            await ctx.invoke(self.bot.get_command("cps"))

    
def setup(bot):
    bot.add_cog(Minigames(bot))