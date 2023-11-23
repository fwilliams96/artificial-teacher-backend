import abc
from typing import Optional
from ai_teacher.users.user_descriptions.domain.user_description import UserDescription

class UserDescriptionRepository(abc.ABC):

    @abc.abstractclassmethod
    def save_description(self, user_description: UserDescription):
        pass

    @abc.abstractclassmethod
    def update_description(self, user_description: UserDescription) -> UserDescription:
        pass

    @abc.abstractclassmethod
    def find_description(self, user_description_id: str) -> UserDescription:
        pass

    @abc.abstractclassmethod
    def find_by_routine_id(self, user_routine_id: str) -> list[UserDescription]:
        pass