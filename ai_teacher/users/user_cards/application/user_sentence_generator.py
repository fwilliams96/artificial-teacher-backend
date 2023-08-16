from ai_teacher.users.user_cards.infrastructure.openai.chatgpt_sentence_generator import ChatgptSentenceGenerator

class UserSentenceGenerator:

    def __init__(self, external_sentence_generator = ChatgptSentenceGenerator()) -> None:
        self.external_sentence_generator = external_sentence_generator

    def generate(self, word: str) -> str:
        return self.external_sentence_generator.generate(word)

        