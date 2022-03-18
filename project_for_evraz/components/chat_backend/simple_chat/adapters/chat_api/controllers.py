import json

from simple_chat.application import services
from classic.components import component

from .join_points import join_point
from falcon import Request, Response

from classic.http_auth import (
    authenticate,
    authenticator_needed,
    authorize,
)



@component
class ChatController:
    chat_controller: services.ChatService

    @join_point
    def on_post_add_chat(self, request:Request, response:Response):
        self.chat_controller.add_chat(**request.media)
        response.body=json.dumps('Chat created')


    @join_point
    def on_patch_update_chat(self, request: Request, response: Response):
        self.chat_controller.update_chat(**request.media)
        response.body = json.dumps('Chat Updated')

@component
class Register:
    register: services.RegisterService

    @join_point
    def on_post_register(self, request: Request, response: Response):
        user = self.register.add_user(**request.media)
        response.media = {
            'user_id': user.id,
            'user_name': user.name,
            'email': user.email,
        }
