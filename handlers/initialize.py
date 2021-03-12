from aiogram import Dispatcher, types
from .other_commands import command_start, command_help, command_report
from .show_command import (command_show, subreddit_input, sortby_input,
                           quantity_input)
from .raw_idle import raw_idle
from utils.states import ChatStates


def initialize_handlers(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=["start"])
    dp.register_message_handler(command_help, commands=["help"])
    dp.register_message_handler(command_report, commands=["report"])
    dp.register_message_handler(command_show, commands=["show"])
    dp.register_message_handler(subreddit_input, state=ChatStates.INP_SUBREDDIT)
    dp.register_message_handler(sortby_input, state=ChatStates.INP_SORTBY)
    dp.register_message_handler(quantity_input, state=ChatStates.INP_QUANTITY)
    dp.register_message_handler(raw_idle, content_types=["text"], state="*")


async def register_bot_commands(dp: Dispatcher):
    initialize_handlers(dp)
    commands = [
        types.BotCommand(command="help", description="help and source code"),
        types.BotCommand(command="report", description="report bug"),
        types.BotCommand(
            command="show",
            description="get a bunch of posts from specified subreddit")
    ]
    await dp.bot.set_my_commands(commands)
