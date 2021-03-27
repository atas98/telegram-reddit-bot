from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.dispatcher import FSMContext
from typing import List
import logging


def sortby_kb() -> ReplyKeyboardMarkup:
    btn_hot = KeyboardButton('hot')
    btn_top = KeyboardButton('top')
    btn_new = KeyboardButton('new')
    btn_rising = KeyboardButton('rising')
    btn_random = KeyboardButton('random')
    return ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)\
        .row(btn_hot, btn_top)\
        .row(btn_new, btn_rising)\
        .row(btn_random)


def post_url_kb(post_url: str) -> InlineKeyboardMarkup:
    inline_btn_url = InlineKeyboardButton('Open on reddit', url=post_url)
    return InlineKeyboardMarkup(row_width=1)\
        .add(inline_btn_url)


def quantity_kb() -> ReplyKeyboardMarkup:
    btn_1 = KeyboardButton('1')
    btn_3 = KeyboardButton('3')
    btn_5 = KeyboardButton('5')
    btn_10 = KeyboardButton('10')
    return ReplyKeyboardMarkup(resize_keyboard=True,
                               one_time_keyboard=True)\
        .row(btn_1, btn_3)\
        .row(btn_5, btn_10)


async def _get_favorites(state: FSMContext) -> List[str]:
    default = ["memes", "games", "aww", "pics", "gifs",
               "worldnews"]  # TODO: move to config
    try:
        favorites = await state.get_data()
        favorites = favorites['favorites']
    except KeyError:
        return default
    else:
        try:
            return default[:len(default) - len(favorites)] + favorites
        except Exception as err:
            logging.error(err)
            return default


async def subreddit_kb(state: FSMContext) -> ReplyKeyboardMarkup:
    favorites = await _get_favorites(state)

    btn_1 = KeyboardButton(favorites[0])
    btn_2 = KeyboardButton(favorites[1])
    btn_3 = KeyboardButton(favorites[2])
    btn_4 = KeyboardButton(favorites[3])
    btn_5 = KeyboardButton(favorites[4])
    btn_6 = KeyboardButton(favorites[5])
    return ReplyKeyboardMarkup(resize_keyboard=True,
                               one_time_keyboard=True)\
        .row(btn_1, btn_2)\
        .row(btn_3, btn_4)\
        .row(btn_5, btn_6)
