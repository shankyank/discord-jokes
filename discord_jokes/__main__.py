import logging
import os

from discord.utils import setup_logging
from dotenv import load_dotenv

from .bot import bot

setup_logging(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

if "DISCORD_TOKEN" not in os.environ:
    logger.critical("DISCORD_TOKEN not set")
    raise ValueError("DISCORD_TOKEN not set")

TOKEN = os.environ["DISCORD_TOKEN"]
bot.run(TOKEN)
