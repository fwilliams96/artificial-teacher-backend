from fastapi import UploadFile, File
import whisper

model = whisper.load_model("base")

def transcribe(audio: UploadFile = File(...)) -> str:
    response = model.transcribe(audio=audio.filename, language="en")
    return response["text"]
