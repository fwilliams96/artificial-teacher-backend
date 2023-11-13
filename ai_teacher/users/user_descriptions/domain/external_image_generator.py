import abc

class ExternalImageGenerator(abc.ABC):

    @abc.abstractclassmethod
    def generate(self, topic: str) -> str:
        pass