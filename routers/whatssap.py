from fastapi import APIRouter, Request, Response, status, HTTPException
from fastapi.routing import APIRoute
from db.models.whatssap import WhatssapMessage, WhatssapMessageOrigin

from open_ai.customer_support import answer_message

router = APIRouter(prefix='/whatssap', tags=["whatssap"], responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})

@router.get('/webhook')
async def verify(request: Request):
    if not request.query_params.get("hub.verify_token") == 'SneilaAtlantis':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized.")
    return int(request.query_params.get("hub.challenge"))
    
@router.post('/webhook', response_model=WhatssapMessage, status_code=status.HTTP_200_OK)
async def send_message(request: Request):
    # if not request.query_params.get("hub.verify_token") == 'SneilaAtlantis':
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized.")
    
    data = await request.json()

    client_phone = data['entry'][0]['changes'][0]['value']['messages'][0]['from']
    message = data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
    message_id = data['entry'][0]['changes'][0]['value']['messages'][0]['id']
    print(f"Message id: {message_id}")
    timestamp = data['entry'][0]['changes'][0]['value']['messages'][0]['timestamp']
    print(f"Message timestamp: {timestamp}")

    if data is None or message is None or client_phone is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Body not properly informed.")

    return answer_message(
        WhatssapMessage(
            client_phone=client_phone,
            message=message,
            origin=WhatssapMessageOrigin.CLIENT,
            timestamp=timestamp
        )
    )