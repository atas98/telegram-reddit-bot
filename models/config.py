from dataclasses import dataclass
from typing import Tuple, List


@dataclass
class RedditCredits:
    client_id: str
    user_agent: str
    client_secret: str


@dataclass
class Redis:
    URL: str
    HOST: str
    PORT: int
    DB: int
    PASSWORD: str


@dataclass
class Webhook:
    HOST: str
    PORT: int
    PATH: str


@dataclass
class Webserver:
    HOST: str
    PORT: str


@dataclass
class DataBorders:
    MIN: int
    MAX: int


@dataclass
class BotConfig:
    langs: Tuple[str]
    default_favorites: List[str]
    subreddit_length: DataBorders
    quantity: DataBorders


@dataclass
class Settings:
    use_webhook: bool
    telegramToken: str
    reddit: RedditCredits
    redis: Redis
    webhook: Webhook
    webserver: Webserver
    botconfig: BotConfig
