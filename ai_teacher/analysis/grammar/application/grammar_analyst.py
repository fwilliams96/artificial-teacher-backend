from ai_teacher.analysis.grammar.infrastructure.openai.chatgpt_grammar_analyst import ChatgptGrammarAnalyst
from ai_teacher.analysis.shared.domain.analysis import SentenceAnalysis

class GrammarAnalyst:

    def __init__(self, external_grammar_analyst = ChatgptGrammarAnalyst()) -> None:
        self.external_grammar_analyst = external_grammar_analyst

    def analyze(self, sentence: str) -> SentenceAnalysis:
        return self.external_grammar_analyst.analyze(sentence)
