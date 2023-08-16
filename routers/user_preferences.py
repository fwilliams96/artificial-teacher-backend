from fastapi import APIRouter, Depends, HTTPException, status
from ai_teacher.users.user_preferences.application.user_preference_creator import UserPreferenceCreator
from ai_teacher.users.user_preferences.application.user_preference_finder import UserPreferenceFinder
from ai_teacher.users.user_preferences.domain.user_preference import UserPreference
from db.models.user import User

from users.auth import get_current_user

router = APIRouter(prefix='/user-preferences', tags=["user-preferences"], responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}}, dependencies=[Depends(get_current_user)])

@router.get('/', response_model=list[UserPreference], status_code=status.HTTP_200_OK)
def get_preferences(user: User = Depends(get_current_user)):
    return UserPreferenceFinder().get_preferences(user.id)

@router.post('/', response_model=list[UserPreference], status_code=status.HTTP_200_OK)
def save_preferences(user_preferences: list[UserPreference], user: User = Depends(get_current_user)):
    user_preference_creator = UserPreferenceCreator()
    preferences_are_valid = True
    for user_preference in user_preferences:
        user_preference.user_id = user.id
        if user_preference.preference_id is None:
            preferences_are_valid = False
    if not preferences_are_valid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Preferences are not valid.")

    return [user_preference_creator.create(user_preference) for user_preference in user_preferences]