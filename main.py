import asyncio
import logging
import sys

from aiogram import Bot
from aiogram.enums import ParseMode

import handlers
from loader import TOKEN
from handlers import dp


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    handlers.setup(dp)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

    asyncio.run(main())
