import logging

# Configuração básica do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_channel_created(channel_name):
    logger.info(f"Canal criado: {channel_name}")

def log_channel_cleanup(channel_name):
    logger.info(f"Canal limpado e removido: {channel_name}")
