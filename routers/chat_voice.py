import shutil
from fastapi import APIRouter, status, UploadFile, File
from db.models.chat import Message
from chatgpt.talker import talk_chatgpt
from elevenlabs.speaker import text_to_speech
from whisper_tool.transcriptor import transcribe
from fastapi.responses import FileResponse
from fastapi.concurrency import run_in_threadpool

router = APIRouter(prefix='/chat-voice', tags=["chat-voice"], responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})

@router.post('/{context_id}/text', response_model=Message, status_code=status.HTTP_200_OK)
async def chat_voice_text(context_id: str, audio: UploadFile = File(...)):
    print(f'Audio filename: {audio.filename}')
    print(f'Context id: {context_id}')
    with open(f'{audio.filename}', 'wb') as buffer:
        shutil.copyfileobj(audio.file, buffer)
        transcription = transcribe(audio)
        # buffer.write(audio.file.read())

        # response = model.transcribe(audio=audio.filename, language="en")
        # transcription = response['text']
        print(transcription)

        message = Message(content=transcription)

        answer = talk_chatgpt(context_id, message)
        return Message(content=answer.content, transcription=transcription)

@router.post('/{context_id}/voice', response_class=FileResponse, status_code=status.HTTP_200_OK)
async def chat_voice_voice(context_id: str, audio: UploadFile = File(...)):
    print(f'Audio filename: {audio.filename}')
    print(f'Context id: {context_id}')
    with open(f'{audio.filename}', 'wb') as buffer:
        shutil.copyfileobj(audio.file, buffer)
        transcription = transcribe(audio)
        # buffer.write(audio.file.read())

        # response = model.transcribe(audio=audio.filename, language="en")
        # transcription = response['text']
        print(transcription)

        message = Message(content=transcription)

        answer = talk_chatgpt(context_id, message)
        audio_answer = text_to_speech(answer.content)
        # Guarda el contenido de audio en un archivo temporal (cambia la extensión según el formato de audio)
        with open("temp_audio.mp3", "wb") as f:
            f.write(audio_answer)

        return FileResponse("temp_audio.mp3", media_type="audio/mpeg")

'''@router.post('/', status_code=status.HTTP_200_OK)
async def upload_file(audio: UploadFile = File(...)):
    print(audio.filename)
    with open(f'{audio.filename}', 'wb') as buffer:
        shutil.copyfileobj(audio.file, buffer)
        response = openai.Audio.transcribe(
                api_key="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",
                model="whisper-1",
                file=buffer
        )
        print(response)
        print(audio)
        return { "file_name": audio.filename}
'''
'''
async def upload_file(audio: UploadFile = File(...)):
    with open(f'{audio.filename}', 'rb') as buffer:
        buffer.write(audio.file.read())
        response = openai.Audio.transcribe(
                api_key="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",
                model="whisper-1",
                file=buffer
        )
        print(response)
        print(audio)
        return { "file_name": audio.filename}'''