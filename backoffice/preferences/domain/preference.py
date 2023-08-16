from pydantic import BaseModel

class Preference(BaseModel):
    id: str | None
    preference: str