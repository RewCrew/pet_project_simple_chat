import pytest
from unittest.mock import Mock
import datetime
from simple_chat.application import interfaces, dataclasses


@pytest.fixture(scope='function')
def user():
    return dataclasses.User(
        id = 1,
        name='TestUser',
        email='TestEmail'
    )


@pytest.fixture(scope='function')
def chat():
    return dataclasses.Chat(
        chat_id=1,
        chat_title='TestChat',
        creator=1
    )


@pytest.fixture(scope='function')
def member():
    return dataclasses.ChatUsers(
        chat_id=1,
        user_id=1,
        id=1
    )


@pytest.fixture(scope='function')
def message():
    return dataclasses.Message(
        chat_id=1,
        sent_from=1,
        message_text='TestMessage',
        message_id=1,
        sent_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )


@pytest.fixture(scope='function')
def users_repo(user):
    users_repo = Mock(interfaces.UsersRepo)
    users_repo.get_by_id = Mock(return_value=user)
    return users_repo

@pytest.fixture(scope='function')
def chats_repo(chat):
    chats_repo = Mock(interfaces.ChatsRepo)
    chats_repo.get_by_id = Mock(return_value=chat)
    chats_repo.add = Mock(return_value=chat)
    return chats_repo

@pytest.fixture(scope='function')
def chat_user_member_short():
    return dataclasses.ChatUsersShort(chat_id=1, user_id=1)

@pytest.fixture(scope='function')
def chat_users_repo(member, chat_user_member_short):
    chat_users_repo = Mock(interfaces.ChatUsersRepo)
    chat_users_repo.get_by_id_chat = Mock(return_value=chat_user_member_short)
    chat_users_repo.add=Mock(return_value=member)
    return chat_users_repo



@pytest.fixture(scope='function')
def messages_repo(message):
    messages_repo = Mock(interfaces.MessagesRepo)
    messages_repo.get_messages = Mock(return_value=message)
    messages_repo.add=Mock(return_value=message)
    return messages_repo
