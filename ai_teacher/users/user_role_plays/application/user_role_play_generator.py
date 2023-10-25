from datetime import datetime
import random
from ai_teacher.users.user_role_plays.application.user_role_play_talker import UserRolePlayTalker
from ai_teacher.users.user_role_plays.domain.role_play import RolePlay, RolePlayMessage, RolePlayMessageType, RolePlayType
from ai_teacher.users.user_role_plays.infrastructure.openai.chatgpt_role_play_talker import ChatgptRolePlayTalker
from ai_teacher.users.user_role_plays.infrastructure.persistence.mongo.mongo_role_play_repository import MongoRolePlayRepository

class UserRolePlayGenerator:

    def __init__(self, 
                 user_role_play_talker = UserRolePlayTalker(),
                 role_play_repository = MongoRolePlayRepository()) -> None:
        self.user_role_play_talker = user_role_play_talker
        self.role_play_repository = role_play_repository

    def create(self, user_id: str, role_play_type = None, routine_id = None) -> RolePlay:

        if role_play_type is None:
            role_play_type = RolePlayType.JOB_INTERVIEW #random.choice(list(RolePlayType))

        print(f"Role play type: {role_play_type}")

        role_play = RolePlay(
            type=role_play_type,
            messages=[],
            is_over=False,
            user_id=user_id,
            routine_id=routine_id,
            creation_date=datetime.now()
        )

        role_play = self.role_play_repository.create(role_play)

        role_play_message = RolePlayMessage(
            message="Hello",
            type=RolePlayMessageType.TEXT,
            sender_id=user_id,
            role_play_id=role_play.id,
            sent_date=datetime.now(),
            last_message=False
        )

        self.user_role_play_talker.talk(role_play_message)
        return role_play
        

        
        
