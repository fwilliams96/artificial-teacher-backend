import base64
import os
import time

from fastapi import HTTPException
from shared.infrastructure.openai.whisper.whisper_speech_to_text_transcriber import WhisperSpeechToTextTranscriber

class SpeechToTextTranscriber:

    def __init__(self, external_speech_to_text_transcriber = WhisperSpeechToTextTranscriber()) -> None:
        self.external_speech_to_text_transcriber = external_speech_to_text_transcriber

    def transcribe(self, speech_base64: str) -> str:
        NANOts = time.time_ns() # generate to avoid clobber
        audio_filename = f"user_{NANOts}.wav"
        audio_bytes = self.base64_to_bytes(speech_base64)
        with open(f'{audio_filename}', 'wb') as buffer:
            buffer.write(audio_bytes)
        transcription = self.external_speech_to_text_transcriber.transcribe(audio_filename)
        self.delete_file(audio_filename)
        return transcription
    
    def base64_to_bytes(self, base64Text: str):
        try:
            audio_bytes = base64.b64decode(base64Text)
            return audio_bytes
        except Exception as e:
            raise HTTPException(status_code=400, detail="Invalid base64 data") from e
        
    def delete_file(self, filename: str):
     if os.path.isfile(filename):
        os.remove(filename)