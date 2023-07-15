from typing import Tuple
from fastapi import APIRouter, Depends, HTTPException, status
from db.models.preference import Preference
from db.models.user import User
from open_ai.preference import create_preference_db, get_preferences_db

from users.auth import get_authenticated_user, get_current_user

router = APIRouter(prefix='/preferences', tags=["preferences"], responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}}, dependencies=[Depends(get_current_user)])

@router.post('/', response_model=Preference, status_code=status.HTTP_200_OK)
def create_preference(preference: Preference):
    return create_preference_db(preference)

@router.get('/', response_model=list[Preference], status_code=status.HTTP_200_OK)
def get_preferences():
    return get_preferences_db()
