from classic.http_api import App

from simple_chat.application import services
from . import controllers


def create_app(
        chats: services.ChatService,
        register: services.RegisterService,
) -> App:
    app = App(prefix='/api')

    app.register(controllers.ChatController(chat_controller=chats))
    app.register(controllers.Register(register=register))
    return app