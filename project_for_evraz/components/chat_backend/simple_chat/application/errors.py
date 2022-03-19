from classic.app.errors import AppError


class NotMember(AppError):
    msg_template = "user with id '{user_id}' not a member of chat"
    code = 'chat.not_member'


class NoChat(AppError):
    msg_template = "No chat with id '{chat_id}' exist"
    code = 'chat.no_chat'


class NotCreator(AppError):
    msg_template = "user with id '{user_id}' not a creator of chat"
    code = 'chat.not_creator'

#
# class EmptyCart(AppError):
#     msg_template = "Cart is empty"
#     code = 'shop.cart_is_empty'