import abc
from typing import Optional
from ai_teacher.users.user_role_plays.domain.role_play import RolePlay, RolePlayMessage

class RolePlayRepository(abc.ABC):

    @abc.abstractclassmethod
    def create(self, role_play: RolePlay) -> RolePlay:
        pass

    @abc.abstractclassmethod
    def update(self, role_play: RolePlay) -> RolePlay:
        pass

    @abc.abstractclassmethod
    def add_message(self, role_play_message: RolePlayMessage) -> RolePlayMessage:
        pass

    @abc.abstractclassmethod
    def find(self, role_play_id: id) -> Optional[RolePlay]:
        pass

    @abc.abstractclassmethod
    def find_by_routine_id(self, user_routine_id: str) -> Optional[RolePlay]:
        pass