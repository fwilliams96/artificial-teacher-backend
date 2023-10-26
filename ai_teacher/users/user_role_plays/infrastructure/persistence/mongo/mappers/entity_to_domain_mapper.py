from datetime import datetime
from ai_teacher.users.user_role_plays.domain.role_play import RolePlay, RolePlayMessage, RolePlayMessageType, RolePlayType

def map_entity_to_domain(role_play: dict) -> RolePlay:
    return RolePlay(
        id=str(role_play["_id"]),
        type=RolePlayType[str(role_play["type"]).upper()],
        is_over=role_play["is_over"],
        user_id=str(role_play["user_id"]),
        routine_id=str(role_play["routine_id"]) if role_play["routine_id"] != None else None,
        creation_date=datetime.strptime(role_play["creation_date"], '%Y-%m-%d %H:%M:%S'),
    )
    
def map_message_entity_to_domain(role_play_message: dict) -> RolePlay:
    return RolePlayMessage(
        id=str(role_play_message["_id"]),
        type=RolePlayMessageType[str(role_play_message["type"]).upper()],
        message=role_play_message["message"],
        sender_id=str(role_play_message["sender_id"]) if role_play_message["sender_id"] != None else None,
        role_play_id=str(role_play_message["role_play_id"]),
        sent_date=datetime.strptime(role_play_message["sent_date"], '%Y-%m-%d %H:%M:%S') if role_play_message["sent_date"] != None else None,
        last_message=role_play_message["last_message"]
    )