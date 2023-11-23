import base64
import os
import time
from ai_teacher.users.user_descriptions.domain.user_description import UserDescription, UserDescriptionCorrection, UserSolution, UserSolutionType
from ai_teacher.users.user_descriptions.infrastructure.openai.chatgpt_description_rater import ChatgptDescriptionRater
from shared.application.speech_to_text_transcriber import SpeechToTextTranscriber

class UserDescriptionRater:

    BACKEND_DOMAIN = os.environ.get("BACKEND_DOMAIN")
    IMAGES_FOLDER = os.path.join("static", "images")

    def __init__(self, 
                 external_description_rater = ChatgptDescriptionRater(),
                 speech_to_text_transcriber = SpeechToTextTranscriber()
                 ) -> None:
        self.external_description_rater = external_description_rater
        self.speech_to_text_transcriber = speech_to_text_transcriber

    def rate(self, user_solution: UserSolution, image_b64: str) -> UserDescriptionCorrection:
        image_url = self.save_image(image_b64)
        #print(image_url)
        user_description = user_solution.content
        if user_solution.type == UserSolutionType.SPEECH:
            user_description = self.speech_to_text_transcriber.transcribe(user_solution.content)
            #print(user_description)
        return self.external_description_rater.rate(user_description, image_url)
    
    def save_image(self, image_b64: str) -> str:
        image_bytes = base64.b64decode(image_b64.encode('utf-8'))

        NANOts = time.time_ns() # generate to avoid clobber
        image_filename = f"image_{NANOts}.png"

        image_fullpath = os.path.join(self.IMAGES_FOLDER, image_filename)
    
        with open(f'{image_fullpath}', 'wb') as buffer:
            buffer.write(image_bytes)
        return f"{self.BACKEND_DOMAIN}/images/{image_filename}"