from typing import List, Optional, Tuple

from pydantic import conint, validate_arguments

from classic.app import DTO, validate_with_dto
from classic.aspects import PointCut
from classic.components import component
from classic.messaging import Message, Publisher

from . import interfaces
from .dataclasses import Chat, Message, User

join_points = PointCut()
join_point = join_points.join_point


class UserInfo(DTO):
    name: str
    email: str

class MessageInfo(DTO):
    message_id: Optional[int]
    message_text: str
    sent_from: User
    sent_date: str
    chat_id: Chat

class ChatInfo(DTO):
    chat_title: str
    users_list: list[User]
    creator: User
    chat_messages: list[Message]

class ChatInfoForChange(DTO):
    chat_id: Optional[int]
    chat_title: str = None
    users_list: list[User]
    creator: User
    chat_messages: list[Message]

class ChatUsersInfo(DTO):
    chat_id: int
    user_id: int

class ChatUsersInfoForChange(DTO):
    chat_id: int
    user_id: int


@component
class UserService:
    users_repo: interfaces.UsersRepo

    @join_point
    @validate_with_dto
    def add_user(self, user_info: UserInfo):
        user = user_info.create_obj(User)
        self.users_repo.add(user)


@component
class ChatService:
    chats_repo: interfaces.ChatsRepo

    @join_point
    @validate_arguments
    def get_all_users_in_chat(self, id: int) -> List[User]:
        chat = self.chats_repo.get_by_id(id)
        users_list = chat.users_list  # ????
        return users_list
