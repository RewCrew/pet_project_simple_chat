from abc import ABC, abstractmethod
from typing import List, Optional

from .dataclasses import User, Chat, Message

class UsersRepo(ABC):
    @abstractmethod
    def add(self, user:User):
        pass


class ChatsRepo(ABC):
    @abstractmethod
    def add(self, chat:Chat):
        pass

class MessagesRepo(ABC):
    @abstractmethod
    def add(self, message:Message):
        pass