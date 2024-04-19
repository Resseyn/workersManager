import json
import re

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto, Message

from configs import admins
from keyboard.start_keyboard import worker_keyboard, adm_keyboard, back_button_k, approve_k, accounts_types, \
    get_accounts_types_k
from loader import dp

from aiogram import types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import json
import os
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import BufferedInputFile

class WorkerAccountInput(StatesGroup):
    waiting_for_user_input = State()



async def get_account(callback: CallbackQuery,  state: FSMContext) -> None:
    await callback.message.answer("Аккаунты для...",
                                  reply_markup=get_accounts_types_k)
    await state.set_state(WorkerAccountInput.waiting_for_user_input)


async def await_getting_account(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(f"Введите количество желаемых аккаунтов для {callback.data[4:]}",
                                  reply_markup=back_button_k)
    await state.set_state(WorkerAccountInput.waiting_for_user_input)
    await state.update_data(account_type=callback.data)

async def get_account_type(message: Message, state: FSMContext):
    state_data = await state.get_data()
    account_type = state_data.get('account_type')

    user_input = message.text
    if not re.match(r'^[0-9]+$', user_input):
        await message.answer("Неверный формат ввода. Попробуйте еще раз.", reply_markup=back_button_k)
        return
    if int(user_input) > 100:
        await message.answer("Слишком большое количество аккаунтов. Попробуйте еще раз.", reply_markup=back_button_k)
        return
    if int(user_input) <= 0:
        await message.answer("Слишком маленькое количество аккаунтов. Попробуйте еще раз.", reply_markup=back_button_k)
        return

    approve_k.inline_keyboard[0][0].callback_data = f"accApprove_{message.from_user.id}_{user_input}_{account_type[4:]}"
    approve_k.inline_keyboard[0][1].callback_data = f"accDecline_{message.from_user.id}_{user_input}_{account_type[4:]}"
    file_path = f'data/{account_type[4:]}.json'
    with open(file_path, 'r') as f:
        existing_data = json.load(f)

    for admin in admins:
        if len(existing_data) < int(user_input):
            await message.bot.send_message(admin, f"Воркер {message.from_user.id} запросил {user_input} акаунтов для {account_type[4:]}, но у вас только {len(existing_data)}",
                                           reply_markup=approve_k)
        else:
            await message.bot.send_message(admin, f"Воркер {message.from_user.id} запросил {user_input} акаунтов для {account_type[4:]}",
                                           reply_markup=approve_k)
    await message.answer(f"Запрос отправлен администраторам.")

    await message.answer("Привет, воркер!", reply_markup=worker_keyboard)
    await state.clear()

async def approval(callback: CallbackQuery):
    user_id, amount, accounts_type = callback.data.split('_')[1:]
    file_path = f'data/{accounts_type}.json'
    with open(file_path, 'r') as f:
        existing_data = json.load(f)

    approved_accs = existing_data[:int(amount)]
    if len(approved_accs) == 0:
        await callback.message.answer("Нет доступных аккаунтов")
        await callback.bot.send_message(user_id, ("Нет доступных аккаунтов"))
        await callback.message.delete()
        return

    approved_accs = json.dumps(approved_accs)
    approved_accs = approved_accs[1:-1].replace(',', '\n')
    approved_accs = approved_accs[1:-1].replace('"', '')

    text_file = BufferedInputFile(bytes(approved_accs, 'utf-8'), filename="file.txt")

    await callback.bot.send_document(user_id, text_file)
    with open(file_path, 'w') as f:
        if len(existing_data) > int(amount):
            json.dump([], f)
        else:
            json.dump(existing_data[int(amount):], f)
    await callback.message.delete()
async def decline(callback: CallbackQuery):
    user_id = callback.data.split('_')[1]
    await callback.bot.send_message(user_id, ("Отказано в запросе на аккаунты"))
    await callback.message.delete()
