from abc import ABC, abstractmethod
from typing import List, Optional

from .dataclasses import User, Chat, Message, ChatUsers

class UsersRepo(ABC):
    @abstractmethod
    def add(self, user:User):
        pass

    @abstractmethod
    def get_or_create(self, user:User):
        pass

    @abstractmethod
    def get_by_id(self, id_:int):
        pass


class ChatsRepo(ABC):
    @abstractmethod
    def add(self, chat:Chat):
        pass
    @abstractmethod
    def get_by_id(self, chat_id:int):
        pass
    @abstractmethod
    def delete(self, chat:Chat):
        pass

class MessagesRepo(ABC):
    @abstractmethod
    def add(self, message:Message):
        pass


class ChatUsersRepo(ABC):
    @abstractmethod
    def get_by_id_chat(self, chat_id:int) -> Optional[List[User]]:
        pass

    @abstractmethod
    def get_by_id_user(self, user_id:int)-> Optional[List[Chat]]:
        pass

    @abstractmethod
    def add(self, chat_users:ChatUsers):
        pass
