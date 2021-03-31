import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from utils.messages import get_language, all_strings


async def command_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(all_strings.get(await get_language(
        message.from_user.language_code, state)).get("start"),
                         disable_notification=True)


async def command_help(message: types.Message, state: FSMContext):
    await message.answer(all_strings.get(await get_language(
        message.from_user.language_code, state)).get("help"),
                         disable_notification=True)


async def command_report(message: types.Message):
    logging.info(f"Report:{message.from_user.username}:{message.get_args()}")


async def command_cancel(message: types.Message, state: FSMContext):
    await message.answer("❌ ", reply_markup=types.ReplyKeyboardRemove())
    await state.reset_state(with_data=False)
