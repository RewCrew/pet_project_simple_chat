import datetime

from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
)

metadata = MetaData()

users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String, nullable=False),
    Column('email', String, nullable=True)
)

chats = Table(
    'chats',
    Column('chat_id', Integer, primary_key=True, autoincrement=True),
    Column('chat_title', String, nullable=False),
    Column('creator', Integer, ForeignKey('users.id'), nullable=False)
)

messages = Table(
    'messages',
    Column('message_id', Integer, primary_key=True, autoincrement=True),
    Column('message_text', String, nullable=False),
    Column('sent_from', Integer, ForeignKey('users.id')),
    Column('sent_date', DateTime, nullable=False, default=datetime.datetime.now()),
    Column('chat_id', Integer, ForeignKey('chats.chat_id'), nullable=False )
)

chat_users =Table(
    'chat_users',
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('chat_id', Integer, ForeignKey('chats.chats_id'), nullable=False),
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False)

)


