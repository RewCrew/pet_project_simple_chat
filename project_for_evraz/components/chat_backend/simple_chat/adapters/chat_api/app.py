from classic.http_api import App

from simple_chat.application import services
from . import controllers


def create_app(
        chats: services.ChatService,

) -> App:
    app = App(prefix='/api')

    app.register(controllers.ChatController(chat_controller=chats))

    return app