import falcon

from . import controllers, auth
from classic.http_api import App
from classic.http_auth import Authenticator
from simple_chat.application import services


def create_app(
        is_dev_mode: bool,
        chats: services.ChatService,
        register: services.RegisterService,
) -> App:
    authenticator = Authenticator(app_groups=auth.ALL_GROUPS)

    if is_dev_mode:
        authenticator.set_strategies(auth.jwt_strategy)

    app = App(prefix='/api')

    app.register(controllers.ChatController(chat_controller=chats, authenticator=authenticator))
    app.register(controllers.Register(register=register))
    return app
