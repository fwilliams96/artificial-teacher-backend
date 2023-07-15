from pydantic import BaseModel

class UserPreference(BaseModel):
    id: str | None
    preference_id: str
    preference: str | None
    user_id: str | None

class Preference(BaseModel):
    id: str | None
    preference: str