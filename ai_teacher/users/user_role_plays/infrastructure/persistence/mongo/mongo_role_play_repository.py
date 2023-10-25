from datetime import datetime
from typing import Optional

from bson import ObjectId
from ai_teacher.users.user_role_plays.domain.role_play import RolePlay, RolePlayMessage
from ai_teacher.users.user_role_plays.domain.role_play_repository import RolePlayRepository
from ai_teacher.users.user_role_plays.infrastructure.persistence.mongo.mappers.domain_to_entity_mapper import map_domain_to_entity, map_message_domain_to_entity
from ai_teacher.users.user_role_plays.infrastructure.persistence.mongo.mappers.entity_to_domain_mapper import map_entity_to_domain, map_message_entity_to_domain
from shared.infrastructure.persistence.config.mongo_config import db_client

class MongoRolePlayRepository(RolePlayRepository):

    def create(self, role_play: RolePlay) -> RolePlay:
        role_play_db = map_domain_to_entity(role_play)
        role_play_id = db_client.role_plays.insert_one(role_play_db).inserted_id
        role_play.id = str(role_play_id)

        for role_play_message in role_play.messages:
            role_play_message.role_play_id = role_play.id

        role_play.messages = [self.add_message(role_play_message) for role_play_message in role_play.messages]
        return role_play
    
    def update(self, role_play: RolePlay) -> RolePlay:
        role_play_db = map_domain_to_entity(role_play)
        db_client.role_plays.find_one_and_replace({"_id": ObjectId(role_play.id)}, role_play_db)
        return role_play
    
    def add_message(self, role_play_message: RolePlayMessage) -> RolePlayMessage:
        role_play_message.sent_date = datetime.now()

        role_play_message_db = map_message_domain_to_entity(role_play_message)
        role_play_message_id = db_client.role_play_messages.insert_one(role_play_message_db).inserted_id
        role_play_message.id = str(role_play_message_id)
        return role_play_message

    def find(self, role_play_id: str) -> Optional[RolePlay]:
        role_play_db = db_client.role_plays.find_one({"_id": ObjectId(role_play_id)})

        if role_play_db is None:
            return None

        role_play = map_entity_to_domain(role_play_db)
        role_play.messages = self.get_messages(role_play.id)
        return role_play
    
    def find_by_routine_id(self, user_routine_id: str) -> Optional[RolePlay]:
        role_play_db = db_client.role_plays.find_one({"routine_id": ObjectId(user_routine_id)})

        if role_play_db is None:
            return None

        role_play = map_entity_to_domain(role_play_db)
        role_play.messages = self.get_messages(role_play.id)
        return role_play
    
    def get_messages(self, role_play_id: str) -> list[RolePlayMessage]:
        role_play_messages_db = db_client.role_play_messages.find({"role_play_id": ObjectId(role_play_id)})
        return [map_message_entity_to_domain(role_play_message_db) for role_play_message_db in role_play_messages_db]
