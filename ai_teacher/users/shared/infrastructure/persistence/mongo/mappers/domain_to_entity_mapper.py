from ai_teacher.users.shared.domain.user import UserDb

def map_domain_to_entity(user: UserDb) -> dict:
    return {
        "email": user.email,
        "password": user.password,
        "disabled": user.disabled,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "level": user.level,
        "score": user.score
    }