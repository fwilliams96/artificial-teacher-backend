from bson import ObjectId
from pydantic import BaseModel


class WordSentence(BaseModel):
    id: str | None
    audio: str
    word: str
    sentence: str
    user_id: str | None