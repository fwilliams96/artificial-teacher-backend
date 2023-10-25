from typing import Optional
from bson import ObjectId
from ai_teacher.chat.free.domain.free_chat import FreeChat, FreeChatMessage
from ai_teacher.chat.free.domain.free_chat_repository import FreeChatRepository
from ai_teacher.chat.free.infrastructure.persistence.mongo.mappers.domain_to_entity_mapper import map_domain_message_to_entity, map_domain_to_entity
from ai_teacher.chat.free.infrastructure.persistence.mongo.mappers.entity_to_domain_mapper import map_entity_message_to_domain, map_entity_to_domain
from datetime import datetime
from shared.infrastructure.persistence.config.mongo_config import db_client

class MongoFreeChatRepository(FreeChatRepository):

    def create(self, free_chat: FreeChat) -> FreeChat:
        free_chat_db = map_domain_to_entity(free_chat)
        chat_id = db_client.free_chats.insert_one(free_chat_db).inserted_id
        free_chat.id = str(chat_id)

        for free_chat_message in free_chat.messages:
            free_chat_message.chat_id = free_chat.id

        free_chat.messages = [self.add_message(free_chat_message) for free_chat_message in free_chat.messages]
        return free_chat
    
    def update(self, free_chat: FreeChat) -> FreeChat:
        free_chat_db = map_domain_to_entity(free_chat)
        db_client.free_chats.find_one_and_replace({"_id": ObjectId(free_chat.id)}, free_chat_db)
        return free_chat
    
    def add_message(self, free_chat_message: FreeChatMessage) -> FreeChatMessage:
        free_chat_message.sent_date = datetime.now()

        free_chat_message_db = map_domain_message_to_entity(free_chat_message)
        message_id = db_client.free_chat_messages.insert_one(free_chat_message_db).inserted_id
        free_chat_message.id = str(message_id)
        return free_chat_message

    def find(self, free_chat_id: str) -> Optional[FreeChat]:
        free_chat_db = db_client.free_chats.find_one({"_id": ObjectId(free_chat_id)})
        
        if free_chat_db is None:
            return None

        free_chat = map_entity_to_domain(free_chat_db)

        free_chat_messages_db = db_client.free_chat_messages.find({"chat_id": ObjectId(free_chat_id)})
        free_chat.messages = [map_entity_message_to_domain(message_db) for message_db in free_chat_messages_db]
        return free_chat