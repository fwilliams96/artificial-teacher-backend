from bson import ObjectId
from ai_teacher.chat.free.domain.free_chat import FreeChat, FreeChatMessage

def map_domain_to_entity(free_chat: FreeChat) -> dict:
    return {
        "user_id": ObjectId(free_chat.user_id),
        "creation_date": free_chat.creation_date.strftime('%Y-%m-%d %H:%M:%S'),
        "is_over": free_chat.is_over
    }

def map_domain_message_to_entity(free_chat_message: FreeChatMessage) -> dict:
    return {
        "message": free_chat_message.message,
        "type": free_chat_message.type,
        "sender_id": ObjectId(free_chat_message.sender_id) if free_chat_message.sender_id != None else None,
        "chat_id": ObjectId(free_chat_message.chat_id),
        "sent_date": free_chat_message.sent_date.strftime('%Y-%m-%d %H:%M:%S')
    }