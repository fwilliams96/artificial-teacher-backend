import abc
from ai_teacher.activities.listening.domain.listening import Listening

class ListeningRepository(abc.ABC):

    @abc.abstractclassmethod
    def save(self, listening: Listening):
        pass

    @abc.abstractclassmethod
    def find(self, listening_id: str) -> Listening | None:
        pass