from typing import Any, Optional, Union
from pydantic import BaseModel, Field
from enum import Enum

# Entidad chatgpt question
class ChatGPTQuestion(BaseModel):
    context_id: Optional[str]
    content: str

# Entidad chatgpt answer
class ChatGPTAnswer(BaseModel):
    context_id: str
    content: str
    transcription: Optional[str]

class ActivityType(str, Enum):
    FLASHCARD = 'flashcard'

class FlashCard(BaseModel):
    sentence: str
    correct_sentence: str
    correct_option: str
    options: list[str]

class Activity(BaseModel):
    incorrect: str
    correct: str
    activity_type: ActivityType
    comments: Optional[str]
    active = True

class AgentFlashCardActivity(Activity):
    flashcard: FlashCard
    activity_type = ActivityType.FLASHCARD

class MessageContentType(str, Enum):
    TEXT = 'text'
    AUDIO = 'audio'

class MessageType(str, Enum):
    ACTIVITY = 'activity',
    ANALYSIS = 'analysis',
    CONVERSATION = 'conversation'

class UserMessage(BaseModel):
    content_type: MessageContentType
    content: str
    message_type: MessageType | None

# Entidad chatgpt answer
class ServerMessage(BaseModel):
    content_type: MessageContentType
    content: str | AgentFlashCardActivity
    message_type: MessageType
    transcription: Optional[str] = None

# Entidad context
class ServerContext(BaseModel):
    context_id: Optional[str]
    content: str

class AgentAnalysis(BaseModel):
    comments: Optional[str]
    grammatical_errors: list[str] = []
    spelling_errors: list[str] = []
    pronunciation_errors: list[str] = []
