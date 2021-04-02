from typing import Union

import asyncstdlib
from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards import quantity_kb, sortby_kb, subreddit_kb
from misc import reddit
from models.reddit import Sort_Types
from utils import UserStates, get_favorites
from utils.messages import all_strings, get_language
from config.load_config import CONFIG

from .type_handlers import type_handlers


def validate_subreddit(subreddit: str) -> Union[str, None]:
    # Max subreddit name length is 21 char, and min is 2
    if subreddit[:2] == 'r/':
        subreddit = subreddit[2:]
    if CONFIG.botconfig.subreddit_length.MIN > len(
            subreddit) > CONFIG.botconfig.subreddit_length.MAX\
                and reddit.sub_exists(subreddit):
        return None
    else:
        return subreddit


def validate_sortby(sortby: str) -> Union[Sort_Types, None]:
    try:
        return Sort_Types.get(sortby.upper())
    except KeyError:
        return None


def validate_quantity(quantity: str) -> Union[int, None]:
    if not quantity.isnumeric():
        return quantity
    quantity = int(quantity)
    if CONFIG.botconfig.quantity.MIN > quantity > CONFIG.botconfig.quantity.MAX:
        return None
    else:
        return quantity


# FIXME: subreddit vertification dosnt work
async def command_show(message: types.Message, state: FSMContext):
    args = message.get_args().split()
    if not args:
        await UserStates.INP_SUBREDDIT.set()
        await message.answer(all_strings.get(await get_language(
            message.from_user.language_code, state)).get("input_inv_subreddit"),
                             reply_markup=await subreddit_kb(state),
                             disable_notification=True)
        return  # Start input session Sub -> Sortby -> Quantity
    if len(args) != 3:
        await message.answer(all_strings.get(await get_language(
            message.from_user.language_code, state)).get("error_wrong_args"),
                             disable_notification=True)
        return

    subreddit, sort_by, quantity = args
    subreddit = validate_subreddit(subreddit)
    sort_by = validate_sortby(sort_by)
    quantity = validate_quantity(quantity)

    if not subreddit or not sort_by or not quantity:
        await message.answer(all_strings.get(await get_language(
            message.from_user.language_code, state)).get("error_wrong_args"),
                             disable_notification=True)
        return

    # Cache inputed data for show_more_btn
    await state.update_data(subreddit=subreddit,
                            sortby=sort_by,
                            quantity=quantity,
                            stoped_at=quantity)

    async for i, post in asyncstdlib.enumerate(
            reddit.get_posts_from_subreddit(subreddit, sort_by, quantity)):
        islast = i + 1 == quantity
        await type_handlers[post.type](message, post, state, islast=islast)


async def _update_favorites(state: FSMContext, subreddit: str):
    default = CONFIG.botconfig.default_favorites
    favorites = await get_favorites(state, fill=False)

    if len(favorites) < 6\
       and subreddit not in favorites\
       and subreddit not in default:
        favorites.append(subreddit)
    await state.update_data(favorites=favorites)


async def subreddit_input(message: types.Message, state: FSMContext):
    subreddit = validate_subreddit(message.text)
    # TODO: Check if sub exists
    if not subreddit:
        await message.answer(all_strings.get(await get_language(
            message.from_user.language_code, state)).get("error_wrong_input"),
                             disable_notification=True)
        return
    await state.update_data(subreddit=subreddit)
    await _update_favorites(state, subreddit)

    await UserStates.next()
    await message.answer(all_strings.get(await get_language(
        message.from_user.language_code, state)).get("input_inv_sortby"),
                         reply_markup=sortby_kb(),
                         disable_notification=True)


async def sortby_input(message: types.Message, state: FSMContext):
    sortby = validate_sortby(message.text)
    if not sortby:
        await message.answer(all_strings.get(await get_language(
            message.from_user.language_code, state)).get("error_wrong_input"),
                             disable_notification=True)
        return
    await state.update_data(sortby=sortby)
    await UserStates.next()
    await message.answer(all_strings.get(await get_language(
        message.from_user.language_code, state)).get("input_inv_quantity"),
                         reply_markup=quantity_kb(),
                         disable_notification=True)


async def quantity_input(message: types.Message, state: FSMContext):
    input_quantity = validate_quantity(message.text)
    if not input_quantity:
        await message.answer(all_strings.get(await get_language(
            message.from_user.language_code, state)).get("error_wrong_input"),
                             disable_notification=True)
        return

    # Cache inputed data for show_more_btn
    await state.update_data(quantity=input_quantity, stoped_at=input_quantity)

    # Retrive data from state
    input_data = await state.get_data()
    input_subreddit = input_data['subreddit']
    input_sortby = input_data['sortby']

    # Return posts
    async for i, post in asyncstdlib.enumerate(
        reddit.get_posts_from_subreddit(input_subreddit, input_sortby,
                                        input_quantity)):
        islast = i + 1 == input_quantity
        await type_handlers[post.type](message, post, state, islast=islast)

    await state.reset_state(with_data=False)
