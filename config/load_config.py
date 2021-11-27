import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple
from urllib.parse import urlparse

from models.config import (RedditCredits, Redis, Settings, Webhook, Webserver,
                           BotConfig, DataBorders)


def load_config(path: Path) -> Settings:
    global CONFIG
    config = json.load(open(path, 'r'))
    CONFIG = Settings(
        telegramToken=config["telegramToken"],
        reddit=RedditCredits(**config["reddit"]),
        redis=Redis(**config["redis"]),
        webhook=Webhook(**config["webhook"]),
        webserver=Webserver(**config["webserver"]),
        botconfig=BotConfig(
            langs=tuple(config["botconfig"]["langs"]),
            default_favorites=config["botconfig"]["default_favorites"],
            subreddit_length=DataBorders(
                **config["botconfig"]["subreddit_length"]),
            quantity=DataBorders(**config["botconfig"]["quantity"])))

    # Retieve port for heroku
    CONFIG.webserver.PORT = os.environ.get('PORT', CONFIG.webserver.PORT)

    # Retieve redist connection params for heroku's rediscloud
    url = os.environ.get('REDISCLOUD_URL')
    if url:
        url = urlparse(url)
        (CONFIG.redis.HOST, CONFIG.redis.PORT,
         CONFIG.redis.PASSWORD) = (url.hostname, url.port, url.password)
    return CONFIG
