import abc

class ExternalSentenceGenerator(abc.ABC):

    @abc.abstractclassmethod
    def generate(topic: str) -> str:
        pass