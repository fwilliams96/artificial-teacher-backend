from ai_teacher.users.shared.domain.user import UserDb
from ai_teacher.users.shared.domain.user_repository import UserRepository

class UserFinder:

    def __init__(self, user_repository = UserRepository()) -> None:
        self.user_repository = user_repository

    def find_user_by_email(self, email: str) -> UserDb | None:
        return self.user_repository.find_by_email(email)
    
    def find_user_by_id(self, user_id: str) -> UserDb | None:
        return self.user_repository.find_by_id(user_id)