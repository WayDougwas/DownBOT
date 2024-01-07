import discord
from discord.ext import commands

class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def stats(self, ctx):
        latency = round(self.bot.latency * 1000)  # Latência em milissegundos
        guild_count = len(self.bot.guilds)
        member_count = sum(guild.member_count for guild in self.bot.guilds)

        embed = discord.Embed(title="Bot Stats", color=discord.Color.blue())
        embed.add_field(name="Latency", value=f"{latency} ms")
        embed.add_field(name="Guilds", value=guild_count)
        embed.add_field(name="Members", value=member_count)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Stats(bot))
