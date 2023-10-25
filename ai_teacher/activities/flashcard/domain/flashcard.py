from pydantic import BaseModel

class FlashCard(BaseModel):
    incomplete_sentence: str
    correct_sentence: str
    correct_option: str
    wrong_options: list[str]