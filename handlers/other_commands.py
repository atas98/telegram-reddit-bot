import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from utils import get_language, all_strings


async def command_start(message: types.Message, state: FSMContext):
    # TODO: if logged in show keyboard
    await state.finish()
    await message.answer(all_strings.get(
        get_language(message.from_user.language_code)).get("start"),
                         disable_notification=True)


async def command_help(message: types.Message):
    await message.answer(all_strings.get(
        get_language(message.from_user.language_code)).get("help"),
                         disable_notification=True)


async def command_report(message: types.Message):
    logging.info(f"Report:{message.from_user.username}:{message.get_args()}")


async def command_cancel(message: types.Message, state: FSMContext):
    await state.reset_state(with_data=False)