from bot import CONFIG
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2

# Initialize bot and dispatcher
bot = Bot(token=CONFIG.telegramConfig, parse_mode="HTML", validate_token=True)
dp = Dispatcher(bot, storage=RedisStorage2(host="redis"))