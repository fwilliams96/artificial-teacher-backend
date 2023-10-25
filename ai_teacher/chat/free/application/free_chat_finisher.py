from fastapi import HTTPException, status
from ai_teacher.chat.free.domain.free_chat import FreeChat
from ai_teacher.chat.free.infrastructure.persistence.mongo.mongo_free_chat_repository import MongoFreeChatRepository

class FreeChatFinisher:

    def __init__(self, 
                 free_chat_repository = MongoFreeChatRepository()) -> None:
        self.free_chat_repository = free_chat_repository

    def finish(self, chat_id: str) -> FreeChat:
        free_chat = self.free_chat_repository.find(chat_id)
        if free_chat.is_over == True:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The chat is already over")
        free_chat.is_over = True
        self.free_chat_repository.update(free_chat)
        return free_chat        

        
        
