from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from controllers.reddit import Reddit
from utils.load_config import CONFIG

# Initialize bot and dispatcher
reddit = Reddit(CONFIG.reddit.client_id, CONFIG.reddit.client_secret,
                CONFIG.reddit.user_agent)
bot = Bot(token=CONFIG.telegramToken, parse_mode="HTML", validate_token=True)
dp = Dispatcher(bot,
                storage=RedisStorage2(host=CONFIG.redis.HOST,
                                      port=CONFIG.redis.PORT,
                                      db=CONFIG.redis.DB,
                                      password=CONFIG.redis.PASSWORD))


async def on_startup(dp):
    from handlers import register_bot_commands
    WEBHOOK_URL = f"{CONFIG.webhook.HOST}{CONFIG.webhook.PATH}"
    await bot.set_webhook(WEBHOOK_URL)
    await register_bot_commands(dp)


async def on_shutdown(dp):
    """
    Graceful shutdown. This method is recommended by aiohttp docs.
    """
    # Remove webhook.
    await bot.delete_webhook()

    # Close Redis connection.
    await dp.storage.close()
    await dp.storage.wait_closed()