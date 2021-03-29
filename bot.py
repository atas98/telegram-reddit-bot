import logging
from pathlib import Path
from utils import load_config

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # Initialize and check config
    try:
        load_config(Path.joinpath(Path(__file__).parent, "config/config.json"))
    except ValueError as ex:
        exit(f"Error: {ex}")

    # Now load everything else
    from aiogram import executor
    from misc import dp
    from handlers import register_bot_commands

    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=register_bot_commands)
