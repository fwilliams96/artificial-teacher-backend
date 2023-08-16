import abc
from ai_teacher.users.user_listenings.domain.user_listening import UserListening

class UserListeningRepository(abc.ABC):

    @abc.abstractclassmethod
    def save_listening(self, user_listening: UserListening):
        pass