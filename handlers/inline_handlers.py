from aiogram import types
from aiogram.types.message import ParseMode
from misc import reddit, bot


async def comments_bnt_callback(callback_query: types.CallbackQuery):
    post_id = callback_query.data[-6:]
    post = await reddit.submission(id=post_id)
    post_comments = await post.comments()

    for i in range(5):
        comment = post_comments[i]
        if not comment:
            break
        await bot.send_message(callback_query.from_user.id,
                               f'{comment.author.name}: {comment.body}',
                               parse_mode=ParseMode.MARKDOWN)
    await bot.answer_callback_query(callback_query.id)
    await bot.answer_callback_query(callback_query.id)
