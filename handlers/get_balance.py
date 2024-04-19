import json
import re

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto, Message

from configs import admins
from keyboard.start_keyboard import worker_keyboard, adm_keyboard, back_button_k, approve_k
from loader import dp

from aiogram import types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import json
import os
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import BufferedInputFile


class WorkerBalanceInput(StatesGroup):
    waiting_for_card_input = State()
    waiting_for_balance_input = State()


async def get_balance_card(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer("Введите номер карты для пополнения баланса",
                                  reply_markup=back_button_k)
    await state.set_state(WorkerBalanceInput.waiting_for_card_input)


async def get_balance_amount(message: Message, state: FSMContext) -> None:
    user_input = message.text
    # if not re.match(r'^[0-9 ]+$', user_input):
    #     await message.answer("Неверный формат ввода. Попробуйте еще раз.", reply_markup=back_button_k)
    #     return
    await state.update_data(card=user_input)
    await message.answer("Введите сумму для пополнения",
                         reply_markup=back_button_k)
    await state.set_state(WorkerBalanceInput.waiting_for_balance_input)


async def get_balance_approval(message: Message, state: FSMContext):
    user_input = message.text
    state_data = await state.get_data()
    card = state_data.get('card')

    approve_k.inline_keyboard[0][0].callback_data = f"blnApprove_{message.from_user.id}"
    approve_k.inline_keyboard[0][1].callback_data = f"blnDecline_{message.from_user.id}"

    for admin in admins:
        await message.bot.send_message(admin, f"Воркер {message.from_user.id} запросил {user_input} баланса на карту {card}",
                                       reply_markup=approve_k)
    await message.answer(f"Запрос отправлен администраторам.")

    await message.answer("Привет, воркер!", reply_markup=worker_keyboard)
    await state.clear()


async def approval(callback: CallbackQuery):
    user_id = callback.data.split('_')[1]

    await callback.bot.send_message(user_id, ("Баланс пополнен"))
    await callback.message.delete()

async def decline(callback: CallbackQuery):
    user_id = callback.data.split('_')[1]
    await callback.bot.send_message(user_id, ("Отказано в пополнении"))
    await callback.message.delete()
