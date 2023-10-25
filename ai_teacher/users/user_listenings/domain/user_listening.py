from typing import Optional
from pydantic import BaseModel

class UserWord(BaseModel):
    word: str
    is_word: bool
    askable: bool
    wrong: bool

class UserSentence(BaseModel):
    words: list[UserWord]
    sentence: str
    audio: str

class UserListening(BaseModel):
    id: Optional[str] = None
    topic: str
    user_id: str
    finished: bool = False
    sentences: list[UserSentence] = []
    routine_id: Optional[str] = None