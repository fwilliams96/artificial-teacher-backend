import abc
from ai_teacher.activities.flashcard.domain.flashcard import FlashCard
from ai_teacher.analysis.shared.domain.analysis import SentenceAnalysis

class ExternalFlashcardGenerator(abc.ABC):

    @abc.abstractclassmethod
    def generate(self, sentence_analysis: SentenceAnalysis) -> FlashCard:
        pass