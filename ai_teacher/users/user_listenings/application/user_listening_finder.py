from typing import Optional
from ai_teacher.users.user_listenings.domain.user_listening import UserListening
from ai_teacher.users.user_listenings.infrastructure.persistence.mongo.mongo_user_listening_repository import MongoUserListeningRepository

class UserListeningFinder:

    def __init__(self, user_listening_repository = MongoUserListeningRepository()) -> None:
        self.user_listening_repository = user_listening_repository

    def find(self, user_listening_id: str) -> UserListening:
        return self.user_listening_repository.find_listening(user_listening_id)
    
    def find_by_routine(self, user_routine_id: str) -> Optional[UserListening]:
        return self.user_listening_repository.find_by_routine_id(user_routine_id)