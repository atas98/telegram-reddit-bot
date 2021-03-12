from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btn_hot = KeyboardButton('hot')
btn_top = KeyboardButton('top')
btn_new = KeyboardButton('new')
btn_rising = KeyboardButton('rising')
btn_random = KeyboardButton('random')
sortby_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)\
        .row(btn_hot, btn_top)\
        .row(btn_new, btn_rising)\
        .row(btn_random)
