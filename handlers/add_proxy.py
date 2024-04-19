import json

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto, Message

from configs import admins
from keyboard.start_keyboard import worker_keyboard, adm_keyboard, back_button_k
from loader import dp

from aiogram import types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import json
import os
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class AdminProxyInput(StatesGroup):
    waiting_for_user_input = State()



async def add_proxy(callback: CallbackQuery,  state: FSMContext) -> None:
    await callback.message.answer("Добавьте прокси в формате CSV в виде ip:port:login:password,ip:port:login:password и т.д.\nhttps://convertio.co/ru/rtf-csv/ может помочь",
                                  reply_markup=back_button_k)
    await state.set_state(AdminProxyInput.waiting_for_user_input)

async def add_user_proxy(message: Message, state: FSMContext):
    user_input = message.text
    user_input = user_input.split(',')

    file_path = 'data/proxies.json'
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, 'r') as f:
            existing_data = json.load(f)
            existing_data = set(existing_data)
    else:
        existing_data = set()

    existing_data.update(user_input)
    existing_data = list(existing_data)

    with open(file_path, 'w') as f:
        json.dump(existing_data, f)

    await message.answer(f"Данные сохранены")
    await message.answer("Привет, администратор!", reply_markup=adm_keyboard)
    await state.clear()