from enum import Enum
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class FreeChatMessageType(str, Enum):
    SPEECH = 'SPEECH',
    TEXT = 'TEXT',

class FreeChatMessage(BaseModel):
    id: Optional[str] = None
    message: str
    type: FreeChatMessageType
    sender_id: Optional[str] = None
    chat_id: Optional[str] = None
    sent_date: Optional[datetime] = None

class FreeChat(BaseModel):
    id: Optional[str] = None
    messages: list[FreeChatMessage] = []
    is_over: bool = False
    user_id: str
    creation_date: datetime