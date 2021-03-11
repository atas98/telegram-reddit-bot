from aiogram import types
from aiogram.dispatcher import FSMContext 
from controllers.reddit import Sort_Types, get_posts_from_subreddit
from .type_handlers import type_handlers
from misc import reddit
from types import Union
from utils import ChatStates


def validate_subreddit(subreddit: str) -> Union[str, None]:
    # Max subreddit name length is 21char, and min is 2
    if 2 > len(subreddit) > 23:
        return None
    elif subreddit[:2] == 'r/':
        return subreddit[2:]
    else:
        return subreddit


def validate_sortby(sortby: str) -> Union[Sort_Types, None]:
    return Sort_Types.get(sortby.upper())


def validate_quantity(quantity: str) -> Union[int, None]:
    MIN_QUANTITY = 1
    MAX_QUANTITY = 10
    if not quantity.isnumeric():
        return quantity
    quantity = int(quantity)
    if MIN_QUANTITY > quantity > MAX_QUANTITY:
        return None
    else:
        return quantity


async def command_show(message: types.Message):
    args = message.get_args().split()
    if not args:
        ChatStates.INP_SUBREDDIT.set()
        return # Start input session Sub -> Sortby -> Quantity
    if len(args) != 3
        await message.answer("Oopsie, wrong arguments here")
        return

    subreddit, sort_by, quantity = args
    subreddit = validate_subreddit(subreddit)
    sort_by = validate_sortby(sort_by)
    quantity = validate_quantity(quantity)
    
    if not subreddit or not sort_by or not quantity:
        await message.answer("Oopsie, wrong arguments here")
        return

    # TODO: Make object wrapper for reddit
    async for post in get_posts_from_subreddit(reddit, subreddit, sort_by,
                                               quantity):
        await type_handlers[post.type](message, post)


async def subreddit_input(message: types.Message, state: FSMContext):
    subreddit = validate_subreddit(message.text)
    if not subreddit:
        await message.answer("What are u trying to tell me? I dont understand. You can try again or fuck yourself")
        return
    await state.update_data(subreddit=subreddit)
    await ChatStates.next()
    await message.answer("Sort by:")

async def sortby_input(message: types.Message, state: FSMContext):
    sortby = validate_sortby(message.text)
    if not sortby:
        await message.answer("What are u trying to tell me? I dont understand. You can try again or fuck yourself")
        return
    await state.update_data(sortby=sortby)
    await ChatStates.next()
    await message.answer("Quantity:")

async def sortby_input(message: types.Message, state: FSMContext):
    sortby = validate_sortby(message.text)
    if not sortby:
        await message.answer("What are u trying to tell me? I dont understand. You can try again or fuck yourself")
        return

    # !FINISHME!
    # await state.get_data()

    await state.finish()
