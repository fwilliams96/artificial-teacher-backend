import base64
from shared.infrastructure.elevenlabs.elevenlabs_text_to_speech_transformer import ElevenlabsTextToSpeechTransformer

class TextToSpeechTransformer:

    def __init__(self, external_text_to_speech_transformer = ElevenlabsTextToSpeechTransformer()) -> None:
        self.external_text_to_speech_transformer = external_text_to_speech_transformer

    def transform(self, text: str) -> bytes:
        return self.external_text_to_speech_transformer.transform(text)

    def transform_to_base64(self, text: str) -> str:
        speech_bytes = self.external_text_to_speech_transformer.transform(text)
        return base64.b64encode(speech_bytes).decode('utf-8')