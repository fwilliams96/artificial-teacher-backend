import abc

class ExternalTextToSpeechTransformer(abc.ABC):

    @abc.abstractclassmethod
    def transform(self, text: str) -> bytes:
        pass