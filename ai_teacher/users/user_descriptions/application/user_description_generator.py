import os
import time
from ai_teacher.activities.listening.application.topic_planner import TopicPlanner
from ai_teacher.users.user_descriptions.domain.user_description import UserDescription
from ai_teacher.users.user_descriptions.infrastructure.openai.chatgpt_image_generator import ChatgptImageGenerator
from ai_teacher.users.user_descriptions.infrastructure.persistence.mongo_user_description_repository import MongoUserDescriptionRepository
from shared.application.text_to_speech_transformer import TextToSpeechTransformer
import requests

class UserDescriptionGenerator:

    AUDIOS_FOLDER = os.path.join("static", "images")
    BACKEND_DOMAIN = os.environ.get("BACKEND_DOMAIN")

    def __init__(self, 
                 topic_planner = TopicPlanner(), 
                 external_image_generator = ChatgptImageGenerator(),
                 user_description_repository = MongoUserDescriptionRepository(),
                 text_to_speech = TextToSpeechTransformer()) -> None:
        self.topic_planner = topic_planner
        self.external_image_generator = external_image_generator
        self.user_description_repository = user_description_repository
        self.text_to_speech = text_to_speech

    def generate(self, user_id: str, routine_id = None) -> UserDescription:
        topic = self.topic_planner.user_random_topic(user_id)
        image_url = "https://oaidalleapiprodscus.blob.core.windows.net/private/org-ke1fTmkISrpEBJIBlQoBOWGz/user-nU292ZiwjLsolPfkijyK9TSD/img-YDUWSxtvTOSVFAO1QZSmcipB.png?st=2023-11-14T21%3A08%3A55Z&se=2023-11-14T23%3A08%3A55Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2023-11-14T13%3A54%3A43Z&ske=2023-11-15T13%3A54%3A43Z&sks=b&skv=2021-08-06&sig=tuHRn%2BNBQ7E%2B1rC%2BeZZYlLWxoiUkOd0gAv8EcBNiYI0%3D" #self.external_image_generator.generate(topic)
        print(image_url)

        response = requests.get(image_url)
        image = response.content

        local_image_url = self.save_image(image)
        print(local_image_url)

        user_description = UserDescription(
            topic=topic,
            user_id=user_id,
            finished=False,
            image=local_image_url,
            routine_id=routine_id
        )
        return self.user_description_repository.save_description(user_description)
    
    def save_image(self, image_bytes: bytes) -> str:
        NANOts = time.time_ns() # generate to avoid clobber
        image_filename = f"image_{NANOts}.png"

        image_fullpath = os.path.join(self.AUDIOS_FOLDER, image_filename)
    
        with open(f'{image_fullpath}', 'wb') as buffer:
            buffer.write(image_bytes)
        return f"{UserDescriptionGenerator.BACKEND_DOMAIN}/images/{image_filename}"