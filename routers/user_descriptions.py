from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from ai_teacher.users.shared.application.user_auth import get_current_user
from ai_teacher.users.shared.application.user_score_incrementer import UserScoreIncrementer
from ai_teacher.users.shared.domain.user import UserDb
from ai_teacher.users.user_cards.application.user_card_creator import UserCardCreator
from ai_teacher.users.user_cards.application.user_card_generator import UserCardGenerator
from ai_teacher.users.user_descriptions.application.user_description_finder import UserDescriptionFinder
from ai_teacher.users.user_descriptions.application.user_description_generator import UserDescriptionGenerator
from ai_teacher.users.user_descriptions.application.user_description_rater import UserDescriptionRater
from ai_teacher.users.user_descriptions.application.user_description_updater import UserDescriptionUpdater
from ai_teacher.users.user_descriptions.domain.user_description import UserDescription, UserSolution

router = APIRouter(prefix='/user-descriptions', tags=["user-descriptions"], responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}}, dependencies=[Depends(get_current_user)])

@router.post('/', response_model=UserDescription, status_code=status.HTTP_200_OK)
def create_user_description(user: UserDb = Depends(get_current_user)):
    return UserDescriptionGenerator().generate(user_id=user.id)

@router.get('/{user_description_id}', response_model=UserDescription, status_code=status.HTTP_200_OK)
def get_user_description(user_description_id: str):
    description = UserDescriptionFinder().find(user_description_id)
    if description == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Description not found")
    return description

@router.post('/{user_description_id}/close', response_model=UserDescription, status_code=status.HTTP_200_OK)
def close_user_description(user_description_id: str, user_solution: UserSolution, background_tasks: BackgroundTasks, user: UserDb = Depends(get_current_user)):
    user_description = UserDescriptionFinder().find(user_description_id)
    if user_description == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Description not found")
    
    user_description_correction = UserDescriptionRater().rate(user_solution, user_description.image)
    user_description.correction = user_description_correction
    user_description.user_solution = user_solution

    user_description.id = user_description_id
    user_description.finished = True
    user_description.user_id = user.id
    user_description = UserDescriptionUpdater().update(user_description)
    background_tasks.add_task(UserScoreIncrementer().increment, user.id, 20)
    return user_description