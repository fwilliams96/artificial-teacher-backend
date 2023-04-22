from fastapi import HTTPException, status
import openai
from db.models.chat import Message, Context
from db.client import db_client
from db.schemas.conversation import conversation_schema
from bson import ObjectId
from chatgpt_config import API_KEY

openai.api_key = API_KEY

initial_content_translator = "Eres un asistente de traducción de español a inglés" # Condicionar para que tenga un enfoque profesional
initial_content_useful = "Eres un asistente muy útil" # Condicionar para que tenga un enfoque profesional
initial_content_english_teacher = "Eres un asistente de idiomas para aprender inglés" # Condicionar para que tenga un enfoque profesional

initial_content_english_teacher2 = "Eres un asistente experto en enseñar inglés y por ello te pido que simulemos una conversación en inglés. "\
"Vas a ser corregirme si digo algo incorrecto y además me añaderás un flashcard para practicar."\
"Te pido que todas tus respuestas sigan la siguiente estructura JSON: { \"response\": tu respuesta, \"flashcard\": tu flashcard si hay }."
"Te pido que todas tus respuestas sigan la siguiente estructura JSON: { \"response\": tu respuesta, \"flashcard\": tu flashcard si hay, \"type\": 'message' en caso de respuesta normal o 'flashcard' en caso de ser un flashcard }."

initial_content_english_teacher3 = "Eres un asistente experto en enseñar inglés y por ello te pido que simulemos una conversación en inglés. "\
"Empieza primero presentándote con una pregunta, cuando yo te responda me das retroalimentación y me vuelves a preguntar una vez te haya contestado. "\
"Cuando diga algo incorrecto, me lo vas a decir y además me vas a enviar un flashcard para practicar la palabra. "\
"MUY importante, voy a usar una API para invocar tus servicios, por lo que te pido que tus respuestas sigan esta estructura JSON: { \"response\": tu respuesta, \"flashcard\": tu flashcard si hay }."

initial_content_english_teacher4 = "Eres un asistente experto en enseñar inglés y por ello te pido que simulemos una conversación en inglés. "\
"MUY importante, voy a usar una API para invocar tus servicios, por lo que te pido que tus respuestas sigan esta estructura JSON: { \"response\": tu respuesta, \"flashcard\": tu flashcard si hay }."
"Empieza primero presentándote con una pregunta, cuando yo te responda me das retroalimentación y me vuelves a preguntar una vez te haya contestado. "\
"Cuando diga algo incorrecto, me lo vas a decir y además me vas a enviar un flashcard para practicar la palabra. " #Works OK

initial_content_english_teacher5 = "Eres un asistente experto en enseñar inglés y por ello te pido que simulemos una conversación en inglés. "\
"Antes de empezar, muy importante, voy a usar una API por lo que te pido que tus respuestas sigan esta estructura JSON: { \"response\": tu respuesta, \"flashcard\": tu flashcard si hay }."
"Aclarado esto, empieza primero presentándote con una pregunta, cuando yo te responda me das retroalimentación y me vuelves a preguntar una vez te haya contestado. "\
"Cuando diga algo incorrecto, me lo vas a señalar y además me vas a enviar un flashcard para practicar la palabra. El flashcard irá en el atributo flashcard del JSON comentado anteriormente, la respuesta irá en el atributo response."

initial_content_english_teacher6 = "Eres un asistente experto en enseñar inglés y por ello te pido que simulemos una conversación en inglés. "\
"MUY importante, voy a usar una API para invocar tus servicios, por lo que te pido que tus respuestas sigan esta estructura JSON: { \"response\": tu respuesta, \"flashcard\": tu flashcard si hay }."
"Empieza primero presentándote con una pregunta y cuando yo te responda me vuelves a preguntar. "\
"Cuando diga algo incorrecto, me lo vas a decir y además me vas a enviar un flashcard para practicar la palabra. "

initial_content_english_teacher7 = "Eres un asistente experto en enseñar inglés y por ello te pido que simulemos una conversación en inglés. "\
"Genera una respuesta JSON con la siguiente estructura: { \"response\": tu respuesta, \"flashcard\": tu flashcard si hay }. "\
"Empieza primero presentándote con una pregunta, cuando yo te responda me das retroalimentación y me vuelves a preguntar una vez te haya contestado. "\
"Cuando diga algo incorrecto, me lo vas a decir y además me vas a enviar un flashcard para practicar la palabra. " #Works OK

initial_content_english_teacher8 = "Eres un asistente experto en enseñar inglés y por ello te pido que simulemos una conversación en inglés. "\
"MUY importante, voy a usar una API para invocar tus servicios, por lo que te pido que tus respuestas sigan esta estructura JSON: { \"response\": tu respuesta, \"flashcard\": tu flashcard si hay }."\
"Empieza primero presentándote con una pregunta, cuando yo te responda me das retroalimentación y me vuelves a preguntar una vez te haya contestado. "\
"Cuando diga algo incorrecto, me lo vas a decir y además me vas a enviar un flashcard para practicar la palabra. " #Works OK

initial_content_english_teacher9 = "You are an expert assistant in teaching English and therefore I ask you to simulate a conversation in English. "\
"VERY important, I'm going to use an API to invoke your services, so I ask that your responses follow this JSON structure: { \"response\": your response, \"flashcard\": your flashcard if any }." \
"Start first by introducing yourself with a question, when I answer you give me feedback and ask me again once I have answered you. "\
"When I say something wrong, you are going to tell me and you are also going to send me a flashcard to practice the word."

initial_content_english_teacher10 = "You are an expert assistant in teaching English and therefore I ask you to simulate a conversation in English. "\
"VERY important, I ask you to follow this JSON structure: { \"response\": your response, \"flashcard\": your flashcard if any }." \
"Start first by introducing yourself with a question, when I answer you give me feedback and ask me again once I have answered you. "\
"When I say something wrong, you are going to tell me and you are also going to send me a flashcard to practice the word."

initial_content_english_teacher11 = "You are an expert assistant in teaching English and therefore I ask you to simulate a conversation in English. "\
"Start first by introducing yourself with a question, when I answer you give me feedback and ask me again once I have answered you. "\
"Important, when I say something wrong, you will start your answer with an 'Oops, flashcard time', followed by a flashcard to practice the wrong word." #OK

initial_content_english_teacher12 = "You are an expert assistant in teaching English and therefore I ask you to simulate a conversation in English. "\
"Important, when I say something wrong, you will start your answer with an 'Flashcard time', followed by a flashcard to practice the wrong word. "\
"Start first by introducing yourself with a question, when I answer you give me feedback and ask me again once I have answered you. "\
"Introduce creative activities while we discuss."

initial_content_english_teacher13 = "You are an expert assistant in teaching English and therefore I ask you to simulate a conversation in English. "\
"Important, when I say something wrong, you will start your answer with an 'Flashcard time', followed by a flashcard to practice the wrong word. "\
"The flashcard will consist in an sentence with the a missing word that I must complete with the wrong word (but in the correct way)."\
"Start first by introducing yourself with a question, when I answer you give me feedback and ask me again once I have answered you. "\
"Introduce creative activities while we discuss."

initial_content_english_teacher14 = "You are an English expert teacher and your job is to have a conversation with me in English. "\
"If I write something incorrect, create a flashcard using the right word or phrase. "\
"Introduce creative activities while we discuss."

initial_content_english_teacher15 = "You are an English expert teacher and your job is to have a conversation with me in English. "\
"You have to be strict, when I write something incorrect, create a flashcard using the right word or phrase. "\
"Finally, introduce creative activities while we discuss."

def start_context_chatgpt(context: Context) -> Context:
    messages=[{"role": "system", "content": initial_content_english_teacher15}] 
    messages.append({"role": "user", "content": context.content})
    chatgpt_response = send_messages_chatgpt(messages)
    messages.append({"role": "assistant", "content": chatgpt_response})
    context_id = create_conversation_and_get_context_id(messages)
    return Context(context_id=context_id, content=chatgpt_response)

def talk_chatgpt(context_id: str, message: Message) -> Message:
    check_conversation_exists(context_id)
    messages = recover_conversation_messages(context_id)
    messages.append({"role": "user", "content": message.content})
    chatgpt_response = send_messages_chatgpt(messages)
    messages.append({"role": "assistant", "content": chatgpt_response})
    context_id = update_conversation(context_id, messages)
    return Message(content=chatgpt_response)

def send_messages_chatgpt(messages: list) -> str:
    try:
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        response_content = response.choices[0].message.content
        return response_content
        '''return messages
        if context_id != None:
            context_id = update_conversation_and_get_context_id(message.context_id, messages)
        else:
            context_id = create_conversation_and_get_context_id(messages)
        answer = {
            "context_id": context_id,
            "content": response_content
        }
        # print(messages)
        return Message(**answer)'''
    except openai.error.RateLimitError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Your user has exceed the quota")

def check_conversation_exists(context_id: str):
    conversation_db = db_client.conversations.find_one({"_id": ObjectId(context_id)})
    if not conversation_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Context not found")

def create_conversation_and_get_context_id(messages: list) -> str:
    conversation = {
        "messages": messages
    }
    return str(db_client.conversations.insert_one(conversation).inserted_id)

def recover_conversation_messages(context_id: str) -> list:
    conversation_db = db_client.conversations.find_one({"_id": ObjectId(context_id)})
    if not conversation_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Context not found")
    conversation = conversation_schema(conversation_db)
    return conversation['messages']

def update_conversation(context_id: str, messages: list):
    conversation = {
        "messages": messages
    }
    db_client.conversations.find_one_and_replace({"_id": ObjectId(context_id)}, conversation)

