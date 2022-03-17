from simple_chat.application import services
from classic.components import component

from .join_points import join_point
from falcon import Request, Response




@component
class ChatController:
    chat_controller: services.ChatService

    @join_point
    def on_post_add_chat(self, request:Request, response:Response):
        self.chat_controller.add_chat(**request.media)