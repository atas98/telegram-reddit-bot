from utils import load_config
from pathlib import Path
import logging
import os

if __name__ == '__main__':
    # Configure logging
    if os.path.exists("./dump.log"):
        os.remove("./dump.log")
    logging.basicConfig(level=logging.DEBUG, filename='dump.log')

    # Initialize and check config
    try:
        load_config(Path.joinpath(Path(__file__).parent, "config/config.json"))
    except ValueError as ex:
        exit(f"Error: {ex}")

    # Now load everything else
    from aiogram import executor
    from misc import dp
    from handlers import register_bot_commands

    # TODO: Switch polling to webhooks
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=register_bot_commands)
