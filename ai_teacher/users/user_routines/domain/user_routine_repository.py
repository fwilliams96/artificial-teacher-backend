import abc
from typing import Optional
from ai_teacher.users.user_routines.domain.user_routine import UserRoutine

class UserRoutineRepository(abc.ABC):

    @abc.abstractclassmethod
    def create(self, user_routine: UserRoutine) -> UserRoutine:
        pass

    @abc.abstractclassmethod
    def find_by_id(self, user_routine_id: str) -> Optional[UserRoutine]:
        pass

    @abc.abstractclassmethod
    def find_all(self, user_id: str) -> list[UserRoutine]:
        pass