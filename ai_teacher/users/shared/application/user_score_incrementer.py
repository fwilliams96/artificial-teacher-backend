from ai_teacher.users.shared.infrastructure.persistence.mongo.mongo_user_repository import MongoUserRepository

class UserScoreIncrementer():

    def __init__(self, user_repository = MongoUserRepository()) -> None:
        self.user_repository = user_repository

    def increment(self, user_id: str, score: int):
        self.user_repository.increment_score(user_id, score)