import logging
import re

from discord import Colour, Embed, Intents, Message
from discord.ext import commands, tasks

from .jokes import NoJoke, random_joke

logger = logging.getLogger(__name__)

IM_DAD_PATTERN = re.compile(r"^(im|i'm|i am)(( [^ ]+){1,4})$", re.IGNORECASE)
DAD_JOKE_IMAGE = (
    "https://raw.githubusercontent.com/shankyank/discord-jokes/bot/dadjokes.jpeg"
)

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
        title = None
        message = (
            f"{joke.setup}\n\n||{joke.punchline}||" if joke.setup else joke.punchline
        )
        color = Colour.blurple()
    except NoJoke:
        title = "Dad-abase Down!"
        message = "Sorry, I couldn't find a joke in the dadabase!"
        color = Colour.dark_red()

    embed = Embed(title=title, description=message, color=color)

    await ctx.send(embed=embed)


@bot.command(name="jokeoftheday", help="Set up a Joke of the Day post")
async def joke_of_the_day(ctx: commands.Context):
    await ctx.send("Setting up Joke of the Day...")

    JokeOfTheDay(ctx)
    await ctx.send("Joke of the Day set up!")


@bot.event
async def on_message(message: Message):
    if message.author == bot.user:
        return

    m = IM_DAD_PATTERN.match(message.content)
    if m:
        await message.channel.send(f"Hi {m.group(2).strip().title()}, I'm Dad!")
    else:
        await bot.process_commands(message)


class JokeOfTheDay(commands.Cog):
    def __init__(self, ctx: commands.Context):
        self.ctx = ctx
        self.send_joke.start()

    def cog_unload(self):
        self.send_joke.cancel()

    @tasks.loop(seconds=10)
    async def send_joke(self):
        await tell_joke(self.ctx)
