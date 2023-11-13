from typing import Optional
from bson import ObjectId
from ai_teacher.users.user_pronunciations.domain.user_pronunciation import UserPronunciation
from ai_teacher.users.user_pronunciations.domain.user_pronunciation_repository import UserPronunciationRepository
from ai_teacher.users.user_pronunciations.infrastructure.persistence.mappers.domain_to_entity_mapper import map_domain_to_entity
from ai_teacher.users.user_pronunciations.infrastructure.persistence.mappers.entity_to_domain_mapper import map_entity_to_domain
from shared.infrastructure.persistence.config.mongo_config import db_client

class MongoUserPronunciationRepository(UserPronunciationRepository):

    def save_pronunciation(self, user_pronunciation: UserPronunciation) -> UserPronunciation:
        user_pronunciation_db = map_domain_to_entity(user_pronunciation)
        user_pronunciation_id = db_client.user_pronunciations.insert_one(user_pronunciation_db).inserted_id
        user_pronunciation.id = str(user_pronunciation_id)
        return user_pronunciation
    
    def update_pronunciation(self, user_listening: UserPronunciation) -> UserPronunciation:
        user_pronunciation_db = map_domain_to_entity(user_listening)
        db_client.user_pronunciations.find_one_and_replace({"_id": ObjectId(user_listening.id)}, user_pronunciation_db)
        return user_listening
    
    def find_pronunciation(self, user_pronunciation_id: str) -> UserPronunciation:
        user_pronunciation_db = db_client.user_pronunciations.find_one({"_id": ObjectId(user_pronunciation_id)})
        return map_entity_to_domain(user_pronunciation_db) if user_pronunciation_db != None else None
    
    def find_by_routine_id(self, user_routine_id: str) -> Optional[UserPronunciation]:
        user_pronunciations_db = db_client.user_pronunciations.find({"routine_id": ObjectId(user_routine_id)})
        return [map_entity_to_domain(user_pronunciation_db) for user_pronunciation_db in user_pronunciations_db]