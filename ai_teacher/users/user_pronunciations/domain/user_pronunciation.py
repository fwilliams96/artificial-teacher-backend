from typing import Optional
from pydantic import BaseModel

class UserSpeech(BaseModel):
    audio: str

class SentenceWord(BaseModel):
    word: str
    is_word: bool
    wrong: bool

class Sentence(BaseModel):
    words: list[SentenceWord]
    sentence: str
    audio: str

class UserPronunciation(BaseModel):
    id: Optional[str] = None
    topic: str
    user_id: str
    finished: bool = False
    sentence: Sentence
    user_speech: Optional[UserSpeech] = None
    routine_id: Optional[str] = None