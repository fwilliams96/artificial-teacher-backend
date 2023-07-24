def whatssap_conversation_schema(conversation) -> dict:
    return {
        "id": str(conversation["_id"]),
        "client_phone": conversation["client_phone"],
        "messages": messages_chema(conversation["messages"])
    }

def messages_chema(messages) -> list:
    return [message_chema(message) for message in messages] 

def message_chema(message: dict) -> dict:
    return {
        "type": message["type"],
        "message": {
            "role": str(message["message"]["role"]),
            "content": message["message"]["content"],
            "timestamp": message["message"]["timestamp"]
        }
    }