from ai_teacher.chat.free.domain.free_chat import FreeChat
from ai_teacher.chat.free.infrastructure.persistence.mongo.mongo_free_chat_repository import MongoFreeChatRepository

class FreeChatFinder:

    def __init__(self, free_chat_repository = MongoFreeChatRepository()) -> None:
        self.free_chat_repository = free_chat_repository

    def find(self, free_chat_id: str) -> FreeChat:
        return self.free_chat_repository.find(free_chat_id)