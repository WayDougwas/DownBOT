import asyncio
import discord
from discord.ext import commands
from scripts.logger import log_channel_created, log_channel_cleanup

class CreateChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_cleanup_tasks = {}

    @commands.command()
    async def create_channel(self, ctx):
        author = ctx.message.author
        guild = ctx.guild

        try:
            # Verifica se já existe um canal com o mesmo nome
            existing_channel = discord.utils.get(guild.voice_channels, name=self.get_channel_name(author))

            if existing_channel:
                await ctx.send(f"Já existe um canal chamado {self.get_channel_name(author)}.")
            else:
                # Cria o canal de voz com o nome do autor
                new_channel = await guild.create_voice_channel(self.get_channel_name(author))
                await ctx.send(f"Canal de voz {self.get_channel_name(author)} criado com sucesso!")

                # Inicia o temporizador para limpar o canal após 1 minutos se estiver vazio
                self.start_channel_cleanup_timer(new_channel)
                log_channel_created(new_channel.name)  # Log do canal criado

        except discord.Forbidden:
            await ctx.send("O bot não tem permissão para criar canais de voz.")

    def start_channel_cleanup_timer(self, channel):
        # Inicia o temporizador para limpar o canal após 1 minutos se estiver vazio
        cleanup_task = asyncio.ensure_future(self.schedule_channel_cleanup(channel))
        self.channel_cleanup_tasks[channel.id] = cleanup_task

    async def schedule_channel_cleanup(self, channel):
        # Agende a verificação e a exclusão do canal após 1 minutos se estiver vazio
        await asyncio.sleep(1 * 60)  # 1 minutos em segundos
        if len(channel.members) == 0:
            await channel.delete()
            log_channel_cleanup(channel.name)  # Log do canal removido automaticamente

        # Remove a tarefa de limpeza associada a este canal
        del self.channel_cleanup_tasks[channel.id]

    def get_channel_name(self, author):
        return f"{author.name}'s Channel"

def setup(bot):
    bot.add_cog(CreateChannel(bot))
