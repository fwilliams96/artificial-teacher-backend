from bson import ObjectId
from ai_teacher.users.user_preferences.domain.user_preference import UserPreference

def map_domain_to_entity(user_preference: UserPreference) -> dict:
    return {
        "preference_id": ObjectId(user_preference.preference_id),
        "user_id": ObjectId(user_preference.user_id)
    }