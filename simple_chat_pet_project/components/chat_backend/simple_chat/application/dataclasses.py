import datetime
from typing import Optional

import attr


@attr.dataclass
class User:
    name: str
    email: str
    id: Optional[int] = None


@attr.dataclass
class Chat:
    chat_title: str
    creator: int
    chat_id: Optional[int] = None

@attr.dataclass
class Message:
    message_text: str
    sent_from: int
    chat_id: int
    sent_date: Optional[str] = attr.ib(
    factory=lambda: str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    message_id: Optional[int] = None

@attr.dataclass
class ChatUsers:
    chat_id: int
    user_id: int
    id: Optional[int] = None

@attr.dataclass
class ChatUsersShort:
    chat_id: int
    user_id: int