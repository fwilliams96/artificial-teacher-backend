from bson import ObjectId
from ai_teacher.users.user_cards.domain.user_card_repository import UserCardRepository
from ai_teacher.users.user_cards.domain.user_card import UserCard
from ai_teacher.users.user_cards.infrastructure.persistence.mongo.mappers.domain_to_entity_mapper import map_domain_to_entity
from ai_teacher.users.user_cards.infrastructure.persistence.mongo.mappers.entity_to_domain_mapper import map_entity_to_domain
from shared.infrastructure.persistence.config.mongo_config import db_client

class MongoUserCardRepository(UserCardRepository):

    def save(self, user_card: UserCard) -> UserCard:
        user_card_db = map_domain_to_entity(user_card)
        user_card_id = db_client.user_cards.insert_one(user_card_db).inserted_id
        user_card.id = str(user_card_id)
        return user_card
    
    def find_all(self, user_id: str) -> list[UserCard]:
        user_cards_db = db_client.user_cards.find({"user_id": ObjectId(user_id)})

        '''cards = []
        for user_card_db in user_cards_db:
            user_card = map_entity_to_domain(user_card_db)
            function_is_true = self.starts_by_gam(user_card.word)
            if function_is_true:
                cards.append(user_card)
        
        return cards'''
        return [map_entity_to_domain(user_card_db) for user_card_db in user_cards_db]

    def starts_by_gam(self, word: str) -> bool:
        if word.lower().startswith("gam"):
            return True
        return False