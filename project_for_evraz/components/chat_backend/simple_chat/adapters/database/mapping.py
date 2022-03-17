from sqlalchemy.orm import registry, relationship

from simple_chat.application import dataclasses

from . import tables

mapper = registry()

mapper.map_imperatively(dataclasses.User, tables.users)
mapper.map_imperatively(dataclasses.Chat, tables.chats, properties={
    # 'creator': relationship(
    #     dataclasses.User, uselist=False, lazy='joined'
    # ),
    'chat_messages': relationship(
        dataclasses.Message, lazy='subquery'
    ),
    'user_list': relationship(
        dataclasses.User, lazy='subquery'
    )
})
mapper.map_imperatively(dataclasses.Message, tables.messages
                        # , properties={
    # 'sent_from': relationship(
    #     dataclasses.User, uselist=False, lazy='joined'
    # ),
    # 'chat_id': relationship(
    #         dataclasses.Chat, uselist=False, lazy='joined'
    # )}
                    )
mapper.map_imperatively(dataclasses.ChatUsers, tables.chat_users
#                         , properties={
#     'user_id': relationship(
#         dataclasses.User, uselist=False, lazy='joined'
#     ),
#     'chat_id': relationship(
#         dataclasses.Chat, uselist=False, lazy='joined'
#     )
#
# }
                        )

