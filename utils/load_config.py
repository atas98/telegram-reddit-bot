import os
import re
import json
from pathlib import Path
from urllib.parse import urlparse
from dataclasses import dataclass
from typing import Tuple


@dataclass
class RedditCredits:
    client_id: str
    user_agent: str
    client_secret: str


@dataclass
class Mongo:
    HOST: str
    PORT: int


@dataclass
class Redis:
    HOST: str
    PORT: int
    DB: int
    PASSWORD: str


@dataclass
class Settings:
    telegramToken: str
    reddit: RedditCredits
    mongo: Mongo
    redis: Redis


def load_config(path: Path) -> Settings:
    global CONFIG
    config = json.load(open(path, 'r'))
    CONFIG = Settings(telegramToken=config["telegramToken"],
                      reddit=RedditCredits(**config["reddit"]),
                      mongo=Mongo(**config["mongo"]),
                      redis=Redis(**config["redis"]))

    # Retieve redist connection params for heroku's rediscloud
    url = os.environ.get('REDISCLOUD_URL')
    if url:
        url = urlparse(url)
        (CONFIG.redis.HOST, CONFIG.redis.PORT,
         CONFIG.redis.PASSWORD) = (url.hostname, url.port, url.password)
    return CONFIG
