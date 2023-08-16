from ai_teacher.users.user_cards.domain.user_card import UserCard

def map_domain_to_entity(user_card: UserCard) -> dict:
    return {
        "word": user_card.word,
        "sentence": user_card.sentence,
        "audio_sentence": user_card.audio_sentence
    }