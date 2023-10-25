from bson import ObjectId
from ai_teacher.users.user_listenings.domain.user_listening import UserListening, UserSentence, UserWord

def map_domain_to_entity(user_listening: UserListening) -> dict:
    return {
        "topic": user_listening.topic,
        "user_id": ObjectId(user_listening.user_id),
        "finished": user_listening.finished,
        "sentences": [map_sentence_domain_to_entity(sentence) for sentence in user_listening.sentences],
        "routine_id": ObjectId(user_listening.routine_id) if user_listening.routine_id != None else None
    }

def map_sentence_domain_to_entity(user_listening_sentence: UserSentence) -> dict:
    return {
        "words": [map_sentence_word_domain_to_entity(word) for word in user_listening_sentence.words],
        "sentence": user_listening_sentence.sentence,
        "audio": user_listening_sentence.audio
    }

def map_sentence_word_domain_to_entity(user_listening_word: UserWord) -> dict:
    return {
        "word": user_listening_word.word,
        "is_word": user_listening_word.is_word,
        "askable": user_listening_word.askable,
        "wrong": user_listening_word.wrong
    }