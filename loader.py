import os

from aiogram import Dispatcher

import configs

# Bot token can be obtained via https://t.me/BotFather
TOKEN = configs.bot_token

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()
