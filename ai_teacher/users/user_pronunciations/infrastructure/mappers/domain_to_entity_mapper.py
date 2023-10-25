from typing import Optional
from bson import ObjectId
from ai_teacher.users.user_pronunciations.domain.user_pronunciation import UserPronunciation, Sentence, SentenceWord

def map_domain_to_entity(user_pronunciation: UserPronunciation) -> dict:
    return {
        "topic": user_pronunciation.topic,
        "user_id": ObjectId(user_pronunciation.user_id),
        "finished": user_pronunciation.finished,
        "sentence": map_sentence_domain_to_entity(user_pronunciation.sentence),
        "user_speech": get_user_speech(user_pronunciation),
        "routine_id": ObjectId(user_pronunciation.routine_id) if user_pronunciation.routine_id != None else None
    }

def get_user_speech(user_pronunciation: UserPronunciation) -> dict:
    if user_pronunciation.user_speech != None:
        return {
            "audio": user_pronunciation.user_speech.audio    
        }
    return None

def map_sentence_domain_to_entity(user_pronunciation_sentence: Sentence) -> dict:
    return {
        "words": [map_sentence_word_domain_to_entity(word) for word in user_pronunciation_sentence.words],
        "sentence": user_pronunciation_sentence.sentence,
        "audio": user_pronunciation_sentence.audio
    }

def map_sentence_word_domain_to_entity(user_pronunciation_word: SentenceWord) -> dict:
    return {
        "word": user_pronunciation_word.word,
        "wrong": user_pronunciation_word.wrong,
        "is_word": user_pronunciation_word.is_word,
    }