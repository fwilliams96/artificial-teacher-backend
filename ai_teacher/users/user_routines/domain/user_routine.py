from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from ai_teacher.users.user_listenings.domain.user_listening import UserListening
from ai_teacher.users.user_pronunciations.domain.user_pronunciation import UserPronunciation
from ai_teacher.users.user_role_plays.domain.role_play import RolePlay

class UserRoutine(BaseModel):
    id: Optional[str] = None
    user_id: str
    creation_date: datetime
    active: bool
    listenings: list[UserListening] = []
    pronunciations: list[UserPronunciation] = []
    role_play: Optional[RolePlay]