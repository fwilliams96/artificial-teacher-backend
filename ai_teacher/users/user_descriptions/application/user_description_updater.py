from ai_teacher.users.user_descriptions.domain.user_description import UserDescription
from ai_teacher.users.user_descriptions.infrastructure.persistence.mongo_user_description_repository import MongoUserDescriptionRepository

class UserDescriptionUpdater:

    def __init__(self, user_description_repository = MongoUserDescriptionRepository()) -> None:
        self.user_description_repository = user_description_repository

    def update(self, user_description: UserDescription) -> UserDescription:
        return self.user_description_repository.update_description(user_description)