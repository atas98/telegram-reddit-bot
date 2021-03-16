from aiogram import types
from aiogram.utils.exceptions import (MessageIsTooLong, WrongFileIdentifier,
                                      InvalidHTTPUrlContent)
from utils.keyboards import post_data_kb
from typing import Generator
from controllers.reddit import Post_Data, Post_Types, Reddit

MAX_TELEGRAM_MESSAGE_LENGTH = 4000


def _text_chunks(text: str, chunk_size: int) -> Generator[str, None, None]:
    # notTODO: mind words, split by spaces. Fuck that
    # Smth like, split by the most right space
    # if its not beyond certain ratio of textP
    for i in range(0, len(text), chunk_size):
        yield text[i:i + chunk_size]


async def text_post_handler(message: types.Message, post: Post_Data):
    try:
        await message.answer(f"<b>{post.title}</b>\n{post.text}",
                             parse_mode="html",
                             reply_markup=post_data_kb(post.post_link),
                             disable_notification=True)
    except MessageIsTooLong:
        await message.answer(f"<b>{post.title}</b>",
                             parse_mode="html",
                             disable_notification=True)
        for text_chunk in _text_chunks(post.text, MAX_TELEGRAM_MESSAGE_LENGTH):
            await message.answer(text_chunk, disable_notification=True)


async def picture_post_handler(message: types.Message, post: Post_Data):
    # TODO: capture FileIsTooFBig exception
    await message.answer_photo(post.url,
                               caption=post.title,
                               reply_markup=post_data_kb(post.post_link),
                               disable_notification=True)


async def video_post_handler(message: types.Message, post: Post_Data):
    # TODO: parse post.media
    try:
        await message.answer_video(post.url,
                                   caption=post.title,
                                   reply_markup=post_data_kb(post.post_link),
                                   disable_notification=True)
    except InvalidHTTPUrlContent:
        await message.answer(
            "Thats not a video, you liar!.. At least I think so 😕 .\
            Here's your link anyways:",
            disable_notification=True)
        await link_post_handler(message, post)
    except WrongFileIdentifier:
        await message.answer("Step Dad, what are u doing!? Its too big!! 🤯 ",
                             disable_notification=True)
        await link_post_handler(message, post)


async def album_post_handler(message: types.Message, post: Post_Data):
    album = []
    for i, url in enumerate(Reddit.photos_from_album(post)):
        if i == 0:
            album.append(types.InputMediaPhoto(url, caption=post.title))
        else:
            album.append(types.InputMediaPhoto(url))
    await message.answer_media_group(album,
                                     reply_markup=post_data_kb(post.post_link),
                                     disable_notification=True)


async def gif_post_handler(message: types.Message, post: Post_Data):
    try:
        await message.answer_animation(post.url,
                                       caption=post.title,
                                       reply_markup=post_data_kb(
                                           post.post_link),
                                       disable_notification=True)
    except WrongFileIdentifier:
        # TODO: Add to all_strigs w/ localization
        await message.answer("Step Dad, what are u doing!? Its too big!! 🤯 ",
                             disable_notification=True)
        await link_post_handler(message, post)


async def link_post_handler(message: types.Message, post: Post_Data):
    await message.answer(f"{post.title}\n{post.url}",
                         reply_markup=post_data_kb(post.post_link),
                         disable_notification=True)


async def unknown_post_handler(message: types.Message, post: Post_Data):
    await message.answer("Hey, thats illegal! (post type) 👮 ",
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
