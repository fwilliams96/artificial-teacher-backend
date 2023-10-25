from typing import Optional
from bson import ObjectId
from ai_teacher.users.user_listenings.domain.user_listening import UserListening
from ai_teacher.users.user_listenings.domain.user_listening_repository import UserListeningRepository
from ai_teacher.users.user_listenings.infrastructure.persistence.mongo.mappers.domain_to_entity_mapper import map_domain_to_entity
from ai_teacher.users.user_listenings.infrastructure.persistence.mongo.mappers.entity_to_domain_mapper import map_entity_to_domain
from shared.infrastructure.persistence.config.mongo_config import db_client

class MongoUserListeningRepository(UserListeningRepository):

    def save_listening(self, user_listening: UserListening) -> UserListening:
        user_listening_db = map_domain_to_entity(user_listening)
        preference_id = db_client.user_listenings.insert_one(user_listening_db).inserted_id
        user_listening.id = str(preference_id)
        return user_listening
    
    def update_listening(self, user_listening: UserListening) -> UserListening:
        user_listening_db = map_domain_to_entity(user_listening)
        db_client.user_listenings.find_one_and_replace({"_id": ObjectId(user_listening.id)}, user_listening_db)
        return user_listening
    
    def find_listening(self, user_listening_id: str) -> UserListening:
        user_listening_db = db_client.user_listenings.find_one({"_id": ObjectId(user_listening_id)})
        return map_entity_to_domain(user_listening_db) if user_listening_db != None else None
    
    def find_by_routine_id(self, user_routine_id: str) -> Optional[UserListening]:
        user_listenings_db = db_client.user_listenings.find({"routine_id": ObjectId(user_routine_id)})
        return [map_entity_to_domain(user_listening_db) for user_listening_db in user_listenings_db]