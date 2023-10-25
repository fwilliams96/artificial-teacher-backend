from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from ai_teacher.users.shared.application.user_auth import get_current_user
from ai_teacher.users.shared.application.user_score_incrementer import UserScoreIncrementer
from ai_teacher.users.shared.domain.user import UserDb
from ai_teacher.users.user_cards.application.user_card_creator import UserCardCreator
from ai_teacher.users.user_cards.application.user_card_generator import UserCardGenerator
from ai_teacher.users.user_pronunciations.application.user_pronunciation_analyzer import UserPronunciationAnalyzer
from ai_teacher.users.user_pronunciations.application.user_pronunciation_finder import UserPronunciationFinder
from ai_teacher.users.user_pronunciations.application.user_pronunciation_generator import UserPronunciationGenerator
from ai_teacher.users.user_pronunciations.application.user_pronunciation_updater import UserPronunciationUpdater
from ai_teacher.users.user_pronunciations.domain.user_pronunciation import UserPronunciation, UserSpeech

router = APIRouter(prefix='/user-pronunciations', tags=["user-pronunciations"], responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}}, dependencies=[Depends(get_current_user)])

@router.post('/', response_model=UserPronunciation, status_code=status.HTTP_200_OK)
def create_user_pronunciation(user: UserDb = Depends(get_current_user)):
    return UserPronunciationGenerator().generate(user_id=user.id)

@router.get('/{user_pronunciation_id}', response_model=UserPronunciation, status_code=status.HTTP_200_OK)
def get_user_pronunciation(user_pronunciation_id: str):
    user_pronunciation = UserPronunciationFinder().find(user_pronunciation_id)
    if user_pronunciation == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pronunciation activity not found")
    return user_pronunciation

@router.post('/{user_pronunciation_id}/close', response_model=UserPronunciation, status_code=status.HTTP_200_OK)
def close_user_pronunciation(user_pronunciation_id: str, user_speech: UserSpeech, background_tasks: BackgroundTasks, user: UserDb = Depends(get_current_user)):
    user_pronunciation = UserPronunciationFinder().find(user_pronunciation_id)
    if user_pronunciation == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pronunciation activity not found")
    
    user_pronunciation.user_speech = user_speech
    user_pronunciation = UserPronunciationAnalyzer().analize_pronunciation(user_pronunciation)

    user_pronunciation.id = user_pronunciation_id
    user_pronunciation.finished = True
    user_pronunciation.user_id = user.id

    user_pronunciation = UserPronunciationUpdater().update(user_pronunciation)
    background_tasks.add_task(generate_user_cards_based_on_pronunciation, user_pronunciation)
    background_tasks.add_task(UserScoreIncrementer().increment, user.id, 15)
    return user_pronunciation

def generate_user_cards_based_on_pronunciation(user_pronunciation: UserPronunciation):
    user_card_generator = UserCardGenerator()
    user_card_creator = UserCardCreator()
    
    # Generate and save cards based on the wrong words
    for word in user_pronunciation.sentence.words:
        if word.wrong == True:
            user_card = user_card_generator.generate(user_pronunciation.user_id, word.word)
            user_card_creator.create(user_card)