import logging
import coloredlogs
from pathlib import Path
from config import load_config

if __name__ == '__main__':
    # Configure logging
    coloredlogs.install(level=logging.INFO)

    # Initialize and check config
    try:
        load_config(Path.joinpath(Path(__file__).parent, "config/config.json"))
    except ValueError as ex:
        exit(f"Error: {ex}")

    # Now load everything else
    from aiogram import executor
    from misc import dp, on_startup, on_shutdown
    from config.load_config import CONFIG

    if CONFIG.use_webhook:
        executor.start_webhook(dispatcher=dp,
                            webhook_path=CONFIG.webhook.PATH,
                            on_startup=on_startup,
                            on_shutdown=on_shutdown,
                            skip_updates=True,
                            host=CONFIG.webserver.HOST,
                            port=CONFIG.webserver.PORT)
    else:
        executor.start_polling(dispatcher=dp,
                            on_startup=on_startup,
                            on_shutdown=on_shutdown,
                            skip_updates=True)
