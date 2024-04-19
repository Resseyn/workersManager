import json
import re

import requests
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto, Message

import configs
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


class WorkerProxyInput(StatesGroup):
    waiting_for_user_input = State()


async def get_proxy(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer("Введите количество желаемых прокси",
                                  reply_markup=back_button_k)
    await state.set_state(WorkerProxyInput.waiting_for_user_input)


async def get_country(message: Message, state: FSMContext) -> None:
    if not re.match(r'^[0-9 ]+$', message.text):
        await message.answer("Неверный формат ввода. Попробуйте еще раз.", reply_markup=back_button_k)
        return
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    keyboard.inline_keyboard.append([InlineKeyboardButton(text="США", callback_data=f"{message.text}_3")])
    keyboard.inline_keyboard.append([InlineKeyboardButton(text="Турция", callback_data=f"{message.text}_94")])
    keyboard.inline_keyboard.append([InlineKeyboardButton(text="Назад", callback_data="back")])
    await message.answer(f"Выберите страну:",
                         reply_markup=keyboard)
    await state.set_state(WorkerProxyInput.waiting_for_user_input)
    await state.update_data(account_type=message.text)


async def get_user_proxy(callback: CallbackQuery, state: FSMContext):
    amount, country = callback.data.split('_')
    approve_k.inline_keyboard[0][0].callback_data = f"prxApprove_{callback.from_user.id}_{amount}_{country}"
    approve_k.inline_keyboard[0][1].callback_data = f"prxDecline_{callback.from_user.id}_{amount}_{country}"

    for admin in admins:
        await callback.bot.send_message(admin, f"Воркер {callback.from_user.id} запросил {amount} прокси {
        'США' if country == '3' else 'Турция'}",
                                        reply_markup=approve_k)
    await callback.message.answer(f"Запрос отправлен администраторам.")

    await callback.message.answer("Привет, воркер!", reply_markup=worker_keyboard)
    await state.clear()


async def approval(callback: CallbackQuery):
    user_id, amount, country = callback.data.split('_')[1:]
    print(user_id, amount, country)
    req = requests.post("https://apid.iproyal.com/v1/reseller/orders",
                        json={
                            "product_id": 2,
                            "product_plan_id": 4,
                            "product_location_id": int(country),
                            "quantity": int(amount),
                            "auto_extend": False,
                            "product_question_answers": [],
                        },
                        headers={"X-Access-Token": configs.proxy_token})
    if req.status_code == 200:
        approved_proxies = json.dumps(req.text)['proxy_data']['proxies']

        text_file = BufferedInputFile(bytes(approved_proxies, 'utf-8'), filename="file.txt")

        await callback.bot.send_document(user_id, text_file)
        await callback.message.delete()
    else:
        await callback.bot.send_message(user_id, ("Отказано в запросе на прокси"))
        await callback.message.answer("Недостаточно баланса")


async def decline(callback: CallbackQuery):
    user_id = callback.data.split('_')[1]
    await callback.bot.send_message(user_id, ("Отказано в в запросе на прокси"))
    await callback.message.delete()
