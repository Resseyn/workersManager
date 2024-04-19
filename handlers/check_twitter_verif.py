import json
import re

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto, Message

import helpers.openai
from configs import admins
from helpers.twitter_checker import check_verified
from keyboard.start_keyboard import worker_keyboard, adm_keyboard, back_button_k, approve_k
from loader import dp

from aiogram import types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import json
import os
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import BufferedInputFile


class WorkerTwitterInput(StatesGroup):
    waiting_for_user_input = State()


async def check(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer("Напишите тег пользователя",
                                  reply_markup=back_button_k)
    await state.set_state(WorkerTwitterInput.waiting_for_user_input)

async def get_responce(message: Message, state: FSMContext):
    await state.clear()
    user_input = message.text
    responce = check_verified(user_input)
    if responce == "User doesn't exist":
        await message.answer("Пользователь не найден или проблемы с авторизацией, обратитесь к администратору")
    elif responce == False:
        await message.answer("Пользователь не верифицирован")
    elif responce == True:
        await message.answer("Пользователь верифицирован")
    await message.answer("Привет, воркер!", reply_markup=worker_keyboard)