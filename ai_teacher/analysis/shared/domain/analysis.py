from enum import Enum
from pydantic import BaseModel

class SentenceAnalysisType(str, Enum):
    GRAMMAR = 'GRAMMAR',
    SPELLING = 'SPELLING'

class SentenceAnalysis(BaseModel):
    type: SentenceAnalysisType
    errors: list[str]
    comment: str