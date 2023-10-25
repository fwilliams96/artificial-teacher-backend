from bson import ObjectId
from ai_teacher.users.user_role_plays.domain.role_play import RolePlay, RolePlayMessage

def map_domain_to_entity(role_play: RolePlay) -> dict:
    return {
        "type": role_play.type,
        "is_over": role_play.is_over,
        "user_id": ObjectId(role_play.user_id),
        "routine_id": ObjectId(role_play.routine_id) if role_play.routine_id != None else None,
        "creation_date": role_play.creation_date.strftime('%Y-%m-%d %H:%M:%S')
    }

def map_message_domain_to_entity(message: RolePlayMessage) -> dict:
    return {
        "message": message.message,
        "type": message.type,
        "sender_id": ObjectId(message.sender_id) if message.sender_id != None else None,
        "role_play_id": ObjectId(message.role_play_id),
        "sent_date": message.sent_date.strftime('%Y-%m-%d %H:%M:%S'),
        "last_message": message.last_message
    }