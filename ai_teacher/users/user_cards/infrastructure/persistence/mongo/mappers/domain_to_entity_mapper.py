from bson import ObjectId
from ai_teacher.users.user_cards.domain.user_card import UserCard

def map_domain_to_entity(user_card: UserCard) -> dict:
    return {
        "word": user_card.word,
        "sentence": user_card.sentence,
        "sentence_speech": user_card.sentence_speech,
        "user_id": ObjectId(user_card.user_id)
    }