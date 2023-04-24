import shutil
import time
from fastapi import APIRouter, HTTPException, Response, UploadFile, status, File
from db.models.chat import Context, Message
from chatgpt.talker import start_context_chatgpt, talk_chatgpt

from elevenlabs.speaker import text_to_speech
from whisper_tool.transcriptor import transcribe
import os

router = APIRouter(prefix='/chat', tags=["chat"], responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})

@router.post('/', response_model=Context, status_code=status.HTTP_200_OK)
def create_context(context: Context):
     try:
        return start_context_chatgpt(context)
     except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error generating context")

@router.post('/{context_id}/text-text', response_model=Message, status_code=status.HTTP_200_OK)
def chat_text_text(context_id: str, message: Message):
     try:
        return talk_chatgpt(context_id, message)
     except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error generating text")

@router.post('/{context_id}/text-voice', response_class=Response, status_code=status.HTTP_200_OK)
def chat_text_voice(context_id: str, message: Message):
     try:
        answer = talk_chatgpt(context_id, message)
        audio_bytes = text_to_speech(answer.content)
        return Response(content=audio_bytes, media_type="audio/wav")
     except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error generating audio")

@router.post('/{context_id}/voice-text', response_model=Message, status_code=status.HTTP_200_OK)
def chat_voice_text(context_id: str, audio: UploadFile = File(...)):
    NANOwav = time.time_ns() # generate to avoid clobber
    audio.filename = f"user_{NANOwav}.wav"

    try:
        with open(f'{audio.filename}', 'wb') as buffer:
            shutil.copyfileobj(audio.file, buffer)
            transcription = transcribe(audio)
            print(transcription)
            message = Message(content=transcription)
            answer = talk_chatgpt(context_id, message)
            return Message(content=answer.content, transcription=transcription)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error loading audio")
    finally:
        delete_file(audio.filename)

@router.post('/{context_id}/voice-voice', response_class=Response, status_code=status.HTTP_200_OK)
def chat_voice_voice(context_id: str, audio: UploadFile = File(...)):
    NANOwav = time.time_ns() # generate to avoid clobber
    audio.filename = f"user_{NANOwav}.wav"
    try:
        with open(f'{audio.filename}', 'wb') as buffer:
            shutil.copyfileobj(audio.file, buffer)
            transcription = transcribe(audio)
            print(transcription)
            message = Message(content=transcription)
            answer = talk_chatgpt(context_id, message)
            audio_answer_bytes = text_to_speech(answer.content)
            return Response(content=audio_answer_bytes, media_type="audio/wav")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error generating/loading audio")
    finally:
        delete_file(audio.filename)

def delete_file(filename: str):
     if os.path.isfile(filename):
        os.remove(filename)