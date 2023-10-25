from ai_teacher.users.user_listenings.domain.user_listening import UserListening, UserWord

class UserListeningChecker:

    def __init__(self) -> None:
        pass

    def extract_wrong_words(self, user_listening: UserListening) -> list[UserWord]:
        return [word for sentence in user_listening.sentences for word in sentence.words if word.wrong]