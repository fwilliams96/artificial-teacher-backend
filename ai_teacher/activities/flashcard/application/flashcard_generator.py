from ai_teacher.activities.flashcard.domain.flashcard import FlashCard
from ai_teacher.activities.flashcard.infrastructure.openai.chatgpt_flashcard_generator import ChatgptFlashcardGenerator
from ai_teacher.analysis.shared.domain.analysis import SentenceAnalysis

class FlashcardGenerator:

    def __init__(self, external_flashcard_generator = ChatgptFlashcardGenerator()) -> None:
        self.external_flashcard_generator = external_flashcard_generator

    def generate(self, sentence_analysis: SentenceAnalysis) -> FlashCard:
        return self.external_flashcard_generator.generate(sentence_analysis)