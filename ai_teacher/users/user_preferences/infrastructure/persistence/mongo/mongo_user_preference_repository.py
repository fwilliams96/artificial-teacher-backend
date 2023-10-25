from bson import ObjectId
from ai_teacher.users.user_preferences.domain.user_preference import UserPreference
from ai_teacher.users.user_preferences.domain.user_preference_repository import UserPreferenceRepository
from ai_teacher.users.user_preferences.infrastructure.persistence.mongo.mappers.domain_to_entity_mapper import map_domain_to_entity
from ai_teacher.users.user_preferences.infrastructure.persistence.mongo.mappers.entity_to_domain_mapper import map_entity_to_domain
from shared.infrastructure.persistence.config.mongo_config import db_client

class MongoUserPreferenceRepository(UserPreferenceRepository):
     
   def find(self, user_id: str) -> list[UserPreference]:
      user_preferences_db = db_client.user_preferences.find({"user_id": ObjectId(user_id)})
      return [map_entity_to_domain(user_preference_db) for user_preference_db in user_preferences_db]

   def create(self, user_preference: UserPreference) -> UserPreference:
      user_preference_db = map_domain_to_entity(user_preference)
      user_preference_id = db_client.user_preferences.insert_one(user_preference_db).inserted_id
      user_preference.id = str(user_preference_id)
      return user_preference

