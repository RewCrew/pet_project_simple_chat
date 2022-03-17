import datetime
from typing import List, Optional

import attr

@attr.dataclass
class User:
    id: int
    name: str
    email: str


@attr.dataclass
class Chat:
    chat_id: int
    chat_title: str
    users_list: User
    creator: User
    chat_messages: Message

@attr.dataclass
class Message:
    message_id:int
    message_text: str
    sent_from: User
    sent_date: datetime.datetime



