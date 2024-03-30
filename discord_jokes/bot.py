import re
from discord import Intents, Message
from discord.ext import commands
from .jokes import NoJoke, random_joke
import logging

logger = logging.getLogger(__name__)

IM_DAD_PATTERN = re.compile(r"^(im|i'm|i am)(( [^ ]+){1,2})$", re.IGNORECASE)
TELL_ME_A_JOKE_PATTERN = re.compile(r"^tell me a joke (about ? (.+))$", re.IGNORECASE)

intents = Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)


@bot.event
async def on_ready():
    logger.info(f"{bot.user} has connected to Discord!")


@bot.command(name="joke", help="Responds with a random Dad Joke")
async def tell_joke(ctx: commands.Context, *about: str):
    if ctx.author == bot.user:
        return

    try:
        joke = random_joke()
        message = joke["joke"]
    except NoJoke:
        message = "Sorry, I couldn't find a joke in the dadabase!"

    await ctx.send(message)


async def im_dad(message: Message, match: re.Match):
    await message.channel.send(f"Hi {match.group(2).strip().title()}, I'm Dad!")


async def find_joke(message: Message, match: re.Match):
    if match.group(3):
        joke = random_joke(match.group(3))
    else:
        joke = random_joke()

    await message.channel.send(joke["joke"])


@bot.event
async def on_message(message: Message):
    if message.author == bot.user:
        return

    m = IM_DAD_PATTERN.match(message.content)
    if m:
        await message.channel.send(f"Hi {m.group(2).strip().title()}, I'm Dad!")
    else:
        await bot.process_commands(message)
