import asyncio
from utils.load_config import CONFIG
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
from controllers.reddit import Reddit
from handlers import register_bot_commands

loop = asyncio.get_event_loop()
WEBHOOK_URL = f"https://{CONFIG.webhook.HOST}:{CONFIG.webhook.PORT}{CONFIG.webhook.URL_PATH}"

# Initialize bot and dispatcher
reddit = Reddit(CONFIG.reddit.client_id, CONFIG.reddit.client_secret,
                CONFIG.reddit.user_agent)
bot = Bot(token=CONFIG.telegramToken,
          parse_mode="HTML",
          validate_token=True,
          loop=loop)
dp = Dispatcher(bot,
                storage=RedisStorage2(host=CONFIG.redis.HOST,
                                      port=CONFIG.redis.PORT,
                                      db=CONFIG.redis.DB,
                                      password=CONFIG.redis.PASSWORD))


async def on_startup():
    await register_bot_commands()

    # Get current webhook status
    webhook = await bot.get_webhook_info()

    # If URL is bad
    if webhook.url != WEBHOOK_URL:
        # If URL doesnt match current - remove webhook
        if not webhook.url:
            await bot.delete_webhook()

        # Set new URL for webhook
        await bot.set_webhook(WEBHOOK_URL,
                              certificate=open(CONFIG.ssl.CERT, 'rb'))


async def on_shutdown():
    """
    Graceful shutdown. This method is recommended by aiohttp docs.
    """
    # Remove webhook.
    await bot.delete_webhook()

    # Close Redis connection.
    await dp.storage.close()
    await dp.storage.wait_closed()
