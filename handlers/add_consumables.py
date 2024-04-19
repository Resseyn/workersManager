from aiogram.types import CallbackQuery, InputMediaPhoto, Message

from keyboard.start_keyboard import worker_keyboard, adm_keyboard, back_button_k, accounts_types

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import json
import os

class AdminAccountInput(StatesGroup):
    waiting_for_user_input = State()



async def add_account(callback: CallbackQuery,  state: FSMContext) -> None:
    await callback.message.answer("Добавить аккаунты для...",
                                  reply_markup=accounts_types)
    await state.set_state(AdminAccountInput.waiting_for_user_input)

async def await_adding_account(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(f"Введите аккаунты для {callback.data} в формате CSV в виде login:pass:email/number:auth_token:proxy,login:pass:email/number:auth_token:proxy и т.д.\nhttps://convertio.co/ru/txt-csv/ может помочь",
                                  reply_markup=back_button_k)
    await state.set_state(AdminAccountInput.waiting_for_user_input)
    await state.update_data(account_type=callback.data)


async def add_account_by_type(message: Message, state: FSMContext):
    state_data = await state.get_data()
    account_type = state_data.get('account_type')

    user_input = message.text
    user_input = user_input.split(',')

    file_path = f'data/{account_type}.json'
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

