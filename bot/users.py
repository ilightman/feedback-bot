from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot import texts
from bot.admin import ADMINS
from bot.filters import ChatTypeFilter
from bot.functions import send_news_to_admin

users_router = Router()


@users_router.message(~(F.from_user.id.in_(ADMINS)), CommandStart(), ChatTypeFilter(chat_type=['private']))
async def command_start_handler(message: Message) -> None:
    await message.answer(texts.GREETINGS)


@users_router.message(~(F.from_user.id.in_(ADMINS)), F.content_type.in_({'text', 'photo'}), ChatTypeFilter(chat_type=['private']))
async def content_in(message: Message) -> None:
    """Тут обрабатываем 'новость' """
    await send_news_to_admin(message=message)
    await message.answer(texts.ANSWER_TEXT)


@users_router.message(~(F.from_user.id.in_(ADMINS)), ChatTypeFilter(chat_type=['private']))
async def other_messages(message: Message) -> None:
    """Фильтруем весь контент не текст и не фото"""
    await message.answer(texts.GREETINGS)
    await message.delete()
