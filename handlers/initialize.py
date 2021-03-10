from aiogram import Dispatcher, types
from .other_commands import command_start, command_help, command_report
from .show_command import command_show
from .raw_idle import raw_idle


def initialize_handlers(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=["start"])
    dp.register_message_handler(command_help, commands=["help"])
    dp.register_message_handler(command_report, commands=["report"])
    dp.register_message_handler(command_show, commands=["show"])
    dp.register_message_handler(raw_idle, content_types=["text"])


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
