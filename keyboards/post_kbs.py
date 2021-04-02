from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


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