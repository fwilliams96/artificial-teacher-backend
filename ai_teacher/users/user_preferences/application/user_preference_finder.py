from ai_teacher.users.user_preferences.domain.user_preference import UserPreference
from ai_teacher.users.user_preferences.infrastructure.persistence.mongo.mongo_user_preference_repository import MongoUserPreferenceRepository

class UserPreferenceFinder:

    def __init__(self, user_preference_repository = MongoUserPreferenceRepository()) -> None:
        self.user_preference_repository = user_preference_repository

    def get_preferences(self, user_id: str) -> list[UserPreference]:
        return self.user_preference_repository.find(user_id)
