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
