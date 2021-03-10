from aiogram import Dispatcher, types
from .commands import command_start, command_help
from .raw_idle import raw_idle


def initialize_handlers(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=["start"])
    dp.register_message_handler(command_help, commands=["help"])
    dp.register_message_handler(raw_idle, content_types=["text"])


async def register_bot_commands(dp: Dispatcher):
    initialize_handlers(dp)
    commands = [
        # types.BotCommand(command="show",
        # description="custom password, configured in /settings"),
        types.BotCommand(command="help", description="help and source code")
    ]
    await dp.bot.set_my_commands(commands)
