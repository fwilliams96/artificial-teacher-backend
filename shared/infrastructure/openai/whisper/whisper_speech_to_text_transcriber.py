from shared.domain.external_speech_to_text_transcriber import ExternalSpeechToTextTranscriber
from shared.infrastructure.openai.client.openai_client import transcribe_audio_to_text

class WhisperSpeechToTextTranscriber(ExternalSpeechToTextTranscriber):
    def __init__(self) -> None:
        pass

    def transcribe(self, filename: str) -> str:
        with open(filename, "rb") as audio_file:
            return transcribe_audio_to_text(audio_file)