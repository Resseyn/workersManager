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


class WorkerTicketInput(StatesGroup):
    waiting_for_user_input = State()


async def get_ticket(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer("Напишите ваш вопрос или проблему",
                                  reply_markup=back_button_k)
    await state.set_state(WorkerTicketInput.waiting_for_user_input)



async def send_ticket(message: Message, state: FSMContext):
    user_input = message.text
    ticket_k = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Завершить", callback_data=f"tkcApprove_{message.from_user.id}")]])
    for admin in admins:
        await message.bot.send_message(admin, f"Воркер {message.from_user.id} написал тикет: \n{user_input}",
                                       reply_markup=ticket_k)
    await message.answer(f"Тикет отправлен администраторам.")

    await message.answer("Привет, воркер!", reply_markup=worker_keyboard)
    await state.clear()

async def approval(callback: CallbackQuery):
    user_id = callback.data.split('_')[1]
    await callback.bot.send_message(user_id, ("Тикет закрыт"))
    await callback.message.delete()