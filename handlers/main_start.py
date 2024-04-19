import json

from aiogram.filters import Command
from aiogram.types import Message

from configs import admins
from keyboard.start_keyboard import adm_keyboard, worker_keyboard

from loader import dp



async def command_start_handler(message: Message) -> None:
    with open('data/workers.json', 'r') as f:
        workers = json.load(f)
    if message.from_user.id in admins:
        await message.answer("Привет, администратор!", reply_markup=adm_keyboard)
    elif message.from_user.id in workers:
        await message.answer("Привет, воркер!", reply_markup=worker_keyboard)
    else:
        print(message.from_user.id)

async def standart_handler(message: Message) -> None:
    with open('data/workers.json', 'r') as f:
        workers = json.load(f)
    if message.from_user.id in admins:
        await message.answer("Привет, администратор!", reply_markup=adm_keyboard)
    elif message.from_user.id in workers:
        await message.answer("Привет, воркер!", reply_markup=worker_keyboard)
