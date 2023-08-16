import abc
from ai_teacher.activities.listening.domain.listening import Sentence

class ExternalSentenceGenerator(abc.ABC):

    @abc.abstractclassmethod
    def generate(topic: str) -> Sentence:
        pass