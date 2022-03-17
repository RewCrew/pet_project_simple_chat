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
    id: int
    name: str
    email: str

@component
class UserService:
    users_repo: interfaces.UsersRepo
    @join_point
    @validate_arguments
    def add_user(self, user_info: UserInfo):
        user = user_info.create_obj(User)
        self.users_repo.add(user)


@component
class ChatService:
    chats_repo: interfaces.ChatsRepo
    @join_point
    @validate_arguments
    def get_all_users_in_chat(self, id:int) -> List[User]:
        chat =  self.chats_repo.get_by_id(id)
        users_list = chat.users_list #????
        return users_list

