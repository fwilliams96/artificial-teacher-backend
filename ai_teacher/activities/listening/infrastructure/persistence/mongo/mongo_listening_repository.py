from bson import ObjectId
from ai_teacher.activities.listening.domain.listening import Listening
from ai_teacher.activities.listening.domain.listening_repository import ListeningRepository
from ai_teacher.activities.listening.infrastructure.persistence.mongo.mappers.domain_to_entity_mapper import map_domain_to_entity
from ai_teacher.activities.listening.infrastructure.persistence.mongo.mappers.entity_to_domain_mapper import map_entity_to_domain
from shared.infrastructure.persistence.mongo.config.mongo_config import db_client

class MongoListeningRepository(ListeningRepository):

    def save(self, listening: Listening):
        listening_db = map_domain_to_entity(listening)
        preference_id = db_client.listenings.insert_one(listening_db).inserted_id
        listening_db.id = preference_id
        return listening_db
    
    def find(self, listening_id: str) -> Listening | None:
        listening_db = db_client.listenings.find_one({"_id": ObjectId(listening_id)})
        return map_entity_to_domain(listening_db) if listening_db != None else None