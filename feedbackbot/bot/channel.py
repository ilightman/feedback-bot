import logging
import os
from typing import List

from aiogram import Router, types
from aiogram.enums import ContentType
from aiogram_media_group import MediaGroupFilter, media_group_handler
from .config import (
    DEVELOPER,
    MAIN_CHANNEL_ID,
    SECOND_CHANNEL_ID,
    TEST_CHANNEL_1_CHAT_ID,
    TEST_CHANNEL_2_CHAT_ID,
)
from .filters import ChannelsFilter
from datetime import datetime

logger = logging.getLogger(__name__)
channel_router = Router()


async def make_media_group(messages: list[types.Message]) -> List:
    """Создает список InputMedia файлов"""
    media_list = []
    logger.info(f"{datetime.now().isoformat()} - общее количество всех сообщений - {len(messages)}")
    for message in messages:
        logger.info(f"{datetime.now().isoformat()} - {message.message_id} - message length (html text)- {len(message.html_text)}")
        if message.content_type == ContentType.PHOTO:
            media_list.append(
                types.InputMediaPhoto(
                    media=message.photo[-1].file_id, caption=message.html_text
                )
            )
        elif message.content_type == ContentType.VIDEO:
            media_list.append(
                types.InputMediaVideo(
                    media=message.video.file_id, caption=message.html_text
                )
            )
    if media_list:
        logger.info(f"{datetime.now().isoformat()} media list is done")
    else: 
        logger.info(f"{datetime.now().isoformat()} media list is None")
    return media_list


@channel_router.channel_post(ChannelsFilter() and MediaGroupFilter())  # , F.media_group_id)
@media_group_handler(receive_timeout=10)
async def album_handler(messages: list[types.Message]):
    """Обрабатывает только сообщения содержащие альбомы с несколькими медиа файлами"""
    try:
        logger.info(f"{datetime.now().isoformat()} - найдено сообщение из медиафайлов")
        media_list = await make_media_group(messages)
        # channel_id = SECOND_CHANNEL_ID if messages[0].chat.id == MAIN_CHANNEL_ID else TEST_CHANNEL_2_CHAT_ID
        channel_id = SECOND_CHANNEL_ID if os.getenv("DEBUG") == "False" else TEST_CHANNEL_2_CHAT_ID
        await messages[0].bot.send_media_group(chat_id=channel_id, media=media_list)
    except Exception as e:
        await messages[0].bot.send_message(chat_id=DEVELOPER, text=e)


@channel_router.channel_post(ChannelsFilter())
async def single_channel_post_handler(channel_post: types.Message):
    """Обрабатывает посты в канале с единичными видео или фото файлами"""
    logger.info(f"{datetime.now().isoformat()} single_message")
    # channel_id = SECOND_CHANNEL_ID if messages[0].chat.id == MAIN_CHANNEL_ID else TEST_CHANNEL_2_CHAT_ID
    try:
        channel_id = (
            SECOND_CHANNEL_ID if os.getenv("DEBUG") == "False" else TEST_CHANNEL_2_CHAT_ID
        )
        logger.info(f"{channel_id=} {channel_post.sender_chat.full_name}")
        if channel_post.content_type == ContentType.TEXT:
            await channel_post.bot.send_message(
                chat_id=channel_id, text=channel_post.html_text
            )
        elif channel_post.content_type == ContentType.PHOTO:
            await channel_post.bot.send_photo(
                chat_id=channel_id,
                photo=channel_post.photo[-1].file_id,
                caption=channel_post.html_text,
            )
        elif channel_post.content_type == ContentType.VIDEO:
            await channel_post.bot.send_video(
                chat_id=channel_id,
                video=channel_post.video.file_id,
                caption=channel_post.html_text,
            )
    except Exception as e:
        await channel_post.bot.send_message(chat_id=DEVELOPER, text=e)