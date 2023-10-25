from ai_teacher.users.user_cards.domain.user_card import UserCard
from ai_teacher.users.user_cards.infrastructure.persistence.mongo.mongo_user_card_repository import MongoUserCardRepository
from ai_teacher.users.user_listenings.domain.user_listening import UserSentence

class UserCardCreator:

    def __init__(self, user_card_repository = MongoUserCardRepository()) -> None:
        self.user_card_repository = user_card_repository

    def create(self, user_card: UserCard) -> UserCard:
        return self.user_card_repository.save(user_card)