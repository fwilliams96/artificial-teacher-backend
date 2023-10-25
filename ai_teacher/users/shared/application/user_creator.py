from fastapi import HTTPException, status
from ai_teacher.users.shared.application.user_finder import UserFinder
from ai_teacher.users.shared.domain.user import User, UserDb
from ai_teacher.users.shared.infrastructure.persistence.mongo.mongo_user_repository import MongoUserRepository

class UserCreator:

    def __init__(self, user_finder = UserFinder(), user_repository = MongoUserRepository()) -> None:
        self.user_finder = user_finder
        self.user_repository = user_repository

    def create(self, user: UserDb) -> User:
        if self.user_finder.find_user_by_email(user.email) != None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
        user.score = 0
        user.level = 1
        user_db = self.user_repository.create(user)
        return User(
            id=user_db.id,
            disabled=user_db.disabled,
            email=user_db.email,
            first_name=user_db.first_name,
            last_name=user_db.last_name,
            level=user_db.level,
            score=user_db.score
        )