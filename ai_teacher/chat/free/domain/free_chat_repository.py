import abc
from typing import Optional
from ai_teacher.chat.free.domain.free_chat import FreeChat, FreeChatMessage

class FreeChatRepository(abc.ABC):

    @abc.abstractclassmethod
    def create(self, free_chat: FreeChat) -> FreeChat:
        pass

    @abc.abstractclassmethod
    def update(self, free_chat: FreeChat) -> FreeChat:
        pass

    @abc.abstractclassmethod
    def add_message(self, free_chat_message: FreeChatMessage) -> FreeChatMessage:
        pass

    @abc.abstractclassmethod
    def find(self, free_chat_id: str) -> Optional[FreeChat]:
        pass