import abc
from backoffice.preferences.domain.preference import Preference

class PreferenceRepository(abc.ABC):

    @abc.abstractclassmethod
    def find_preference(self, preference_id: str) -> Preference | None:
        pass

    @abc.abstractclassmethod
    def find_all(self):
        pass

    @abc.abstractclassmethod
    def create_preference(self, preference: Preference) -> Preference:
        pass

