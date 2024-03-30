import logging
from typing import TypedDict

import requests

logger = logging.getLogger(__name__)

USER_AGENT = "Dad Jokes Bot (https://github.com/shankyank/discord-jokes)"
JOKE_API = "https://icanhazdadjoke.com"

Joke = TypedDict(
    "Joke",
    {
        "id": str,
        "joke": str,
    },
)


def random_joke() -> Joke:
    try:
        headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
        response = requests.get(JOKE_API, headers=headers, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as err:
        logger.error(f"Error fetching joke: {err}")
        raise NoJoke() from err


class NoJoke(Exception):
    pass
