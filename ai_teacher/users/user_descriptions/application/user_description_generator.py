import base64
from datetime import datetime, timedelta
import os
import time

from fastapi import HTTPException, status
from ai_teacher.activities.listening.application.topic_planner import TopicPlanner
from ai_teacher.users.shared.application.user_finder import UserFinder
from ai_teacher.users.shared.application.user_updater import UserUpdater
from ai_teacher.users.shared.domain.user import User
from ai_teacher.users.user_descriptions.domain.user_description import ImageDescription, UserDescription
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
                 text_to_speech = TextToSpeechTransformer(),
                 user_finder = UserFinder(),
                 user_updater = UserUpdater()) -> None:
        self.topic_planner = topic_planner
        self.external_image_generator = external_image_generator
        self.user_description_repository = user_description_repository
        self.text_to_speech = text_to_speech
        self.user_finder = user_finder
        self.user_updater = user_updater

    def generate(self, user_id: str, routine_id = None) -> UserDescription:
        topics = self.topic_planner.get_all_topics(user_id)

        image_descriptions = self.user_description_repository.find_all_image_descriptions()
        completed_image_descriptions_ids = [user_description.image_id for user_description in self.user_description_repository.find_by_user_id(user_id) if user_description.finished]

        image_descriptions_filtered = [image_description for image_description in image_descriptions if image_description.topic in topics and image_description.id not in completed_image_descriptions_ids]

        image_description = None
        if len(image_descriptions_filtered) > 0:
            image_description = image_descriptions[0]
        else:
            #print("Generar imagen")
            user = self.user_finder.find_user_by_id(user_id)
            if self.user_recently_generated_image(user):
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="User has reached the image generation limit")
            topic = self.topic_planner.user_random_topic(user_id)
            image_url = self.external_image_generator.generate(topic)
            response = requests.get(image_url)
            image_bytes = response.content
            image = base64.b64encode(image_bytes).decode('utf-8')
            #image = "toto"
            image_description = ImageDescription(
                image=image,
                topic=topic
            )
            image_description = self.user_description_repository.save_image_description(image_description)
            user.last_image_generation = datetime.now()
            self.user_updater.update(user)

        user_description = UserDescription(
            topic=image_description.topic,
            user_id=user_id,
            finished=False,
            image=image_description.image,
            image_id=image_description.id,
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
    
    def user_recently_generated_image(self, user: User) -> bool:
        if user.last_image_generation == None :
            return False
        one_day = timedelta(days=1)
        now_datetime = datetime.now()
        difference = now_datetime - user.last_image_generation
        return difference < one_day

