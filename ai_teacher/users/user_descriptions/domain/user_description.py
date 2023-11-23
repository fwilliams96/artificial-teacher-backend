from enum import Enum
from typing import Optional
from pydantic import BaseModel

class UserSolutionType(str, Enum):
    SPEECH = 'SPEECH',
    TEXT = 'TEXT'

class UserSolution(BaseModel):
    content: str
    type: UserSolutionType

class UserDescriptionCorrection(BaseModel):
    description: Optional[str] = None
    rating: float
    comments: Optional[str] = None

class UserDescription(BaseModel):
    id: Optional[str] = None
    topic: str
    user_id: str
    finished: bool = False
    image: Optional[str] = None
    image_id: str
    user_solution: Optional[UserSolution] = None
    correction: Optional[UserDescriptionCorrection] = None
    routine_id: Optional[str] = None

class ImageDescription(BaseModel):
    id: Optional[str] = None
    topic: str
    image: str