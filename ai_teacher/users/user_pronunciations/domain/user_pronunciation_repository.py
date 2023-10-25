import abc
from typing import Optional
from ai_teacher.users.user_pronunciations.domain.user_pronunciation import UserPronunciation

class UserPronunciationRepository(abc.ABC):

    @abc.abstractclassmethod
    def save_pronunciation(self, user_pronunciation: UserPronunciation):
        pass

    @abc.abstractclassmethod
    def update_pronunciation(self, user_pronunciation: UserPronunciation) -> UserPronunciation:
        pass

    @abc.abstractclassmethod
    def find_pronunciation(self, user_pronunciation_id: str) -> UserPronunciation:
        pass

    @abc.abstractclassmethod
    def find_by_routine_id(self, user_routine_id: str) -> Optional[UserPronunciation]:
        pass