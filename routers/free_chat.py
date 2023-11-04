from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from ai_teacher.chat.free.application.free_chat_agent_talker import FreeChatAgentTalker
from ai_teacher.chat.free.application.free_chat_finder import FreeChatFinder
from ai_teacher.chat.free.application.free_chat_finisher import FreeChatFinisher
from ai_teacher.chat.free.application.free_chat_generator import FreeChatGenerator
from ai_teacher.chat.free.domain.free_chat import FreeChat, FreeChatMessage
from ai_teacher.users.shared.application.user_auth import get_current_user
from ai_teacher.users.shared.application.user_score_incrementer import UserScoreIncrementer
from ai_teacher.users.shared.domain.user import UserDb

router = APIRouter(prefix='/free-chat', tags=["free-chat"], responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}}, dependencies=[Depends(get_current_user)])

@router.post('/', response_model=FreeChat, status_code=status.HTTP_200_OK)
def create_chat(user: UserDb = Depends(get_current_user)):
    return FreeChatGenerator().create(user.id)

@router.post('/{chat_id}', response_model=list[FreeChatMessage], status_code=status.HTTP_200_OK)
def chat(chat_id: str, user_message: FreeChatMessage, response_in_speech: bool = False, user: UserDb = Depends(get_current_user)):
    user_message.chat_id = chat_id
    user_message.sender_id = user.id
    return FreeChatAgentTalker().talk(user_message, response_in_speech)
     
@router.get('/{chat_id}', response_model=FreeChat, status_code=status.HTTP_200_OK)
def recover_chat(chat_id: str):
    free_chat = FreeChatFinder().find(chat_id)
    if free_chat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Free chat not found")
    return free_chat
   
@router.post('/{chat_id}/finish', response_model=FreeChat, status_code=status.HTTP_200_OK)
def finish_chat(chat_id: str, background_tasks: BackgroundTasks, user: UserDb = Depends(get_current_user)):
    free_chat = FreeChatFinisher().finish(chat_id)
    background_tasks.add_task(UserScoreIncrementer().increment, user.id, 50)
    return free_chat