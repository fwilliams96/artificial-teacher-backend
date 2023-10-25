from backoffice.preferences.domain.preference import Preference
from backoffice.preferences.infrastructure.persistence.mongo.mongo_preference_repository import MongoPreferenceRepository

class PreferenceCreator:
    
    def __init__(self, preference_repository = MongoPreferenceRepository()) -> None:
        self.preference_repository = preference_repository

    def create(self, preference: Preference) -> Preference:
        return self.preference_repository.create_preference(preference)