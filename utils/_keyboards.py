from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton,
                           ReplyKeyboardRemove)
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


def post_inline_kb(post_url: str,
                   show_more_btn: bool = False) -> InlineKeyboardMarkup:
    inline_btn_url = InlineKeyboardButton('Open on reddit', url=post_url)
    if not show_more_btn:
        return InlineKeyboardMarkup(row_width=1)\
            .add(inline_btn_url)
    else:
        inline_btn_showmore = InlineKeyboardButton(
            'Show more', callback_data="show_more_callback")
        return InlineKeyboardMarkup(row_width=1)\
            .add(inline_btn_url)\
            .add(inline_btn_showmore)


def quantity_kb() -> ReplyKeyboardMarkup:
    btn_1 = KeyboardButton('1')
    btn_3 = KeyboardButton('3')
    btn_5 = KeyboardButton('5')
    btn_10 = KeyboardButton('10')
    return ReplyKeyboardMarkup(resize_keyboard=True,
                               one_time_keyboard=True)\
        .row(btn_1, btn_3)\
        .row(btn_5, btn_10)


# TODO: move to utils and change code in delsub to this
async def _get_favorites(state: FSMContext, fill=True) -> List[str]:
    default = ["memes", "games", "aww", "pics", "gifs",
               "worldnews"]  # TODO: move to config

    favorites = await state.get_data()
    favorites = favorites.get('favorites', [])
    try:
        if fill:
            return default[:len(default) - len(favorites)] + favorites
        else:
            return favorites
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


def settings_kb() -> ReplyKeyboardMarkup:
    btn_1 = KeyboardButton("Language")
    btn_2 = KeyboardButton("Delete subreddit")
    return ReplyKeyboardMarkup(resize_keyboard=True,
                               one_time_keyboard=True)\
        .add(btn_1).add(btn_2)


def settings_lang_kb() -> ReplyKeyboardMarkup:
    btn_1 = KeyboardButton('en')
    btn_2 = KeyboardButton('ru')
    return ReplyKeyboardMarkup(resize_keyboard=True,
                               one_time_keyboard=True)\
        .add(btn_1).add(btn_2)


async def settings_del_sub_kb(state: FSMContext) -> ReplyKeyboardMarkup:
    favorites = await _get_favorites(state, fill=False)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    for favorite in favorites:
        keyboard.add(KeyboardButton(favorite))
    return keyboard