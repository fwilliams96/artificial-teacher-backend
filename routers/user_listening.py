from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from ai_teacher.activities.listening.application.listening_finder import ListeningFinder
from ai_teacher.users.user_cards.application.user_card_creator import UserCardCreator
from ai_teacher.users.user_cards.application.user_card_generator import UserCardGenerator
from ai_teacher.users.user_listenings.application.user_listening_checker import WrongWordsExtractor
from ai_teacher.users.user_listenings.application.user_listening_creator import UserListeningCreator
from ai_teacher.users.user_listenings.domain.user_listening import UserListening
from db.models.user import User

from users.auth import get_current_user

router = APIRouter(prefix='/user-listenings', tags=["user-listenings"], responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}}, dependencies=[Depends(get_current_user)])

@router.post('/', status_code=status.HTTP_204_NO_CONTENT, response_model=UserListening)
def create_user_listening(user_listening: UserListening, user: User = Depends(get_current_user), background_tasks = BackgroundTasks):
    if user_listening.listening_id == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Listening id not informed")

    listening = ListeningFinder().find(user_listening.listening_id)

    if listening == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listening not found")
    
    background_tasks.add_task(generate_user_cards_based_on_listening, user_listening)

    return UserListeningCreator().create(user_listening)

def generate_user_cards_based_on_listening(user_listening: UserListening):
    wrong_words = WrongWordsExtractor().extract(user_listening)

    user_card_generator = UserCardGenerator()
    user_card_creator = UserCardCreator()
    
    # Generate and save cards based on the wrong words
    for wrong_word in wrong_words:
        user_card = user_card_generator.generate(wrong_word)
        user_card_creator.create(user_card)