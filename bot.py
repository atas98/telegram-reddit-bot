import os
import ssl
import logging
from aiohttp import web
from pathlib import Path
from utils import load_config
from aiogram.dispatcher.webhook import get_new_configured_app

if __name__ == '__main__':
    # Configure logging
    if os.path.exists("./.log"):
        os.remove("./.log")
    logging.basicConfig(level=logging.DEBUG, filename='dump.log')

    # Initialize and check config
    try:
        load_config(Path.joinpath(Path(__file__).parent, "config/config.json"))
    except ValueError as ex:
        exit(f"Error: {ex}")

    # Now load everything else
    # from aiogram import executor
    from misc import dp, WEBHOOK_URL_PATH, on_startup, on_shutdown
    from utils.load_config import CONFIG

    # Get instance of :class:`aiohttp.web.Application` with configured router.
    app = get_new_configured_app(dispatcher=dp, path=WEBHOOK_URL_PATH)

    # Setup event handlers.
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    # Generate SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain(CONFIG.ssl.CERT, CONFIG.ssl.PRIV)

    # Start web-application.
    web.run_app(app,
                host=CONFIG.webapp.HOST,
                port=CONFIG.webapp.PORT,
                ssl_context=context)
