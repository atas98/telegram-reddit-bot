import logging
from typing import List

from aiogram.dispatcher import FSMContext
from config.load_config import CONFIG


async def get_favorites(state: FSMContext, fill=True) -> List[str]:
    default = CONFIG.botconfig.default_favorites

    favorites = await state.get_data()
    favorites = favorites.get('favorites', [])
    try:
        if fill:
            return default[:len(default) - len(favorites)] + favorites
        else:
            return favorites
    except Exception as err:
        logging.error(err)
        return default
