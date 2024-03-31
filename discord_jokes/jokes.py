import logging
import re
from typing import Optional, TypedDict

import requests

logger = logging.getLogger(__name__)

USER_AGENT = "Dad Jokes Bot (https://github.com/shankyank/discord-jokes)"
JOKE_API = "https://icanhazdadjoke.com"

JokeResponse = TypedDict(
    "Joke",
    {
        "id": str,
        "joke": str,
    },
)


class Joke:
    def __init__(self, response: JokeResponse):
        self.id = response["id"]
        self.joke = response["joke"]
        if "?" in self.joke:
            setup, punchline = self.joke.split("?", 1)
            self.setup: Optional[str] = f"{setup}?"
            self.punchline = re.sub(r"\.$", "!", punchline.strip())
        else:
            self.setup = None
            self.punchline = self.joke


def random_joke() -> Joke:
    try:
        headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
        response = requests.get(JOKE_API, headers=headers, timeout=5)
        response.raise_for_status()
        return Joke(response.json())
    except Exception as err:
        logger.error(f"Error fetching joke: {err}")
        raise NoJoke() from err


class NoJoke(Exception):
    pass
