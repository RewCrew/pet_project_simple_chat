import datetime

from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    DateTime
)

naming_convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
}

# даем имя схемы только для БД MSSQL, связано с инфраструктурными особенностями
# metadata = MetaData(naming_convention=naming_convention, schema='app')

metadata = MetaData(naming_convention=naming_convention)


users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String, nullable=False),
    Column('email', String, nullable=True)
)

chats = Table(
    'chats',
    metadata,
    Column('chat_id', Integer, primary_key=True, autoincrement=True),
    Column('chat_title', String, nullable=False),
    Column('creator', Integer, ForeignKey('users.id'), nullable=False)
)

messages = Table(
    'messages',
    metadata,
    Column('message_id', Integer, primary_key=True, autoincrement=True),
    Column('message_text', String, nullable=False),
    Column('sent_from', Integer, ForeignKey('users.id')),
    Column('sent_date', DateTime, nullable=False),
    Column('chat_id', Integer, ForeignKey('chats.chat_id'), nullable=False )
)

chat_users = Table(
    'chat_users',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('chat_id', Integer, ForeignKey('chats.chat_id', ondelete='CASCADE'), nullable=False),
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

)


