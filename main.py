import os
import discord
import asyncio
import schedule
import time
import subprocess
from discord.ext import commands
from colorama import init, Fore
from scripts.logger import log_info, log_error
from scripts.database import get_prefix

# Inicializa o colorama para permitir o uso de cores no console
init(autoreset=True)

intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix=get_prefix, intents=intents)  # Prefixo será definido dinamicamente

@bot.event
async def on_ready():
    log_info(f"Logged in as {bot.user}")

    # Agende o job para ser executado a cada 5 minutos, mas não o execute imediatamente
    schedule.every(5).minutes.do(job)

    # Executar o loop assíncrono para os comandos
    while True:
        await asyncio.sleep(1)
        schedule.run_pending()

# Carrega os comandos
bot.load_extension("scripts.commands")

def refresh_terminal():
    try:
        log_info("All systems online captain!")
    except Exception as e:
        log_error(f"Erro ao atualizar o terminal: {e}")

def job():
    refresh_terminal()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(bot.start(os.environ["DISCORD_TOKEN"]))
    loop.run_forever()
