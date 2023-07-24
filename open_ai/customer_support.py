from typing import Tuple
from db.client import db_client
from db.models.whatssap import WhatssapMessage, WhatssapMessageOrigin
from db.schemas.whatssap_conversation import whatssap_conversation_schema

from open_ai.general import get_agent_response

customer_support_context = "Eres un agente de soporte al cliente en el área de odontología, por lo que solo debes responder consultas de este tipo."

def answer_message(client_whatssap_message: WhatssapMessage) -> str:
    conversation_db = recover_conversation_db(client_whatssap_message.client_phone)
    agent_response = answer_message(client_whatssap_message.message)

    agent_whatssap_message = WhatssapMessage(
        client_phone=client_whatssap_message.client_phone,
        origin=WhatssapMessageOrigin.SERVER,
        message=agent_response
    )

    if conversation_db is None:
        conversation_db = {
            "client_phone": client_whatssap_message.client_phone,
            "messages": [build_db_conversation_message(client_whatssap_message), build_db_conversation_message(agent_whatssap_message)]
        }
        conversation_id = db_client.whatssap_conversations.insert_one(conversation_db)
        print(f"Conversation id: {conversation_id}")
        return agent_whatssap_message

    conversation_db["messages"].extend([build_db_conversation_message(client_whatssap_message), build_db_conversation_message(agent_whatssap_message)])
    db_client.whatssap_conversations.find_one_and_replace({"client_phone": client_whatssap_message.client_phone}, conversation_db)
    return agent_whatssap_message


def build_db_conversation_message(whatssap_message: WhatssapMessage):
    return {
        'origin': whatssap_message.origin.value,
        'message': whatssap_message.message,
        'timestamp': whatssap_message.timestamp
    }

def answer_message(question: str) -> Tuple[str, str]:
    messages=[{"role": "system", "content": customer_support_context}] 
    messages.append({"role": "user", "content": question})
    agent_response = get_agent_response(messages)
    return agent_response

def recover_conversation_db(client_phone: str):
    conversation_db = db_client.whatssap_conversations.find_one({"client_phone": client_phone})
    if not conversation_db:
        return None
    conversation = whatssap_conversation_schema(conversation_db)
    return conversation
