import abc

class ExternalSpeechToTextTranscriber(abc.ABC):

    @abc.abstractclassmethod
    def transcribe(self, filename: str) -> str:
        pass