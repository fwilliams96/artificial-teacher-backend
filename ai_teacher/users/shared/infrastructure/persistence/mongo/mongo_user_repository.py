from bson import ObjectId
from ai_teacher.users.shared.domain.user import User, UserDb
from ai_teacher.users.shared.domain.user_repository import UserRepository
from ai_teacher.users.shared.infrastructure.persistence.mongo.mappers.domain_to_entity_mapper import map_domain_to_entity
from ai_teacher.users.shared.infrastructure.persistence.mongo.mappers.entity_to_domain_mapper import map_entity_to_domain
from shared.infrastructure.persistence.mongo.config.mongo_config import db_client

class MongoUserRepository(UserRepository):

    def create(self, user: UserDb) -> User:
        user_db = map_domain_to_entity(user)
        user_id = db_client.users.insert_one(user_db).inserted_id

        return User(
            id=user_id,
            email=user.email,
            disabled=user.disabled
        )
    
    def update(self, user: UserDb) -> User:
        user_db = map_domain_to_entity(user)
        db_client.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_db)

        return User(
            id=user.id,
            email=user.email,
            disabled=user.disabled
        )

    def find_by_email(self, email: str) -> User | None:
        user_db = db_client.users.find_one({"email": email})
        return map_entity_to_domain(user_db) if user_db != None else None

    def find_by_id(self, user_id: str) -> User | None:
        user_db = db_client.users.find_one({"_id": ObjectId(user_id)})
        return map_entity_to_domain(user_db) if user_db != None else None