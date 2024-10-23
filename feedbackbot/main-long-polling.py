import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
import aiohttp
from bot.admin import admin_router
from bot.channel import channel_router
from bot.users import users_router
from dotenv import load_dotenv

load_dotenv()
TOKEN = getenv('FEEDBACK_BOT_TOKEN')
dp = Dispatcher()


# async def send_message_to_admin(message_text: str, admin_id:str) -> None:
#     params = {
#         'chat_id': int(admin_id),
#         'text': message_text
#     }
#     async with aiohttp.ClientSession() as session:
#         async with session.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage', params=params) as resp:
#             print(resp)


# async def on_startup(dp: Dispatcher):
#     await send_message_to_admin('Бот включается', admin_id=getenv('DEVELOPER'))
    
# async def on_shutdown(dp: Dispatcher):
#     await send_message_to_admin('Бот выключается', admin_id=getenv('DEVELOPER'))
    
async def main() -> None:
    dp.include_router(admin_router)
    dp.include_router(channel_router)
    dp.include_router(users_router)
    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    # await dp.start_polling(bot, on_startup=on_startup, on_shutdown=on_shutdown)
    await dp.start_polling(bot)


if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    logging.Formatter(fmt='%(asctime)s-%(message)s',datefmt='%Y-%m-%d,%H:%M:%S.%f')
    logging.basicConfig(level=logging.INFO, filename='../bots/logs/feedback_bot.log')
    asyncio.run(main())