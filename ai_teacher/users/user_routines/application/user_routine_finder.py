from typing import Optional
from ai_teacher.users.user_listenings.application.user_listening_finder import UserListeningFinder
from ai_teacher.users.user_pronunciations.application.user_pronunciation_finder import UserPronunciationFinder
from ai_teacher.users.user_role_plays.application.user_role_play_finder import UserRolePlayFinder
from ai_teacher.users.user_routines.domain.user_routine import UserRoutine
from ai_teacher.users.user_routines.infrastructure.persistence.mongo.mongo_user_routine_repository import MongoUserRoutineRepository


class UserRoutineFinder:

    def __init__(self, 
                 user_routine_repository = MongoUserRoutineRepository(),
                 user_listening_finder = UserListeningFinder(),
                 user_role_play_finder = UserRolePlayFinder(),
                 user_pronunciation_finder = UserPronunciationFinder()) -> None:
        self.user_routine_repository = user_routine_repository
        self.user_listening_finder = user_listening_finder
        self.user_role_play_finder = user_role_play_finder
        self.user_pronunciation_finder = user_pronunciation_finder

    def find_by_id(self, routine_id: str) -> Optional[UserRoutine]:
        user_routine = self.user_routine_repository.find_by_id(routine_id)
        user_routine.listenings = self.user_listening_finder.find_by_routine(routine_id)
        user_routine.role_play = self.user_role_play_finder.find_by_routine_id(routine_id)
        user_routine.pronunciations = self.user_pronunciation_finder.find_by_routine(routine_id)
        return user_routine

    def find_all(self, user_id: str) -> list[UserRoutine]:
        return self.user_routine_repository.find_all(user_id)

    def find_active(self, user_id: str) -> list[UserRoutine]:
        user_routines = self.user_routine_repository.find_all(user_id)
        return [user_routine for user_routine in user_routines if user_routine.active]
