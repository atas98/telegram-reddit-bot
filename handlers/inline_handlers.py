import logging
import asyncstdlib
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.message import ParseMode
from .type_handlers import type_handlers
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


async def show_more_btn_callback(callback_query: types.CallbackQuery,
                                 state: FSMContext):
    # Retrive data from state
    # Retrieve last index from cache
    inputted_data = await state.get_data()
    subreddit = inputted_data['subreddit']
    sort_by = inputted_data['sortby']
    quantity = inputted_data['quantity']
    stoped_at = inputted_data['stoped_at']

    # Cache viewed quantity for show_more_btn
    await state.update_data(stoped_at=(stoped_at + quantity))

    async for i, post in asyncstdlib.enumerate(
            reddit.get_posts_from_subreddit(subreddit,
                                            sort_by,
                                            stoped_at + quantity,
                                            skip=stoped_at)):
        islast = (i == quantity - 1)
        logging.warning(f"{i}:{stoped_at + quantity-2}")
        await type_handlers[post.type](callback_query.message,
                                       post,
                                       state,
                                       islast=islast)
    await bot.answer_callback_query(callback_query.id)
