import logging
from asyncpraw.exceptions import InvalidURL
from aiogram import types
from aiogram.utils.exceptions import MessageIsTooLong
from functools import partial

# from aiogram.dispatcher import FSMContext

from misc import reddit
from controllers.reddit import get_post_by_url, Post_Types

MAX_LENGTH = 4000


async def raw_idle(message: types.Message):
    try:
        post = await get_post_by_url(reddit, message.text)
    except InvalidURL as err:
        logging.warning(err)

    if post.type == Post_Types.TEXT:
        try:
            await message.answer(f"<b>{post.title}</b>\n{post.text}",
                                 parse_mode='html')
        except MessageIsTooLong:
            # FIXME: divide text stirng
            await message.answer(f"<b>{post.title}</b>", parse_mode='html')
            for text_chunk in iter(partial(post.text, MAX_LENGTH), ''):
                await message.answer(text_chunk)
        # if post.type == Post_Types.PIC:
        #     await message.answer_photo(post.url, caption=post.title)
        # if post.type == Post_Types.VID:
        #     await message.answer_video(post.url, caption=post.title)
        # if post.type == Post_Types.GIF:
        #     await message.answer_animation(post.url, caption=post.title)
        # if post.type == Post_Types.LINK:
        #     await message.answer(f"[{post.title}]({post.url})",
        #                          parse_mode='MarkdownV2')


# def raw_command_show(message: types.Message, state: FSMContext):
#     pass

# def raw_sub(message: types.Message, state: FSMContext):
#     # input subreddit
#     # validate subreddit
#     # if valid save
#     # set next state
#     pass

# def raw_sortby(message: types.Message, state: FSMContext):
#     # TODO: show custom keyboard
#     # if valid save
#     # set next state
#     pass

# def raw_quantity(message: types.Message, state: FSMContext):
#     # TODO: show custom keyboard
#     # input number of posts to show
#     # validate
#     # if valid save
#     # set next state
#     pass
