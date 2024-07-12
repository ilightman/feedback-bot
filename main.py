import logging
import os
import sys

from aiogram import types, Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from bot.admin import admin_router
from bot.channel import channel_router
from bot.users import users_router

app = FastAPI(docs_url=None, redoc_url=None)
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

SECRET_TOKEN = os.getenv('SECRET_TOKEN')
DETA_URL = os.getenv('DETA_URL')
WEBHOOK_PATH = os.getenv('WEBHOOK_PATH')
WEBHOOK_URL = DETA_URL + f'/{WEBHOOK_PATH}'
API_TELEGRAM_URL = f'https://api.telegram.org/bot{BOT_TOKEN}'


@app.on_event('startup')
async def startup():
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(
            url=WEBHOOK_URL
        )
    dp.include_router(channel_router)
    dp.include_router(admin_router)
    dp.include_router(users_router)


@app.post(f'/{WEBHOOK_PATH}')
async def bot_webhook(update: dict, request: Request):
    telegram_token = request.headers.get('X-Telegram-Bot-Api-Secret-Token')
    if telegram_token == SECRET_TOKEN:
        telegram_update = types.Update(**update)
        await dp.feed_update(bot=bot, update=telegram_update)
        return JSONResponse(content={'success': True}, status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(content={'detail': 'Not authorized, secret token header is not provided!'},
                            status_code=status.HTTP_401_UNAUTHORIZED)


@app.on_event('shutdown')
async def shutdown():
    await bot.session.close()


@app.get('/docs')
@app.get('/redocs')
@app.get('/')
@app.get(WEBHOOK_PATH)
async def get_webhook():
    return JSONResponse(content={'detail': 'Not authorized! You are not supposed to be here!'},
                        status_code=status.HTTP_403_FORBIDDEN)


@app.get('/init')
async def test():
    return {
        'webhook_url': WEBHOOK_URL,
        'get_webhook_method': API_TELEGRAM_URL + '/getwebhookinfo',
        'set_webhook_link': API_TELEGRAM_URL + f'/setWebhook?'
                                               f'url={WEBHOOK_URL}'
                                               f'&secret_token={SECRET_TOKEN}'
                                               f'&drop_pending_updates=True',
        'delete_webhook_link': API_TELEGRAM_URL + '/deleteWebhook',
    }
