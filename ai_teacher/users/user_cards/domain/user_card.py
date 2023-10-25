from typing import Optional
from pydantic import BaseModel

class UserCard(BaseModel):
    id: Optional[str] = None
    word: str
    sentence: str
    sentence_speech: str
    user_id: str

class UserCardSentence(BaseModel):
    id: Optional[str] = None
    word: str
    sentence: str