import openai
from fastapi import APIRouter, HTTPException, status
from db.models.chat import ChatGPTAnswer, ChatGPTQuestion
from db.client import db_client
from db.schemas.conversation import conversation_schema
from bson import ObjectId

openai.api_key = "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"
router = APIRouter(prefix='/chat', tags=["chat"], responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})

initial_content_translator = "Eres un asistente de traducción de español a inglés" # Condicionar para que tenga un enfoque profesional
initial_content_useful = "Eres un asistente muy útil" # Condicionar para que tenga un enfoque profesional
initial_content_english_teacher = "Eres un asistente de idiomas para aprender inglés" # Condicionar para que tenga un enfoque profesional
initial_content_english_teacher2 = "Eres un experto en enseñar inglés y usar técnicas creativas para ello. Te pido que simulemos una conversación en inglés y en el momento en que me equivoque al escribir una palabra en inglés me devuelvas un ejemplo de frase con la palabra escrita correctamente y a continuación un flashcard con otro ejemplo de frase incompleta donde sea yo quién tenga que completarlo con la palabra, usa el guión bajo para representar la palabra faltante. Para diferenciar entre distintos tipos de mensajes vas a responderme un formato JSON donde content sea el mensaje de texto y type el tipo de mensaje, el type será 'message' cuando sea texto normal, si en cambio es una flashcard, el type será 'flashcard'" # Condicionar para que tenga un enfoque profesional

#messages=[{"role": "system", "content": initial_content_translator}] 
#messages=[{"role": "system", "content": initial_content_useful}] # Condicionar para que tenga un enfoque profesional
#messages=[{"role": "system", "content": initial_content_english_teacher}] 

# Condicionar para que tenga un enfoque profesional

@router.post('/', response_model=ChatGPTAnswer, status_code=status.HTTP_200_OK)
async def ask(question: ChatGPTQuestion):
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
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Your user has exceed the quota")

@router.post('/teacher', response_model=ChatGPTAnswer, status_code=status.HTTP_200_OK)
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
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Your user has exceed the quota")

def recover_conversation_messages(context_id: str) -> list:
        conversation_db = db_client.conversations.find_one({"_id": ObjectId(context_id)})
        if not conversation_db:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Context not found")
        conversation = conversation_schema(conversation_db)
        return conversation['messages']

def update_conversation_and_get_context_id(context_id: str, messages: list):
        conversation = {
                "messages": messages
        }
        db_client.conversations.find_one_and_replace({"_id": ObjectId(context_id)}, conversation)
        return context_id

def create_conversation_and_get_context_id(messages: list) -> str:
        conversation = {
                "messages": messages
        }
        return str(db_client.conversations.insert_one(conversation).inserted_id)