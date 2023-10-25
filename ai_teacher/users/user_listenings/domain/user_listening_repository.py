import abc
from typing import Optional
from ai_teacher.users.user_listenings.domain.user_listening import UserListening

class UserListeningRepository(abc.ABC):

    @abc.abstractclassmethod
    def save_listening(self, user_listening: UserListening):
        pass

    @abc.abstractclassmethod
    def update_listening(self, user_listening: UserListening) -> UserListening:
        pass

    @abc.abstractclassmethod
    def find_listening(self, user_listening_id: str) -> UserListening:
        pass

    @abc.abstractclassmethod
    def find_by_routine_id(self, user_routine_id: str) -> Optional[UserListening]:
        pass