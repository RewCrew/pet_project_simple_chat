from typing import List, Optional

from sqlalchemy import select, desc

from classic.components import component
from classic.sql_storage import BaseRepository

from simple_chat.application import interfaces
from simple_chat.application.dataclasses import Users, Chats, Messages, ChatUsers


@component
class UsersRepo(BaseRepository, interfaces.UsersRepo):
    def add(self, user: Users):
        self.session.add(user)
        self.session.flush()


@component
class ChatsRepo(BaseRepository, interfaces.ChatsRepo):
    def get_by_id(self, chat_id: int) -> Optional[Chats]:
        query = select(Chats).where(Chats.id == chat_id)
        return self.session.execute(query).scalars().one_or_none()

    def add(self, chat: Chats):
        self.session.add(chat)
        self.session.flush()

    def delete(self, chat: Chats):
        self.session.delete(chat)
        self.session.flush()


@component
class ChatUsersRepo(BaseRepository, interfaces.ChatUsersRepo):

    def get_by_id_chat(self, chat_id: int) -> Optional[List[Users]]:
        users = self.session.query(User.name).filter_by(chat_id=chat_id).join(
            ChatUsers, User.id == ChatUsers.user_id)
        return users.all()

    def get_by_id_user(self, user_id: int) -> Optional[List[Chat]]:
        chats = self.session.query(Chat.chat_title).filter_by(user_id=user_id).join(
            ChatUsers, Chat.chat_id == ChatUsers.chat_id)
        return users.all()

    def add(self, chat_users: ChatUsers):
        self.session.add(chat_users)
        self.session.flush()


@component
class MessagesRepo(BaseRepository, interfaces.MessagesRepo):

    def add(self, message: Messages):
        self.session.add(message)
        self.session.flush()
