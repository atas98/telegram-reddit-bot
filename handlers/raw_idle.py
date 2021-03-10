import logging
from asyncpraw.exceptions import InvalidURL
from aiogram import types
from aiogram.utils.exceptions import MessageIsTooLong
from functools import partial
from typing import Generator

# from aiogram.dispatcher import FSMContext

from misc import reddit
from controllers.reddit import get_post_by_url, photos_from_album, Post_Types

MAX_LENGTH = 4000


def text_chunks(text: str, chunk_size: int) -> Generator[str, None, None]:
    # TODO: mind words, split by spaces
    for i in range(0, len(text), chunk_size):
        yield text[i:i + chunk_size]


async def raw_idle(message: types.Message):
    try:
        post = await get_post_by_url(reddit, message.text)
    except InvalidURL as err:
        logging.warning(err)
        return

    if post.type == Post_Types.TEXT:
        try:
            await message.answer(f"**{post.title}**")
        except MessageIsTooLong:
            await message.answer(f"**{post.title}**")
            for text_chunk in text_chunks(post.text, MAX_LENGTH):
                await message.answer(text_chunk)
    elif post.type == Post_Types.PIC:
        await message.answer_photo(post.url, caption=post.title)
    elif post.type == Post_Types.ALB:  # FUCK
        album = types.MediaGroup()
        for i, url in enumerate(photos_from_album(post)):
            if i == 0:
                album.attach_photo(url, caption=post.title)
            else:
                album.attach_photo(url)
        await message.answer_media_group(album)
    elif post.type == Post_Types.VID:  # FUCK
        await message.answer_video(post.url, caption=post.title)
    elif post.type == Post_Types.GIF:  # FUCK
        await message.answer_animation(post.url, caption=post.title)
    elif post.type == Post_Types.LINK:
        await message.answer(f"{post.title}\n{post.url}")
    else:
        await message.answer("Hey, thats illegal! (post type)")


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
