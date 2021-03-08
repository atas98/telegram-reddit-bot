import json
from pathlib import Path
from dataclasses import dataclass


@dataclass
class RedditCredits:
    client_id: str
    user_agent: str
    client_secret: str


@dataclass
class Settings:
    telegramToken: str
    reddit: RedditCredits


def load_config(path: Path) -> Settings:
    config = json.load(open(path, 'r'))
    global CONFIG
    CONFIG = Settings(telegramToken=config["telegramToken"],
                      reddit=RedditCredits(**config["reddit"]))
    return CONFIG
