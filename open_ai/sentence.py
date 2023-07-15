from bson import ObjectId
from fastapi import HTTPException, status
from db.client import db_client
from db.models.listening import Sentence, Word
from db.models.sentence import WordSentence
from db.models.user import User
from db.schemas.sentence import sentence_schema
from open_ai.general import check_is_valid_json_and_get_correct_json, get_agent_response, json_to_string, string_to_json
from open_ai.listening_planner import generate_audio_base64

json_format = {
    "sentence": "full sentence", 
    "comments": "your extra comments"
}

json_example_format = {
    "sentence": "The ancient ruins were destroyed", 
    "comments": "N/A"
}

sentence_writer_context = "You are a sentence writer and your job is to make up short sentences using a provided word."\
f"The response should follow this JSON format: {json_to_string(json_format)}"

sentence_writer_user_message = lambda topic: "Write a short sentence of 50 characters that contains this word: " + topic
sentence_writer_assistant = f"{json_to_string(json_example_format)}"

def create_sentence(word: str, user: User) -> WordSentence:
    messages=[{"role": "system", "content": sentence_writer_context}]
    messages.append({"role": "user", "content": sentence_writer_user_message("ruins")})
    messages.append({"role": "assistant", "content": sentence_writer_assistant})

    messages.append({"role": "user", "content": sentence_writer_user_message(word)})

    #agent_messages = fix_json_quotes(agent_messages)
    
    print(f"\n>>>>>>>>>>>>>>>>> [SENTENCE] Sent messages <<<<<<<<<<<<<<<<<<<\n")
    print(f"{messages} \n")
    agent_response = get_agent_response(messages, 50)
    print(f"\n>>>>>>>>>>>>>>>>> [SENTENCE] Received message <<<<<<<<<<<<<<<<<<<\n")
    print(f"{agent_response} \n")

    max_retries = 1
    retries = 0
    retry_messages = []
    retry_messages.extend(messages)
    valid_json, agent_response = check_is_valid_json_and_get_correct_json(agent_response)
    while (not valid_json) and (retries < max_retries):
        print(f"\n>>>>>>>>>>>>>>>>> [SENTENCE] Sent messages (retry) <<<<<<<<<<<<<<<<<<<\n")
        print(f"{retry_messages} \n")
        retry_messages.append({"role": "user", "content": "Return the response in the JSON format I asked you in the first message please."})
        agent_response = get_agent_response(retry_messages, 50)
        print(f"\n>>>>>>>>>>>>>>>>> [SENTENCE] Received messages (retry) <<<<<<<<<<<<<<<<<<<\n")
        print(f"{agent_response} \n")
        valid_json, agent_response = check_is_valid_json_and_get_correct_json(agent_response)
        retries += 1

    if retries == max_retries and not valid_json:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An internal error occurred generating the activity")

    agent_response_json = string_to_json(agent_response)
    messages.append({"role": "assistant", "content": agent_response_json})

    sentence = WordSentence(
        sentence=agent_response_json['sentence'],
        word=word,
        audio=generate_audio_base64(agent_response_json['sentence'])
    )

    save_sentence(sentence, user)

    return sentence

def save_sentence(word_sentence: WordSentence, user: User):
    word_sentence_db = {
        "word": word_sentence.word,
        "sentence": word_sentence.sentence,
        "user_id": ObjectId(user.id),
        "audio": word_sentence.audio
    }

    sentence_id = str(db_client.sentences.insert_one(word_sentence_db).inserted_id)
    word_sentence.id = sentence_id

    return word_sentence

def get_user_sentences(user: User) -> list[WordSentence]:
    sentences_db = db_client.sentences.find({"user_id": ObjectId(user.id)})
    return [build_word_sentence(sentence_db) for sentence_db in sentences_db]

def build_word_sentence(sentence_db: dict) -> WordSentence:
    sentence_db_schema = sentence_schema(sentence_db)
    return WordSentence(
        id=sentence_db_schema["id"],
        audio=sentence_db_schema["audio"],
        sentence=sentence_db_schema['sentence'],
        word=sentence_db_schema['word'],
        user_id=sentence_db_schema["user_id"]
    )

def generate_user_sentences(listening_sentences: list[Sentence], user: User):
    #words = [extract_words_from_sentence(sentence) for sentence in listening_sentences]
    words = []
    for sentence in listening_sentences:
        words.extend(extract_words_from_sentence(sentence))
    
    words = [word.word for word in words if word.askable and word.wrong]
    for word in words:
        create_sentence(word, user)

def extract_words_from_sentence(listening_sentence: Sentence) -> list[Word]:
    return listening_sentence.words