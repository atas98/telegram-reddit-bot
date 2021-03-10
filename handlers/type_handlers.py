from controllers.reddit.reddit import Post_Data
from aiogram import types
from aiogram.utils.exceptions import MessageIsTooLong, WrongFileIdentifier
from typing import Generator
from controllers.reddit import photos_from_album, Post_Types


def _text_chunks(text: str, chunk_size: int) -> Generator[str, None, None]:
    # TODO: mind words, split by spaces
    for i in range(0, len(text), chunk_size):
        yield text[i:i + chunk_size]


async def text_post_handler(message: types.Message, post: Post_Data):
    try:
        await message.answer(f"**{post.title}**")
    except MessageIsTooLong:
        await message.answer(f"**{post.title}**")
        for text_chunk in _text_chunks(post.text, MAX_TELEGRAM_MESSAGE_LENGTH):
            await message.answer(text_chunk)


async def picture_post_handler(message: types.Message, post: Post_Data):
    # TODO: capture FileIsTooFBig exception
    await message.answer_photo(post.url, caption=post.title)


async def video_post_handler(message: types.Message, post: Post_Data):
    # FIXME: parse post.media
    try:
        await message.answer_video(post.url, caption=post.title)
    except WrongFileIdentifier:
        await message.answer("Step Dad, what are u doing!? Its too big!! 🤯 ")
        await link_post_handler(message, post)


async def album_post_handler(message: types.Message, post: Post_Data):
    album = types.MediaGroup()
    for i, url in enumerate(photos_from_album(post)):
        if i == 0:
            album.attach_photo(url, caption=post.title)
        else:
            album.attach_photo(url)
    # FIXME: Separate messages!
    await message.answer_media_group(album)


async def gif_post_handler(message: types.Message, post: Post_Data):
    try:
        await message.answer_animation(post.url, caption=post.title)
    except WrongFileIdentifier:
        # TODO: Add to all_strigs w/ localization
        await message.answer("Step Dad, what are u doing!? Its too big!! 🤯 ")
        await link_post_handler(message, post)


async def link_post_handler(message: types.Message, post: Post_Data):
    await message.answer(f"{post.title}\n{post.url}")


async def unknown_post_handler(message: types.Message, post: Post_Data):
    # TODO: Add to all_strigs w/ localization
    await message.answer("Hey, thats illegal! (post type) 👮 ")


type_handlers = {
    Post_Types.TEXT: text_post_handler,
    Post_Types.PIC: picture_post_handler,
    Post_Types.VID: video_post_handler,
    Post_Types.ALB: album_post_handler,
    Post_Types.GIF: gif_post_handler,
    Post_Types.LINK: link_post_handler,
    Post_Types.UNKNOWN: unknown_post_handler
}
