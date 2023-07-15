from fastapi import APIRouter, Depends, HTTPException, status
from db.models.preference import Preference, UserPreference
from db.models.user import User
from open_ai.preference import create_user_preference_db, get_user_preferences

from users.auth import get_current_user

router = APIRouter(prefix='/user-preferences', tags=["user-preferences"], responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}}, dependencies=[Depends(get_current_user)])

@router.get('/', response_model=list[UserPreference], status_code=status.HTTP_200_OK)
def get_preferences(user: User = Depends(get_current_user)):
    return get_user_preferences(user)

@router.post('/', response_model=list[UserPreference], status_code=status.HTTP_200_OK)
def add_preference(user_preferences: list[UserPreference], user: User = Depends(get_current_user)):
    for user_preference in user_preferences:
        if user_preference.preference_id is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Preference id must be informed.")
        user_preference = create_user_preference_db(user, user_preference)
    return user_preferences