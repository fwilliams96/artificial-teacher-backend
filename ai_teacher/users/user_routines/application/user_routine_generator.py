from datetime import datetime
from ai_teacher.users.user_listenings.application.user_listening_generator import UserListeningGenerator
from ai_teacher.activities.listening.application.topic_planner import TopicPlanner
from ai_teacher.users.user_pronunciations.application.user_pronunciation_generator import UserPronunciationGenerator
from ai_teacher.users.user_role_plays.application.user_role_play_generator import UserRolePlayGenerator
from ai_teacher.users.user_role_plays.domain.role_play import RolePlayType
from ai_teacher.users.user_routines.domain.user_routine import UserRoutine
from ai_teacher.users.user_routines.infrastructure.persistence.mongo.mongo_user_routine_repository import MongoUserRoutineRepository
import random

class UserRoutineGenerator:

    def __init__(self, 
                 user_routine_repository = MongoUserRoutineRepository(), 
                 user_role_play_generator = UserRolePlayGenerator(),
                 user_listening_generator = UserListeningGenerator(),
                 user_pronunciation_generator = UserPronunciationGenerator()
                 ) -> None:
        self.user_routine_repository = user_routine_repository
        self.user_role_play_generator = user_role_play_generator
        self.user_listening_generator = user_listening_generator
        self.user_pronunciation_generator = user_pronunciation_generator

    def generate(self, user_id: str) -> UserRoutine:

        user_routine = UserRoutine(
            creation_date=datetime.now(),
            user_id=user_id,
            active=True
        )

        user_routine = self.user_routine_repository.create(user_routine)

        num_listenings = 2 #TODO
        num_pronunciations = 2

        for i in range(0, num_listenings):
            self.user_listening_generator.generate(user_id=user_id, num_sentences=3, routine_id=user_routine.id)

        for i in range(0, num_pronunciations):
            self.user_pronunciation_generator.generate(user_id=user_id, routine_id=user_routine.id)

        self.user_role_play_generator.create(user_id=user_id, role_play_type=None, routine_id=user_routine.id)

        return user_routine
