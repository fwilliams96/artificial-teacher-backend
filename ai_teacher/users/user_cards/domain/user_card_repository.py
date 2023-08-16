import abc
from ai_teacher.users.user_cards.domain.user_card import UserCard

class UserCardRepository(abc.ABC):

    @abc.abstractclassmethod
    def save(self, user_card: UserCard) -> UserCard:
        pass

    @abc.abstractclassmethod
    def find_all(self, user_id: str) -> list[UserCard]:
        pass