import abc

class ExternalTextToSpeechTransformer(abc.ABC):

    @abc.abstractclassmethod
    def transform(text: str) -> bytes:
        pass