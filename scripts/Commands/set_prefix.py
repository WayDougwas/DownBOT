from discord.ext import commands
from scripts.database import set_prefix

class SetPrefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def setprefix(self, ctx, new_prefix):
        guild = ctx.guild
        set_prefix(guild.id, new_prefix)
        await ctx.send(f"Prefixo do servidor atualizado para '{new_prefix}'.")

def setup(bot):
    bot.add_cog(SetPrefix(bot))
