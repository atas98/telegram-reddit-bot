import re
import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from misc import reddit
from .type_handlers import type_handlers


async def raw_idle(message: types.Message, state: FSMContext):
    try:
        urls = re.findall("(https?://[^\s]+)", message.text)
        for url in urls:
            post = await reddit.get_post_by_url(url)
            await type_handlers[post.type](message, post, state)
    except ValueError as err:
        logging.warning(err)
        return
