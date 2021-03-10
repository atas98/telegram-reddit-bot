import logging
from aiogram import types
from misc import dp
from utils import get_language, all_strings


async def command_start(message: types.Message):
    # TODO: if logged in show keyboard
    # TODO: reset state
    await message.answer(
        all_strings.get(get_language(
            message.from_user.language_code)).get("start"))


async def command_help(message: types.Message):
    await message.answer(
        all_strings.get(get_language(
            message.from_user.language_code)).get("help"))


async def command_report(message: types.Message):
    logging.info(f"Report:{message.from_user.username}:{message.get_args()}")
