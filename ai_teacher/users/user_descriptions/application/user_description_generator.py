from ai_teacher.activities.listening.application.topic_planner import TopicPlanner
from ai_teacher.users.user_descriptions.domain.user_description import UserDescription
from ai_teacher.users.user_descriptions.infrastructure.openai.chatgpt_image_generator import ChatgptImageGenerator
from ai_teacher.users.user_descriptions.infrastructure.persistence.mongo_user_description_repository import MongoUserDescriptionRepository
from shared.application.text_to_speech_transformer import TextToSpeechTransformer

class UserDescriptionGenerator:

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
        image_url = self.external_image_generator.generate(topic)

        user_description = UserDescription(
            topic=topic,
            user_id=user_id,
            finished=False,
            image=image_url,
            routine_id=routine_id
        )
        return self.user_description_repository.save_description(user_description)
