from typing import Optional
from pydantic import BaseModel

# Entidad chatgpt question
class ChatGPTQuestion(BaseModel):
    context_id: Optional[str]
    content: str

# Entidad chatgpt answer
class ChatGPTAnswer(BaseModel):
    context_id: str
    content: str
    transcription: Optional[str]

# Entidad chatgpt answer
class Message(BaseModel):
    content: str
    transcription: Optional[str]

# Entidad context
class Context(BaseModel):
    context_id: Optional[str]
    content: str