from ai_teacher.users.shared.domain.user import UserDb

def map_domain_to_entity(user: UserDb) -> dict:
    return {
        "email": user.email,
        "password": user.password,
        "disabled": user.disabled
    }