from pydantic import BaseModel
from typing import Optional

# Entidad user
class User(BaseModel):
    id: Optional[str]
    email: Optional[str] = None
    disabled: Optional[bool]
    first_name: str
    last_name: str
    level: int
    score: int

class UserDb(User):
    password: str
