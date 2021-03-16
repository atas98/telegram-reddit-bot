import logging
from aiogram import types
from misc import reddit
from .type_handlers import type_handlers


async def raw_idle(message: types.Message):
    try:
        post = await reddit.get_post_by_url(message.text)
    except ValueError as err:
        logging.warning(err)
        return
    await type_handlers[post.type](message, post)
