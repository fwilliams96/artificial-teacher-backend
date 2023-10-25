from ai_teacher.users.user_cards.domain.user_card import UserCard

def map_entity_to_domain(user_card: dict) -> UserCard:
    return UserCard(
        id=str(user_card["_id"]),
        word=user_card["word"],
        sentence=user_card["sentence"],
        sentence_speech=user_card["sentence_speech"],
        user_id=str(user_card["user_id"])
    )