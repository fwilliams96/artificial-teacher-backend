from ai_teacher.users.user_cards.application.user_sentence_generator import UserSentenceGenerator
from ai_teacher.users.user_cards.domain.user_card import UserCard
from shared.application.text_to_speech_transformer import TextToSpeechTransformer

class UserCardGenerator:

    def __init__(self, user_sentence_generator = UserSentenceGenerator(), text_to_speech_transformer = TextToSpeechTransformer()) -> None:
        self.user_sentence_generator = user_sentence_generator
        self.text_to_speech_transformer = text_to_speech_transformer

    def generate(self, word: str) -> UserCard:
        sentence = self.user_sentence_generator.generate(word)
        sentence_base64 = self.text_to_speech_transformer.transform_to_base64(sentence)
        return UserCard(
            word=word,
            sentence=sentence,
            sentence_speech=sentence_base64
        )