from fastapi import APIRouter, Depends, HTTPException, status
from ai_teacher.users.shared.application.user_auth import get_current_user
from ai_teacher.users.shared.domain.user import UserDb
from ai_teacher.users.user_routines.application.user_routine_finder import UserRoutineFinder
from ai_teacher.users.user_routines.application.user_routine_generator import UserRoutineGenerator
from ai_teacher.users.user_routines.domain.user_routine import UserRoutine

router = APIRouter(prefix='/user-routines', tags=["user-routines"], responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})

@router.post('/', response_model=UserRoutine, status_code=status.HTTP_200_OK)
def create_routine(user: UserDb = Depends(get_current_user)):
    return UserRoutineGenerator().generate(user.id)

@router.get('/', response_model=list[UserRoutine], status_code=status.HTTP_200_OK)
def get_routines(active = False, user: UserDb = Depends(get_current_user)):
    if active:
        return UserRoutineFinder().find_active(user.id)
    return UserRoutineFinder().find_all(user.id)

@router.get('/{routine_id}', response_model=UserRoutine, status_code=status.HTTP_200_OK)
def get_routine(routine_id: str):
    user_routine = UserRoutineFinder().find_by_id(routine_id)
    if user_routine is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Routine not found")
    return user_routine

