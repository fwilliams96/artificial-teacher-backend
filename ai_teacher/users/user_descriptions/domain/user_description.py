from typing import Optional
from pydantic import BaseModel

class UserSolution(BaseModel):
    text: Optional[str] = None

class UserDescriptionCorrection(BaseModel):
    description: Optional[str] = None
    rating: float
    comments: Optional[str] = None

class UserDescription(BaseModel):
    id: Optional[str] = None
    topic: str
    user_id: str
    finished: bool = False
    image: str
    user_solution: Optional[UserSolution] = None
    correction: Optional[UserDescriptionCorrection] = None
    routine_id: Optional[str] = None

