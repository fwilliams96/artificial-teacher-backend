from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel

class RolePlayType(str, Enum):
    JOB_INTERVIEW = 'JOB_INTERVIEW',
    BUY_SUPERMARKET = 'BUY_SUPEMARKET',
    CHECKIN_AIRPORT = 'CHECKIN_AIRPORT',
    ORDER_FOOD_RESTAURANT = 'ORDER_FOOD_RESTAURANT',
    CHECKIN_ACCOMMODATION = 'CHECKIN_ACCOMMODATION',
    DOCTOR_VISIT = 'DOCTOR_VISIT',
    TRAVEL_AGENCY = 'TRAVEL_AGENCY',
    PARENTS_SCHOOL_MEETING = 'PARENTS_SCHOOL_MEETING',
    PARTYING_WITH_STRANGERS = 'PARTYING_WITH_STRANGERS',
    URGENCY_CALL_POLICE = 'URGENCY_CALL_POLICE'

class RolePlayMessageType(str, Enum):
    SPEECH = 'SPEECH',
    TEXT = 'TEXT'

class RolePlayMessage(BaseModel):
    id: Optional[str] = None
    message: str
    type: RolePlayMessageType
    sender_id: Optional[str] = None
    role_play_id: Optional[str] = None
    sent_date: Optional[datetime] = None
    last_message: bool = False

class RolePlay(BaseModel):
    id: Optional[str] = None
    type: RolePlayType
    messages: list[RolePlayMessage] = []
    is_over: bool = False
    user_id: str
    routine_id: Optional[str] = None
    creation_date: datetime

'''class RolePlaySituationDecisition(BaseModel):
    decisition: str
    is_correct: bool

class RolePlaySituation(BaseModel):
    description: str
    goal: str
    decisions: list[RolePlaySituationDecisition]

class RolePlay(BaseModel):
    id: Optional[str] = None
    topic: str
    situations: list[RolePlaySituation]'''