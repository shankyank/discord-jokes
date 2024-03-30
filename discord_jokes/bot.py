import logging
import re

from discord import Intents, Message
from discord.ext import commands

from .jokes import NoJoke, random_joke

logger = logging.getLogger(__name__)

IM_DAD_PATTERN = re.compile(r"^(im|i'm|i am)(( [^ ]+){1,2})$", re.IGNORECASE)

intents = Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)


@bot.event
async def on_ready():
    logger.info(f"{bot.user} has connected to Discord!")


@bot.command(name="joke", help="Responds with a random Dad Joke")
async def tell_joke(ctx: commands.Context):
    if ctx.author == bot.user:
        return

    try:
        joke = random_joke()
        message = joke["joke"]
    except NoJoke:
        message = "Sorry, I couldn't find a joke in the dadabase!"

    await ctx.send(message)


@bot.event
async def on_message(message: Message):
    if message.author == bot.user:
        return

    m = IM_DAD_PATTERN.match(message.content)
    if m:
        await message.channel.send(f"Hi {m.group(2).strip().title()}, I'm Dad!")
    else:
        await bot.process_commands(message)
