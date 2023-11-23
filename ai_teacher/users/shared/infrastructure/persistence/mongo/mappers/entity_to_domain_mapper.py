from datetime import datetime
from typing import Optional
from ai_teacher.users.shared.domain.user import User, UserDb

def map_entity_to_domain(user: dict) -> UserDb:
    return UserDb(
        id=str(user["_id"]),
        email=user["email"],
        disabled=user["disabled"],
        password=user["password"],
        first_name=user["first_name"],
        last_name=user["last_name"],
        level=user["level"],
        score=user["score"],
        last_image_generation=get_last_image_generation(user)
    )

def get_last_image_generation(user: dict) -> Optional[str]:
    if "last_image_generation" in user and user["last_image_generation"] != None:
        return datetime.strptime(user["last_image_generation"], '%Y-%m-%d %H:%M:%S')
    return None