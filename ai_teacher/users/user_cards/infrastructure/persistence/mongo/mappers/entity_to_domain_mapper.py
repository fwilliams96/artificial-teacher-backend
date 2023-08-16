from ai_teacher.users.user_cards.domain.user_card import UserCard

def map_entity_to_domain(user_card: dict) -> UserCard:
    return UserCard(
        id=str(user_card["_id"]),
        word=user_card["word"],
        sentence=user_card["sentence"],
        audio_sentence=user_card["audio_sentence"]
    )