import abc

from ai_teacher.users.user_descriptions.domain.user_description import UserDescriptionCorrection, UserSolution

class ExternalDescriptionRater(abc.ABC):

    @abc.abstractclassmethod
    def rate(self, user_description: str, image: str) -> UserDescriptionCorrection:
        pass