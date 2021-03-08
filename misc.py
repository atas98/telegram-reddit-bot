# from bot import CONFIG
from utils.load_config import CONFIG
from aiogram import Bot, Dispatcher
# from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from asyncpraw import Reddit

# Initialize bot and dispatcher
reddit = Reddit(client_id=CONFIG.reddit.client_id,
                client_secret=CONFIG.reddit.client_secret,
                user_agent=CONFIG.reddit.user_agent)
bot = Bot(token=CONFIG.telegramToken, parse_mode="HTML", validate_token=True)
dp = Dispatcher(bot, storage=MemoryStorage())
