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
    def on_post_add_chat(self, request: Request, response: Response):
        self.chat_controller.add_chat(**request.media)
        response.body = json.dumps('Chat created')

    @join_point
    def on_post_update_chat(self, request: Request, response: Response):
        self.chat_controller.update_chat(**request.media)
        response.body = json.dumps('Chat Updated')

    @join_point
    def on_post_delete_chat(self, request: Request, response: Response):
        self.chat_controller.delete_chat(**request.media)
        response.body = json.dumps('Chat deleted')

    @join_point
    def on_post_add_participant(self, request: Request, response: Response):
        self.chat_controller.add_participant(**request.media)

    @join_point
    def on_get_show_chat_info(self, request: Request, response: Response):
        chat_info = self.chat_controller.get_chat_info(**request.media)
        response.media = {
            'title': chat_info.chat_title,
            'creator': chat_info.creator,
            # 'chat_messages': chat_info.chat_messages
        }

    @join_point
    def on_post_send_message(self, request: Request, response: Response):
        message = self.chat_controller.send_message(**request.media)
        response.media = {
            'message_text': message.message_text,
            'sent_from': message.sent_from,
            'sent_to': message.chat_id,
            'sent_date': message.sent_date.strftime("%Y-%m-%d %H:%M:%S")

        }

    @join_point
    def on_get_chat_messages(self, request: Request, response: Response):
        messages = self.chat_controller.get_messages(**request.media)
        response.media = {
            'messages': [{
                'message_text': message.message_text,
                'sent_from': message.sent_from,
                'sent_to': message.chat_id,
                'sent_date': message.sent_date.strftime("%Y-%m-%d %H:%M:%S")

            } for message in messages]

        }


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
