from typing import Optional
from bson import ObjectId
from ai_teacher.users.user_descriptions.domain.user_description import ImageDescription, UserDescription
from ai_teacher.users.user_descriptions.domain.user_description_repository import UserDescriptionRepository
from ai_teacher.users.user_descriptions.infrastructure.persistence.mappers.domain_to_entity_mapper import map_domain_to_entity, map_image_description_to_entity
from ai_teacher.users.user_descriptions.infrastructure.persistence.mappers.entity_to_domain_mapper import map_entity_to_domain, map_image_description_to_domain
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
    
    def find_by_routine_id(self, user_routine_id: str) -> list[UserDescription]:
        user_descriptions_db = db_client.user_descriptions.find({"routine_id": ObjectId(user_routine_id)})
        return [map_entity_to_domain(user_description_db) for user_description_db in user_descriptions_db]
    
    def find_by_user_id(self, user_id: str) -> list[UserDescription]:
        user_descriptions_db = db_client.user_descriptions.find({"user_id": ObjectId(user_id)})
        return [map_entity_to_domain(user_description_db) for user_description_db in user_descriptions_db]
    
    def save_image_description(self, image_description: ImageDescription) -> ImageDescription:
        image_description_db = map_image_description_to_entity(image_description)
        image_description_id = db_client.image_descriptions.insert_one(image_description_db).inserted_id
        image_description.id = str(image_description_id)
        return image_description
    
    def find_all_image_descriptions(self) -> list[ImageDescription]:
        image_descriptions_db = db_client.image_descriptions.find()
        return [map_image_description_to_domain(image_description_db) for image_description_db in image_descriptions_db]
    
    def find_image_descriptions_by_topic(self, topic: str) -> list[ImageDescription]:
        image_descriptions_db = db_client.image_descriptions.find({"topic": topic})
        return [map_image_description_to_domain(image_description_db) for image_description_db in image_descriptions_db]