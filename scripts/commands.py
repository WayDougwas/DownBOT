from pathlib import Path
from discord.ext import commands

def setup(bot):
    # Carrega todos os comandos na pasta Commands
    for cog_file in Path("scripts/Commands").glob("*.py"):
        if cog_file.stem != "__init__":
            cog_name = f"scripts.Commands.{cog_file.stem}"
            bot.load_extension(cog_name)

    # Adicione outras configurações ou carregamentos de extensões aqui, se necessário
