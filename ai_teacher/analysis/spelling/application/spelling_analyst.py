from ai_teacher.analysis.shared.domain.analysis import SentenceAnalysis
from ai_teacher.analysis.spelling.infrastructure.openai.chatgpt_spelling_analyst import ChatgptSpellingAnalyst

class SpellingAnalyst:

    def __init__(self, external_spelling_analyst = ChatgptSpellingAnalyst()) -> None:
        self.external_spelling_analyst = external_spelling_analyst

    def analyze(self, sentence: str) -> SentenceAnalysis:
        return self.external_spelling_analyst.analyze(sentence)