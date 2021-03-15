from aiogram import Dispatcher, types
from aiogram.types import ContentTypes

from .other_commands import (command_start, command_help, command_report,
                             command_cancel)
from .show_command import (command_show, subreddit_input, sortby_input,
                           quantity_input)
from .raw_idle import raw_idle
from .inline_handlers import comments_bnt_callback
from .stickers import sticker_handler
from utils.states import ChatStates


def initialize_handlers(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=["start"])
    dp.register_message_handler(command_help, commands=["help"])
    dp.register_message_handler(command_cancel, commands=["cancel"])
    dp.register_message_handler(command_report, commands=["report"])
    dp.register_message_handler(command_show, commands=["show"])

    dp.register_message_handler(subreddit_input, state=ChatStates.INP_SUBREDDIT)
    dp.register_message_handler(sortby_input, state=ChatStates.INP_SORTBY)
    dp.register_message_handler(quantity_input, state=ChatStates.INP_QUANTITY)

    dp.register_message_handler(raw_idle,
                                content_types=ContentTypes.TEXT,
                                state="*")

    dp.register_message_handler(sticker_handler,
                                content_types=ContentTypes.STICKER)

    # dp.register_callback_query_handler(
    #     comments_bnt_callback,
    #     lambda c: c.data and c.data.startswith('post_comments:'))


async def register_bot_commands(dp: Dispatcher):
    initialize_handlers(dp)
    commands = [
        types.BotCommand(command="help", description="help and source code"),
        types.BotCommand(command="report", description="report bug"),
        types.BotCommand(command="cancel", description="to reset input"),
        types.BotCommand(
            command="show",
            description="get a bunch of posts from specified subreddit")
    ]
    await dp.bot.set_my_commands(commands)
