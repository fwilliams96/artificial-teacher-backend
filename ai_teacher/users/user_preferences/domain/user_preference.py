from typing import Optional
from pydantic import BaseModel

class UserPreference(BaseModel):
    id: Optional[str] = None
    preference_id: str
    preference: Optional[str] = None
    user_id: Optional[str] = None
