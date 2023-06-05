from pydantic import BaseModel
from enum import Enum

class MessageContentType(str, Enum):
    TEXT = 'text'
    AUDIO = 'audio'

class MessageType(str, Enum):
    CONVERSATION = 'conversation',
    LISTENING = 'listening'

class Word(BaseModel):
    value: str
    writable: bool

class Sentence(BaseModel):
    id: str
    audio: str
    words: list[Word]
    sentence: str

class Listening(BaseModel):
    id: str | None
    topic: str
    sentences: list[Sentence] | None

class SentenceCheckRequest(BaseModel):
    user_sentence: str

class SentenceCheckResult(BaseModel):
    correct: bool
    correct_sentence: str