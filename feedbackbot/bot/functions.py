import os
import zoneinfo
from datetime import datetime

from aiogram import Bot
from aiogram.enums import ContentType

from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

import bot.texts as texts
from bot.config import ADMIN, DEVELOPER


async def update_caption_or_text(message: Message) -> Message:
    """Добавляет подпись бота к фото или к тексту"""
    if message.content_type == ContentType.PHOTO:
        updated_caption = texts.ADDITIONAL_TEXT.format(bot_link=os.getenv("BOT_LINK"))
        if message.caption is not None:
            updated_caption = message.caption + texts.ADDITIONAL_TEXT.format(
                bot_link=os.getenv("BOT_LINK")
            )
        await message.edit_caption(caption=updated_caption)
    elif message.content_type == ContentType.TEXT:
        updated_text = message.text + texts.ADDITIONAL_TEXT.format(
            bot_link=os.getenv("BOT_LINK")
        )
        await message.edit_text(text=updated_text)
    return message


async def send_news_to_admin(message: Message) -> None:
    """Отправляет сообщение из предложки Админу"""
    admin_id = ADMIN if os.getenv("DEBUG") == "False" else DEVELOPER
    time = datetime.now(tz=zoneinfo.ZoneInfo("Europe/Moscow")).strftime(
        "%d.%m.%y-%H:%M:%S"
    )
    try:
        await message.bot.send_message(
            chat_id=admin_id, text=f"{message.chat.id}" # and {type(message.chat)}"
        )
        await message.bot.send_message(
            chat_id=admin_id,
            text=f"{time} @{message.from_user.username}\nНачало сообщения:",
        )
        admin_msg = await message.send_copy(admin_id)
        await update_caption_or_text(admin_msg)
        await message.bot.send_message(chat_id=admin_id, text="Конец сообщения")
    except Exception as e:
        await message.bot.send_message(chat_id=DEVELOPER, text=e)


async def send_bot_button_to_channel(channel_chat_id: str, bot: Bot) -> None:
    """Отправляет сообщение в канал и добавляет в закрепленные сообщения"""
    inl_keyboard = InlineKeyboardBuilder()
    button = InlineKeyboardButton(text="Предложить новость", url=os.getenv("BOT_LINK"))
    inl_keyboard.add(button)
    ad_message = await bot.send_message(
        chat_id=channel_chat_id,
        text=texts.CHANNEL_BOT_AD.format(bot_link=os.getenv("BOT_LINK")),
        reply_markup=inl_keyboard.as_markup(),
    )
    await bot.pin_chat_message(
        chat_id=channel_chat_id, message_id=ad_message.message_id
    )
