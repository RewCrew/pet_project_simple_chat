from classic.http_api import App

from simple_chat.application import services
from . import controllers


def create_app(
        profiles: services.Profiles,

) -> App:
    app = App(prefix='/api')

    app.register(controllers.Profiles(profiles=profiles))

    return app