from pydantic import BaseModel

class Word(BaseModel):
    word: str
    is_word: bool
    askable: bool
    
class Sentence(BaseModel):
    id: str
    words: list[Word]
    sentence: str

class AudioSentence(Sentence):
    audio: str

class Listening(BaseModel):
    id: str | None
    topic: str
    sentences: list[Sentence] | None

class SentenceCheckResult(BaseModel):
    correct: bool
    correct_sentence: str