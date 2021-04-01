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
class Redis:
    HOST: str
    PORT: int
    DB: int
    PASSWORD: str


@dataclass
class Webhook:
    HOST: str
    PATH: str


@dataclass
class Webserver:
    HOST: str
    PORT: str


@dataclass
class Settings:
    telegramToken: str
    reddit: RedditCredits
    redis: Redis
    webhook: Webhook
    webserver: Webserver
    langs: Tuple[str]


def load_config(path: Path) -> Settings:
    global CONFIG
    config = json.load(open(path, 'r'))
    CONFIG = Settings(telegramToken=config["telegramToken"],
                      reddit=RedditCredits(**config["reddit"]),
                      redis=Redis(**config["redis"]),
                      webhook=Webhook(**config["webhook"]),
                      webserver=Webserver(**config["webserver"]),
                      langs=tuple(config["langs"]))
    # Retieve port for heroku
    CONFIG.webserver.PORT = os.environ.get('PORT', CONFIG.webserver.PORT)

    # Retieve redist connection params for heroku's rediscloud
    url = os.environ.get('REDISCLOUD_URL')
    if url:
        url = urlparse(url)
        (CONFIG.redis.HOST, CONFIG.redis.PORT,
         CONFIG.redis.PASSWORD) = (url.hostname, url.port, url.password)
    return CONFIG
