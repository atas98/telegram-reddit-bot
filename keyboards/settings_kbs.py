from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from utils import get_favorites


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
    favorites = await get_favorites(state, fill=False)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    for favorite in favorites:
        keyboard.add(KeyboardButton(favorite))
    return keyboard
