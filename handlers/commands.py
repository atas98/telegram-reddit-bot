from aiogram import types
from misc import dp
from utils import get_language, all_strings

@dp.message_handler(commands=["show"])
async def command_start(message: types.Message):
    # TODO: if logged in show keyboard
    await message.answer(all_strings.get(get_language(message.from_user.language_code)).get("start"))


@dp.message_handler(commands=["show"])
async def command_help(message: types.Message):
    await message.answer(all_strings.get(get_language(message.from_user.language_code)).get("help"))
  
   
# @dp.message_handler(commands=["show"])
# async def command_help(message: types.Message):
#   change user state to sub 


# @dp.message_handler(commands=["reset"])
# async def command_help(message: types.Message):
#   reset user state to idle 