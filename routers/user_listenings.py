from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from ai_teacher.users.shared.application.user_auth import get_current_user
from ai_teacher.users.shared.application.user_score_incrementer import UserScoreIncrementer
from ai_teacher.users.shared.domain.user import UserDb
from ai_teacher.users.user_cards.application.user_card_creator import UserCardCreator
from ai_teacher.users.user_cards.application.user_card_generator import UserCardGenerator
from ai_teacher.users.user_listenings.application.user_listening_checker import UserListeningChecker
from ai_teacher.users.user_listenings.application.user_listening_finder import UserListeningFinder
from ai_teacher.users.user_listenings.application.user_listening_generator import UserListeningGenerator
from ai_teacher.users.user_listenings.application.user_listening_updater import UserListeningUpdater
from ai_teacher.users.user_listenings.domain.user_listening import UserListening

router = APIRouter(prefix='/user-listenings', tags=["user-listenings"], responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}}, dependencies=[Depends(get_current_user)])

@router.post('/', response_model=UserListening, status_code=status.HTTP_200_OK)
def create_user_listening(num_sentences: int, user: UserDb = Depends(get_current_user)):
    return UserListeningGenerator().generate(user_id=user.id, num_sentences=num_sentences)

@router.get('/{user_listening_id}', response_model=UserListening, status_code=status.HTTP_200_OK)
def get_user_listening(user_listening_id: str):
    listening = UserListeningFinder().find(user_listening_id)
    if listening == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listening not found")
    return listening

@router.post('/{user_listening_id}/close', response_model=UserListening, status_code=status.HTTP_200_OK)
def close_user_listening(user_listening_id: str, user_listening: UserListening, background_tasks: BackgroundTasks, user: UserDb = Depends(get_current_user)):
    listening = UserListeningFinder().find(user_listening_id)
    if listening == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listening not found")
    
    user_listening.id = user_listening_id
    user_listening.finished = True
    user_listening.user_id = user.id
    user_listening = UserListeningUpdater().update(user_listening)
    background_tasks.add_task(generate_user_cards_based_on_listening, user_listening)
    background_tasks.add_task(UserScoreIncrementer().increment, user.id, 15)
    return user_listening

def generate_user_cards_based_on_listening(user_listening: UserListening):
    wrong_words = UserListeningChecker().extract_wrong_words(user_listening)

    user_card_generator = UserCardGenerator()
    user_card_creator = UserCardCreator()
    
    # Generate and save cards based on the wrong words
    for wrong_word in wrong_words:
        user_card = user_card_generator.generate(user_listening.user_id, wrong_word.word)
        user_card_creator.create(user_card)