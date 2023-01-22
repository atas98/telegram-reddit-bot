import json
import os
from pathlib import Path

from models.config import (RedditCredits, Redis, Settings, Webhook, Webserver,
                           BotConfig, DataBorders)


def load_config(path: Path) -> Settings:
    global CONFIG
    config = json.load(open(path, 'r'))
    CONFIG = Settings(
        use_webhook=config.get('use_webhook', True),
        telegramToken=os.environ.get('TG_TOKEN') or config['telegramToken'],
        reddit=RedditCredits(
            client_id=os.environ.get('REDDIT_CLIENT_ID') or config['reddit'].get('client_id'),
            client_secret=os.environ.get('REDDIT_CLIENT_SECRET')
                or config['reddit'].get('client_secret'),
            user_agent=config['reddit'].get('user_agent'),
        ),
        redis=Redis(
            URL=os.environ.get('REDIS_URL') or config['redis'].get('URL'),
            HOST=os.environ.get('REDIS_HOST') or config['redis'].get('HOST'),
            PORT=os.environ.get('REDIS_PORT') or config['redis'].get('PORT'),
            PASSWORD=(os.environ.get('REDIS_PASSWORD') or config['redis'].get('PASSWORD'))
                     if not os.environ.get('REDIS_WO_PASSWORD') else None,
            DB=os.environ.get('REDIS_DB') or config['redis'].get('DB'),
        ),
        webhook=Webhook(
            HOST=os.environ.get('WEBHOOK_HOST') or config['webhook'].get('HOST'),
            PORT=os.environ.get('WEBHOOK_PORT') or config['webhook'].get('PORT'),
            PATH=os.environ.get('WEBHOOK_PATH') or config['webhook'].get('PATH'),
        ),
        webserver=Webserver(
            HOST=os.environ.get('WEBSERVER_HOST') or config['webserver'].get('HOST'),
            PORT=os.environ.get('WEBSERVER_PORT') or config['webserver'].get('PORT'),
        ),
        botconfig=BotConfig(
            langs=tuple(config['botconfig']['langs']),
            default_favorites=config['botconfig']['default_favorites'],
            subreddit_length=DataBorders(
                **config['botconfig']['subreddit_length']),
            quantity=DataBorders(**config['botconfig']['quantity'])))

    return CONFIG
