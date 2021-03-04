from aiogram import types
from aiogram.types import message
from messages import messages
from reddit import get_post

async def start_handler(event: types.Message):
    await event.answer(messages['start_message'])
    
async def help_handler(event: types.Message):
    await event.answer(messages['help_message'])
    
async def text_handler(event: types.Message):
    try:
        post = await get_post(event.text)
        await event.answer(post)
    except Exception as err:
        print(err)
        await event.answer("Something went wrong...")
    