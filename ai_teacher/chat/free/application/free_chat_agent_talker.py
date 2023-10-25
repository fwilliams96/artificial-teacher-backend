from fastapi import HTTPException, status
from ai_teacher.chat.free.domain.free_chat import FreeChatMessage, FreeChatMessageType
from ai_teacher.chat.free.infrastructure.openai.chatgpt_free_chat_agent_talker import ChatGptFreeChatAgentTalker
from ai_teacher.chat.free.infrastructure.persistence.mongo.mongo_free_chat_repository import MongoFreeChatRepository
from shared.application.speech_to_text_transcriber import SpeechToTextTranscriber
from shared.application.text_to_speech_transformer import TextToSpeechTransformer

class FreeChatAgentTalker:

    def __init__(self,
                 free_chat_repository = MongoFreeChatRepository(),
                 external_free_chat_talker = ChatGptFreeChatAgentTalker(),
                 text_to_speech_transformer = TextToSpeechTransformer(),
                 speech_to_text_transcriber = SpeechToTextTranscriber()) -> None:
        self.free_chat_repository = free_chat_repository
        self.external_free_chat_talker = external_free_chat_talker
        self.text_to_speech_transformer = text_to_speech_transformer
        self.speech_to_text_transcriber = speech_to_text_transcriber
    def talk(self, free_chat_message: FreeChatMessage, response_in_speech = False) -> list[FreeChatMessage]:

        if free_chat_message.chat_id is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Free chat id not informed")
        role_play = self.free_chat_repository.find(free_chat_message.chat_id)
        if role_play is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Free chat not found")

        if free_chat_message.type == FreeChatMessageType.SPEECH:
            transcription = self.speech_to_text_transcriber.transcribe(free_chat_message.message)
            free_chat_message.message = transcription
            free_chat_message.type = FreeChatMessageType.TEXT

        self.free_chat_repository.add_message(free_chat_message)
        
        free_chat = self.free_chat_repository.find(free_chat_message.chat_id)

        agent_message = self.external_free_chat_talker.talk(free_chat.messages)
        agent_message = self.free_chat_repository.add_message(agent_message)
        if response_in_speech == True:
            agent_speech_base64_message = self.text_to_speech_transformer.transform_to_base64(agent_message.message)
            agent_message.message = agent_speech_base64_message
            agent_message.type = FreeChatMessageType.SPEECH

        return [agent_message]
