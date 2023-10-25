import re
import string
from ai_teacher.activities.listening.application.topic_planner import TopicPlanner
from ai_teacher.users.user_pronunciations.domain.user_pronunciation import SentenceWord, Sentence, UserPronunciation
from ai_teacher.users.user_pronunciations.infrastructure.mongo_user_pronunciation_repository import MongoUserPronunciationRepository
from ai_teacher.users.user_pronunciations.infrastructure.openai.chatgpt_sentence_generator import ChatgptSentenceGenerator
from shared.application.text_to_speech_transformer import TextToSpeechTransformer

class UserPronunciationGenerator:

    def __init__(self, 
                 topic_planner = TopicPlanner(), 
                 external_sentence_generator = ChatgptSentenceGenerator(),
                 user_pronunciation_repository = MongoUserPronunciationRepository(),
                 text_to_speech = TextToSpeechTransformer()) -> None:
        self.topic_planner = topic_planner
        self.external_sentence_generator = external_sentence_generator
        self.user_pronunciation_repository = user_pronunciation_repository
        self.text_to_speech = text_to_speech

    def generate(self, user_id: str, routine_id = None) -> UserPronunciation:
        topic = self.topic_planner.user_random_topic(user_id)

        sentence = self.external_sentence_generator.generate(topic)

        sentence = Sentence(
            sentence=sentence,
            audio=self.text_to_speech.transform_to_base64(sentence),
            words=self.generate_words(sentence)
        )

        user_pronunciation = UserPronunciation(
            topic=topic,
            user_id=user_id,
            sentence=sentence,
            routine_id=routine_id
        )
        return self.user_pronunciation_repository.save_pronunciation(user_pronunciation)
    
    def generate_words(self, sentence: str) -> list[SentenceWord]:

        # Agregamos espacios antes y después de cada signo de puntuación
        sentence_with_spaces = re.sub("([.,!?;])", r' \1 ', sentence)

        elements = sentence_with_spaces.split()

        # Creamos una lista de diccionarios, donde cada diccionario representa un elemento
        # y tiene un indicador de si es una palabra (no un signo de puntuación).
        elements_with_indicators = [
            {'word': element, 'is_word': element not in string.punctuation, 'wrong': False}
            for element in elements
        ]

        return [SentenceWord(**element) for element in elements_with_indicators]