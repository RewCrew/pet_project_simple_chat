import datetime
from typing import List, Optional

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
    # chat_messages: List['Message'] = attr.ib(factory=list)
    chat_id: Optional[int] = None
    # users_list: List[User] = attr.ib(factory=list)

@attr.dataclass
class Message:
    message_text: str
    sent_from: int
    chat_id: int
    sent_date: datetime.datetime = attr.ib(
    factory=lambda: datetime.datetime.now())
    message_id: Optional[int] = None

@attr.dataclass
class ChatUsers:
    chat_id: int
    user_id: int
    id: Optional[int] = None
