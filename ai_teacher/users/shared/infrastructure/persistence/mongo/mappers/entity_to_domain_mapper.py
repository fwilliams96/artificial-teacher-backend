from ai_teacher.users.shared.domain.user import User

def map_entity_to_domain(user: dict) -> User:
    return User(
        id=str(user["_id"]),
        email=user["email"],
        disabled=user["disabled"]
    )