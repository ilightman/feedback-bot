from typing import Union, List

from aiogram.filters import BaseFilter
from aiogram.types import Message

from .config import MAIN_CHANNEL_ID, SECOND_CHANNEL_ID, TEST_CHANNEL_1_CHAT_ID, TEST_CHANNEL_2_CHAT_ID


class ChatTypeFilter(BaseFilter):
    def __init__(self, chat_type: Union[str, list]):
        self.chat_type = chat_type

    async def __call__(self, message: Message) -> bool:
        if isinstance(self.chat_type, str):
            return message.chat.type == self.chat_type
        else:
            return message.chat.type in self.chat_type

class ChannelsFilter(BaseException):
    def __init__(self) -> None:
        self.channels_list = [MAIN_CHANNEL_ID] #, TEST_CHANNEL_1_CHAT_ID]
    
    def __call__(self, message: Union[Message, List[Message]]) -> bool:
        if isinstance(message, List):
            return message[0].chat.id in self.channels_list
        elif isinstance(message, Message):
            return message.chat.id in self.channels_list