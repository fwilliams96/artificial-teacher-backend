from ai_teacher.activities.listening.domain.listening import Listening
from ai_teacher.activities.listening.infrastructure.persistence.mongo.mongo_listening_repository import MongoListeningRepository

class ListeningCreator:

    def __init__(self, listening_repository = MongoListeningRepository()) -> None:
        self.listening_repository = listening_repository

    def save(self, listening: Listening) -> Listening:
        return self.listening_repository.save(listening)