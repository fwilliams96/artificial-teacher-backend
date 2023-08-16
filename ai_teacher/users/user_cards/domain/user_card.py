from pydantic import BaseModel

class UserCard(BaseModel):
    id: str | None
    word: str
    sentence: str
    sentence_speech: str

class UserCardSentence(BaseModel):
    id: str | None
    word: str
    sentence: str