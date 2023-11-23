from fastapi import APIRouter, Depends, status
from ai_teacher.users.shared.application.user_auth import encrypt_password, get_current_user
from ai_teacher.users.shared.application.user_creator import UserCreator
from ai_teacher.users.shared.application.user_finder import UserFinder
from ai_teacher.users.shared.application.user_updater import UserUpdater
from ai_teacher.users.shared.domain.user import NewUser, User, UserDb
from ai_teacher.users.user_cards.application.user_card_finder import UserCardFinder
from ai_teacher.users.user_cards.domain.user_card import UserCard

router = APIRouter(prefix='/users', tags=["users"], responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})

@router.post('/', response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: NewUser):
    return UserCreator().create(user)

@router.get('/', response_model=User, status_code=status.HTTP_201_CREATED)
async def get_user(user: User = Depends(get_current_user)):
    return UserFinder().find_user_by_id(user.id)

@router.get('/wall-of-fame', response_model=list[User], status_code=status.HTTP_201_CREATED)
async def get_top_users():
    return UserFinder().find_top_users()

@router.get('/cards', response_model=list[UserCard], status_code=status.HTTP_201_CREATED)
async def get_cards(user: User = Depends(get_current_user)):
    return UserCardFinder().find_all(user.id)

@router.put('/', status_code=status.HTTP_204_NO_CONTENT)
async def update_user(user_db: UserDb, user: User = Depends(get_current_user)):
    user_db.id = user.id
    return UserUpdater().update(user_db)