from bson import ObjectId
from ai_teacher.users.user_routines.domain.user_routine import UserRoutine

def map_domain_to_entity(user_routine: UserRoutine) -> dict:
    return {
        "user_id": ObjectId(user_routine.user_id),
        "creation_date": user_routine.creation_date.strftime('%Y-%m-%d %H:%M:%S'),
        "active": user_routine.active
    }