import logging
import os

from aiogram import Router, F
from aiogram.exceptions import TelegramForbiddenError
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

from bot.filters import ChatTypeFilter
from bot.functions import send_bot_button_to_channel
from bot.texts import ADMIN_HELP
from bot.config import ADMIN, DEVELOPER

load_dotenv()
admin_router = Router()

ADMINS = [ADMIN, DEVELOPER]


@admin_router.message(F.from_user.id.in_(ADMINS), Command("help"), ChatTypeFilter(chat_type=['private']))
async def admin_start(message: Message) -> None:
    await message.answer(ADMIN_HELP)


@admin_router.message(F.from_user.id.in_(ADMINS), Command("send_pin_bot"), ChatTypeFilter(chat_type=['private']))
async def admin_send_button(message: Message) -> None:
    channel_chat_id = os.getenv('CHANNEL_CHAT_ID')
    await send_bot_button_to_channel(channel_chat_id=channel_chat_id, bot=message.bot)


@admin_router.message(ChatTypeFilter(chat_type=['group', 'supergroup']))
async def safety_filter(message: Message) -> None:
    try:
        await message.chat.leave()
    except TelegramForbiddenError:
        logging.info(msg='leaving_chat')

# @admin_router.message(F.from_user.id.in_(ADMINS))
# async def admin_answer(message: Message):
#     await message.answer('ты админ')
