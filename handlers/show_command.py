import asyncstdlib
from aiogram import types
from aiogram.dispatcher import FSMContext
from controllers.reddit import Sort_Types
from .type_handlers import type_handlers
from misc import reddit
from typing import Union
from utils import ChatStates
from utils.keyboards import subreddit_kb, sortby_kb, quantity_kb
from utils.messages import all_strings, get_language


def validate_subreddit(subreddit: str) -> Union[str, None]:
    # Max subreddit name length is 21char, and min is 2
    MIN_LENGTH = 1
    MAX_LENGTH = 21
    if subreddit[:2] == 'r/':
        subreddit = subreddit[2:]
    if MIN_LENGTH > len(subreddit) > MAX_LENGTH:
        return None
    else:
        return subreddit


def validate_sortby(sortby: str) -> Union[Sort_Types, None]:
    try:
        return Sort_Types.get(sortby.upper())
    except KeyError:
        return None


def validate_quantity(quantity: str) -> Union[int, None]:
    MIN_QUANTITY = 1  # TODO: Move to config
    MAX_QUANTITY = 10
    if not quantity.isnumeric():
        return quantity
    quantity = int(quantity)
    if MIN_QUANTITY > quantity > MAX_QUANTITY:
        return None
    else:
        return quantity


async def command_show(message: types.Message, state: FSMContext):
    args = message.get_args().split()
    if not args:
        await ChatStates.INP_SUBREDDIT.set()
        await message.answer(all_strings.get(
            get_language(
                message.from_user.language_code)).get("input_inv_subreddit"),
                             reply_markup=await subreddit_kb(state),
                             disable_notification=True)
        return  # Start input session Sub -> Sortby -> Quantity
    if len(args) != 3:
        await message.answer(all_strings.get(
            get_language(
                message.from_user.language_code)).get("error_wrong_args"),
                             disable_notification=True)
        return

    subreddit, sort_by, quantity = args
    subreddit = validate_subreddit(subreddit)
    sort_by = validate_sortby(sort_by)
    quantity = validate_quantity(quantity)

    if not subreddit or not sort_by or not quantity:
        await message.answer(all_strings.get(
            get_language(
                message.from_user.language_code)).get("error_wrong_args"),
                             disable_notification=True)
        return

    # Cache viewed quantity for show_more_btn
    await state.update_data(stoped_at=quantity)

    async for i, post in asyncstdlib.enumerate(
            reddit.get_posts_from_subreddit(subreddit, sort_by, quantity)):
        islast = i + 1 == quantity
        await type_handlers[post.type](message, post, islast=islast)


async def _update_favorites(state: FSMContext, subreddit: str):
    default = ["memes", "games", "aww", "pics", "gifs", "worldnews"]
    favorites = await state.get_data()
    try:
        favorites = favorites['favorites']
    except KeyError:
        favorites = []
    if len(favorites) < 6\
       and subreddit not in favorites\
       and subreddit not in default:
        favorites.append(subreddit)
    await state.update_data(favorites=favorites)


async def subreddit_input(message: types.Message, state: FSMContext):
    subreddit = validate_subreddit(message.text)
    # TODO: Check if sub exists
    if not subreddit:
        await message.answer(all_strings.get(
            get_language(
                message.from_user.language_code)).get("error_wrong_input"),
                             disable_notification=True)
        return
    await state.update_data(subreddit=subreddit)
    await _update_favorites(state, subreddit)

    await ChatStates.next()
    await message.answer(all_strings.get(
        get_language(message.from_user.language_code)).get("input_inv_sortby"),
                         reply_markup=sortby_kb(),
                         disable_notification=True)


async def sortby_input(message: types.Message, state: FSMContext):
    sortby = validate_sortby(message.text)
    if not sortby:
        await message.answer(all_strings.get(
            get_language(
                message.from_user.language_code)).get("error_wrong_input"),
                             disable_notification=True)
        return
    await state.update_data(sortby=sortby)
    await ChatStates.next()
    await message.answer(all_strings.get(
        get_language(
            message.from_user.language_code)).get("input_inv_quantity"),
                         reply_markup=quantity_kb(),
                         disable_notification=True)


async def quantity_input(message: types.Message, state: FSMContext):
    input_quantity = validate_quantity(message.text)
    if not input_quantity:
        await message.answer(all_strings.get(
            get_language(
                message.from_user.language_code)).get("error_wrong_input"),
                             disable_notification=True)
        return

    # Retrive data from state
    input_data = await state.get_data()
    input_subreddit = input_data['subreddit']
    input_sortby = input_data['sortby']

    # Return posts
    async for post in reddit.get_posts_from_subreddit(input_subreddit,
                                                      input_sortby,
                                                      input_quantity):
        await type_handlers[post.type](message, post)

    await state.reset_state(with_data=False)
