from bson import ObjectId
from backoffice.preferences.domain.preference import Preference
from backoffice.preferences.domain.preference_repository import PreferenceRepository
from backoffice.preferences.infrastructure.persistence.mongo.mappers.domain_to_entity_mapper import map_domain_to_entity
from backoffice.preferences.infrastructure.persistence.mongo.mappers.entity_to_domain_mapper import map_entity_to_domain
from shared.infrastructure.persistence.config.mongo_config import db_client

class MongoPreferenceRepository(PreferenceRepository):

    def find_preference(self, preference_id: str) -> Preference | None:
        preference_db = db_client.preferences.find_one({"_id": ObjectId(preference_id)})
        return map_entity_to_domain(preference_db) if preference_db != None else None
    
    def find_all(self):
        preferences_db = db_client.preferences.find()
        return [map_entity_to_domain(preference_db) for preference_db in preferences_db]
    
    def create_preference(self, preference: Preference) -> Preference:
        preference_db = map_domain_to_entity(preference)
        preference_id = db_client.preferences.insert_one(preference_db).inserted_id
        preference.id = str(preference_id)
        return preference
