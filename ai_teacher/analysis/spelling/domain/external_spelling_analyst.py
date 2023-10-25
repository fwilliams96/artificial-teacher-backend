import abc
from ai_teacher.analysis.shared.domain.analysis import SentenceAnalysis

class ExternalSpellingAnalyst(abc.ABC):

    @abc.abstractclassmethod
    def analyze(self, sentence: str) -> SentenceAnalysis:
        pass