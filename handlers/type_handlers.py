import logging
from math import ceil
from typing import Generator, Tuple

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import (InvalidHTTPUrlContent, MessageIsTooLong,
                                      WrongFileIdentifier)
from controllers.reddit import Reddit
from keyboards import post_inline_kb
from models.reddit import Post_Data, Post_Types
from utils.messages import all_strings, get_language

MAX_TELEGRAM_MESSAGE_LENGTH = 4000


def _text_chunks(text: str,
                 chunk_size: int) -> Generator[Tuple[str, bool], None, None]:
    chunks = ceil(len(text) / chunk_size)
    for i in range(0, len(text), chunk_size):
        yield (text[i:i + chunk_size], i + 1 == chunks)


async def text_post_handler(message: types.Message,
                            post: Post_Data,
                            state: FSMContext,
                            islast: bool = False):
    try:
        await message.answer(f"<b>{post.title}</b>\n{post.text}",
                             parse_mode="html",
                             reply_markup=post_inline_kb(post.post_link,
                                                         show_more_btn=islast),
                             disable_notification=True)
    except MessageIsTooLong:
        await message.answer(f"<b>{post.title}</b>",
                             parse_mode="html",
                             disable_notification=True)
        for text_chunk, end in _text_chunks(post.text,
                                            MAX_TELEGRAM_MESSAGE_LENGTH):
            if not end:
                await message.answer(text_chunk, disable_notification=True)
            else:
                await message.answer(text_chunk,
                                     reply_markup=post_inline_kb(
                                         post.post_link, show_more_btn=islast),
                                     disable_notification=True)


async def picture_post_handler(message: types.Message,
                               post: Post_Data,
                               state: FSMContext,
                               islast: bool = False):
    try:
        await message.answer_photo(post.url,
                                   caption=post.title,
                                   reply_markup=post_inline_kb(
                                       post.post_link, show_more_btn=islast),
                                   disable_notification=True)
    except WrongFileIdentifier as err:
        logging.error(err)
        await link_post_handler(message, post, state, islast=islast)


async def video_post_handler(message: types.Message,
                             post: Post_Data,
                             state: FSMContext,
                             islast: bool = False):
    try:
        await message.answer_video(post.media['reddit_video']['fallback_url'],
                                   caption=post.title,
                                   reply_markup=post_inline_kb(
                                       post.post_link, show_more_btn=islast),
                                   disable_notification=True)
    except InvalidHTTPUrlContent:
        await message.answer(all_strings.get(await get_language(
            message.from_user.language_code, state)).get("error_video"),
                             disable_notification=True)
        await link_post_handler(message, state, post, islast=islast)
    except WrongFileIdentifier:
        await message.answer(all_strings.get(await get_language(
            message.from_user.language_code, state)).get("error_file_2_big"),
                             disable_notification=True)
        await link_post_handler(message, post, state, islast=islast)


async def album_post_handler(message: types.Message,
                             post: Post_Data,
                             state: FSMContext,
                             islast: bool = False):
    album = []
    for url in Reddit.photos_from_album(post):
        album.append(types.InputMediaPhoto(url))
    await message.answer_media_group(album, disable_notification=True)
    await message.answer(post.title,
                         reply_markup=post_inline_kb(post.post_link,
                                                     show_more_btn=islast),
                         disable_notification=True)


async def gif_post_handler(message: types.Message,
                           post: Post_Data,
                           state: FSMContext,
                           islast: bool = False):
    try:
        await message.answer_animation(
            post.url,
            caption=post.title,
            reply_markup=post_inline_kb(post.post_link, show_more_btn=islast),
            disable_notification=True)
    except WrongFileIdentifier:
        await message.answer(all_strings.get(await get_language(
            message.from_user.language_code, state)).get("error_file_2_big"),
                             disable_notification=True)
        await link_post_handler(message, post, state, islast=islast)


async def link_post_handler(message: types.Message,
                            post: Post_Data,
                            state: FSMContext,
                            islast: bool = False):
    await message.answer(f"{post.title}\n{post.url}",
                         reply_markup=post_inline_kb(post.post_link,
                                                     show_more_btn=islast),
                         disable_notification=True)


async def unknown_post_handler(message: types.Message,
                               state: FSMContext,
                               post: Post_Data,
                               islast=False):
    await message.answer(all_strings.get(await get_language(
        message.from_user.language_code, state)).get("error_wrong_post_type"),
                         disable_notification=True)


type_handlers = {
    Post_Types.TEXT: text_post_handler,
    Post_Types.PIC: picture_post_handler,
    Post_Types.VID: video_post_handler,
    Post_Types.ALB: album_post_handler,
    Post_Types.GIF: gif_post_handler,
    Post_Types.LINK: link_post_handler,
    Post_Types.UNKNOWN: unknown_post_handler
}
