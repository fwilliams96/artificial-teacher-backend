from datetime import datetime
from ai_teacher.chat.free.domain.free_chat import FreeChat, FreeChatMessage, FreeChatMessageType

def map_entity_to_domain(free_chat: FreeChat) -> FreeChat:
    return FreeChat(
        id=str(free_chat["_id"]),
        is_over=free_chat["is_over"],
        user_id=str(free_chat["user_id"]),
        creation_date=datetime.strptime(free_chat["creation_date"], '%Y-%m-%d %H:%M:%S'),
    )

def map_entity_message_to_domain(message: dict) -> FreeChatMessage:
    return FreeChatMessage(
        id=str(message["_id"]),
        message=message["message"],
        type=FreeChatMessageType[str(message["type"]).upper()],
        sender_id=str(message["sender_id"]) if message["sender_id"] != None else None,
        chat_id=str(message["chat_id"]),
        sent_date=datetime.strptime(message["sent_date"], '%Y-%m-%d %H:%M:%S') if message["sent_date"] != None else None
    )