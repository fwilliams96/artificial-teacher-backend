from ai_teacher.users.user_cards.domain.user_card import UserCard
from ai_teacher.users.user_cards.infrastructure.persistence.mongo.mongo_user_card_repository import MongoUserCardRepository

class UserCardFinder:

    def __init__(self, user_card_repository = MongoUserCardRepository()) -> None:
        self.user_card_repository = user_card_repository

    def find_all(self, user_id: str) -> list[UserCard]:
        return self.user_card_repository.find_all(user_id)