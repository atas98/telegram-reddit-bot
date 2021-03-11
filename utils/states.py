from aiogram.dispatcher.filters.state import State, StatesGroup


class ChatStates(StatesGroup):
    INP_SUBREDDIT = State()
    INP_SORTBY = State()
    INP_QUANTITY = State()