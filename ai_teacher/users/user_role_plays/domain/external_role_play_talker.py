import abc
from ai_teacher.users.user_role_plays.domain.role_play import RolePlayMessage, RolePlayType

class ExternalRolePlayTalker(abc.ABC):

    @abc.abstractclassmethod
    def talk(self, role_play_messages: list[RolePlayMessage], role_play_type: RolePlayType) -> RolePlayMessage:
        pass