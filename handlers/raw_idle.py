import logging
from aiogram import types
from misc import reddit
from controllers.reddit import get_post_by_url
from .type_handlers import type_handlers

MAX_TELEGRAM_MESSAGE_LENGTH = 4000


async def raw_idle(message: types.Message):
    try:
        post = await get_post_by_url(reddit, message.text)
    except ValueError as err:
        logging.warning(err)
        return
    await type_handlers[post.type](message, post)
