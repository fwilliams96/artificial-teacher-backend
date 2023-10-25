from typing import Optional
from ai_teacher.users.user_pronunciations.domain.user_pronunciation import UserPronunciation
from ai_teacher.users.user_pronunciations.infrastructure.mongo_user_pronunciation_repository import MongoUserPronunciationRepository

class UserPronunciationFinder:

    def __init__(self, user_pronunciation_repository = MongoUserPronunciationRepository()) -> None:
        self.user_pronunciation_repository = user_pronunciation_repository

    def find(self, user_pronunciation_id: str) -> UserPronunciation:
        return self.user_pronunciation_repository.find_pronunciation(user_pronunciation_id)
    
    def find_by_routine(self, user_routine_id: str) -> Optional[UserPronunciation]:
        return self.user_pronunciation_repository.find_by_routine_id(user_routine_id)