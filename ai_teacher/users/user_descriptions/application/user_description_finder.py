from typing import Optional
from ai_teacher.users.user_descriptions.domain.user_description import UserDescription
from ai_teacher.users.user_descriptions.infrastructure.persistence.mongo_user_description_repository import MongoUserDescriptionRepository

class UserDescriptionFinder:

    def __init__(self, user_description_repository = MongoUserDescriptionRepository()) -> None:
        self.user_description_repository = user_description_repository

    def find(self, user_description_id: str) -> Optional[UserDescription]:
        return self.user_description_repository.find_description(user_description_id)
    
    def find_by_routine(self, user_routine_id: str) -> Optional[UserDescription]:
        return self.user_description_repository.find_by_routine_id(user_routine_id)