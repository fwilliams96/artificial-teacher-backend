from ai_teacher.users.user_listenings.domain.user_listening import UserListening

def map_entity_to_domain(user_listening: dict) -> UserListening:

    return UserListening(
        id=str(user_listening["_id"]),
        listening_id=str(user_listening["listening_id"]),
        user_id=str(user_listening["user_id"]),
        finished=user_listening["finished"]
    )