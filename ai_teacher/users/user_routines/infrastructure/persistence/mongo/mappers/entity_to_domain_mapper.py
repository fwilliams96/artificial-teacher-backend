from datetime import datetime
from ai_teacher.users.user_routines.domain.user_routine import UserRoutine

def map_entity_to_domain(user_routine: dict) -> UserRoutine:
    return UserRoutine(
        id=str(user_routine["_id"]),
        user_id=str(user_routine["user_id"]),
        creation_date=datetime.strptime(user_routine["creation_date"], '%Y-%m-%d %H:%M:%S'),
        active=user_routine["active"]
    )