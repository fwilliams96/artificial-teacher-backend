from io import BufferedWriter
import openai

from openai_config import API_KEY
openai.api_key = API_KEY

def transcribe(filename: str) -> str:
    with open(filename, "rb") as audio_file:
        response = openai.Audio.transcribe("whisper-1", audio_file)
        return response["text"]
