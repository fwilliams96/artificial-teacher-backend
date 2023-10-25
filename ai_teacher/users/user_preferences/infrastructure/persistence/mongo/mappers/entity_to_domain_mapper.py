from ai_teacher.users.user_preferences.domain.user_preference import UserPreference

def map_entity_to_domain(user_preference: dict) -> UserPreference:
    return UserPreference(
        id=str(user_preference["_id"]),
        preference_id=str(user_preference['preference_id']),
        user_id=str(user_preference['user_id'])
    )