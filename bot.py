import os
import ssl
import logging
from aiohttp import web
from pathlib import Path
from utils import load_config
from aiogram.dispatcher.webhook import get_new_configured_app
from aiogram.utils.executor import start_polling  # start_webhook

if __name__ == '__main__':
    # Configure logging
    if os.path.exists("./logs"):
        os.remove("./logsP`")
    logging.basicConfig(level=logging.DEBUG, filename='logs')

    # Initialize and check config
    try:
        load_config(Path.joinpath(Path(__file__).parent, "config/config.json"))
    except ValueError as ex:
        exit(f"Error: {ex}")

    # Now load everything else
    from aiogram import executor
    from utils.load_config import CONFIG
    from misc import dp  # , on_startup, on_shutdown  #, loop
    from handlers import register_bot_commands

    # Get instance of :class:`aiohttp.web.Application` with configured router.
    # app = get_new_configured_app(dispatcher=dp, path=CONFIG.webhook.URL_PATH)

    # Setup event handlers.
    # app.on_startup.append(on_startup)
    # app.on_shutdown.append(on_shutdown)

    # Generate SSL context
    # # TODO: generate selfsigned sertificates
    # context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    # context.load_cert_chain(CONFIG.ssl.CERT, CONFIG.ssl.PRIV)

    # start_webhook(
    #     dispatcher=dp,
    #     webhook_path=CONFIG.webhook.URL_PATH,
    #     on_startup=on_startup,
    #     on_shutdown=on_shutdown,
    #     skip_updates=True,
    #     host=CONFIG.webapp.HOST,
    #     port=CONFIG.webapp.PORT,
    # )

    # Start web-application.
    # web.run_app(app,
    #             host=CONFIG.webapp.HOST,
    #             port=CONFIG.webapp.PORT,
    #             ssl_context=context)

    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=register_bot_commands)
