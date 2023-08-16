import abc
from ai_teacher.users.shared.domain.user import User, UserDb

class UserRepository(abc.ABC):

    @abc.abstractclassmethod
    def create(self, user: UserDb) -> User:
        pass
    
    @abc.abstractclassmethod
    def update(self, user: UserDb) -> User:
        pass

    @abc.abstractclassmethod
    def find_by_email(self, email: str) -> UserDb | None:
        pass

    @abc.abstractclassmethod
    def find_by_id(self, user_id: str) -> UserDb | None:
        pass