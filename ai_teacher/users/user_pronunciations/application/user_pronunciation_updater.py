from ai_teacher.users.user_pronunciations.domain.user_pronunciation import UserPronunciation
from ai_teacher.users.user_pronunciations.infrastructure.mongo_user_pronunciation_repository import MongoUserPronunciationRepository

class UserPronunciationUpdater:

    def __init__(self, 
                 user_pronunciation_repository = MongoUserPronunciationRepository()) -> None:
        self.user_pronunciation_repository = user_pronunciation_repository

    def update(self, user_pronunciation: UserPronunciation) -> UserPronunciation:
        return self.user_pronunciation_repository.update_pronunciation(user_pronunciation)