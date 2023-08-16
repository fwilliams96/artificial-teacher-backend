from ai_teacher.activities.listening.domain.listening import Listening
from ai_teacher.activities.listening.infrastructure.persistence.mongo.mongo_listening_repository import MongoListeningRepository

class ListeningFinder:

    def __init__(self, listening_repository = MongoListeningRepository()) -> None:
        self.listening_repository = listening_repository

    def find(self, listening_id: str) -> Listening | None:
        return self.listening_repository.find(listening_id)