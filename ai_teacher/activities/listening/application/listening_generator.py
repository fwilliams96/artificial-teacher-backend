from ai_teacher.activities.listening.application.topic_planner import TopicPlanner
from ai_teacher.activities.listening.domain.listening import Listening
from ai_teacher.activities.listening.infrastructure.openai.chatgpt_sentence_generator import ChatgptSentenceGenerator

class ListeningGenerator:

    def __init__(self, topic_planner = TopicPlanner(), external_sentence_generator = ChatgptSentenceGenerator()) -> None:
        self.topic_planner = topic_planner
        self.external_sentence_generator = external_sentence_generator

    def generate(self, topic: str, num_sentences: int) -> Listening:
        sentences = [{}]*num_sentences
        for num_sentence in range(num_sentences):
            sentences[num_sentence] = self.external_sentence_generator.generate(topic)

        return Listening(
            topic=topic,
            sentences=sentences
        )