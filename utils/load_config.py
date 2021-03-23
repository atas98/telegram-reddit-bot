import json
from pathlib import Path
from dataclasses import dataclass


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
class Webapp:
    HOST: str
    PORT: int


@dataclass
class SSL:
    CERT: str
    PRIV: int


@dataclass
class Webhook:
    HOST: str
    PORT: int
    URL_PATH: str


@dataclass
class Settings:
    telegramToken: str
    reddit: RedditCredits
    mongo: Mongo
    redis: Redis
    webapp: Webapp
    ssl: SSL
    webhook: Webhook


def load_config(path: Path) -> Settings:
    global CONFIG
    config = json.load(open(path, 'r'))
    CONFIG = Settings(telegramToken=config["telegramToken"],
                      reddit=RedditCredits(**config["reddit"]),
                      mongo=Mongo(**config["mongo"]),
                      redis=Redis(**config["redis"]),
                      webapp=Webapp(**config["webapp"]),
                      ssl=SSL(**config["ssl"]),
                      webhook=Webhook(**config["webhook"]))
    return CONFIG
