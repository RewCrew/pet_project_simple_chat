from sqlalchemy import create_engine

from classic.sql_storage import TransactionContext

from simple_chat.adapters import database, chat_api
from simple_chat.application import services


class Settings:
    db = database.Settings()


class DB:
    engine = create_engine(Settings.db.DB_URL)
    database.metadata.create_all(engine)

    context = TransactionContext(bind=engine)

    users_repo = database.repositories.UsersRepo(context=context)
    chats_repo = database.repositories.ChatsRepo(context=context)
    chat_users_repo = database.repositories.ChatUsersRepo(context=context)
    messages_repo = database.repositories.MessagesRepo(context=context)


class Application:
    user_controller = services.UserService(
        users_repo=DB.users_repo,
    )
    chat_controller = services.ChatService(
        chats_repo=DB.chats_repo,
        # chat_users_repo = DB.chat_users_repo,
        # messages_repo = DB.messages_repo
    )

class Aspects:
    services.join_points.join(DB.context)
    chat_api.join_points.join(DB.context)


app = chat_api.create_app(
    chats=Application.chat_controller
    ,)


if __name__ == "__main__":
    from wsgiref import simple_server

    with simple_server.make_server('', 8000, app=app) as server:
        server.serve_forever()