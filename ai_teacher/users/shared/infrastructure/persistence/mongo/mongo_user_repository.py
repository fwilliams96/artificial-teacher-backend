from bson import ObjectId
from ai_teacher.users.shared.domain.user import User, UserDb
from ai_teacher.users.shared.domain.user_repository import UserRepository
from ai_teacher.users.shared.infrastructure.persistence.mongo.mappers.domain_to_entity_mapper import map_domain_to_entity
from ai_teacher.users.shared.infrastructure.persistence.mongo.mappers.entity_to_domain_mapper import map_entity_to_domain
from shared.infrastructure.persistence.config.mongo_config import db_client

class MongoUserRepository(UserRepository):

    def create(self, user: UserDb) -> UserDb:
        user_db = map_domain_to_entity(user)
        user_id = db_client.users.insert_one(user_db).inserted_id
        user.id = str(user_id)
        return user
    
    def update(self, user: UserDb) -> UserDb:
        user_db = map_domain_to_entity(user)
        db_client.users.find_one_and_update({"_id": ObjectId(user.id)}, {"$set" : user_db})
        return user

    def find_by_email(self, email: str) -> UserDb | None:
        user_db = db_client.users.find_one({"email": email})
        return map_entity_to_domain(user_db) if user_db != None else None

    def find_by_id(self, user_id: str) -> UserDb | None:
        user_db = db_client.users.find_one({"_id": ObjectId(user_id)})
        return map_entity_to_domain(user_db) if user_db != None else None
    
    def increment_score(self, user_id: str, score: int):
        user_score_db = db_client.users.find_one({"_id": ObjectId(user_id)})

        if user_score_db != None:
            user_score = map_entity_to_domain(user_score_db)
            user_score.score += score
            while user_score.score >= 100:
                remaining = user_score.score - 100
                user_score.score = remaining
                user_score.level += 1
            db_client.users.find_one_and_replace({"_id": ObjectId(user_id)}, map_domain_to_entity(user_score))

    def find_all(self) -> list[User]:
        users_db = db_client.users.find().sort("level", -1)
        users = [map_entity_to_domain(user_db) for user_db in users_db]
        return [self.clean_user(user) for user in users]

    def clean_user(self, user: UserDb):
        return User(
            first_name=user.first_name,
            level=user.level,
            score=user.score
        )