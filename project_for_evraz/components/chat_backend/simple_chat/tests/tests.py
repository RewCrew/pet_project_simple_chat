import datetime

import pytest
from attr import asdict
from simple_chat.application import services, errors


@pytest.fixture(scope='function')
def user_test(users_repo):
    return services.UserService(users_repo=users_repo)


@pytest.fixture(scope='function')
def chat_test(chats_repo, users_repo, messages_repo, chat_users_repo):
    return services.ChatService(
        chats_repo=chats_repo,
        chat_users_repo=chat_users_repo,
        users_repo=users_repo,
        messages_repo=messages_repo
    )


test_data_user = {
    'id': 1,
    'name': 'TestUser',
    'email': 'TestEmail'
}

test_data_user2 = {
    'id': 2,
    'name': 'TestUser2',
    'email': 'TestEmail2'}

test_data_chat = {
    'chat_id': 1,
    'chat_title': 'TestChat',
    'creator': 1,
}

test_data_chat_user = {
    'chat_id': 1,
    'user_id': 2
}

test_data_message = {
    'chat_id': 1,
    'sent_from': 1,
    'message_text': 'TestMessage',
    'sent_date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    'message_id':1
}

test_chat_update = {
    'chat_id': 10,
    'creator': 1,
    'chat_title': 'testUpdate',
}

test_data_get_messages = {
    'chat_id': 1,
    'sent_from': 1,
    'message_text': 'TestMessage',
    'sent_date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    'message_id': 1
}

test_data_get_users = {
    'user_id': 1,
    'chat_id': 1,

}


def test_add_user(user_test):
    user_test.add_user(**test_data_user)
    user_test.users_repo.add.assert_called_once()


def test_get_user(user_test):
    user = user_test.users_repo.get_by_id(test_data_user['id'])
    assert asdict(user) == test_data_user


def test_add_chat(chat_test):
    chat = chat_test.add_chat(**test_data_chat)
    chat_test.chats_repo.add.assert_called_once()
    assert asdict(chat) == test_data_chat

def test_add_member(chat_test):
    member = chat_test.add_participant(
        chat_id=test_data_chat['chat_id'],
        creator_id=test_data_user['id'],
        user_id=test_data_user2['id'])
    chat_test.chat_users_repo.add.assert_called_once()
    assert asdict(member) == test_data_chat_user


def test_update_chat(chat_test):
    chat = chat_test.update_chat(**test_chat_update)
    assert asdict(chat) == test_chat_update


#
def test_delete_chat(chat_test):
    chat = chat_test.delete_chat(chat_id=test_data_chat['chat_id'], user_id=test_data_user['id'])
    assert chat == None


def test_send_message(chat_test):
    message = chat_test.send_message(**test_data_message)
    chat_test.messages_repo.add.assert_called_once()
    assert asdict(message) == test_data_message


def test_leave_chat(chat_test):
    chat_test.chat_users_repo.leave_chat(**test_data_chat_user)
    chat_test.chat_users_repo.leave_chat.assert_called_once()


def test_get_chat_members(chat_test):
    members = chat_test.get_users_in_chat(
        chat_id=test_data_chat['chat_id'], user_id=test_data_user['id'])
    assert asdict(members) == test_data_get_users


def test_get_chat_messages(chat_test):
    messages = chat_test.get_messages(
        chat_id=test_data_chat['chat_id'], user_id=test_data_user['id'])
    assert asdict(messages) == test_data_get_messages


def test_not_chat_creator(chat_test):
    with pytest.raises(errors.NotCreator):
        chat_test.add_participant(chat_id=test_data_chat['chat_id'],
                                  creator_id=test_data_user2['id'],
                                  user_id=test_data_user2['id'])
