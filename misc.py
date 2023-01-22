import redis

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from controllers.reddit import Reddit
from config.load_config import CONFIG

# Initialize bot and dispatcher
reddit = Reddit(CONFIG.reddit.client_id, CONFIG.reddit.client_secret,
                CONFIG.reddit.user_agent)
bot = Bot(token=CONFIG.telegramToken, parse_mode="HTML", validate_token=True)
if CONFIG.redis.URL:
    storage = RedisStorage2()
    storage._redis = redis.from_url(CONFIG.redis.URL)
else:
    storage = RedisStorage2(host=CONFIG.redis.HOST, port=CONFIG.redis.PORT,
                            db=CONFIG.redis.DB, password=CONFIG.redis.PASSWORD)
dp = Dispatcher(bot,
                storage=storage)


async def on_startup(dp, use_webhook: bool = False):
    from handlers import register_bot_commands

    if CONFIG.use_webhook:
        # Set webhook
        WEBHOOK_URL = f"{CONFIG.webhook.HOST}:{CONFIG.webhook.PORT}{CONFIG.webhook.PATH}"
        if not await bot.set_webhook(WEBHOOK_URL):
            exit("Failed to set webhook")
    await register_bot_commands(dp)


async def on_shutdown(dp):
    """
    Graceful shutdown. This method is recommended by aiohttp docs.
    """
    # Remove webhook.
    if CONFIG.use_webhook:
        await bot.delete_webhook()

    # Close Redis connection.
    await dp.storage.close()
    await dp.storage.wait_closed()
