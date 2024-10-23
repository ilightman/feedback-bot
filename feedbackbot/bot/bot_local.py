import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from bot.admin import admin_router
from bot.users import users_router

load_dotenv()
TOKEN = os.getenv('TOKEN')
dp = Dispatcher()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)


async def main() -> None:
    dp.include_router(admin_router)
    dp.include_router(users_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
