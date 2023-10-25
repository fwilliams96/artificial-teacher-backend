from backoffice.preferences.domain.preference import Preference
from backoffice.preferences.infrastructure.persistence.mongo.mongo_preference_repository import MongoPreferenceRepository

class PreferenceFinder:

    def __init__(self, preference_repository = MongoPreferenceRepository()) -> None:
        self.preference_repository = preference_repository

    def find_all(self) -> list[Preference]:
        return self.preference_repository.find_all()

    def find(self, preference_id: str) -> Preference | None:
        return self.preference_repository.find_preference(preference_id)