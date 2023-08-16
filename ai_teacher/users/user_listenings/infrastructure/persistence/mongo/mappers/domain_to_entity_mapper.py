from bson import ObjectId
from ai_teacher.users.user_listenings.domain.user_listening import UserListening

def map_domain_to_entity(user_listening: UserListening) -> dict:
    return {
        "listening_id": ObjectId(user_listening.listening_id),
        "user_id": ObjectId(user_listening.user_id),
        "finished": user_listening.finished
    }