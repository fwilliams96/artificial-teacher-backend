import abc
from ai_teacher.chat.free.domain.free_chat import FreeChat, FreeChatMessage

class ExternalFreeChatAgentTalker(abc.ABC):

    @abc.abstractclassmethod
    def talk(self, free_chat_messages: list[FreeChatMessage], new_chat = False) -> FreeChatMessage:
        pass