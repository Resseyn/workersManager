import json

from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto, Message
from aiogram.utils.markdown import hbold

from configs import admins
from keyboard import start_keyboard
from keyboard.start_keyboard import adm_keyboard, worker_keyboard
from loader import dp

async def back_handler(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    with open('data/workers.json', 'r') as f:
        workers = json.load(f)
    if callback.from_user.id in admins:
        await callback.message.answer("Привет, администратор!", reply_markup=adm_keyboard)
    elif callback.from_user.id in workers:
        await callback.message.answer("Привет, воркер!", reply_markup=worker_keyboard)

