from fastapi.responses import FileResponse
import requests
from elevenlabs_config import API_KEY, URL, TEXT_TO_SPEECH_ENDPOINT, VOICE_ID

def text_to_speech(text: str) -> FileResponse:
    headers = {"xi-api-key": API_KEY}
    body = {
        "text": text,
        "voice_settings": {
            "stability": 0.75,
            "similarity_boost": 0.75
        }
    }

    stream = "/stream"
    response = requests.post(f'{URL}{TEXT_TO_SPEECH_ENDPOINT}{VOICE_ID}', headers=headers, json=body)
    return response.content