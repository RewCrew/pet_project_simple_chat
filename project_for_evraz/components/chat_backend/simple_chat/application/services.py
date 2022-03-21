from typing import List, Optional, Tuple

import jwt
from pydantic import conint, validate_arguments

from classic.app import DTO, validate_with_dto
from classic.aspects import PointCut
from classic.components import component

from . import interfaces, errors
from .dataclasses import Chat, Message, User, ChatUsers, ChatUsersShort

join_points = PointCut()
join_point = join_points.join_point


#
class UserInfo(DTO):
    name: str
    email: str
    # id: Optional[int]


#
class MessageInfo(DTO):
    message_text: str
    sent_from: int
    sent_date: Optional[str]
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
    @validate_with_dto
    def add_user(self, user_info: UserInfo):
        print(user_info)
        user = user_info.create_obj(User)
        self.users_repo.add(user)


@component
class ChatService:
    chats_repo: interfaces.ChatsRepo
    chat_users_repo: interfaces.ChatUsersRepo
    messages_repo: interfaces.MessagesRepo
    users_repo: interfaces.UsersRepo

    def is_chat_exist(self, chat_id: int) -> Optional[Chat]:
        chat = self.chats_repo.get_by_id(chat_id)
        if chat is None:
            raise errors.NoChat(chat_id=chat_id)
        return chat

    @staticmethod
    def is_chat_creator(chat: Chat, user_id: int):
        if chat.creator != user_id:
            raise errors.NotCreator(user_id=user_id)
        return chat

    def is_chat_member(self, chat_id: int, user_id: int) -> Optional[ChatUsers]:
        member = self.chat_users_repo.check_user(chat_id, user_id)
        if member is None:
            raise errors.NotMember(user_id=user_id)
        return member

    #
    @join_point
    @validate_with_dto
    def add_chat(self, chat_info: ChatInfo):
        new_chat = chat_info.create_obj(Chat)
        chat = self.chats_repo.add(new_chat)
        chat_users = ChatUsers(chat.chat_id, chat.creator)
        self.chat_users_repo.add(chat_users)
        return chat


    #
    @join_point
    @validate_arguments
    def delete_chat(self, chat_id: int, user_id: int):
        chat_to_delete = self.is_chat_exist(chat_id)
        if chat_to_delete is None:
            raise errors.NoChat(chat_id=chat_id)
        creator = self.is_chat_creator(chat_to_delete, user_id)
        if creator is None:
            raise errors.NotCreator(user_id=user_id)
        self.chat_users_repo.delete(chat_id)
        self.chats_repo.delete(chat_to_delete)

    @join_point
    @validate_with_dto
    def update_chat(self, chat_info: ChatInfoForChange):
        chat = self.is_chat_exist(chat_info.chat_id)
        if chat is None:
            raise errors.NoChat(chat_id=chat_info.chat_id)
        creator = self.is_chat_creator(chat, chat_info.creator)
        if creator is None:
            raise errors.NotCreator(user_id=chat_info.creator)
        chat_info.populate_obj(chat)
        return chat

    @join_point
    def add_participant(self, chat_id: int, creator_id: int, user_id: int)-> ChatUsersShort:
        chat = self.is_chat_exist(chat_id)
        if chat is None:
            raise errors.NoChat(chat_id=chat_id)
        creator = self.is_chat_creator(chat, int(creator_id))
        if creator is None:
            raise errors.NotCreator(user_id=creator_id)
        chat_users = ChatUsers(chat.chat_id, user_id)
        self.chat_users_repo.add(chat_users)
        chat_users = ChatUsersShort(chat.chat_id, user_id)
        return chat_users

    @join_point
    def get_chat_info(self, chat_id: int, user_id: int) -> Chat:
        chat = self.is_chat_exist(chat_id)
        if chat is None:
            raise errors.NoChat(chat_id=chat_id)
        member = self.is_chat_member(chat_id, user_id)
        if member is None:
            raise errors.NotMember(user_id=user_id)
        return chat

    @join_point
    def get_users_in_chat(self, chat_id: int, user_id: int):
        member = self.is_chat_member(chat_id, user_id)
        if member is None:
            raise errors.NotMember
        users_list = self.chat_users_repo.get_by_id_chat(chat_id)
        return users_list

    @join_point
    @validate_with_dto
    def send_message(self, message: MessageInfo):
        chat = self.is_chat_exist(message.chat_id)
        if chat is None:
            raise errors.NoChat(chat_id=message.chat_id)
        member = self.is_chat_member(message.chat_id, message.sent_from)
        if member is None:
            raise errors.NotMember(user_id=message.sent_from)
        message = message.create_obj(Message)
        message = self.messages_repo.add(message)
        return message

    @join_point
    @validate_arguments
    def get_messages(self, chat_id: int, user_id: int) -> List[Message]:
        chat = self.is_chat_exist(chat_id)
        if chat is None:
            raise errors.NoChat(chat_id=chat_id)
        member = self.is_chat_member(chat_id, user_id)
        if member is None:
            raise errors.NotMember(user_id=user_id)
        messages_list = self.messages_repo.get_messages(chat_id)
        return messages_list

    @join_point
    def leave_chat(self, chat_id: int, user_id: int):
        chat = self.is_chat_exist(chat_id)
        if chat is None:
            raise errors.NoChat(chat_id=chat_id)
        if chat.creator == int(user_id):
            self.chat_users_repo.delete(chat_id)
            self.chats_repo.delete(chat)
            return f'user {user_id} leave chat and chat deleted'
        else:
            self.chat_users_repo.leave_chat(chat_id, user_id)
            return f'user {user_id} leave chat {chat_id}'


@component
class RegisterService:
    user_repo: interfaces.UsersRepo

    @join_point
    @validate_with_dto
    def add_user(self, user_info: UserInfo):
        new_user = user_info.create_obj(User)
        user = self.user_repo.get_or_create(new_user)
        token = jwt.encode(
            {"sub": user.id,
             "name": user.name,
             "email": user.email,
             "login": user.name,
             "group": "User"}
            , 'kerim_project', algorithm='HS256')
        return token
