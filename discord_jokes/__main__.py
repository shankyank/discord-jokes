import os
from dotenv import load_dotenv
from .bot import bot
import logging
from discord.utils import setup_logging

setup_logging(level=logging.INFO)

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
