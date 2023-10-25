import random
import re
import string
from ai_teacher.activities.listening.application.topic_planner import TopicPlanner
from ai_teacher.users.user_listenings.infrastructure.openai.chatgpt_sentence_generator import ChatgptSentenceGenerator
from ai_teacher.users.user_listenings.domain.user_listening import UserListening, UserSentence, UserWord
from ai_teacher.users.user_listenings.infrastructure.persistence.mongo.mongo_user_listening_repository import MongoUserListeningRepository
from shared.application.text_to_speech_transformer import TextToSpeechTransformer

class UserListeningGenerator:

    def __init__(self, 
                 topic_planner = TopicPlanner(), 
                 external_sentence_generator = ChatgptSentenceGenerator(),
                 user_listening_repository = MongoUserListeningRepository(),
                 text_to_speech = TextToSpeechTransformer()) -> None:
        self.topic_planner = topic_planner
        self.external_sentence_generator = external_sentence_generator
        self.user_listening_repository = user_listening_repository
        self.text_to_speech = text_to_speech

    def generate(self, user_id: str, num_sentences: int, routine_id = None) -> UserListening:
        topic = self.topic_planner.user_random_topic(user_id)
        sentences = [{}]*num_sentences
        for num_sentence in range(num_sentences):
            sentence = self.external_sentence_generator.generate(topic)

            user_sentence = UserSentence(
                sentence=sentence,
                audio=self.text_to_speech.transform_to_base64(sentence),
                words=self.generate_words(sentence)
            )

            sentences[num_sentence] = user_sentence

        user_listening = UserListening(
            topic=topic,
            user_id=user_id,
            sentences=sentences,
            routine_id=routine_id
        )
        return self.user_listening_repository.save_listening(user_listening)
    
    def generate_words(self, sentence: str) -> list[UserWord]:

        # Agregamos espacios antes y después de cada signo de puntuación
        sentence_with_spaces = re.sub("([.,!?;])", r' \1 ', sentence)

        elements = sentence_with_spaces.split()

        # Creamos una lista de diccionarios, donde cada diccionario representa un elemento
        # y tiene un indicador de si es una palabra (no un signo de puntuación).
        elements_with_indicators = [
            {'word': element, 'is_word': element not in string.punctuation, 'wrong': False}
            for element in elements
        ]

        # Aquí seleccionamos aleatoriamente palabras para preguntar al usuario.
        words = [elemento for elemento in elements_with_indicators if elemento['is_word']]
        num_words_to_ask = max(1, len(words) // 5)

        question_indexes = random.sample(range(len(words)), num_words_to_ask)

        words_picked = [word['word'] for i, word in enumerate(words) if i in question_indexes]
        
        # Agregamos el indicador de pregunta a los elementos que son palabras.
        for element in elements_with_indicators:
            if element['is_word']:
                element['askable'] = element['word'] in words_picked
            else:
                element['askable'] = False

        return [UserWord(**element) for element in elements_with_indicators]