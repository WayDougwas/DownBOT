import discord
from discord.ext import commands
import requests

class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def minecraft(self, ctx, servidor):
        # Obter informações do servidor Minecraft da API
        minecraft_info, is_online = await self.minecraft_server_info(servidor)

        if minecraft_info is None:
            await ctx.send("Erro ao obter informações do servidor de Minecraft.")
            return

        # Determinar a cor do Embed com base no status do servidor
        embed_color = discord.Color.green() if is_online else discord.Color.red()

        # Criar embed com as informações
        embed = discord.Embed(title="Minecraft Server Stats", color=embed_color)
        embed.add_field(name="Server Info", value=minecraft_info, inline=False)

        await ctx.send(embed=embed)

    async def minecraft_server_info(self, servidor):
        try:
            api_url = f"https://api.mcsrvstat.us/3/{servidor}"
            response = requests.get(api_url)

            if response.status_code == 200:
                data = response.json()
                if data.get("online"):
                    players = data.get("players", {})
                    max_players = players.get("max", "N/A")
                    online_players = players.get("online", "N/A")
                    return f"Players Online: {online_players}/{max_players}", True
                else:
                    return "Server Offline", False
            else:
                return None, False
        except Exception as e:
            print(f"Erro ao obter informações do servidor de Minecraft: {e}")
            return None, False

def setup(bot):
    bot.add_cog(Minecraft(bot))
