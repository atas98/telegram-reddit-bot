from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.dispatcher import FSMContext


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


def post_data_kb(post_url: str) -> InlineKeyboardMarkup:
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


def subreddit_kb() -> ReplyKeyboardMarkup:
    return None
    # query to db about users last subs
    # if answer is None: return None
    # else return kb with last sub choices
