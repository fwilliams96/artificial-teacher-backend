from ai_teacher.users.user_listenings.domain.user_listening import UserListening, UserSentence, UserWord

def map_entity_to_domain(user_listening: dict) -> UserListening:

    return UserListening(
        id=str(user_listening["_id"]),
        topic=user_listening["topic"],
        user_id=str(user_listening["user_id"]),
        finished=user_listening["finished"],
        sentences=[map_sentence_entity_to_domain(sentence) for sentence in user_listening["sentences"]],
        routine_id=str(user_listening["routine_id"]) if user_listening["routine_id"] != None else None
    )

def map_sentence_entity_to_domain(user_sentence: dict) -> UserSentence:
    return UserSentence(
        words=[map_sentence_word_entity_to_domain(word) for word in user_sentence["words"]],
        sentence=user_sentence["sentence"],
        audio=user_sentence["audio"],
    )

def map_sentence_word_entity_to_domain(user_sentence_word: dict) -> UserWord:
    return UserWord(
        word=user_sentence_word["word"],
        is_word=user_sentence_word["is_word"],
        askable=user_sentence_word["askable"],
        wrong=user_sentence_word["wrong"]
    )