from typing import List, Optional

from sqlalchemy import select, desc

from classic.components import component
from classic.sql_storage import BaseRepository

from simple_chat.application import interfaces
from simple_chat.application.dataclasses import User, Chat, Message, ChatUsers


@component
class UsersRepo(BaseRepository, interfaces.UsersRepo):
    def add(self, user: User):
        self.session.add(user)
        self.session.flush()
        
    def get_by_id(self, id_: int) -> Optional[User]:
        query = select(User).where(User.id == id_)
        return self.session.execute(query).scalars().one_or_none()

    def get_or_create(self, user: User) -> User:
        if user.id is None:
            self.add(user)
        else:
            new_user = self.get_by_id(user.id)
            if new_user is None:
                self.add(user)
            else:
                user=new_user
        return user


@component
class ChatsRepo(BaseRepository, interfaces.ChatsRepo):
    def get_by_id(self, chat_id: int) -> Optional[Chat]:
        query = select(Chat).where(Chat.chat_id == chat_id)
        return self.session.execute(query).scalars().one_or_none()

    def add(self, chat: Chat):
        self.session.add(chat)
        self.session.flush()

    def delete(self, chat: Chat):
        self.session.delete(chat)
        self.session.flush()


@component
class ChatUsersRepo(BaseRepository, interfaces.ChatUsersRepo):

    def get_by_id_chat(self, chat_id: int) -> Optional[List[User]]:
        users = self.session.query(User.name).filter_by(chat_id=chat_id).join(
            ChatUsers, User.id == ChatUsers.user_id)
        return users.all()

    def get_by_id_user(self, user_id: int) -> Optional[List[Chat]]:
        chats = self.session.query(Chat.chat_title).filter_by(user_id=user_id).join(
            ChatUsers, Chat.chat_id == ChatUsers.chat_id)
        return chats.all()

    def add(self, chat_users: ChatUsers):
        self.session.add(chat_users)
        self.session.flush()


@component
class MessagesRepo(BaseRepository, interfaces.MessagesRepo):

    def add(self, message: Message):
        self.session.add(message)
        self.session.flush()
