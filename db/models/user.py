from pydantic import BaseModel
from typing import Optional

# Entidad user
class User(BaseModel):
    id: Optional[str]
    email: str
    disabled: Optional[bool]

class UserDb(User):
    password: str
