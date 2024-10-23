from collections import namedtuple
from os import getenv
from dotenv import load_dotenv

load_dotenv()
DEBUG = getenv("DEBUG")
ADMIN = int(getenv("ADMIN"))
DEVELOPER = int(getenv("DEVELOPER"))
SECOND_CHANNEL_ID = int(getenv("SECOND_CHANNEL_ID"))
MAIN_CHANNEL_ID = int(getenv("MAIN_CHANNEL_ID"))
TEST_CHANNEL_1_CHAT_ID = int(getenv("TEST_CHANNEL_1_CHAT_ID"))
TEST_CHANNEL_2_CHAT_ID = int(getenv("TEST_CHANNEL_2_CHAT_ID"))
