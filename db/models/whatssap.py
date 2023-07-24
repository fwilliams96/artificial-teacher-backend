from enum import Enum
from pydantic import BaseModel

class WhatssapMessageOrigin(str, Enum):
    SERVER = 'server'
    CLIENT = 'client'

class WhatssapMessage(BaseModel):
    client_phone: str | None
    origin: WhatssapMessageOrigin
    message: str
    timestamp: str | None

class WhatssapConversation(BaseModel):
    client_phone: str
    messages: list[WhatssapMessage]