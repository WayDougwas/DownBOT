import os
import discord
from discord.ext import commands
from colorama import init, Fore
from scripts.logger import logger
# Inicializa o colorama para permitir o uso de cores no console
init(autoreset=True)

intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)  # Prefixo será definido no evento on_ready

@bot.event
async def on_ready():
    logger.info(f"{Fore.GREEN}Logged in as {bot.user}{Fore.RESET}")

# Carrega os comandos
bot.load_extension("scripts.commands")

bot.run(os.environ["DISCORD_TOKEN"])
