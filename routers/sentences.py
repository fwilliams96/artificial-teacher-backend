from fastapi import APIRouter, Depends, HTTPException, status
from db.models.listening import Word
from db.models.sentence import WordSentence
from db.models.user import User
from open_ai.listening_planner import generate_words
from open_ai.sentence import get_user_sentences
from users.auth import get_current_user

router = APIRouter(prefix='/sentences', tags=["sentences"], responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}}, dependencies=[Depends(get_current_user)])

@router.get('/', response_model=list[WordSentence], status_code=status.HTTP_200_OK)
def get_sentences(user: User = Depends(get_current_user)):
    return get_user_sentences(user)

@router.get('/words', response_model=list[Word], status_code=status.HTTP_200_OK)
def get_words_from_sentence(sentence: str):
    return generate_words(sentence)