from fastapi import APIRouter, Depends, status
from ai_teacher.users.shared.application.user_auth import get_current_user
from backoffice.preferences.application.preference_creator import PreferenceCreator
from backoffice.preferences.application.preference_finder import PreferenceFinder
from backoffice.preferences.domain.preference import Preference

router = APIRouter(prefix='/preferences', tags=["preferences"], responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}}, dependencies=[Depends(get_current_user)])

@router.post('/', response_model=Preference, status_code=status.HTTP_200_OK)
def create_preference(preference: Preference):
    return PreferenceCreator().create(preference)

@router.get('/', response_model=list[Preference], status_code=status.HTTP_200_OK)
def get_preferences():
    return PreferenceFinder().find_all()
