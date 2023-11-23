from ai_teacher.users.user_descriptions.domain.user_description import UserDescription, UserDescriptionCorrection, UserSolution, UserSolutionType
from ai_teacher.users.user_descriptions.infrastructure.openai.chatgpt_description_rater import ChatgptDescriptionRater
from shared.application.speech_to_text_transcriber import SpeechToTextTranscriber

class UserDescriptionRater:

    def __init__(self, 
                 external_description_rater = ChatgptDescriptionRater(),
                 speech_to_text_transcriber = SpeechToTextTranscriber()
                 ) -> None:
        self.external_description_rater = external_description_rater
        self.speech_to_text_transcriber = speech_to_text_transcriber

    def rate(self, user_solution: UserSolution, image: str) -> UserDescriptionCorrection:

        user_description = user_solution.content
        if user_solution.type == UserSolutionType.SPEECH:
            user_description = self.speech_to_text_transcriber.transcribe(user_solution.content)
            #print(user_description)
        return self.external_description_rater.rate(user_description, image)