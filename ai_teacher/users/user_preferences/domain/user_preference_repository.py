import abc
from ai_teacher.users.user_preferences.domain.user_preference import UserPreference

class UserPreferenceRepository(abc.ABC):

    @abc.abstractclassmethod
    def find(self, client_id: str) -> list[UserPreference]:
        pass

    @abc.abstractclassmethod
    def create(self, user_preference: UserPreference) -> UserPreference:
        pass