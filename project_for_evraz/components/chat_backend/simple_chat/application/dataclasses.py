import datetime
from typing import List, Optional

import attr

@attr.dataclass
class User:
    id: Optional[int]=None
    name: str
    email: str


@attr.dataclass
class Chat:
    chat_id: Optional[int]=None
    chat_title: str
    users_list: list[User]
    creator: User
    chat_messages: list[Message]

@attr.dataclass
class Message:
    message_id: Optional[int]=None
    message_text: str
    sent_from: User
    sent_date: datetime.datetime
    chat_id: Chat


@attr.dataclass
class ChatUsers:
    id: Optional[int] = None
    chat_id: Chat
    user_id: User
