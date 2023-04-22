from fastapi import APIRouter, status
from db.models.chat import Context
from chatgpt.talker import start_context_chatgpt

router = APIRouter(prefix='/chat', tags=["chat"], responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})

@router.post('/', response_model=Context, status_code=status.HTTP_200_OK)
async def create_context(context: Context):
        return start_context_chatgpt(context)

