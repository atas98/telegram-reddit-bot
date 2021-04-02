from aiogram import types
from aiogram.dispatcher import FSMContext
from utils import UserStates, get_favorites
from utils.messages import all_strings, get_language
from config.load_config import CONFIG
from keyboards import (settings_kb, settings_del_sub_kb, settings_lang_kb,
                       ReplyKeyboardRemove)


async def command_settings(message: types.Message, state: FSMContext):
    await UserStates.INP_SETTINGS.set()
    await message.answer(all_strings.get(await get_language(
        message.from_user.language_code, state)).get("settings"),
                         reply_markup=settings_kb(),
                         disable_notification=True)


async def settings_choose(message: types.Message, state: FSMContext):
    if message.text == '1' or message.text.lower() == 'language':
        await UserStates.INP_SETTINGS_LANG.set()
        await message.answer(all_strings.get(await get_language(
            message.from_user.language_code, state)).get("settings_lang"),
                             reply_markup=settings_lang_kb(),
                             disable_notification=True)
    elif message.text == 2 or message.text.lower() == 'delete subreddit':
        await UserStates.INP_SETTINGS_DELSUB.set()
        await message.answer(all_strings.get(await get_language(
            message.from_user.language_code, state)).get("settings_del_sub"),
                             reply_markup=await settings_del_sub_kb(state),
                             disable_notification=True)
    else:
        await state.reset_state(with_data=False)


async def settings_lang(message: types.Message, state: FSMContext):
    lang_code = message.text.lower()
    if lang_code in CONFIG.botconfig.langs:
        await state.update_data(lang_code=lang_code)
    else:
        await state.update_data(lang_code='')
    await message.answer("OK!", reply_markup=ReplyKeyboardRemove())
    await state.reset_state(with_data=False)


async def settings_del_sub(message: types.Message, state: FSMContext):
    subreddit = message.text.lower()
    favorites = await get_favorites(state, fill=False)
    if subreddit in favorites:
        favorites.remove(subreddit)
        await state.update_data(favorites=favorites)
    await message.answer("Deleted 👌", reply_markup=ReplyKeyboardRemove())
    await state.reset_state(with_data=False)
