from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from ai_teacher.users.shared.application.user_auth import get_current_user
from ai_teacher.users.shared.application.user_score_incrementer import UserScoreIncrementer
from ai_teacher.users.shared.domain.user import UserDb
from ai_teacher.users.user_role_plays.application.user_role_play_finder import UserRolePlayFinder
from ai_teacher.users.user_role_plays.application.user_role_play_generator import UserRolePlayGenerator
from ai_teacher.users.user_role_plays.application.user_role_play_talker import UserRolePlayTalker
from ai_teacher.users.user_role_plays.domain.role_play import RolePlay, RolePlayMessage, RolePlayType

router = APIRouter(prefix='/role-play', tags=["role-play"], responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}}, dependencies=[Depends(get_current_user)])

@router.post('/', response_model=RolePlay, status_code=status.HTTP_200_OK)
def create_role_play(role_play_type: str, user: UserDb = Depends(get_current_user),):
   return UserRolePlayGenerator().create(user_id=user.id, role_play_type=RolePlayType[role_play_type.upper()])

@router.post('/{role_play_id}', response_model=list[RolePlayMessage], status_code=status.HTTP_200_OK)
def chat(role_play_id: str, user_message: RolePlayMessage, background_tasks: BackgroundTasks, response_in_speech: bool = False, user: UserDb = Depends(get_current_user)):
   user_message.role_play_id = role_play_id
   user_message.sender_id = user.id
   role_play_messages = UserRolePlayTalker().talk(user_message, response_in_speech)
   if len(role_play_messages) > 0 and role_play_messages[-1].last_message == True:
      background_tasks.add_task(UserScoreIncrementer().increment, user.id, 50)
   return role_play_messages
     
@router.get('/{role_play_id}', response_model=RolePlay, status_code=status.HTTP_200_OK)
def recover_role_play(role_play_id: str):
   role_play = UserRolePlayFinder().find_by_id(role_play_id)
   if role_play is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role play not found")
   return role_play