# from controllers.reddit.reddit import Post_Data
from aiogram import types
from controllers.reddit import Sort_Types, get_posts_from_subreddit
from .type_handlers import type_handlers
from misc import reddit


async def command_show(message: types.Message):
    # FIXME: Its ugly :\
    args = message.get_args().split()
    if not args:
        return
    try:
        subreddit, sort_by, quantity = args
        sort_by = sort_by.upper()
    except AttributeError:
        await message.answer("Oopsie, wrong arguments here")
        return
    if not quantity.isnumeric():
        await message.answer("Oopsie, wrong arguments here")
        return
    else:
        quantity = int(quantity)
    if sort_by not in Sort_Types.__members__.keys():
        await message.answer("Oopsie, wrong arguments here")
        return
    else:
        sort_by = Sort_Types.__members__[sort_by]

    async for post in get_posts_from_subreddit(reddit, subreddit, sort_by,
                                               quantity):
        await type_handlers[post.type](message, post)
