from aiogram import Dispatcher, types
from aiogram.types import ContentTypes

from .other_commands import (command_start, command_help, command_report,
                             command_cancel)
from .show_command import (command_show, subreddit_input, sortby_input,
                           quantity_input)
from .settings_command import (command_settings, settings_choose,
                               settings_del_sub, settings_lang)
from .inline_handlers import show_more_btn_callback
from .raw_idle import raw_idle
from .stickers import sticker_handler
from models import UserStates


def initialize_handlers(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=["start"])
    dp.register_message_handler(command_help, commands=["help"])
    dp.register_message_handler(command_cancel, commands=["cancel"], state="*")
    dp.register_message_handler(command_report, commands=["report"])
    dp.register_message_handler(command_show, commands=["show"])
    dp.register_message_handler(command_settings, commands=["settings"])

    dp.register_message_handler(settings_choose, state=UserStates.INP_SETTINGS)
    dp.register_message_handler(settings_lang,
                                state=UserStates.INP_SETTINGS_LANG)
    dp.register_message_handler(settings_del_sub,
                                state=UserStates.INP_SETTINGS_DELSUB)

    dp.register_message_handler(subreddit_input, state=UserStates.INP_SUBREDDIT)
    dp.register_message_handler(sortby_input, state=UserStates.INP_SORTBY)
    dp.register_message_handler(quantity_input, state=UserStates.INP_QUANTITY)

    dp.register_message_handler(raw_idle,
                                content_types=ContentTypes.TEXT,
                                state="*")

    dp.register_message_handler(sticker_handler,
                                content_types=ContentTypes.STICKER)

    dp.register_callback_query_handler(show_more_btn_callback,
                                       lambda q: q.data == "show_more_callback",
                                       state="*")


async def register_bot_commands(dp: Dispatcher):
    initialize_handlers(dp)
    commands = [
        types.BotCommand(
            command="show",
            description="get a bunch of posts from specified subreddit"),
        types.BotCommand(command="report", description="report bug"),
        types.BotCommand(command="settings", description="manage bot settings"),
        types.BotCommand(command="cancel", description="to reset input"),
        types.BotCommand(command="help", description="help and source code")
    ]
    await dp.bot.set_my_commands(commands)
