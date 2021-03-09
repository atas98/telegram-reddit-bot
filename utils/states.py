from aiogram.utils.helper import Helper, HelperMode, ListItem


class TestStates(Helper):
    mode = HelperMode.snake_case

    IDLE = ListItem()
    WAIT_FOR_INPUT = ListItem()
    INP_SUBREDDIT = ListItem()
    INP_SORTBY = ListItem()
    INP_QUANTITY = ListItem()