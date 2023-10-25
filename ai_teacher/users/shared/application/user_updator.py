from fastapi import HTTPException, status
from ai_teacher.users.shared.application.user_finder import UserFinder
from ai_teacher.users.shared.domain.user import User
from ai_teacher.users.shared.infrastructure.persistence.mongo.mongo_user_repository import MongoUserRepository

class UserUpdator:

    def __init__(self, user_finder = UserFinder(), user_repository = MongoUserRepository()) -> None:
        self.user_finder = user_finder
        self.user_repository = user_repository

    def update(self, user: User) -> User:
        if self.user_finder.find_user_by_id(id) is None or id != user.id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")
        user_db = self.user_repository.update(user)
        return User(
            id=user_db.id,
            disabled=user_db.disabled,
            email=user_db.email,
            first_name=user_db.first_name,
            last_name=user_db.last_name,
            level=user_db.level,
            score=user_db.score
        )