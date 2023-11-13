from typing import Optional
from bson import ObjectId
from ai_teacher.users.user_descriptions.domain.user_description import UserDescription
from ai_teacher.users.user_descriptions.domain.user_description_repository import UserDescriptionRepository
from ai_teacher.users.user_descriptions.infrastructure.persistence.mappers.domain_to_entity_mapper import map_domain_to_entity
from ai_teacher.users.user_descriptions.infrastructure.persistence.mappers.entity_to_domain_mapper import map_entity_to_domain
from shared.infrastructure.persistence.config.mongo_config import db_client

class MongoUserDescriptionRepository(UserDescriptionRepository):

    def save_description(self, user_description: UserDescription) -> UserDescription:
        user_description_db = map_domain_to_entity(user_description)
        user_description_id = db_client.user_descriptions.insert_one(user_description_db).inserted_id
        user_description.id = str(user_description_id)
        return user_description
    
    def update_description(self, user_description: UserDescription) -> UserDescription:
        user_description_db = map_domain_to_entity(user_description)
        db_client.user_descriptions.find_one_and_replace({"_id": ObjectId(user_description.id)}, user_description_db)
        return user_description
    
    def find_description(self, user_pronunciation_id: str) -> Optional[UserDescription]:
        user_description_db = db_client.user_descriptions.find_one({"_id": ObjectId(user_pronunciation_id)})
        return map_entity_to_domain(user_description_db) if user_description_db != None else None
    
    def find_by_routine_id(self, user_routine_id: str) -> Optional[UserDescription]:
        user_descriptions_db = db_client.user_descriptions.find({"routine_id": ObjectId(user_routine_id)})
        return [map_entity_to_domain(user_description_db) for user_description_db in user_descriptions_db]