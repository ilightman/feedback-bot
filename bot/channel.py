import os
from typing import List, Union

from aiogram import Router, types, F
from aiogram.enums import ContentType
from aiogram_media_group import media_group_handler

channel_router = Router()
main_channel_id = int(os.getenv('CHANNEL_CHAT_ID'))
second_channel_id = int(os.getenv('SECOND_CHANNEL_ID'))


async def make_media_group(media_album: List[types.Message]) -> List[Union[types.InputMediaAudio,
                                                                           types.InputMediaDocument,
                                                                           types.InputMediaPhoto,
                                                                           types.InputMediaVideo]]:
    """Создает список объектов медиа из сообщений, в зависимости от типа контента"""
    media_list = list()
    for media_album_part in media_album:
        if media_album_part.content_type == ContentType.PHOTO:
            photo = types.InputMediaPhoto(
                media=media_album_part.photo[-1].file_id,
                caption=media_album_part.caption,
                caption_entities=media_album_part.caption_entities, )
            media_list.append(photo)
        elif media_album_part.content_type == ContentType.VIDEO:
            video = types.InputMediaVideo(
                media=media_album_part.video.file_id,
                caption=media_album_part.caption,
                caption_entities=media_album_part.caption_entities,
            )
            media_list.append(video)
    return media_list


@channel_router.channel_post((F.chat.id == main_channel_id), F.media_group_id)
@media_group_handler(receive_timeout=15.0)
async def album_handler(album_channel_post: List[types.Message]):
    """Обрабатывает только сообщения содержащие альбомы с несколькими медиа файлами"""
    new_media_group_list = await make_media_group(media_album=album_channel_post)
    if new_media_group_list:
        await album_channel_post[0].bot.send_media_group(chat_id=second_channel_id, media=new_media_group_list)


@channel_router.channel_post(F.chat.id == main_channel_id)
async def channel_post_handler(channel_post: types.Message):
    """Обрабатывает посты в канале с единичными видео или фото файлами"""
    if channel_post.content_type == ContentType.TEXT:
        await channel_post.bot.send_message(chat_id=second_channel_id, text=channel_post.text)
    elif channel_post.content_type == ContentType.PHOTO:
        await channel_post.bot.send_photo(chat_id=second_channel_id, photo=channel_post.photo[-1].file_id,
                                          caption=channel_post.caption)
    elif channel_post.content_type == ContentType.VIDEO:
        await channel_post.bot.send_video(chat_id=second_channel_id, video=channel_post.video.file_id,
                                          caption=channel_post.caption)
