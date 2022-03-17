from sqlalchemy.orm import registry, relationship

from simple_chat.application import dataclasses

from . import tables

mapper = registry()

mapper.map_imperatively(dataclasses.Chat, tables.chats)
mapper.map_imperatively(dataclasses.User, tables.users)
mapper.map_imperatively(dataclasses.Message, tables.messages)
mapper.map_imperatively(dataclasses.ChatUsers, tables.chat_users)