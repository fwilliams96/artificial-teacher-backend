from datetime import datetime
from ai_teacher.chat.free.domain.external_free_chat_agent_talker import ExternalFreeChatAgentTalker
from ai_teacher.chat.free.domain.free_chat import FreeChatMessage, FreeChatMessageType
from ai_teacher.chat.free.infrastructure.persistence.mongo.mongo_free_chat_repository import MongoFreeChatRepository
from shared.infrastructure.openai.client.openai_client import send_messages_to_ai

class ChatGptFreeChatAgentTalker(ExternalFreeChatAgentTalker):

    talker_context = "You are an English expert and your job is to keep a conversation with a user in a basic level, "\
    "I will be your man in the middle. Keep the conversation active, focusing on learning English."

    def __init__(self):
        pass

    def talk(self, free_chat_messages: list[FreeChatMessage]) -> FreeChatMessage:
        messages=[{"role": "system", "content": self.talker_context}]

        for free_chat_message in free_chat_messages:
            if free_chat_message.sender_id is None:
                messages.append({"role": "assistant", "content": free_chat_message.message})
            else:
                messages.append({"role": "user", "content": free_chat_message.message})

        print(f"\n>>>>>>>>>>>>>>>>> [FREE_CHAT TALKER] Sent messages <<<<<<<<<<<<<<<<<<<\n")
        print(f"{messages} \n")
        agent_response = send_messages_to_ai(messages)
        print(f"\n>>>>>>>>>>>>>>>>> [FREE_CHAT TALKER] Received message <<<<<<<<<<<<<<<<<<<\n")
        print(f"{agent_response} \n")

        messages.append({"role": "assistant", "content": agent_response})

        return FreeChatMessage(
            chat_id=free_chat_message.chat_id,
            sender_id=None,
            message=agent_response,
            type=FreeChatMessageType.TEXT,
            sent_date=datetime.now()
        )