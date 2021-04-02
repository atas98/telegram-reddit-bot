import json
import random
import logging
from pathlib import Path

from aiogram import types

_stickers = json.load(
    open(Path.joinpath(Path(__file__).parent.parent, "config/stickers.json"),
         'r'))['stickers']


async def sticker_handler(message: types.Message):
    logging.info([
        len(_stickers),
        Path.joinpath(Path(__file__).parent.parent, "config/stickers.json")
    ])
    await message.answer_sticker(random.choice(_stickers),
                                 disable_notification=True)
