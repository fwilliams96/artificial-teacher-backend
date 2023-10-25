from fastapi import HTTPException, status
from ai_teacher.users.user_role_plays.domain.role_play import RolePlayMessage, RolePlayMessageType
from ai_teacher.users.user_role_plays.infrastructure.openai.chatgpt_role_play_talker import ChatgptRolePlayTalker
from ai_teacher.users.user_role_plays.infrastructure.persistence.mongo.mongo_role_play_repository import MongoRolePlayRepository

class UserRolePlayTalker:

    def __init__(self, 
                 external_role_play_talker = ChatgptRolePlayTalker(),
                 role_play_repository = MongoRolePlayRepository()) -> None:
        self.external_role_play_talker = external_role_play_talker
        self.role_play_repository = role_play_repository


    def talk(self, role_play_message: RolePlayMessage, response_in_speech = False) -> list[RolePlayMessage]:

        if role_play_message.role_play_id is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role play id not informed")
        role_play = self.role_play_repository.find(role_play_message.role_play_id)
        if role_play is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role play not found")

        '''if role_play_message.type == role_play_message.SPEECH:
            transcription = self.speech_to_text_transcriber.transcribe(role_play_message.message)
            role_play_message.message = transcription
            role_play_message.type = RolePlayMessageType.TEXT'''

        self.role_play_repository.add_message(role_play_message)
        
        role_play = self.role_play_repository.find(role_play_message.role_play_id)

        agent_message = self.external_role_play_talker.talk(role_play.messages, role_play.type)
        agent_message = self.role_play_repository.add_message(agent_message)
        if agent_message.last_message == True:
            role_play.is_over = True
            self.role_play_repository.update(role_play)

        '''if response_in_speech == True:
            agent_speech_base64_message = self.text_to_speech_transformer.transform_to_base64(agent_message.message)
            agent_message.message = agent_speech_base64_message
            agent_message.type = RolePlayMessageType.SPEECH'''

        return [agent_message]


    '''def talk(self, role_play_message: RolePlayMessage, response_in_speech = False) -> list[RolePlayMessage]:
        self.role_play_repository.add_message(role_play_message)
        role_play = self.role_play_repository.find(role_play_message.role_play_id)
        agent_message = self.external_role_play_talker.talk(role_play.messages)
        agent_message = self.role_play_repository.add_message(agent_message)
        if response_in_speech == True:
            agent_speech_base64_message = self.text_to_speech_transformer.transform_to_base64(agent_message.message)
            agent_message.message = agent_speech_base64_message
            agent_message.type = RolePlayMessageType.SPEECH

        return [agent_message]'''