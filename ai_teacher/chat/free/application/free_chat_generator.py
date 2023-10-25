from datetime import datetime
from ai_teacher.chat.free.application.free_chat_agent_talker import FreeChatAgentTalker
from ai_teacher.chat.free.domain.free_chat import FreeChat, FreeChatMessage, FreeChatMessageType
from ai_teacher.chat.free.infrastructure.persistence.mongo.mongo_free_chat_repository import MongoFreeChatRepository

class FreeChatGenerator:

    def __init__(self, 
                 free_chat_talker = FreeChatAgentTalker(),
                 free_chat_repository = MongoFreeChatRepository()) -> None:
        self.free_chat_talker = free_chat_talker
        self.free_chat_repository = free_chat_repository

    def create(self, user_id: str) -> FreeChat:

        free_chat = FreeChat(
            messages=[],
            user_id=user_id,
            creation_date=datetime.now()
        )

        free_chat = self.free_chat_repository.create(free_chat)

        free_chat_message = FreeChatMessage(
            message="Hello",
            type=FreeChatMessageType.TEXT,
            sender_id=user_id,
            chat_id=free_chat.id,
            sent_date=datetime.now()
        )

        self.free_chat_talker.talk(free_chat_message)
        return free_chat
        

        
        
