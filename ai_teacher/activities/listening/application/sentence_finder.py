from ai_teacher.activities.listening.application.listening_finder import ListeningFinder
from ai_teacher.activities.listening.domain.listening import Sentence

class SentenceFinder:

    def __init__(self, listening_finder = ListeningFinder()) -> None:
        self.listening_finder = listening_finder

    def find(self, listening_id: str, sentence_id: str) -> Sentence:
        listening = self.listening_finder.find(listening_id)
        if listening is None:
            return None
        filtered_sentences = [sentence for sentence in listening.sentences if sentence.id == sentence_id]
        if len(filtered_sentences) > 0:
            return filtered_sentences[0]
        return None
