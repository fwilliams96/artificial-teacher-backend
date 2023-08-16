from pydantic import BaseModel

class UserWord(BaseModel):
    word: str
    is_word: bool
    askable: bool
    wrong: bool

class UserSentence(BaseModel):
    id: str
    words: list[UserWord]
    sentence: str

class UserListening(BaseModel):
    id: str | None
    listening_id: str
    user_id: str
    finished: bool = False
    sentences: list[UserSentence] = []