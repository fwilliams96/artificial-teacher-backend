from ai_teacher.users.shared.domain.user import UserDb
from ai_teacher.users.shared.infrastructure.persistence.mongo.mongo_user_repository import MongoUserRepository

class UserFinder:

    def __init__(self, user_repository = MongoUserRepository()) -> None:
        self.user_repository = user_repository

    def find_user_by_email(self, email: str) -> UserDb | None:
        return self.user_repository.find_by_email(email)
    
    def find_user_by_id(self, user_id: str) -> UserDb | None:
        return self.user_repository.find_by_id(user_id)
    
    def find_top_users(self):
        top_users = self.user_repository.find_all()
        if len(top_users) > 5:
            top_users = top_users[0:5]
        return top_users