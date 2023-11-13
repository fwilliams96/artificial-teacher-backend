from ai_teacher.users.user_descriptions.domain.user_description import UserDescription, UserDescriptionCorrection, UserSolution
from ai_teacher.users.user_descriptions.infrastructure.openai.chatgpt_description_rater import ChatgptDescriptionRater

class UserDescriptionRater:

    def __init__(self, external_description_rater = ChatgptDescriptionRater()) -> None:
        self.external_description_rater = external_description_rater

    def rate(self, user_solution: UserSolution, image: str) -> UserDescriptionCorrection:
        return self.external_description_rater.rate(user_solution, image)