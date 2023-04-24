from fastapi import APIRouter, status
from db.models.chat import Message
from open_ai.talker import talk_chatgpt
from fastapi.responses import FileResponse
from elevenlabs.speaker import text_to_speech

router = APIRouter(prefix='/chat-text', tags=["chat-text"], responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})

@router.post('/{context_id}/text', response_model=Message, status_code=status.HTTP_200_OK)
async def chat_text_text(context_id: str, message: Message):
        return talk_chatgpt(context_id, message)

@router.post('/{context_id}/audio', response_class=FileResponse, status_code=status.HTTP_200_OK)
async def chat_text_audio(context_id: str, message: Message):
        answer = talk_chatgpt(context_id, message)
        audio = text_to_speech(answer.content)
        # Guarda el contenido de audio en un archivo temporal (cambia la extensión según el formato de audio)
        with open("temp_audio.mp3", "wb") as f:
            f.write(audio)

        return FileResponse("temp_audio.mp3", media_type="audio/mpeg")

'''@router.post('/teacher', response_model=ChatGPTAnswer, status_code=status.HTTP_200_OK)
async def teacher(question: ChatGPTQuestion):

        context_id = question.context_id
        messages = []
        if  context_id != None:
                messages = recover_conversation_messages(question.context_id)
        else:
                messages=[{"role": "system", "content": initial_content_useful}] 
        messages.append({"role": "user", "content": question.content})
        try:
                response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
                response_content = response.choices[0].message.content
                messages.append({"role": "assistant", "content": response_content})
                if context_id != None:
                        context_id = update_conversation_and_get_context_id(question.context_id, messages)
                else:
                        context_id = create_conversation_and_get_context_id(messages)
                answer = {
                        "context_id": context_id,
                        "content": response_content
                }
                # print(messages)
                return ChatGPTAnswer(**answer)
        except openai.error.RateLimitError:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Your user has exceed the quota")'''