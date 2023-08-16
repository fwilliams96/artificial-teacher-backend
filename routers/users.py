from fastapi import APIRouter, Depends, status
from ai_teacher.users.shared.application.user_auth import UserAuth
from ai_teacher.users.shared.application.user_creator import UserCreator
from ai_teacher.users.shared.application.user_updator import UserUpdator
from ai_teacher.users.shared.domain.user import User, UserDb
from ai_teacher.users.user_cards.application.user_card_finder import UserCardFinder
from ai_teacher.users.user_cards.domain.user_card import UserCard

router = APIRouter(prefix='/users', tags=["users"], responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})

@router.post('/', response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user_db: UserDb):
    user_auth = UserAuth()
    user_db.disabled = False
    user_db.password = user_auth.encrypt_password(user_db.password)

    user_creator = UserCreator()
    return user_creator.create(user_db)

@router.get('/cards', response_model=list[UserCard], status_code=status.HTTP_201_CREATED)
async def get_cards(user: User = Depends(UserAuth().get_current_user)):
    return UserCardFinder().find_all(user.id)

@router.put('/', status_code=status.HTTP_204_NO_CONTENT)
async def update_user(user_db: UserDb, user: User = Depends(UserAuth().get_current_user)):
    user_db.id = user.id
    return UserUpdator().update(user_db)