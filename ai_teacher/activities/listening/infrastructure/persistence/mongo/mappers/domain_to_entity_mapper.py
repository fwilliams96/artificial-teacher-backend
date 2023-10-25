from ai_teacher.activities.listening.domain.listening import Listening, Sentence, Word

def map_domain_to_entity(listening: Listening) -> dict:
    return {
        "topic": listening.topic,
        "sentences": [map_sentence_domain_to_entity(sentence) for sentence in listening.sentences]
    }

def map_sentence_domain_to_entity(sentence: Sentence) -> dict:
    return {
        "sentence": sentence.sentence,
        "words": [map_word_domain_to_entity(word) for word in sentence.words]
    }

def map_word_domain_to_entity(word: Word) -> dict:
    return {
        "word": word.word,
        "is_word": word.is_word,
        "askable": word.askable
    }