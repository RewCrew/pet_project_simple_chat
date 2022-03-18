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

#
class UserInfo(DTO):
    name: str
    email: str
#
class MessageInfo(DTO):

    message_text: str
    sent_from: str
    sent_date: str
    chat_id: int
    message_id: Optional[int]
#
class ChatInfo(DTO):
    creator: int
    chat_title: Optional[str]

class ChatInfoForChange(DTO):
    creator: int
    chat_title: str = None
    chat_id: int = None

class ChatUsersInfo(DTO):
    chat_id: int
    user_id: int

class ChatUsersInfoForChange(DTO):
    chat_id: int
    user_id: int
#

@component
class UserService:
    users_repo: interfaces.UsersRepo

    @join_point
    # @validate_with_dto
    def add_user(self, user_info: UserInfo):
        user = user_info.create_obj(User)
        self.users_repo.add(user)
#
#
@component
class ChatService:
    chats_repo: interfaces.ChatsRepo
    # chats_users_repo: interfaces.ChatUsersRepo
    # messages_repo: interfaces.MessagesRepo

    def is_chat_exist(self, chat_id:int)-> Optional[Chat]:
        chat = self.chats_repo.get_by_id(chat_id)
        if chat is None:
            raise Exception('not found')
        return chat

    @staticmethod
    def is_chat_creator(chat: Chat, user_id: int):
        if chat.creator != user_id:
            raise Exception('Not enough rights (Owner)')

    @join_point
    def get_all_users_in_chat(self, id: int) -> List[User]:
        chat = self.chats_repo.get_by_id(id)
        users_list = chat.users_list  # ????
        return users_list
#
    @join_point
    @validate_with_dto
    def add_chat(self, chat_info: ChatInfo):
        new_chat = chat_info.create_obj(Chat)
        self.chats_repo.add(new_chat)

    @join_point
    @validate_with_dto
    def update_chat(self, chat_info: ChatInfoForChange):
        chat = self.is_chat_exist(chat_info.chat_id)
        self.is_chat_creator(chat, chat_info.creator)
        chat_info.populate_obj(chat)

@component
class RegisterService:
    user_repo: interfaces.UsersRepo

    @join_point
    @validate_with_dto
    def add_user(self, user_info: UserInfo):
        new_user = user_info.create_obj(User)
        user = self.user_repo.get_or_create(new_user)
        return user

