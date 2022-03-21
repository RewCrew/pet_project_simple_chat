from typing import List, Optional

from sqlalchemy import select, desc, delete

from classic.components import component
from classic.sql_storage import BaseRepository

from simple_chat.application import interfaces
from simple_chat.application.dataclasses import User, Chat, Message, ChatUsers, ChatUsersShort


@component
class UsersRepo(BaseRepository, interfaces.UsersRepo):
    def add(self, user: User):
        self.session.add(user)
        self.session.flush()
        self.session.refresh(user)
        return user
        
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
                user = new_user
        return user


@component
class ChatsRepo(BaseRepository, interfaces.ChatsRepo):
    def get_by_id(self, chat_id: int) -> Optional[Chat]:
        query = select(Chat).where(Chat.chat_id == chat_id)
        return self.session.execute(query).scalars().one_or_none()

    def add(self, chat: Chat):
        self.session.add(chat)
        self.session.flush()
        return chat


    def delete(self, chat: Chat):
        self.session.delete(chat)
        self.session.flush()


@component
class ChatUsersRepo(BaseRepository, interfaces.ChatUsersRepo):

    def get_by_id_chat(self, chat_id: int):
        query = self.session.query(User, ChatUsers)
        query = query.join(User, User.id == ChatUsers.user_id)
        query = query.filter(ChatUsers.chat_id == chat_id)
        chat_users = self.session.execute(query).scalars().all()
        return [ChatUsersShort(chat_user.chat_id, chat_user.user_id) for chat_user in chat_users]

    def get_by_id_user(self, user_id: int) -> Optional[List[Chat]]:
        chats = self.session.query(Chat.chat_title).filter_by(user_id=user_id).join(
            ChatUsers, Chat.chat_id == ChatUsers.chat_id)
        return chats.all()

    def add(self, chat_users:ChatUsers):
        self.session.add(chat_users)
        self.session.flush()


    def delete(self, chat_id:int):
        query = delete(ChatUsers).where(ChatUsers.chat_id == chat_id)
        self.session.execute(query)
        self.session.flush()

    def check_user(self, chat_id: int, user_id: int) -> Optional[ChatUsers]:
        query = select(ChatUsers).where(ChatUsers.chat_id == chat_id, ChatUsers.user_id == user_id)
        return self.session.execute(query).scalars().one_or_none()

    def leave_chat(self, chat_id:int, user_id:int):
        query = delete(ChatUsers).where(ChatUsers.chat_id == chat_id, ChatUsers.user_id==user_id)
        self.session.execute(query)
        self.session.flush()


@component
class MessagesRepo(BaseRepository, interfaces.MessagesRepo):

    def add(self, message: Message):
        self.session.add(message)
        self.session.flush()
        self.session.refresh(message)
        return message

    def get_messages(self, chat_id:int):
        query = select(Message).where(Message.chat_id==chat_id)
        return self.session.execute(query).scalars().all()
