from shared.domain.external_text_to_speech_transformer import ExternalTextToSpeechTransformer
from shared.infrastructure.elevenlabs.client.elevenlabs_client import text_to_speech

class ElevenlabsTextToSpeechTransformer(ExternalTextToSpeechTransformer):

    def transform(text: str) -> bytes:
        return text_to_speech(text)