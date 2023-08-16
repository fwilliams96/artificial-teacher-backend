from ai_teacher.activities.listening.domain.listening import Listening, Sentence, Word

def map_entity_to_domain(listening_db: dict) -> Listening:

    return Listening(
        id=str(listening_db["_id"]),
        topic=str(listening_db["topic"]),
        sentences=[map_sentence_entity_to_domain(sentence_db) for sentence_db in listening_db["sentences"]]
    )

def map_sentence_entity_to_domain(sentence_db: dict) -> Sentence:
    return Sentence(
        sentence=sentence_db["sentence"],
        words=[map_word_entity_to_domain(word_db) for word_db in sentence_db["words"]]
    )

def map_word_entity_to_domain(word_db: dict) -> Word:
    return Word(
        word=word_db["word"],
        is_word=word_db["is_word"],
        askable=word_db["askable"]
    )