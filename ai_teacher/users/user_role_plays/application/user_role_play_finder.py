from typing import Optional
from ai_teacher.users.user_role_plays.domain.role_play import RolePlay
from ai_teacher.users.user_role_plays.infrastructure.persistence.mongo.mongo_role_play_repository import MongoRolePlayRepository

class UserRolePlayFinder:

    def __init__(self, role_play_repository = MongoRolePlayRepository()) -> None:
        self.role_play_repository = role_play_repository

    def find_by_routine_id(self, user_routine_id: str) -> Optional[RolePlay]:
        return self.role_play_repository.find_by_routine_id(user_routine_id)
    
    def find_by_id(self, role_play_id: str) -> Optional[RolePlay]:
        return self.role_play_repository.find(role_play_id)