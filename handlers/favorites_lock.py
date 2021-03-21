# from misc import db
from aiogram import types
from aiogram.dispatcher import FSMContext


def command_lock(message: types.Message, state: FSMContext):
    # Parse sub name from message.text
    # Push value to db
    # If not value: set state lock_input
    pass


def command_unlock(message: types.Message, state: FSMContext):
    # Parse sub name from message.text
    # Push value to db
    # If not value: set state lock_input
    pass


def command_show_locked(message: types.Message, state: FSMContext):
    # Query to db for unlocked favorites -> answer
    pass
