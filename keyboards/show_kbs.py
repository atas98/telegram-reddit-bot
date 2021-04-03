from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from utils import get_favorites


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


def quantity_kb() -> ReplyKeyboardMarkup:
    btn_1 = KeyboardButton('1')
    btn_3 = KeyboardButton('3')
    btn_5 = KeyboardButton('5')
    btn_10 = KeyboardButton('10')
    return ReplyKeyboardMarkup(resize_keyboard=True,
                               one_time_keyboard=True)\
        .row(btn_1, btn_3)\
        .row(btn_5, btn_10)


async def subreddit_kb(state: FSMContext) -> ReplyKeyboardMarkup:
    favorites = await get_favorites(state)

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
