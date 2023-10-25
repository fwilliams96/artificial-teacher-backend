from typing import Any, Optional, Union
from pydantic import BaseModel, Field
from enum import Enum

from ai_teacher.activities.flashcard.domain.flashcard import FlashCard

# Entidad chatgpt question
class ChatGPTQuestion(BaseModel):
    context_id: Optional[str]
    content: str

# Entidad chatgpt answer
class ChatGPTAnswer(BaseModel):
    context_id: str
    content: str
    transcription: Optional[str]

class MessageContentType(str, Enum):
    TEXT = 'text'
    AUDIO = 'audio'

class MessageType(str, Enum):
    ACTIVITY = 'activity',
    ANALYSIS = 'analysis',
    CONVERSATION = 'conversation',
    LISTENING = 'listening'

class UserMessage(BaseModel):
    content_type: MessageContentType
    content: str
    message_type: MessageType | None

# Entidad chatgpt answer
class ServerMessage(BaseModel):
    content_type: MessageContentType
    content: str | FlashCard
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
