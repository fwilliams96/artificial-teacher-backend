import random
from ai_teacher.users.user_preferences.application.user_preference_finder import UserPreferenceFinder
from backoffice.preferences.application.preference_finder import PreferenceFinder

class TopicPlanner:

    def __init__(self, user_preference_finder = UserPreferenceFinder(), preference_finder = PreferenceFinder()) -> None:
        self.user_preference_finder = user_preference_finder
        self.preference_finder = preference_finder

    def user_random_topic(self, user_id: str) -> str:
        user_preferences = self.user_preference_finder.get_preferences(user_id)
        random_preference = random.choice(user_preferences)
        return self.preference_finder.find(random_preference.preference_id).preference
