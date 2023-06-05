import base64
import random

from fastapi import HTTPException, status
from db.client import db_client
from bson import ObjectId
from db.models.listening import Listening, Sentence, Word
from db.schemas.listening import listening_schema
from elevenlabs.speaker import text_to_speech

from open_ai.general import check_is_valid_json_and_get_correct_json, get_agent_response, json_to_string, string_to_json

json_format = {
    "sentence": "full sentence", 
    "comments": "your extra comments"
}

json_example_format = {
    "sentence": "The cat meowed", 
    "comments": "N/A"
}

sentence_writer_context = "You are a sentence writer and your job is to make up short sentences based on a provided topic."\
f"The response should follow this JSON format: {json_to_string(json_format)}"

sentence_writer_assistant = f"{json_to_string(json_example_format)}"

sentence_writer_user_message = lambda topic: "Write a short sentence of 50 characters based on " + topic

def save_listening(listening: Listening) -> Listening:

    listening_db = {
        "topic": listening.topic
    }

    listening_id = str(db_client.listenings.insert_one(listening_db).inserted_id)
    listening.id = listening_id

    return listening

def generate_sentence(sentence_id: str, topic: str) -> Sentence:
    messages=[{"role": "system", "content": sentence_writer_context}]
    messages.append({"role": "user", "content": sentence_writer_user_message("cats")})
    messages.append({"role": "assistant", "content": sentence_writer_assistant})
    messages.append({"role": "user", "content": sentence_writer_user_message(topic)})

    #agent_messages = fix_json_quotes(agent_messages)
    
    print(f"\n>>>>>>>>>>>>>>>>> [LISTENING] Sent messages <<<<<<<<<<<<<<<<<<<\n")
    print(f"{messages} \n")
    agent_response = get_agent_response(messages, 50)
    print(f"\n>>>>>>>>>>>>>>>>> [LISTENING] Received message <<<<<<<<<<<<<<<<<<<\n")
    print(f"{agent_response} \n")

    max_retries = 1
    retries = 0
    retry_messages = []
    retry_messages.extend(messages)
    valid_json, agent_response = check_is_valid_json_and_get_correct_json(agent_response)
    while (not valid_json) and (retries < max_retries):
        print(f"\n>>>>>>>>>>>>>>>>> [LISTENING] Sent messages (retry) <<<<<<<<<<<<<<<<<<<\n")
        print(f"{retry_messages} \n")
        retry_messages.append({"role": "user", "content": "Return the response in the JSON format I asked you in the first message please."})
        agent_response = get_agent_response(retry_messages, 50)
        print(f"\n>>>>>>>>>>>>>>>>> [LISTENING] Received messages (retry) <<<<<<<<<<<<<<<<<<<\n")
        print(f"{agent_response} \n")
        valid_json, agent_response = check_is_valid_json_and_get_correct_json(agent_response)
        retries += 1

    if retries == max_retries and not valid_json:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An internal error occurred generating the activity")

    agent_response_json = string_to_json(agent_response)
    messages.append({"role": "assistant", "content": agent_response_json})

    sentence = Sentence(
        id=sentence_id,
        sentence=agent_response_json['sentence'],
        audio=generate_audio_base64(agent_response_json['sentence']),
        words=generate_words(agent_response_json['sentence'])
    )

    return sentence

def generate_words(sentence: str) -> list[Word]:

    words_str = sentence.split(" ")
    words = [{}]*len(words_str) # TODO check that minimum there is one writable word
    any_writable_word = False

    for word_index in range(len(words_str)):
        writable_word = random.choice([True, False])
        if writable_word:
            words[word_index] = Word(value=words_str[word_index], writable=True)
            any_writable_word = True
        else:
            words[word_index] = Word(value=words_str[word_index], writable=False)

    if not any_writable_word:
        words[0].writable = True

    return words

def update_listening(listening_id: str, sentences: list[Sentence]) -> list[Sentence]:
    update_operation = {"$push": {"sentences": {"$each": [build_sentence_db(sentence) for sentence in sentences]}}}
    db_client.listenings.update_one({"_id": ObjectId(listening_id)}, update_operation)

def build_sentence_db(sentence: Sentence):
    return {
        "id": sentence.id,
        "sentence": sentence.sentence
    }

def recover_listening_sentence(listening_id: str, sentence_id: str) -> Sentence:
    listening = recover_listening(listening_id)
    
    num_sentences = len(listening.sentences)
    if num_sentences == 0 or num_sentences <= sentence_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sentence not found")

    return listening.sentences[sentence_id]

def recover_listening(listening_id: str) -> Listening:
    if listening_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listening not found")
    
    check_listening_exists(listening_id)
    listening_db = db_client.listenings.find_one({"_id": ObjectId(listening_id)})
    return Listening(**listening_schema(listening_db))

def check_listening_exists(context_id: str):
    listening_db = db_client.listenings.find_one({"_id": ObjectId(context_id)})
    if not listening_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Context not found")

def generate_audio_base64(sentence: str):
    try:
        audio_bytes = text_to_speech(sentence)
        return bytes_to_base64(audio_bytes)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error generating audio")

def bytes_to_base64(audio_bytes):
    encoded_string = base64.b64encode(audio_bytes).decode('utf-8')
    return encoded_string