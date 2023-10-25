from typing import Optional
from bson import ObjectId
from ai_teacher.users.user_routines.domain.user_routine import UserRoutine
from ai_teacher.users.user_routines.domain.user_routine_repository import UserRoutineRepository
from ai_teacher.users.user_routines.infrastructure.persistence.mongo.mappers.domain_to_entity_mapper import map_domain_to_entity
from ai_teacher.users.user_routines.infrastructure.persistence.mongo.mappers.entity_to_domain_mapper import map_entity_to_domain
from shared.infrastructure.persistence.config.mongo_config import db_client

class MongoUserRoutineRepository(UserRoutineRepository):
    
    def create(self, user_routine: UserRoutine) -> UserRoutine:
        user_routine_db = map_domain_to_entity(user_routine)
        user_routine_id = db_client.user_routines.insert_one(user_routine_db).inserted_id
        user_routine.id = str(user_routine_id)
        return user_routine
    
    def find_by_id(self, user_routine_id: str) -> Optional[UserRoutine]:
        user_routine_db = db_client.user_routines.find_one({"_id": ObjectId(user_routine_id)})
        return map_entity_to_domain(user_routine_db) if user_routine_db != None else None

    def find_all(self, user_id: str) -> list[UserRoutine]:
        user_routines_db = db_client.user_routines.find({"user_id": ObjectId(user_id)})
        return [map_entity_to_domain(user_routine_db) for user_routine_db in user_routines_db]