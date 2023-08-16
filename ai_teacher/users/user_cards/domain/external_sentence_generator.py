import abc
from ai_teacher.users.user_cards.domain.user_card import UserCard

class ExternalSentenceGenerator(abc.ABC):

    @abc.abstractclassmethod
    def generate(self, word: str) -> str:
        pass