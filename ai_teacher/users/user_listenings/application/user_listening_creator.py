from ai_teacher.users.user_listenings.domain.user_listening import UserListening
from ai_teacher.users.user_listenings.infrastructure.persistence.mongo.mongo_user_listening_repository import MongoUserListeningRepository

class UserListeningCreator:

    def __init__(self, user_listening_repository = MongoUserListeningRepository()) -> None:
        self.user_listening_repository = user_listening_repository

    def create(self, user_listening: UserListening) -> UserListening:
        return self.user_listening_repository.save_listening(user_listening)