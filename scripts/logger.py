import os
import logging
from discord_webhook import DiscordWebhook

# Configuração básica do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Obtém a URL do webhook a partir das variáveis de ambiente
webhook_url = os.environ.get("WEBHOOK_URL")

if webhook_url is None:
    raise ValueError("WEBHOOK_URL não encontrada no arquivo .env")

# Adiciona um manipulador de webhook ao logger
webhook_handler = logging.StreamHandler()  # Use StreamHandler para imprimir os logs no console
logger.addHandler(webhook_handler)

def send_to_webhook(message):
    webhook = DiscordWebhook(url=webhook_url, content=message)
    webhook.execute()

def log_info(message):
    logger.info(message)
    send_to_webhook(message)

def log_error(message):
    logger.error(message)
    send_to_webhook(message)

def log_channel_created(channel_name):
    message = f"Canal criado: {channel_name}"
    log_info(message)

def log_channel_cleanup(channel_name):
    message = f"Canal limpado e removido: {channel_name}"
    log_info(message)
