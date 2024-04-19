import json
import re

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto, Message

import helpers.openai
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


class WorkerGPTInput(StatesGroup):
    waiting_for_user_input = State()


async def get_ticket(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer("Напишите ваш вопрос ChatGPT",
                                  reply_markup=back_button_k)
    await state.set_state(WorkerGPTInput.waiting_for_user_input)

async def send_ticket(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Ожидайте ответа")
    user_input = message.text
    answer = await helpers.openai.query_openai_api(user_input)
    await message.answer(answer)
    await message.answer("Привет, воркер!", reply_markup=worker_keyboard)